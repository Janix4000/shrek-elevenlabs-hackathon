"""
Test script for making outbound phone calls using ElevenLabs agent.
"""
import os
from dotenv import load_dotenv
from elevenlabs_wrapper.agent import Agent
from elevenlabs_wrapper.phone_caller import PhoneCaller

load_dotenv()


def main():
    print("=" * 60)
    print("📞 ElevenLabs Phone Call Test")
    print("=" * 60)

    # Get phone number to call
    to_number = os.getenv("TEST_PHONE_NUMBER")
    if not to_number:
        to_number = input("\n📱 Enter phone number to call (format: +1234567890): ")

    # Create agent configuration
    agent_id = os.getenv("AGENT_ID")
    if not agent_id:
        raise ValueError("AGENT_ID must be set in environment variables")

    agent = Agent(
        agent_id=agent_id,
        dynamic_variables={
            "product_name": "Shrek",
            "first_name": "Janek",
        },
    )

    # Optional: Set first message
    # agent.set_first_message("Hello! I'm calling from Shrek. How can I help you today?")

    # Optional: Set language
    # agent.set_language("en")

    print(f"\n📋 Agent Configuration:")
    print(f"   Agent ID: {agent.agent_id}")
    print(f"   Dynamic Variables: {agent.dynamic_variables}")
    print(f"\n📞 Calling {to_number}...")

    try:
        # Initialize phone caller and make the call
        caller = PhoneCaller()

        # Option 1: Make call and wait for completion with transcript
        conversation_data = caller.make_call_and_wait(
            agent=agent,
            to_number=to_number,
            poll_interval=2,  # Check every 2 seconds
            timeout=300,  # 5 minute timeout
            print_transcript=True,  # Auto-print transcript when done
        )

        print("\n" + "=" * 60)
        print("✅ Call completed successfully!")
        print("=" * 60)
        print(f"\n📊 Call Details:")
        print(f"   Conversation ID: {conversation_data.conversation_id}")
        print(f"   Duration: {conversation_data.metadata.call_duration_secs}s")
        print(f"   Messages: {len(conversation_data.transcript)}")
        print(f"   Cost: {conversation_data.metadata.cost}")

        # Print full transcript
        print("\n" + "=" * 60)
        print("📝 Full Transcript:")
        print("=" * 60)
        for i, msg in enumerate(conversation_data.transcript, 1):
            emoji = "👤" if msg.role == "user" else "🤖"
            time_str = f"[{msg.time_in_call_secs:.1f}s]"
            print(f"\n{i}. {emoji} {msg.role.upper()} {time_str}")
            print(f"   {msg.message}")
        print("\n" + "=" * 60)

        # Option 2: Just make the call without waiting
        # response = caller.make_call(agent=agent, to_number=to_number)
        # print(f"Call initiated: {response.conversation_id}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()