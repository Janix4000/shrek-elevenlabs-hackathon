#!/usr/bin/env python3
"""
Test the DisputeEvaluator module.

This script demonstrates:
1. Evaluating a conversation transcript to determine dispute resolution
2. Generating AI-powered evidence text for Stripe submission
3. Submitting evidence to Stripe (staged mode)
"""
import os
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stripe_integration.dispute_evaluator import DisputeEvaluator
from elevenlabs_wrapper.conversation_manager import TranscriptMessage


def create_mock_transcript_resolved():
    """Create a mock transcript where dispute was successfully resolved."""
    return [
        {
            "role": "agent",
            "message": "Hello. I'm Ethan, calling about your recent chargeback request for the subscription of Premium Digital Workspace.",
            "time_in_call_secs": 0.0,
        },
        {
            "role": "user",
            "message": "Hello.",
            "time_in_call_secs": 7.0,
        },
        {
            "role": "agent",
            "message": "I need to inform you that a chargeback is not a valid method for canceling your Premium Digital Workspace subscription. That action will not be accepted.",
            "time_in_call_secs": 11.0,
        },
        {
            "role": "user",
            "message": "Oh no, really? How do I fix it?",
            "time_in_call_secs": 20.0,
        },
        {
            "role": "agent",
            "message": "You have two options to resolve this. We can proceed with an official cancellation of your Premium Digital Workspace subscription according to the terms, or you can choose to renew your subscription. Which option would you prefer?",
            "time_in_call_secs": 23.0,
        },
        {
            "role": "user",
            "message": "I want to renew my subscription.",
            "time_in_call_secs": 36.0,
        },
        {
            "role": "agent",
            "message": "Thank you for confirming. Your Premium Digital Workspace subscription will be renewed. I'll withdraw the chargeback request now.",
            "time_in_call_secs": 39.0,
        },
        {
            "role": "user",
            "message": "Great, thank you for your help!",
            "time_in_call_secs": 46.0,
        },
    ]


def create_mock_transcript_unresolved():
    """Create a mock transcript where dispute was NOT resolved."""
    return [
        {
            "role": "agent",
            "message": "Hello. I'm calling about your recent chargeback request.",
            "time_in_call_secs": 0.0,
        },
        {
            "role": "user",
            "message": "Yeah, I want my money back. This is a scam!",
            "time_in_call_secs": 5.0,
        },
        {
            "role": "agent",
            "message": "I understand your concern. Let me explain the charges and see how we can help.",
            "time_in_call_secs": 10.0,
        },
        {
            "role": "user",
            "message": "No explanation needed. I'm keeping the chargeback. Don't call me again!",
            "time_in_call_secs": 15.0,
        },
    ]


