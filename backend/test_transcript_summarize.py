"""
Test script for TranscriptSummarizer agent.
"""

import os
import asyncio
from dotenv import load_dotenv
from anthropic import AsyncAnthropic

from elevenlabs_wrapper import TranscriptSummarizer
from elevenlabs_wrapper.conversation_manager import TranscriptMessage

load_dotenv()


async def main():
    # Initialize Anthropic client
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY must be set in environment variables")

    client = AsyncAnthropic(api_key=anthropic_api_key)

    # Create example transcript from the conversation
    example_transcript = [
        TranscriptMessage(
            role="agent",
            message="Hello. I'm Ethan, calling about your recent chargeback request for the subscription of Shrek.",
            time_in_call_secs=0.0,
        ),
        TranscriptMessage(
            role="user",
            message="Hello.",
            time_in_call_secs=7.0,
        ),
        TranscriptMessage(
            role="agent",
            message="I need to inform you that a chargeback is not a valid method for canceling your Shrek subscription. That action will not be accepted.",
            time_in_call_secs=11.0,
        ),
        TranscriptMessage(
            role="user",
            message="Oh no, really? How do I fix it?",
            time_in_call_secs=20.0,
        ),
        TranscriptMessage(
            role="agent",
            message="You have two options to resolve this. We can proceed with an official cancellation of your Shrek subscription according to the terms, or you can choose to renew your subscription. Which option would you prefer?",
            time_in_call_secs=23.0,
        ),
        TranscriptMessage(
            role="user",
            message="I want to renew my subscription.",
            time_in_call_secs=36.0,
        ),
        TranscriptMessage(
            role="agent",
            message="Thank you for confirming. Your Shrek subscription will be...",
            time_in_call_secs=39.0,
        ),
    ]

    print("=" * 60)
    print("📝 Testing Transcript Summarizer")
    print("=" * 60)
    print("\n🎭 Example Transcript:")
    print("-" * 60)

    for i, msg in enumerate(example_transcript, 1):
        emoji = "👤" if msg.role == "user" else "🤖"
        print(f"{i}. {emoji} {msg.role.upper()} [{msg.time_in_call_secs:.1f}s]")
        print(f"   {msg.message}")
        if i < len(example_transcript):
            print()

    print("-" * 60)

    # Create summarizer
    print("\n🤖 Initializing TranscriptSummarizer...")
    summarizer = TranscriptSummarizer()

    # Generate summary
    print("🔄 Generating summary (focusing on user decisions only)...")
    summary = await summarizer.summarize(
        client=client,
        transcript=example_transcript,
    )

    print("\n" + "=" * 60)
    print("✨ SUMMARY (User decisions and actions only):")
    print("=" * 60)
    print(f"📊 {summary}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
