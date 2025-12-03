import asyncio
import os
import signal
from uuid import UUID
from dotenv import load_dotenv

load_dotenv()

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import (
    Conversation,
    ClientTools,
    ConversationInitiationData,
)
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

agent_id = os.getenv("AGENT_ID")
api_key = os.getenv("ELEVENLABS_API_KEY")


if not api_key:
    raise ValueError("ELEVENLABS_API_KEY must be set in environment variables.")


def test():
    elevenlabs = ElevenLabs(api_key=api_key)

    # Create ClientTools with custom loop to prevent "different event loop" errors

    if not agent_id:
        raise ValueError("AGENT_ID must be set in environment variables.")

    async def end_conversation(params):
        nonlocal conversation
        conversation.end_session()

    config = ConversationInitiationData(dynamic_variables={"product_name": "Shrek"})

    conversation = Conversation(
        # API client and agent ID.
        elevenlabs,
        agent_id,
        # Assume auth is required when API_KEY is set.
        requires_auth=bool(api_key),
        # Use the default audio interface.
        audio_interface=DefaultAudioInterface(),
        # Simple callbacks that print the conversation to the console.
        callback_agent_response=lambda response: print(f"Agent: {response}"),
        callback_agent_response_correction=lambda original, corrected: print(
            f"Agent: {original} -> {corrected}"
        ),
        callback_user_transcript=lambda transcript: print(f"User: {transcript}"),
        # Uncomment if you want to see latency measurements.
        # callback_latency_measurement=lambda latency: print(f"Latency: {latency}ms"),
        config=config,
    )

    conversation.start_session()  # optional field

    signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())

    conversation_id = conversation.wait_for_session_end()

    print(f"Conversation ID: {conversation_id}")


if __name__ == "__main__":

    test()
