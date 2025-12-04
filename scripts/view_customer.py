#!/usr/bin/env python3
"""
View customer details including billing information.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stripe_integration import StripeClient


def view_customer_details(customer_id):
    """View all details for a specific customer"""
    client = StripeClient()

    print("\n" + "="*80)
    print(f"CUSTOMER DETAILS: {customer_id}")
    print("="*80 + "\n")

    customer = client.get_customer(customer_id)

    print(f"Customer ID: {customer.id}")
    print(f"Name: {customer.name}")
    print(f"Email: {customer.email}")
    print(f"Phone: {customer.phone or 'Not provided'}")
    print(f"Created: {customer.created}")

    # Billing Address
    if customer.address:
        print("\n" + "─"*80)
        print("BILLING ADDRESS")
        print("─"*80 + "\n")
        print(f"  Line 1: {customer.address.line1 or 'Not provided'}")
        print(f"  Line 2: {customer.address.line2 or 'Not provided'}")
        print(f"  City: {customer.address.city or 'Not provided'}")
        print(f"  State: {customer.address.state or 'Not provided'}")
        print(f"  Postal Code: {customer.address.postal_code or 'Not provided'}")
        print(f"  Country: {customer.address.country or 'Not provided'}")
    else:
        print("\n⚠️  No billing address on file")

    print("\n" + "="*80 + "\n")

    return customer


def main():
    if len(sys.argv) < 2:
        print("\n📋 CUSTOMER VIEWER")
        print("="*80)
        print("\nUsage:")
        print("  venv/bin/python scripts/view_customer.py cus_XXXXX")
        print("\nExample:")
        print("  venv/bin/python scripts/view_customer.py cus_TXUdPhnn1KiLXn")
        print()
        return 1

    customer_id = sys.argv[1]

    if not customer_id.startswith("cus_"):
        print("Error: Customer ID must start with 'cus_'")
        return 1

    view_customer_details(customer_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
