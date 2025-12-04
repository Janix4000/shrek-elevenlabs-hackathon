#!/usr/bin/env python3
"""
Simple script to populate Stripe with test transaction data.
Creates customers, charges, and triggers disputes using test cards.
"""

import sys
import os
import time
import random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stripe_integration import StripeClient
import stripe


# Test card that triggers disputes automatically
DISPUTE_CARD = "tok_createDispute"  # Stripe's pre-made token for disputes
NORMAL_CARD = "tok_visa"  # Normal successful card
DECLINED_CARD = "tok_chargeDeclined"

# Product/service types for our business
PRODUCTS = [
    {"name": "Basic Subscription", "price": 999},  # $9.99
    {"name": "Premium Subscription", "price": 2999},  # $29.99
    {"name": "Enterprise Plan", "price": 9999},  # $99.99
    {"name": "One-time Purchase", "price": 4999},  # $49.99
    {"name": "Digital Course", "price": 14999},  # $149.99
    {"name": "Monthly Service", "price": 1999},  # $19.99
]

# Customer profiles
CUSTOMERS = [
    {"name": "Alice Johnson", "email": "alice.johnson@example.com", "will_dispute": False},
    {"name": "Bob Smith", "email": "bob.smith@example.com", "will_dispute": False},
    {"name": "Charlie Brown", "email": "charlie.brown@example.com", "will_dispute": True},
    {"name": "Diana Prince", "email": "diana.prince@example.com", "will_dispute": False},
    {"name": "Eve Adams", "email": "eve.adams@example.com", "will_dispute": True},
    {"name": "Frank Miller", "email": "frank.miller@example.com", "will_dispute": False},
    {"name": "Grace Lee", "email": "grace.lee@example.com", "will_dispute": True},
    {"name": "Henry Davis", "email": "henry.davis@example.com", "will_dispute": False},
    {"name": "Iris Chen", "email": "iris.chen@example.com", "will_dispute": False},
    {"name": "Jack Wilson", "email": "jack.wilson@example.com", "will_dispute": True},
]


def create_test_data(client: StripeClient, num_transactions: int = 20):
    """
    Create test transaction data in Stripe.

    Args:
        client: StripeClient instance
        num_transactions: Number of transactions to create
    """
    print("\n" + "="*80)
    print("CREATING TEST DATA IN STRIPE")
    print("="*80)
    print(f"Target: {num_transactions} transactions")
    print(f"Customers: {len(CUSTOMERS)} profiles")
    print(f"Products: {len(PRODUCTS)} types")
    print("="*80)

    created_customers = {}
    created_charges = []
    dispute_count = 0

    for i in range(num_transactions):
        print(f"\n[{i+1}/{num_transactions}] Creating transaction...")

        try:
            # Pick random customer and product
            customer_profile = random.choice(CUSTOMERS)
            product = random.choice(PRODUCTS)

            # Create or get customer
            customer_key = customer_profile["email"]
            if customer_key not in created_customers:
                print(f"  → Creating customer: {customer_profile['name']}")
                customer = client.create_customer(
                    email=customer_profile["email"],
                    name=customer_profile["name"]
                )
                created_customers[customer_key] = customer.id
                print(f"    ✓ Customer ID: {customer.id}")
            else:
                customer_id = created_customers[customer_key]
                print(f"  → Using existing customer: {customer_profile['name']}")

            customer_id = created_customers[customer_key]

            # Determine if this transaction will dispute
            will_dispute = customer_profile["will_dispute"] and random.random() < 0.7

            # Choose appropriate card token
            if will_dispute:
                source = DISPUTE_CARD
                print(f"  → Product: {product['name']} (${product['price']/100:.2f}) [WILL DISPUTE]")
            else:
                source = NORMAL_CARD
                print(f"  → Product: {product['name']} (${product['price']/100:.2f})")

            # Create metadata with random service usage data
            metadata = {
                "product_name": product["name"],
                "customer_type": "test",
                "created_at": datetime.now().isoformat(),
                # Simulate service delivery
                "service_delivered": True,
                "delivery_date": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
            }

            # Add usage data for some transactions
            if random.random() < 0.6:
                metadata.update({
                    "service_accessed": True,
                    "login_count": random.randint(1, 50),
                    "last_access": (datetime.now() - timedelta(days=random.randint(0, 7))).isoformat(),
                    "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                })

            # Add shipping data for some
            if random.random() < 0.3:
                metadata.update({
                    "tracking_number": f"1Z999AA1{random.randint(1000000000, 9999999999)}",
                    "delivered_date": (datetime.now() - timedelta(days=random.randint(1, 14))).isoformat(),
                    "signature": customer_profile["name"],
                })

            # Create charge
            print(f"  → Creating charge...")
            charge = client.create_charge(
                amount=product["price"],
                currency="usd",
                source=source,
                customer_id=customer_id,
                description=product["name"],
                metadata=metadata
            )

            created_charges.append({
                "charge_id": charge.id,
                "customer_name": customer_profile["name"],
                "product": product["name"],
                "amount": product["price"],
                "will_dispute": will_dispute,
            })

            if will_dispute:
                dispute_count += 1

            print(f"    ✓ Charge ID: {charge.id}")
            print(f"    ✓ Amount: ${charge.amount/100:.2f}")
            print(f"    ✓ Status: {charge.status}")

        except Exception as e:
            print(f"    ✗ Error: {str(e)}")

        # Small delay to avoid rate limits
        time.sleep(0.3)

    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✓ Customers created: {len(created_customers)}")
    print(f"✓ Charges created: {len(created_charges)}")
    print(f"✓ Expected disputes: {dispute_count}")
    print(f"✓ Clean transactions: {len(created_charges) - dispute_count}")

    print("\n" + "="*80)
    print("TRANSACTION DETAILS")
    print("="*80)
    for charge in created_charges:
        status = "🔴 WILL DISPUTE" if charge["will_dispute"] else "✅ CLEAN"
        print(f"{status} | {charge['customer_name']:20s} | ${charge['amount']/100:7.2f} | {charge['product']:30s}")

    print("\n" + "="*80)
    print(f"✓ Test data created successfully!")
    print("="*80)
    print("\nView in Stripe Dashboard:")
    print("  Customers: https://dashboard.stripe.com/test/customers")
    print("  Charges: https://dashboard.stripe.com/test/payments")
    print("  Disputes: https://dashboard.stripe.com/test/disputes")
    print("\nNote: Disputes may take a few moments to appear in your dashboard.")

    return {
        "customers": created_customers,
        "charges": created_charges,
        "dispute_count": dispute_count,
    }


def main():
    print("\n🎯 STRIPE TEST DATA GENERATOR")
    print("This script will create test transactions in your Stripe account.\n")

    # Get number of transactions
    try:
        num_transactions = int(input("How many transactions do you want to create? (default: 20): ") or "20")
    except ValueError:
        num_transactions = 20

    print(f"\n✓ Will create {num_transactions} transactions")
    print("✓ Some will trigger disputes automatically")
    print("✓ Various products and customer profiles\n")

    confirm = input("Continue? (y/n): ").lower()
    if confirm != 'y':
        print("Cancelled.")
        return 0

    # Initialize client
    try:
        client = StripeClient()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("Make sure your .env file has a valid STRIPE_SECRET_KEY")
        return 1

    # Create data
    result = create_test_data(client, num_transactions)

    print(f"\n✓ Done! Created {len(result['charges'])} transactions.")
    print(f"✓ {result['dispute_count']} disputes expected to appear shortly.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
