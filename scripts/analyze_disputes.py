#!/usr/bin/env python3
"""
Script to analyze existing disputes and identify fraudulent chargebacks.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stripe_integration import StripeClient, DisputeAnalyzer


def main():
    print("\n" + "="*80)
    print("STRIPE DISPUTE ANALYZER")
    print("="*80)

    # Initialize client
    print("\n🔧 Initializing Stripe client...")
    try:
        client = StripeClient()
        print("✓ Stripe client initialized successfully")
    except Exception as e:
        print(f"✗ Error: {e}")
        return 1

    # Get all disputes
    print("\n📋 Fetching disputes...")
    disputes = client.list_disputes(limit=100)

    if not disputes:
        print("ℹ No disputes found in your Stripe account")
        print("\nTo generate test disputes, run:")
        print("  python scripts/generate_dispute_data.py")
        return 0

    print(f"✓ Found {len(disputes)} dispute(s)")

    # Initialize analyzer
    analyzer = DisputeAnalyzer()

    # Get summary
    summary = analyzer.get_dispute_summary(disputes)

    print(f"\n{'='*80}")
    print("DISPUTE SUMMARY")
    print(f"{'='*80}")
    print(f"Total Disputes: {summary['total_disputes']}")
    print(f"Total Amount: {summary['total_amount_formatted']}")

    if summary['by_reason']:
        print(f"\nBy Reason:")
        for reason, data in summary['by_reason'].items():
            print(f"  • {reason}: {data['count']} (${data['amount']/100:.2f})")

    if summary['by_status']:
        print(f"\nBy Status:")
        for status, data in summary['by_status'].items():
            print(f"  • {status}: {data['count']} (${data['amount']/100:.2f})")

    # Analyze each dispute
    print(f"\n{'='*80}")
    print("DETAILED ANALYSIS")
    print(f"{'='*80}")

    for i, dispute in enumerate(disputes, 1):
        print(f"\n[{i}/{len(disputes)}] Dispute ID: {dispute.id}")
        print(f"{'─'*80}")
        print(f"  Charge: {dispute.charge}")
        print(f"  Amount: ${dispute.amount/100:.2f}")
        print(f"  Reason: {dispute.reason}")
        print(f"  Status: {dispute.status}")
        print(f"  Created: {dispute.created}")

        # Get the charge to retrieve metadata
        try:
            charge = client.get_charge(dispute.charge)
            metadata = charge.metadata or {}

            if metadata:
                analysis = analyzer.analyze_dispute(dispute, metadata)

                print(f"\n  Validity Assessment: {analysis['validity']}")
                print(f"  Fraud Score: {analysis['fraud_score']}/100")
                print(f"  Recommended Action: {analysis['recommended_action']}")

                if analysis['fraud_indicators']:
                    print(f"\n  Fraud Indicators:")
                    for indicator in analysis['fraud_indicators'][:3]:  # Show top 3
                        print(f"    • {indicator}")

                if analysis['notes']:
                    print(f"\n  Notes:")
                    for note in analysis['notes'][:2]:  # Show top 2
                        print(f"    • {note}")
            else:
                print(f"\n  ℹ No metadata available for analysis")

        except Exception as e:
            print(f"\n  ⚠ Error analyzing: {e}")

    print(f"\n{'='*80}")
    print("✓ Analysis complete!")
    print(f"{'='*80}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
