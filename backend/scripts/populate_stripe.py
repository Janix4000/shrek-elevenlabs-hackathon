#!/usr/bin/env python3
"""
Populate Stripe with diverse test transaction data covering all dispute scenarios.
Run with: venv/bin/python scripts/populate_stripe.py [number_of_transactions]
"""

import sys
import os
import time
import random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stripe_integration import StripeClient


# Stripe test tokens
DISPUTE_CARD = "tok_createDispute"
NORMAL_CARD = "tok_visa"

# All possible dispute reasons
DISPUTE_REASONS = [
    "bank_cannot_process",
    "check_returned",
    "credit_not_processed",
    "customer_initiated",
    "debit_not_authorized",
    "duplicate",
    "fraudulent",
    "general",
    "incorrect_account_details",
    "insufficient_funds",
    "noncompliant",
    "product_not_received",
    "product_unacceptable",
    "subscription_canceled",
    "unrecognized"
]

# Products with different characteristics
PRODUCTS = [
    {"name": "Basic Subscription", "price": 999, "type": "subscription"},
    {"name": "Premium Subscription", "price": 2999, "type": "subscription"},
    {"name": "Enterprise Plan", "price": 9999, "type": "subscription"},
    {"name": "One-time Purchase", "price": 4999, "type": "one_time"},
    {"name": "Digital Course", "price": 14999, "type": "digital"},
    {"name": "Monthly Service", "price": 1999, "type": "service"},
    {"name": "Physical Product", "price": 7999, "type": "physical"},
    {"name": "Software License", "price": 29999, "type": "digital"},
    {"name": "Consulting Service", "price": 49999, "type": "service"},
    {"name": "Annual Membership", "price": 19999, "type": "subscription"},
]

# Customer profiles with different behaviors
CUSTOMERS = [
    {"name": "Alice Johnson", "email": "alice.j@example.com", "risk": "low"},
    {"name": "Bob Smith", "email": "bob.s@example.com", "risk": "low"},
    {"name": "Charlie Fraudster", "email": "charlie.f@example.com", "risk": "high"},
    {"name": "Diana Prince", "email": "diana.p@example.com", "risk": "low"},
    {"name": "Eve Disputer", "email": "eve.d@example.com", "risk": "high"},
    {"name": "Frank Miller", "email": "frank.m@example.com", "risk": "medium"},
    {"name": "Grace Serial", "email": "grace.s@example.com", "risk": "high"},
    {"name": "Henry Davis", "email": "henry.d@example.com", "risk": "low"},
    {"name": "Iris Refunder", "email": "iris.r@example.com", "risk": "medium"},
    {"name": "Jack Abuser", "email": "jack.a@example.com", "risk": "high"},
]


def generate_metadata(product, customer, will_dispute, scenario_type):
    """Generate rich metadata for different dispute scenarios"""

    base_metadata = {
        "product_name": product["name"],
        "product_type": product["type"],
        "customer_name": customer["name"],
        "customer_email": customer["email"],
        "customer_risk": customer["risk"],
        "purchase_date": datetime.now().isoformat(),
        "scenario_type": scenario_type,
    }

    # Add scenario-specific metadata
    if scenario_type == "credit_not_processed":
        base_metadata.update({
            "refund_promised": True,
            "refund_processed": random.choice([True, False]),
            "refund_date": (datetime.now() - timedelta(days=random.randint(5, 20))).isoformat(),
            "refund_amount": product["price"],
            "refund_id": f"re_{random.randint(1000000, 9999999)}",
            "customer_notified": True,
        })

    elif scenario_type == "duplicate":
        base_metadata.update({
            "transaction_count": random.choice([1, 2]),
            "appears_duplicate": random.choice([True, False]),
            "original_charge_id": f"ch_{random.randint(1000000, 9999999)}" if random.random() < 0.5 else None,
            "paid_by_other_means": random.choice([False, True]),
            "other_payment_method": random.choice([None, "cash", "check", "paypal"]),
        })

    elif scenario_type == "fraudulent":
        base_metadata.update({
            "service_delivered": True,
            "service_accessed": random.choice([True, False]),
            "login_count": random.randint(0, 100),
            "last_access": (datetime.now() - timedelta(days=random.randint(0, 7))).isoformat(),
            "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "device_fingerprint": f"fp_{random.randint(100000, 999999)}",
            "cvv_check": random.choice(["pass", "fail", "unavailable"]),
            "avs_check": random.choice(["pass", "fail", "partial"]),
            "card_present": False,
        })

    elif scenario_type == "product_not_received":
        has_tracking = random.random() < 0.7
        base_metadata.update({
            "product_type": "physical",
            "shipped": has_tracking,
            "tracking_number": f"1Z{random.randint(100000000000, 999999999999)}" if has_tracking else None,
            "carrier": random.choice(["UPS", "FedEx", "USPS"]) if has_tracking else None,
            "shipped_date": (datetime.now() - timedelta(days=random.randint(5, 15))).isoformat() if has_tracking else None,
            "delivered": random.choice([True, False]) if has_tracking else False,
            "delivered_date": (datetime.now() - timedelta(days=random.randint(1, 10))).isoformat() if has_tracking and random.random() < 0.8 else None,
            "signature_required": random.choice([True, False]),
            "delivery_signature": customer["name"] if random.random() < 0.5 else None,
        })

    elif scenario_type == "product_unacceptable":
        base_metadata.update({
            "product_received": True,
            "return_requested": random.choice([True, False]),
            "return_policy_shown": True,
            "return_window_days": 30,
            "days_since_purchase": random.randint(1, 60),
            "product_description_match": random.choice([True, False]),
            "customer_complaint": random.choice([
                "not_as_described",
                "defective",
                "wrong_item",
                "quality_issues"
            ]),
        })

    elif scenario_type == "subscription_canceled":
        base_metadata.update({
            "subscription_type": "recurring",
            "billing_cycle": "monthly",
            "cancellation_requested": random.choice([True, False]),
            "cancellation_date": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat() if random.random() < 0.5 else None,
            "cancellation_policy_shown": True,
            "continued_service_usage": random.choice([True, False]),
            "last_login_after_cancellation": (datetime.now() - timedelta(days=random.randint(0, 5))).isoformat() if random.random() < 0.7 else None,
        })

    elif scenario_type == "unrecognized":
        base_metadata.update({
            "statement_descriptor": random.choice(["XYZ*CRYPTIC123", "SHREK*APP", "ONLINE*PURCHASE"]),
            "business_name_clear": random.choice([True, False]),
            "customer_contacted_before_dispute": random.choice([True, False]),
            "service_delivered": True,
            "customer_account_active": True,
        })

    elif scenario_type == "general":
        base_metadata.update({
            "dispute_category": "other",
            "service_delivered": random.choice([True, False]),
            "customer_satisfied": random.choice([True, False]),
            "support_tickets": random.randint(0, 5),
        })

    # Add common evidence fields
    if product["type"] in ["digital", "service"]:
        base_metadata.update({
            "download_count": random.randint(0, 50),
            "content_accessed": random.choice([True, False]),
            "access_logs_available": True,
        })

    # Add customer history
    base_metadata.update({
        "previous_purchases": random.randint(0, 20),
        "account_age_days": random.randint(1, 1000),
        "previous_disputes": random.randint(0, 5) if customer["risk"] == "high" else random.randint(0, 1),
    })

    return base_metadata


