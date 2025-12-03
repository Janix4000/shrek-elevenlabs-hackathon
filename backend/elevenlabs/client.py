import os
import signal
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import (
    Conversation,
    ConversationInitiationData,
)
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.transcript_manager import TranscriptManager

load_dotenv()


class ElevenLabsClient:
    def __init__(
        self,
        api_key: str | None = None,
        agent_id: str | None = None,
        transcript_manager: TranscriptManager | None = None
    ):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        self.agent_id = agent_id or os.getenv("AGENT_ID")

        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY must be set in environment variables or passed to constructor.")
        if not self.agent_id:
            raise ValueError("AGENT_ID must be set in environment variables or passed to constructor.")

        self.elevenlabs = ElevenLabs(api_key=self.api_key)
        self.transcript_manager = transcript_manager or TranscriptManager()
        self.conversation: Conversation | None = None

    def start_conversation(self, dynamic_variables: dict) -> str:
        config = ConversationInitiationData(dynamic_variables=dynamic_variables)

        self.conversation = Conversation(
            self.elevenlabs,
            self.agent_id,
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
        self.transcript_manager.add_agent_message(response)

    def _on_agent_response_correction(self, original: str, corrected: str) -> None:
        try:
            self.transcript_manager.correct_last_agent_message(original, corrected)
        except ValueError as e:
            print(f"Warning: Could not correct agent message: {e}")

    def _on_user_transcript(self, transcript: str) -> None:
        self.transcript_manager.add_user_message(transcript)

    def _end_session(self) -> None:
        if self.conversation:
            self.conversation.end_session()