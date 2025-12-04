#!/usr/bin/env python3
"""
Update customer phone number in Stripe charge metadata.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from stripe_integration.client import StripeClient

def update_phone_number(charge_id: str, new_phone: str):
    """Update the customer_phone in charge metadata."""

    client = StripeClient()

    print(f"💳 Fetching charge: {charge_id}")
    charge = client.get_charge(charge_id)

    print(f"📱 Current phone: {charge.metadata.get('customer_phone', 'N/A')}")
    print(f"📱 New phone: {new_phone}")

    # Update metadata
    import stripe
    updated_charge = stripe.Charge.modify(
        charge_id,
        metadata={
            **charge.metadata,
            'customer_phone': new_phone
        }
    )

    print(f"✅ Phone number updated successfully!")
    print(f"   Charge: {charge_id}")
    print(f"   New phone: {updated_charge.metadata['customer_phone']}")

if __name__ == "__main__":
    CHARGE_ID = "ch_3SaQFuAITa6PCFHj0dnBlMJP"
    NEW_PHONE = "+48668092344"

    update_phone_number(CHARGE_ID, NEW_PHONE)