def test_evaluate_transcript():
    """Test 1: Evaluate transcripts to determine resolution status."""
    print("=" * 80)
    print("TEST 1: TRANSCRIPT EVALUATION")
    print("=" * 80 + "\n")

    evaluator = DisputeEvaluator()
    test_charge_id = "ch_3SaQFuAITa6PCFHj0dnBlMJP"

    # Test resolved transcript
    print("📝 Testing RESOLVED transcript:")
    print("-" * 80)
    resolved_transcript = create_mock_transcript_resolved()

    try:
        evaluation = evaluator.evaluate_transcript(resolved_transcript, test_charge_id)

        print(f"✅ Evaluation Results:")
        print(f"   - Resolved: {evaluation['resolved']}")
        print(f"   - Resolution Type: {evaluation['resolution_type']}")
        print(f"   - Customer Sentiment: {evaluation['customer_sentiment']}")
        print(f"   - Key Points:")
        for point in evaluation['key_points']:
            print(f"     • {point}")
        print(f"   - Recommendation: {evaluation['recommendation']}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "-" * 80)

    # Test unresolved transcript
    print("\n📝 Testing UNRESOLVED transcript:")
    print("-" * 80)
    unresolved_transcript = create_mock_transcript_unresolved()

    try:
        evaluation = evaluator.evaluate_transcript(unresolved_transcript, test_charge_id)

        print(f"✅ Evaluation Results:")
        print(f"   - Resolved: {evaluation['resolved']}")
        print(f"   - Resolution Type: {evaluation['resolution_type']}")
        print(f"   - Customer Sentiment: {evaluation['customer_sentiment']}")
        print(f"   - Key Points:")
        for point in evaluation['key_points']:
            print(f"     • {point}")
        print(f"   - Recommendation: {evaluation['recommendation']}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n")


def test_generate_evidence():
    """Test 2: Generate evidence text for specific fields."""
    print("=" * 80)
    print("TEST 2: EVIDENCE GENERATION")
    print("=" * 80 + "\n")

    evaluator = DisputeEvaluator()
    test_charge_id = "ch_3SaQFuAITa6PCFHj0dnBlMJP"

    # Use resolved transcript for evidence generation
    transcript = create_mock_transcript_resolved()

    # First evaluate the transcript
    print("📊 Evaluating transcript first...")
    try:
        evaluation = evaluator.evaluate_transcript(transcript, test_charge_id)
        print(f"✅ Transcript evaluated: {evaluation['resolution_type']}\n")
    except Exception as e:
        print(f"❌ Evaluation failed: {e}\n")
        return

    # Fetch charge metadata
    print("💳 Fetching charge metadata...")
    try:
        charge = evaluator.stripe_client.get_charge(test_charge_id)
        metadata = charge.metadata or {}
        print(f"✅ Metadata fetched: {len(metadata)} fields\n")
    except Exception as e:
        print(f"❌ Failed to fetch metadata: {e}\n")
        return

    # Test generating evidence for key fields
    test_fields = [
        "cancellation_rebuttal",
        "product_description",
    ]

    for field in test_fields:
        print(f"📝 Generating evidence for: {field}")
        print("-" * 80)

        try:
            evidence_text = evaluator.generate_evidence_text(
                field_name=field,
                charge_metadata=metadata,
                transcript=transcript,
                evaluation=evaluation
            )

            # Show first 500 characters of evidence
            preview = evidence_text[:500] + "..." if len(evidence_text) > 500 else evidence_text
            print(f"✅ Generated ({len(evidence_text)} characters):")
            print(preview)
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

        print()


def test_submit_evidence():
    """Test 3: Complete workflow - submit evidence to Stripe (staged mode)."""
    print("=" * 80)
    print("TEST 3: COMPLETE EVIDENCE SUBMISSION WORKFLOW")
    print("=" * 80 + "\n")

    evaluator = DisputeEvaluator()
    test_charge_id = "ch_3SaQFuAITa6PCFHj0dnBlMJP"
    transcript = create_mock_transcript_resolved()

    print("⚠️  WARNING: This test will generate evidence and stage it in Stripe.")
    print("    It will NOT submit immediately (submit=False).")
    print("    You can review the staged evidence in Stripe dashboard.\n")

    response = input("Do you want to proceed? (yes/no): ").strip().lower()
    if response != "yes":
        print("❌ Test skipped by user.\n")
        return

    print("\n🚀 Starting complete evidence submission workflow...")
    print("-" * 80 + "\n")

    try:
        result = evaluator.submit_evidence_to_stripe(
            charge_id=test_charge_id,
            transcript=transcript,
            submit_immediately=False  # Stage only, don't submit to bank
        )

        print(f"\n✅ Evidence submission completed!")
        print(f"\n📊 Results:")
        print(f"   - Dispute ID: {result['dispute_id']}")
        print(f"   - Status: {result['status']}")
        print(f"\n📋 Evaluation:")
        print(f"   - Resolved: {result['evaluation']['resolved']}")
        print(f"   - Resolution Type: {result['evaluation']['resolution_type']}")
        print(f"   - Customer Sentiment: {result['evaluation']['customer_sentiment']}")
        print(f"\n📄 Evidence Generated ({len(result['evidence_generated'])} fields):")
        for field in result['evidence_generated']:
            print(f"   ✓ {field}")

        print(f"\n💡 Next steps:")
        print(f"   1. Review the staged evidence in Stripe dashboard")
        print(f"   2. If satisfied, submit evidence to bank using:")
        print(f"      stripe.Dispute.modify('{result['dispute_id']}', submit=True)")

    except Exception as e:
        print(f"❌ Error during evidence submission: {e}")
        import traceback
        traceback.print_exc()

    print()


def main():
    print("\n" + "=" * 80)
    print("DISPUTE EVALUATOR TEST SUITE")
    print("=" * 80 + "\n")

    print("This test suite demonstrates the DisputeEvaluator functionality:\n")
    print("1. Transcript evaluation (resolved vs unresolved)")
    print("2. AI-powered evidence text generation")
    print("3. Complete workflow with Stripe submission (staged mode)\n")

    # Test 1: Evaluate transcripts
    test_evaluate_transcript()

    # Test 2: Generate evidence text
    test_generate_evidence()

    # Test 3: Complete submission workflow
    test_submit_evidence()

    print("=" * 80)
    print("TEST SUITE COMPLETED")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
