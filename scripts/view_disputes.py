#!/usr/bin/env python3
"""
View disputes in Stripe account.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stripe_integration import StripeClient


def main():
    client = StripeClient()

    print("\n" + "="*80)
    print("DISPUTES IN YOUR STRIPE ACCOUNT")
    print("="*80 + "\n")

    disputes = client.list_disputes(limit=20)

    if not disputes:
        print("No disputes found.\n")
        return 0

    print(f"Found {len(disputes)} dispute(s):\n")

    for i, dispute in enumerate(disputes, 1):
        charge = client.get_charge(dispute.charge)
        scenario = charge.metadata.get('scenario', 'N/A') if charge.metadata else 'N/A'
        scenario_type = charge.metadata.get('scenario_type', 'N/A') if charge.metadata else 'N/A'

        print(f"[{i}] Dispute ID: {dispute.id}")
        print(f"    Charge: {dispute.charge}")
        print(f"    Amount: ${dispute.amount/100:.2f}")
        print(f"    Reason: {dispute.reason}")
        print(f"    Status: {dispute.status}")
        print(f"    Scenario: {scenario if scenario != 'N/A' else scenario_type}")

        if charge.metadata:
            customer_name = charge.metadata.get('customer_name', 'Unknown')
            customer_email = charge.metadata.get('customer_email', 'Unknown')
            print(f"    Customer: {customer_name} ({customer_email})")

        print()

    print("="*80 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
