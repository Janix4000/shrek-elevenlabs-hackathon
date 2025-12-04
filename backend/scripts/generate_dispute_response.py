#!/usr/bin/env python3
"""
Generate AI-powered response arguments for disputed charges.
Uses Claude AI to analyze charge metadata and create compelling arguments.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stripe_integration import DisputeResponseGenerator


def main():
    if len(sys.argv) < 2:
        print("\n🤖 AI DISPUTE RESPONSE GENERATOR")
        print("="*80)
        print("\nUsage:")
        print("  venv/bin/python scripts/generate_dispute_response.py ch_XXXXX")
        print("\nExample:")
        print("  venv/bin/python scripts/generate_dispute_response.py ch_3SaQFuAITa6PCFHj0dnBlMJP")
        print("\nThis will:")
        print("  1. Fetch charge metadata from Stripe")
        print("  2. Use Claude AI to generate response arguments")
        print("  3. Return prepared text, customer phone, and name")
        print()
        return 1

    charge_id = sys.argv[1]

    if not charge_id.startswith("ch_"):
        print("Error: Charge ID must start with 'ch_'")
        return 1

    print("\n" + "="*80)
    print("AI DISPUTE RESPONSE GENERATOR")
    print("="*80 + "\n")

    try:
        # Initialize the generator
        print("📋 Step 1: Initializing AI Response Generator...")
        generator = DisputeResponseGenerator()
        print("   ✓ Stripe and Anthropic clients initialized")

        # Fetch metadata
        print(f"\n📊 Step 2: Fetching metadata for charge {charge_id}...")
        metadata = generator.fetch_charge_metadata(charge_id)
        print(f"   ✓ Found {len(metadata)} metadata fields")

        # Generate response
        print("\n🤖 Step 3: Generating response arguments using Claude AI...")
        print("   (This may take 5-10 seconds)")
        response_text, phone, name = generator.generate_dispute_response(charge_id)

        # Display results
        print("\n" + "="*80)
        print("✅ RESPONSE GENERATED SUCCESSFULLY")
        print("="*80)
        print(f"\nCustomer Name: {name}")
        print(f"Customer Phone: {phone}")
        print("\n" + "─"*80)
        print("RESPONSE TEXT FOR CUSTOMER:")
        print("─"*80)
        print()
        print(response_text)
        print("\n" + "="*80)

        return 0

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
