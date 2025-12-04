#!/usr/bin/env python3
"""
Script to generate test data with various dispute scenarios.

This script will:
1. Create customers with different profiles
2. Create charges that will trigger disputes (using test cards)
3. Wait for disputes to be created
4. Analyze disputes to identify invalid/fraudulent chargebacks
5. Generate evidence for contesting invalid disputes
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stripe_integration import StripeClient, TestDataGenerator


def main():
    print("\n" + "="*80)
    print("STRIPE DISPUTE DETECTION SYSTEM - TEST DATA GENERATOR")
    print("="*80)
    print("\nThis script will generate test transactions and disputes to demonstrate")
    print("how to identify fraudulent chargebacks where customers violate terms.")
    print("="*80)

    # Initialize client
    print("\n🔧 Initializing Stripe client...")
    try:
        client = StripeClient()
        print("✓ Stripe client initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing Stripe client: {e}")
        print("\nMake sure your .env file contains a valid STRIPE_SECRET_KEY")
        return 1

    # Create generator
    generator = TestDataGenerator(client)

    # Generate all scenarios
    print("\n📝 Generating transaction scenarios...")
    summary = generator.generate_all_scenarios()

    # Print summary
    generator.print_summary(summary)

    # Check for disputes
    print(f"\n⏳ Waiting for disputes to be created in Stripe...")
    print("(In test mode with test cards, disputes appear within seconds)")

    disputes = generator.wait_for_disputes(max_wait_seconds=15)

    if not disputes:
        print("\n⚠ No disputes found yet.")
        print("\nNOTE: Disputes from test cards may take a few moments to appear.")
        print("You can:")
        print("  1. Wait a bit longer and check your Stripe Dashboard")
        print("  2. Run: python scripts/analyze_disputes.py")
        print("  3. Or manually create disputes in the Stripe Dashboard")
        return 0

    # Analyze disputes
    analyses = generator.analyze_disputes(disputes)

    # Print final report
    print(f"\n{'='*80}")
    print("FINAL REPORT")
    print(f"{'='*80}")

    invalid_disputes = [
        a for a in analyses
        if a["analysis"]["validity"] == "invalid"
    ]

    print(f"\nTotal Disputes Analyzed: {len(analyses)}")
    print(f"Invalid/Fraudulent Disputes: {len(invalid_disputes)}")
    print(f"Potential Losses Prevented: ${sum(a['dispute'].amount for a in invalid_disputes)/100:.2f}")

    if invalid_disputes:
        print(f"\n🚨 INVALID DISPUTES TO CONTEST:")
        for analysis_result in invalid_disputes:
            dispute = analysis_result["dispute"]
            record = analysis_result["transaction_record"]
            analysis = analysis_result["analysis"]

            print(f"\n  • {record['customer_name']}")
            print(f"    Amount: ${dispute.amount/100:.2f}")
            print(f"    Reason: {dispute.reason}")
            print(f"    Fraud Score: {analysis['fraud_score']}/100")
            print(f"    Action: {analysis['recommended_action']}")

    print(f"\n{'='*80}")
    print("✓ Test data generation complete!")
    print(f"{'='*80}")

    print("\nNext steps:")
    print("  1. Check Stripe Dashboard: https://dashboard.stripe.com/test/disputes")
    print("  2. View created customers and charges")
    print("  3. Run: python scripts/analyze_disputes.py (to re-analyze)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
