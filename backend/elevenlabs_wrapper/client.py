import os
import signal
from typing import Optional
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import (
    Conversation,
)
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs_wrapper.transcript_manager import TranscriptManager
from elevenlabs_wrapper.agent import Agent

load_dotenv()


class ElevenLabsClient:
    """Client for local conversational AI using agent configuration."""

    def __init__(
        self,
        api_key: str | None = None,
        transcript_manager: TranscriptManager | None = None,
    ):
        """
        Initialize the ElevenLabsClient.

        Args:
            api_key: ElevenLabs API key (defaults to ELEVENLABS_API_KEY env var)
            transcript_manager: Optional transcript manager for tracking conversation
        """
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")

        if not self.api_key:
            raise ValueError(
                "ELEVENLABS_API_KEY must be set in environment variables or passed to constructor."
            )

        self.elevenlabs = ElevenLabs(api_key=self.api_key)
        self.transcript_manager = transcript_manager or TranscriptManager()
        self.conversation: Conversation | None = None

    def start_conversation(
        self,
        agent: Agent,
    ) -> str | None:
        """
        Start a local conversation with the agent.

        Args:
            agent: Agent configuration with all customization options
            audio_interface: Optional audio interface (defaults to DefaultAudioInterface)

        Returns:
            Conversation ID after session ends
        """
        # Use agent callbacks if provided, otherwise use default transcript callbacks
        # Get conversation config from agent
        config = agent.to_conversation_config()

        self.conversation = Conversation(
            self.elevenlabs,
            agent.agent_id,
            user_id=agent.user_id,
            requires_auth=bool(self.api_key),
            audio_interface=DefaultAudioInterface(),
            callback_agent_response=self._on_agent_response,
            callback_agent_response_correction=self._on_agent_response_correction,
            callback_user_transcript=self._on_user_transcript,
            config=config,
        )

        self.conversation.start_session()

        signal.signal(signal.SIGINT, lambda sig, frame: self._end_session())

        conversation_id = self.conversation.wait_for_session_end()

        return conversation_id

    def _on_agent_response(self, response: str) -> None:
        """Default callback for agent responses."""
        self.transcript_manager.add_agent_message(response)
        print(f"🤖 Agent: {response}")

    def _on_agent_response_correction(self, original: str, corrected: str) -> None:
        """Default callback for agent response corrections."""
        try:
            self.transcript_manager.correct_last_agent_message(original, corrected)
            print(f"🔄 Agent Correction: {original} -> {corrected}")
        except ValueError as e:
            print(f"⚠️  Warning: Could not correct agent message: {e}")

    def _on_user_transcript(self, transcript: str) -> None:
        """Default callback for user transcripts."""
        self.transcript_manager.add_user_message(transcript)
        print(f"👤 User: {transcript}")

    def _end_session(self) -> None:
        """End the conversation session."""
        if self.conversation:
            self.conversation.end_session()
