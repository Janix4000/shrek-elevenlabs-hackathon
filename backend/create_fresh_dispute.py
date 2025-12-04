#!/usr/bin/env python3
"""
Create a fresh test charge with a dispute for testing.

This script creates a NEW charge that will automatically have a dispute,
giving you a fresh dispute to test with (no evidence submission limits).
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import stripe

load_dotenv()

stripe.api_key = os.getenv("STRIPE_API_KEY")

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def create_charge_with_dispute(phone_number: str = "+48668092344"):
    """
    Create a new test charge with comprehensive metadata.

    Uses test card 4000000000000259 which automatically creates a dispute.
    """

    print("=" * 80)
    print("CREATING FRESH TEST CHARGE WITH DISPUTE")
    print("=" * 80 + "\n")

    # Comprehensive metadata (same structure as populate_test_data.py)
    metadata = {
        # Customer Information
        'customer_name': 'Robert Disputer',
        'customer_email': 'disputed.subscription@example.com',
        'customer_phone': phone_number,
        'customer_id': 'cus_test_' + datetime.now().strftime('%Y%m%d%H%M%S'),

        # Product Information
        'product_name': 'Premium Digital Workspace',
        'product_type': 'digital_subscription',
        'subscription_tier': 'premium',
        'product_code': 'PDW-PREM-001',

        # Billing Information
        'billing_cycle': 'monthly',
        'billing_period_start': '2025-10-20T01:18:46.169833',
        'billing_period_end': '2025-11-20T01:18:46.169833',
        'subscription_start': '2025-10-20T01:18:46.169833',
        'last_charge_date': '2025-10-20T01:18:46.169833',
        'next_charge_date': '2025-11-20T01:18:46.169833',
        'billing_address': '123 Main St, Anytown, CA 12345',
        'purchase_ip': '192.168.1.100',

        # Usage Metrics
        'logins_count': '23',
        'api_calls_count': '342',
        'files_uploaded': '8',
        'storage_used_gb': '23.4',
        'last_login_date': '2025-12-03T14:30:00',

        # Email Engagement
        'renewal_reminder_email_opened': 'true',
        'final_billing_reminder_opened': 'true',
        'invoice_email_opened': 'true',
        'renewal_reminder_sent': '2025-10-13T01:18:46',
        'final_reminder_sent': '2025-10-17T01:18:46',
        'invoice_sent': '2025-10-20T01:18:46',

        # Account Settings
        'auto_renewal_enabled': 'true',
        'cancellation_requested': 'false',
        'support_tickets_count': '0',
        'terms_accepted_date': '2025-10-20T01:18:46',

        # Transaction History
        'previous_successful_charges': '2',
        'previous_disputes': '0',
        'account_age_days': '45',
        'payment_method_verified': 'true',
    }

    print("💳 Creating charge with dispute test card...")
    print(f"   Card: 4000000000000259 (automatically triggers dispute)")
    print(f"   Amount: $29.99")
    print(f"   Phone: {phone_number}")
    print()

    try:
        # Create charge using dispute test card
        charge = stripe.Charge.create(
            amount=2999,  # $29.99
            currency='usd',
            source='tok_createDispute',  # Special token that creates a dispute
            description='Premium Digital Workspace - Monthly Subscription Renewal',
            metadata=metadata
        )

        print(f"✅ Charge created successfully!")
        print(f"   Charge ID: {charge.id}")
        print(f"   Amount: ${charge.amount / 100:.2f}")
        print(f"   Status: {charge.status}")
        print(f"   Customer: {metadata['customer_name']}")
        print(f"   Phone: {phone_number}")
        print()

        print(f"⏳ Stripe will automatically create a dispute for this charge")
        print(f"   (This may take a few moments in test mode)")
        print()

        print(f"📝 Update your run_dispute_call.py with this charge ID:")
        print(f"   CHARGE_ID = \"{charge.id}\"")
        print()

        print(f"🔍 View in Stripe Dashboard:")
        print(f"   Charge: https://dashboard.stripe.com/test/payments/{charge.id}")
        print(f"   Disputes: https://dashboard.stripe.com/test/disputes")
        print()

        return charge

    except Exception as e:
        print(f"❌ Error creating charge: {e}")
        print()
        print("💡 Note: Make sure you're using Stripe test mode API keys")
        return None


def main():
    """Main entry point."""

    # Check for API key
    if not os.getenv("STRIPE_API_KEY"):
        print("❌ STRIPE_API_KEY not found in environment")
        print("   Set it in your .env file")
        sys.exit(1)

    # Phone number from .env or default
    phone = os.getenv("TEST_PHONE_NUMBER", "+48668092344")

    print(f"\n📞 Using phone number: {phone}")
    print(f"   (Set TEST_PHONE_NUMBER in .env to change)\n")

    # Create the charge
    charge = create_charge_with_dispute(phone)

    if charge:
        print("=" * 80)
        print("✅ SUCCESS - FRESH DISPUTE CREATED")
        print("=" * 80)
        print()
        print("Next steps:")
        print("1. Wait a few moments for dispute to appear in Stripe")
        print("2. Update CHARGE_ID in run_dispute_call.py")
        print("3. Run: python run_dispute_call.py")
        print()


if __name__ == "__main__":
    main()