def main():
    num_transactions = int(sys.argv[1]) if len(sys.argv) > 1 else 30

    print("\n" + "="*80)
    print("CREATING COMPREHENSIVE STRIPE TEST DATA")
    print("="*80)
    print(f"Transactions: {num_transactions}")
    print(f"Dispute scenarios: {len(DISPUTE_REASONS)} types")
    print("="*80 + "\n")

    client = StripeClient()
    created_customers = {}
    created_charges = []
    dispute_count = 0
    scenarios_used = {}

    for i in range(num_transactions):
        print(f"[{i+1}/{num_transactions}] ", end="", flush=True)

        try:
            # Random selections
            customer_profile = random.choice(CUSTOMERS)
            product = random.choice(PRODUCTS)

            # Determine dispute scenario
            will_dispute = customer_profile["risk"] in ["high", "medium"] and random.random() < 0.6
            scenario_type = random.choice(DISPUTE_REASONS) if will_dispute else "clean"

            # Track scenarios
            scenarios_used[scenario_type] = scenarios_used.get(scenario_type, 0) + 1

            # Create/get customer
            email = customer_profile["email"]
            if email not in created_customers:
                customer = client.create_customer(
                    email=email,
                    name=customer_profile["name"]
                )
                created_customers[email] = customer.id

            customer_id = created_customers[email]

            # Choose card source
            source = DISPUTE_CARD if will_dispute else NORMAL_CARD

            # Generate rich metadata
            metadata = generate_metadata(product, customer_profile, will_dispute, scenario_type)
            metadata["customer_id"] = customer_id

            # Create charge
            charge = client.create_charge(
                amount=product["price"],
                currency="usd",
                source=source,
                description=f"{product['name']} - {customer_profile['name']}",
                metadata=metadata
            )

            # Display
            status = "🔴" if will_dispute else "✅"
            scenario_display = scenario_type if will_dispute else "CLEAN"
            print(f"{status} {scenario_display:25s} | {customer_profile['name']:20s} | ${product['price']/100:7.2f} | {product['name']:25s}")

            created_charges.append({
                "charge_id": charge.id,
                "scenario": scenario_type,
                "will_dispute": will_dispute,
            })

            if will_dispute:
                dispute_count += 1

        except Exception as e:
            print(f"ERROR: {str(e)[:80]}")

        time.sleep(0.2)

    # Summary
    print("\n" + "="*80)
    print("✅ DATA CREATION COMPLETE!")
    print("="*80)
    print(f"Customers: {len(created_customers)}")
    print(f"Transactions: {len(created_charges)}")
    print(f"Clean: {len(created_charges) - dispute_count}")
    print(f"Disputes: {dispute_count}")

    print("\n📊 Scenarios Created:")
    for scenario, count in sorted(scenarios_used.items()):
        print(f"  • {scenario:30s}: {count}")

    print("\n" + "="*80)
    print("View in Stripe Dashboard:")
    print("  • Customers: https://dashboard.stripe.com/test/customers")
    print("  • Payments:  https://dashboard.stripe.com/test/payments")
    print("  • Disputes:  https://dashboard.stripe.com/test/disputes")
    print("\n⏳ Disputes will appear within seconds/minutes in test mode.\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
