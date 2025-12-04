#!/usr/bin/env python3
"""
View metadata from charges and disputes.
"""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stripe_integration import StripeClient


def view_charge_metadata(charge_id):
    """View all metadata for a specific charge"""
    client = StripeClient()

    print(f"\n{'='*80}")
    print(f"CHARGE METADATA: {charge_id}")
    print(f"{'='*80}\n")

    # Get the charge
    charge = client.get_charge(charge_id)

    print(f"Amount: ${charge.amount/100:.2f}")
    print(f"Currency: {charge.currency.upper()}")
    print(f"Description: {charge.description}")
    print(f"Status: {charge.status}")
    print(f"Created: {charge.created}")

    # Access metadata
    metadata = charge.metadata

    if not metadata:
        print("\n⚠️  No metadata found for this charge")
        return

    print(f"\n{'─'*80}")
    print(f"METADATA ({len(metadata)} fields)")
    print(f"{'─'*80}\n")

    # Display metadata in organized groups
    for key, value in sorted(metadata.items()):
        print(f"  {key:35s}: {value}")

    print(f"\n{'='*80}\n")

    return metadata


def view_latest_charges(limit=5):
    """View metadata from the latest charges"""
    client = StripeClient()

    print(f"\n{'='*80}")
    print(f"LATEST {limit} CHARGES WITH METADATA")
    print(f"{'='*80}\n")

    # List recent charges
    charges = client.list_charges(limit=limit)

    for i, charge in enumerate(charges, 1):
        print(f"[{i}] Charge: {charge.id}")
        print(f"    Amount: ${charge.amount/100:.2f}")
        print(f"    Description: {charge.description}")
        print(f"    Metadata fields: {len(charge.metadata) if charge.metadata else 0}")

        if charge.metadata:
            # Show key metadata fields (check both 'scenario' and 'scenario_type')
            scenario = charge.metadata.get('scenario') or charge.metadata.get('scenario_type', 'N/A')
            customer_email = charge.metadata.get('customer_email', 'N/A')
            print(f"    Scenario: {scenario}")
            print(f"    Customer: {customer_email}")
        print()


def search_by_scenario(scenario_type):
    """Find all charges with a specific scenario type"""
    client = StripeClient()

    print(f"\n{'='*80}")
    print(f"CHARGES WITH SCENARIO: {scenario_type}")
    print(f"{'='*80}\n")

    # List all charges and filter by metadata
    all_charges = client.list_charges(limit=100)

    matching = []
    for charge in all_charges:
        if charge.metadata:
            # Check both 'scenario' and 'scenario_type' fields
            charge_scenario = charge.metadata.get('scenario') or charge.metadata.get('scenario_type')
            if charge_scenario == scenario_type:
                matching.append(charge)

    print(f"Found {len(matching)} charge(s) with scenario '{scenario_type}':\n")

    for charge in matching:
        print(f"  • {charge.id}")
        print(f"    Amount: ${charge.amount/100:.2f}")
        print(f"    Customer: {charge.metadata.get('customer_name', 'Unknown')}")
        print(f"    Email: {charge.metadata.get('customer_email', 'Unknown')}")
        print()

    return matching


def main():
    if len(sys.argv) < 2:
        print("\n📋 METADATA VIEWER")
        print("="*80)
        print("\nUsage:")
        print("  # View specific charge metadata")
        print("  venv/bin/python scripts/view_metadata.py ch_XXXXX")
        print("\n  # View latest charges")
        print("  venv/bin/python scripts/view_metadata.py latest")
        print("\n  # Search by scenario")
        print("  venv/bin/python scripts/view_metadata.py scenario subscription_canceled")
        print("\nExamples:")
        print("  venv/bin/python scripts/view_metadata.py ch_3SaPLnAITa6PCFHj1qd3pMMQ")
        print("  venv/bin/python scripts/view_metadata.py latest")
        print("  venv/bin/python scripts/view_metadata.py scenario fraudulent")
        print()
        return 1

    command = sys.argv[1]

    if command == "latest":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        view_latest_charges(limit)
    elif command == "scenario":
        if len(sys.argv) < 3:
            print("Error: Please specify scenario type")
            return 1
        scenario_type = sys.argv[2]
        search_by_scenario(scenario_type)
    elif command.startswith("ch_"):
        view_charge_metadata(command)
    else:
        print(f"Error: Unknown command '{command}'")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
