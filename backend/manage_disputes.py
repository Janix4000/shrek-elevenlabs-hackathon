#!/usr/bin/env python3
"""
Manage Stripe Disputes - Close existing and create new disputes for testing.

This script helps manage test disputes:
1. Close existing dispute (mark as lost/won)
2. Create new dispute for testing
3. List all disputes for a charge
"""
import os
import sys
from dotenv import load_dotenv
import stripe

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from stripe_integration.client import StripeClient


def list_disputes(charge_id: str):
    """List all disputes for a charge."""
    client = StripeClient()

    print(f"📋 Listing disputes for charge: {charge_id}\n")

    disputes = client.get_charge_disputes(charge_id)

    if not disputes:
        print("✅ No disputes found for this charge.")
        return []

    for i, dispute in enumerate(disputes, 1):
        print(f"{i}. Dispute: {dispute.id}")
        print(f"   Status: {dispute.status}")
        print(f"   Reason: {dispute.reason}")
        print(f"   Amount: ${dispute.amount / 100:.2f}")
        print(f"   Created: {dispute.created}")
        print(f"   Evidence submitted: {dispute.evidence_details.submission_count if dispute.evidence_details else 0}")
        print()

    return disputes


def close_dispute(dispute_id: str):
    """
    Close a dispute by marking it as lost.

    Note: In test mode, you can't actually close disputes the same way as production.
    The best approach is to let the dispute expire or create a new charge.
    """
    print(f"🔒 Closing dispute: {dispute_id}")

    try:
        # In test mode, disputes can't be fully closed like in production
        # But we can mark them with metadata to ignore them
        dispute = stripe.Dispute.modify(
            dispute_id,
            metadata={
                'closed_for_testing': 'true',
                'closed_at': str(stripe.util.convert_to_stripe_object({'created': 'now'}, None, None))
            }
        )
        print(f"✅ Dispute marked as closed (metadata updated)")
        print(f"   Status: {dispute.status}")
        return dispute
    except Exception as e:
        print(f"❌ Error closing dispute: {e}")
        return None


def create_test_dispute(charge_id: str):
    """
    Create a new test dispute for a charge.

    Note: This requires using Stripe's test dispute creation tokens.
    """
    print(f"🆕 Creating new test dispute for charge: {charge_id}\n")
    print("⚠️  Note: To create test disputes, you need to:")
    print("   1. Use a test card that triggers disputes (4000000000000259)")
    print("   2. Or manually create a dispute in Stripe Dashboard")
    print("   3. Test disputes are automatically created when using dispute test cards\n")

    print("💡 Recommended approach:")
    print("   Create a NEW charge with a different test card to get a fresh dispute.")
    print("   Use the populate_test_data.py script to create new test charges.\n")


def reset_charge_for_testing(charge_id: str):
    """Create a fresh charge for testing."""
    print(f"🔄 To reset for testing:\n")
    print("Option 1: Create a new test charge")
    print(f"   cd backend/scripts")
    print(f"   python populate_test_data.py\n")

    print("Option 2: Use Stripe Dashboard")
    print(f"   1. Go to: https://dashboard.stripe.com/test/disputes")
    print(f"   2. Find dispute for charge: {charge_id}")
    print(f"   3. The dispute will expire after submission limit is reached\n")

    print("Option 3: Create new charge with dispute test card")
    print(f"   Card: 4000000000000259 (automatically creates dispute)")
    print(f"   This creates a fresh charge with a new dispute")


def main():
    """Main entry point."""

    CHARGE_ID = "ch_3SaQFuAITa6PCFHj0dnBlMJP"

    print("=" * 80)
    print("STRIPE DISPUTE MANAGEMENT")
    print("=" * 80 + "\n")

    # List current disputes
    disputes = list_disputes(CHARGE_ID)

    if not disputes:
        print("\n💡 No disputes to manage.")
        print("   To create test disputes, use a dispute test card (4000000000000259)")
        return

    print("=" * 80)
    print("OPTIONS")
    print("=" * 80)
    print("1. Close current dispute (mark with metadata)")
    print("2. Show reset instructions")
    print("3. Exit")
    print()

    choice = input("Select option (1-3): ").strip()

    if choice == "1":
        print()
        for i, dispute in enumerate(disputes, 1):
            print(f"Closing dispute {i}/{len(disputes)}: {dispute.id}")
            close_dispute(dispute.id)
            print()

        print("✅ All disputes marked as closed")
        print("\n💡 Note: The disputes still exist in Stripe but are marked with metadata.")
        print("   To get fresh disputes, create a new charge with populate_test_data.py")

    elif choice == "2":
        print()
        reset_charge_for_testing(CHARGE_ID)

    else:
        print("👋 Exiting...")

    print()


if __name__ == "__main__":
    main()
