#!/usr/bin/env python3
"""
Complete Dispute Resolution Call Workflow
==========================================

This script runs the complete end-to-end workflow:
1. Fetches charge details from Stripe (customer info, product info, metadata)
2. Generates AI-powered dispute response arguments using Claude
3. Queries RAG knowledge base for relevant context
4. Makes phone call with ElevenLabs agent
5. Evaluates transcript with Claude AI
6. Generates professional evidence for Stripe
7. Submits evidence to Stripe automatically

All customer and product data is fetched from Stripe - no hardcoded data needed!

Usage:
    python run_dispute_call.py
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path before imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import after path is set up
from conversation.service import ConversationService  # noqa: E402
from conversation.models import ConversationRequest, ChargebackInfo  # noqa: E402


def run_complete_dispute_workflow(
    charge_id: str,
    reason: str = "subscription_canceled",
    fake_call: bool = False
):
    """
    Run complete dispute resolution workflow using Stripe integration.

    All customer and product data is automatically fetched from Stripe!

    Args:
        charge_id: Stripe charge ID (e.g., "ch_3SaQFuAITa6PCFHj0dnBlMJP")
        reason: Dispute reason (e.g., "subscription_canceled", "product_not_received")
        fake_call: If True, uses fake conversation for testing (default: False)

    Returns:
        ConversationResult with transcript, summary, and dispute status
    """
    print("=" * 80)
    print("DISPUTE RESOLUTION CALL - COMPLETE AUTOMATED WORKFLOW")
    print("=" * 80 + "\n")

    # Initialize service (includes Stripe, RAG, and DisputeEvaluator)
    print("📋 Initializing services...")
    print("   - ConversationService")
    print("   - Stripe Integration (DisputeResponseGenerator)")
    print("   - RAG Service (Pinecone vector database)")
    print("   - DisputeEvaluator (AI-powered evidence generation)")
    service = ConversationService()

    # Create request - user_info is optional, will be fetched from Stripe
    print(f"\n💳 Charge ID: {charge_id}")
    print(f"⚠️  Dispute Reason: {reason}")
    print(f"📊 Mode: {'FAKE CALL (5 second simulation)' if fake_call else 'REAL PHONE CALL'}\n")

    request = ConversationRequest(
        # user_info is optional - will be fetched from Stripe automatically
        chargeback_info=ChargebackInfo(
            charge_id=charge_id,
            product_name="Placeholder",  # Will be fetched from Stripe
            reason=reason
        )
    )

    # Create conversation
    print("🆕 Creating conversation...")
    conv_id = service.create_conversation(request)
    print(f"   Conversation ID: {conv_id}\n")

    # Run conversation - this automatically:
    # 1. Fetches customer data from Stripe (name, email, phone)
    # 2. Fetches product data from Stripe (name, description, price)
    # 3. Generates AI response arguments using Claude
    # 4. Queries RAG for dispute scripts and policies
    # 5. Makes phone call with ElevenLabs agent
    # 6. Evaluates transcript with Claude AI
    # 7. Generates evidence for Stripe
    # 8. Submits evidence immediately to Stripe
    print("🚀 Starting automated workflow...\n")
    print("=" * 80)
    print("WORKFLOW STEPS (ALL AUTOMATIC)")
    print("=" * 80)
    print("1. 💳 Fetch Stripe charge data (customer, product, metadata)")
    print("2. 🤖 Generate AI response arguments (15+ evidence points)")
    print("3. 🔍 Query RAG knowledge base (dispute scripts, policies)")
    print("4. 📞 Make phone call with ElevenLabs agent")
    print("5. 📊 Evaluate transcript with Claude AI")
    print("6. 📝 Generate professional evidence (7 Stripe fields)")
    print("7. ✅ Submit evidence to Stripe (immediate submission)")
    print("=" * 80 + "\n")

    service.run_conversation(conv_id, request, fake_conv=fake_call)

    # Get final result
    result = service.get_conversation_result(conv_id)

    print("\n" + "=" * 80)
    print("WORKFLOW COMPLETED SUCCESSFULLY")
    print("=" * 80 + "\n")

    print(f"📊 Conversation Status: {result.status}")
    print(f"⏱️  Duration: {result.duration_seconds:.1f} seconds")

    if result.transcript:
        print(f"💬 Transcript: {len(result.transcript)} messages")
        print("\n📝 First few messages:")
        for i, msg in enumerate(result.transcript[:3], 1):
            speaker_emoji = "👤" if msg.speaker == "user" else "🤖"
            print(f"   {i}. {speaker_emoji} {msg.speaker.upper()}: {msg.text[:80]}{'...' if len(msg.text) > 80 else ''}")

    if result.summary:
        print("\n💡 Summary:")
        print(f"   {result.summary}")

    if result.error:
        print(f"\n❌ Error: {result.error}")

    print("\n🎉 Evidence has been automatically submitted to Stripe!")
    print("   📍 Check dispute status: https://dashboard.stripe.com/test/disputes")
    print(f"   📍 View charge details: https://dashboard.stripe.com/test/payments/{charge_id}")
    print()

    return result


def main():
    """Main entry point for the script."""

    # ============================================================================
    # CONFIGURATION - Edit these values for your use case
    # ============================================================================

    CHARGE_ID = "ch_3SaQFuAITa6PCFHj0dnBlMJP"  # Stripe charge ID with dispute
    DISPUTE_REASON = "subscription_canceled"     # Dispute reason
    FAKE_CALL = False  # Set to True for 5-second test, False for real call

    # ============================================================================

    print("\n" + "=" * 80)
    print("STRIPE DISPUTE RESOLUTION - AUTOMATED WORKFLOW")
    print("=" * 80)
    print("\nThis script automatically:")
    print("  ✓ Fetches ALL data from Stripe (customer, product, metadata)")
    print("  ✓ Generates AI-powered response arguments")
    print("  ✓ Makes phone call with context-aware agent")
    print("  ✓ Evaluates call outcome with AI")
    print("  ✓ Submits evidence to Stripe immediately")
    print("\n" + "=" * 80)
    print("CONFIGURATION")
    print("=" * 80)
    print(f"Charge ID: {CHARGE_ID}")
    print(f"Dispute Reason: {DISPUTE_REASON}")
    print(f"Mode: {'FAKE CALL (5 second test)' if FAKE_CALL else 'REAL PHONE CALL'}")
    print("=" * 80 + "\n")

    # Validate environment variables
    required_env_vars = [
        "AGENT_ID",           # ElevenLabs agent ID
        "ANTHROPIC_API_KEY",  # Claude AI for response generation and evaluation
        "STRIPE_API_KEY",     # Stripe for charge/dispute data
        "ELEVENLABS_API_KEY", # ElevenLabs for phone calls
        "PINECONE_API_KEY",   # Pinecone for RAG
    ]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]

    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Set them in your .env file")
        sys.exit(1)

    # Confirm execution for real calls
    if not FAKE_CALL:
        print("⚠️  WARNING: This will make a REAL phone call!")
        print(f"   The system will fetch the phone number from Stripe charge: {CHARGE_ID}")
        response = input("\nContinue? (yes/no): ").strip().lower()
        if response != "yes":
            print("❌ Aborted by user")
            sys.exit(0)
        print()

    # Run the complete workflow
    try:
        result = run_complete_dispute_workflow(
            charge_id=CHARGE_ID,
            reason=DISPUTE_REASON,
            fake_call=FAKE_CALL
        )

        print("=" * 80)
        print("✅ SUCCESS - COMPLETE WORKFLOW FINISHED")
        print("=" * 80)
        print("\nWhat happened:")
        print("  1. ✅ Fetched customer & product data from Stripe")
        print("  2. ✅ Generated AI response arguments")
        print("  3. ✅ Queried RAG knowledge base")
        print("  4. ✅ Made phone call with AI agent")
        print("  5. ✅ Evaluated call transcript")
        print("  6. ✅ Generated professional evidence")
        print("  7. ✅ Submitted evidence to Stripe")
        print("\n💡 Check Stripe dashboard to see the submitted evidence!")
        print()

    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
