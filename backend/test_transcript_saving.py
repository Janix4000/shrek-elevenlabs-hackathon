#!/usr/bin/env python3
"""
Test transcript saving and success/failure evaluation.
Uses fake_conv=True for quick testing without making real calls.
"""
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from conversation.service import ConversationService
from conversation.models import ConversationRequest, UserInfo, ChargebackInfo


def main():
    print("=" * 80)
    print("TESTING TRANSCRIPT SAVING & SUCCESS/FAILURE EVALUATION")
    print("=" * 80 + "\n")

    service = ConversationService()

    # Test 1: Successful conversation (using fake_conv=True for quick testing)
    print("Test 1: Successful Conversation (Fake)")
    print("-" * 80)

    request = ConversationRequest(
        user_info=UserInfo(
            first_name="Test",
            last_name="User",
            phone_number="+1234567890"
        ),
        chargeback_info=ChargebackInfo(
            charge_id="ch_3SaQFuAITa6PCFHj0dnBlMJP",
            product_name="Premium Digital Workspace",
            reason="subscription_canceled"
        )
    )

    # Create conversation and run with fake_conv=True (no real call)
    conv_id = service.create_conversation(request)
    print(f"  Conversation ID: {conv_id}")
    print(f"  Status: {service.get_conversation_result(conv_id).status}")

    # Run the conversation
    print(f"  Running fake conversation...")
    service.run_conversation(conv_id, request, fake_conv=True)

    # Check result
    result = service.get_conversation_result(conv_id)
    print(f"\n  ✅ Result:")
    print(f"     Status: {result.status}")
    print(f"     Duration: {result.duration_seconds:.1f}s")
    print(f"     Transcript messages: {len(result.transcript) if result.transcript else 0}")
    print(f"     Error: {result.error or 'None'}")

    # Check if transcript was saved
    transcripts = service.list_saved_transcripts()
    print(f"\n  💾 Saved transcripts: {len(transcripts)}")
    if transcripts:
        print(f"     Latest: {transcripts[0]['filename']}")

    print("\n" + "=" * 80)
    print("TEST COMPLETED")
    print("=" * 80 + "\n")

    print("📁 To view saved transcripts, run:")
    print("   python view_transcripts.py")
    print()


if __name__ == "__main__":
    main()
