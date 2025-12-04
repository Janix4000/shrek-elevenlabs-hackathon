import time
from typing import List, Dict, Any
import stripe
from .client import StripeClient
from .models import TRANSACTION_SCENARIOS, TransactionScenario
from .dispute_analyzer import DisputeAnalyzer


class TestDataGenerator:
    """Generates test data for dispute scenarios"""

    def __init__(self, stripe_client: StripeClient):
        self.client = stripe_client
        self.analyzer = DisputeAnalyzer()
        self.created_customers = []
        self.created_charges = []
        self.transaction_records = []

    def generate_all_scenarios(self) -> Dict[str, Any]:
        """
        Generate all predefined transaction scenarios.

        Returns:
            Summary of created transactions and expected disputes
        """
        print("="*80)
        print("GENERATING TEST DATA FOR DISPUTE SCENARIOS")
        print("="*80)

        for i, scenario in enumerate(TRANSACTION_SCENARIOS, 1):
            print(f"\n[{i}/{len(TRANSACTION_SCENARIOS)}] Processing: {scenario.customer_name}")
            print(f"   Email: {scenario.customer_email}")
            print(f"   Amount: ${scenario.amount/100:.2f}")
            print(f"   Will Dispute: {scenario.will_dispute}")
            print(f"   Validity: {scenario.dispute_validity}")

            try:
                result = self.create_transaction_scenario(scenario)
                self.transaction_records.append(result)
                print(f"   ✓ Customer created: {result['customer_id']}")
                print(f"   ✓ Charge created: {result['charge_id']}")

                if scenario.will_dispute:
                    print(f"   ⚠ Dispute expected ({scenario.dispute_reason})")
                    print(f"   📝 {scenario.notes[:100]}...")

            except Exception as e:
                print(f"   ✗ Error: {str(e)}")

            # Small delay to avoid rate limits
            time.sleep(0.5)

        return self.get_summary()

    def create_transaction_scenario(self, scenario: TransactionScenario) -> Dict[str, Any]:
        """
        Create a single transaction scenario.

        Args:
            scenario: TransactionScenario to create

        Returns:
            Dictionary with created customer, charge, and metadata
        """
        # Create customer
        customer = self.client.create_customer(
            email=scenario.customer_email,
            name=scenario.customer_name
        )
        self.created_customers.append(customer.id)

        # Create payment method and charge
        # Use Stripe's test token directly instead of creating from raw card number
        try:
            # Try creating token (requires raw card API access)
            token = self.client.create_token(scenario.card_number)
            source = token.id
        except Exception as e:
            # Fallback: Use the card number directly as source (works in some test modes)
            # Or use a pre-made test token
            print(f"   Note: Using direct card source (token creation not available)")
            source = scenario.card_number

        # Create charge
        charge = self.client.create_charge(
            amount=scenario.amount,
            currency="usd",
            source=source,
            customer_id=customer.id,
            description=scenario.description,
            metadata=scenario.metadata
        )
        self.created_charges.append(charge.id)

        return {
            "customer_id": customer.id,
            "customer_email": scenario.customer_email,
            "customer_name": scenario.customer_name,
            "charge_id": charge.id,
            "amount": scenario.amount,
            "description": scenario.description,
            "will_dispute": scenario.will_dispute,
            "dispute_reason": scenario.dispute_reason.value if scenario.dispute_reason else None,
            "dispute_validity": scenario.dispute_validity.value,
            "notes": scenario.notes,
            "metadata": scenario.metadata,
            "created_at": charge.created
        }

    def wait_for_disputes(self, max_wait_seconds: int = 10) -> List[stripe.Dispute]:
        """
        Wait for disputes to be created (in test mode, they appear quickly).

        Args:
            max_wait_seconds: Maximum time to wait

        Returns:
            List of disputes found
        """
        print(f"\n{'='*80}")
        print("WAITING FOR DISPUTES TO BE CREATED...")
        print(f"{'='*80}")

        disputes = []
        for i in range(max_wait_seconds):
            print(f"Checking for disputes... ({i+1}/{max_wait_seconds})")
            all_disputes = self.client.list_disputes()

            # Filter to only our charges
            our_disputes = [
                d for d in all_disputes
                if d.charge in self.created_charges
            ]

            if our_disputes:
                disputes = our_disputes
                print(f"✓ Found {len(disputes)} disputes!")
                break

            time.sleep(1)

        return disputes

    def analyze_disputes(self, disputes: List[stripe.Dispute]) -> List[Dict[str, Any]]:
        """
        Analyze all disputes and generate reports.

        Args:
            disputes: List of Stripe Dispute objects

        Returns:
            List of analysis results
        """
        print(f"\n{'='*80}")
        print("ANALYZING DISPUTES")
        print(f"{'='*80}")

        analyses = []

        for dispute in disputes:
            # Find the original transaction record
            transaction_record = next(
                (r for r in self.transaction_records if r["charge_id"] == dispute.charge),
                None
            )

            if not transaction_record:
                print(f"\n⚠ Warning: No transaction record found for dispute {dispute.id}")
                continue

            metadata = transaction_record.get("metadata", {})
            analysis = self.analyzer.analyze_dispute(dispute, metadata)

            analyses.append({
                "dispute": dispute,
                "transaction_record": transaction_record,
                "analysis": analysis
            })

            self._print_dispute_analysis(dispute, transaction_record, analysis)

        return analyses

    def _print_dispute_analysis(
        self,
        dispute: stripe.Dispute,
        transaction_record: Dict[str, Any],
        analysis: Dict[str, Any]
    ):
        """Print formatted dispute analysis"""
        print(f"\n{'─'*80}")
        print(f"DISPUTE: {dispute.id}")
        print(f"{'─'*80}")
        print(f"Customer: {transaction_record['customer_name']} ({transaction_record['customer_email']})")
        print(f"Charge: {dispute.charge}")
        print(f"Amount: ${dispute.amount/100:.2f}")
        print(f"Reason: {dispute.reason}")
        print(f"Status: {dispute.status}")
        print(f"\nVALIDITY ASSESSMENT:")
        print(f"  Validity: {analysis['validity']}")
        print(f"  Fraud Score: {analysis['fraud_score']}/100")
        print(f"  Recommended Action: {analysis['recommended_action']}")

        if analysis['fraud_indicators']:
            print(f"\nFRAUD INDICATORS:")
            for indicator in analysis['fraud_indicators']:
                print(f"  • {indicator}")

        if analysis['evidence_available']:
            print(f"\nEVIDENCE AVAILABLE:")
            for evidence in analysis['evidence_available']:
                print(f"  • {evidence}")

        if analysis['notes']:
            print(f"\nNOTES:")
            for note in analysis['notes']:
                print(f"  • {note}")

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of generated test data"""
        return {
            "total_customers": len(self.created_customers),
            "total_charges": len(self.created_charges),
            "total_transactions": len(self.transaction_records),
            "expected_disputes": sum(
                1 for r in self.transaction_records if r["will_dispute"]
            ),
            "invalid_disputes_expected": sum(
                1 for r in self.transaction_records
                if r["dispute_validity"] == "invalid"
            ),
            "customers": self.created_customers,
            "charges": self.created_charges,
            "transaction_records": self.transaction_records,
        }

    def print_summary(self, summary: Dict[str, Any]):
        """Print formatted summary"""
        print(f"\n{'='*80}")
        print("SUMMARY")
        print(f"{'='*80}")
        print(f"Total Customers Created: {summary['total_customers']}")
        print(f"Total Charges Created: {summary['total_charges']}")
        print(f"Expected Disputes: {summary['expected_disputes']}")
        print(f"Expected Invalid Disputes: {summary['invalid_disputes_expected']}")

        print(f"\nTRANSACTION BREAKDOWN:")
        for record in summary['transaction_records']:
            status = "🔴 WILL DISPUTE" if record['will_dispute'] else "✅ CLEAN"
            validity = record['dispute_validity'].upper() if record['will_dispute'] else "N/A"
            print(f"  {status} - {record['customer_name']}: ${record['amount']/100:.2f} ({validity})")
