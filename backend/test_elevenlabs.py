"""
Test script for ElevenLabs conversation using custom client.
Uses microphone input and prints output to console.
"""

import os
from dotenv import load_dotenv

# Import our custom client and agent
from elevenlabs_wrapper.client import ElevenLabsClient
from elevenlabs_wrapper.transcript_manager import TranscriptManager
from elevenlabs_wrapper.agent import Agent

load_dotenv()


def main():
    print("=" * 60)
    print("🎬 Starting ElevenLabs Conversation Test")
    print("=" * 60)

    # Get agent ID
    agent_id = os.getenv("AGENT_ID")
    if not agent_id:
        raise ValueError("AGENT_ID must be set in environment variables")

    # Create agent configuration
    agent = Agent(
        agent_id=agent_id,
        dynamic_variables={"product_name": "Shrek", "first_name": "Janek"},
    )

    # Optional: Set first message
    # agent.set_first_message("Hello! How can I help you today?")

    # Create transcript manager to track conversation
    transcript_manager = TranscriptManager()

    # Initialize client
    client = ElevenLabsClient(transcript_manager=transcript_manager)

    print("\n📋 Configuration:")
    print(f"  Agent ID: {agent.agent_id}")
    print(f"  Dynamic Variables: {agent.dynamic_variables}")
    print("\n💬 Starting conversation...")
    print("   (Speak into your microphone, press Ctrl+C to end)\n")

    try:
        # Start conversation - this will block until ended
        conversation_id = client.start_conversation(agent)

        print("\n" + "=" * 60)
        print(f"✅ Conversation ended successfully")
        print(f"🆔 Conversation ID: {conversation_id}")
        print("=" * 60)

        # Print conversation transcript
        print("\n📝 Conversation Transcript:")
        print("-" * 60)
        transcript = transcript_manager.get_transcript()
        for i, message in enumerate(transcript, 1):
            role = "👤 User" if message.speaker == "user" else "🤖 Agent"
            print(f"{i}. {role}: {message.text}")
        print("-" * 60)

        print(f"\n📊 Total messages: {len(transcript)}")

    except KeyboardInterrupt:
        print("\n\n🛑 Received interrupt signal")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
