from typing import List, Dict, Any, Optional
import stripe
from .models import DisputeValidity, DisputeReason


class DisputeAnalyzer:
    """Analyzes disputes to identify invalid chargebacks and rule violations"""

    def __init__(self):
        self.fraud_indicators = []

    def analyze_dispute(
        self,
        dispute: stripe.Dispute,
        transaction_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze a dispute and determine if it's likely invalid/fraudulent.

        Args:
            dispute: Stripe Dispute object
            transaction_metadata: Original transaction metadata with evidence

        Returns:
            Analysis dictionary with validity assessment and recommendations
        """
        analysis = {
            "dispute_id": dispute.id,
            "charge_id": dispute.charge,
            "amount": dispute.amount,
            "currency": dispute.currency,
            "reason": dispute.reason,
            "status": dispute.status,
            "created": dispute.created,
            "validity": DisputeValidity.UNKNOWN,
            "fraud_score": 0,
            "fraud_indicators": [],
            "evidence_available": [],
            "recommended_action": "investigate",
            "notes": []
        }

        if not transaction_metadata:
            analysis["notes"].append("No transaction metadata available for analysis")
            return analysis

        # Calculate fraud score based on indicators
        fraud_score = 0
        indicators = []

        # Check for service delivery proof
        if transaction_metadata.get("service_delivered"):
            fraud_score += 20
            indicators.append("Service was marked as delivered")
            analysis["evidence_available"].append("Service delivery confirmation")

        # Check for service usage after purchase
        if transaction_metadata.get("service_accessed"):
            fraud_score += 30
            indicators.append("Customer accessed/used the service")
            analysis["evidence_available"].append("Usage logs")

            if transaction_metadata.get("login_count", 0) > 10:
                fraud_score += 20
                indicators.append(f"High usage: {transaction_metadata['login_count']} logins")

        # Check for tracking/delivery proof
        if transaction_metadata.get("tracking_number"):
            fraud_score += 25
            indicators.append("Delivery tracking available")
            analysis["evidence_available"].append("Shipping tracking")

            if transaction_metadata.get("delivered_date"):
                fraud_score += 15
                indicators.append("Product confirmed delivered")

            if transaction_metadata.get("signature"):
                fraud_score += 10
                indicators.append("Delivery signature obtained")
                analysis["evidence_available"].append("Delivery signature")

        # Check for prior refund
        if transaction_metadata.get("refund_processed"):
            fraud_score += 40
            indicators.append("Refund already processed - potential double-dip attempt")
            analysis["evidence_available"].append("Refund transaction record")
            analysis["notes"].append(
                f"CRITICAL: Refund already issued on {transaction_metadata.get('refund_date')}. "
                f"This appears to be a double-refund attempt."
            )

        # Check for serial disputer pattern
        if transaction_metadata.get("previous_disputes", 0) > 2:
            fraud_score += 35
            indicators.append(f"Serial disputer: {transaction_metadata['previous_disputes']} previous disputes")
            analysis["notes"].append(
                "WARNING: Customer has pattern of repeated disputes. Possible serial fraudster."
            )

        # Check for content download (digital goods)
        if transaction_metadata.get("content_downloaded"):
            fraud_score += 25
            indicators.append("Digital content was downloaded")
            analysis["evidence_available"].append("Download logs")

            if transaction_metadata.get("download_count", 0) > 1:
                fraud_score += 15
                indicators.append(f"Multiple downloads: {transaction_metadata['download_count']}")

        # Check for continued usage after dispute
        if transaction_metadata.get("continued_usage"):
            fraud_score += 30
            indicators.append("Customer continued using service after filing dispute")
            analysis["notes"].append(
                "STRONG INDICATOR: Customer still actively using service after claiming fraud/cancellation"
            )

        # Analyze specific dispute reasons
        if dispute.reason == "fraudulent":
            if fraud_score > 40:
                analysis["notes"].append(
                    "Fraudulent claim contradicted by strong usage/delivery evidence"
                )
        elif dispute.reason == "product_not_received":
            if transaction_metadata.get("tracking_number") and transaction_metadata.get("delivered_date"):
                analysis["notes"].append(
                    "Product marked as not received but tracking shows delivery"
                )
        elif dispute.reason == "duplicate":
            if transaction_metadata.get("transaction_count") == 1:
                fraud_score += 25
                indicators.append("Duplicate claim but only one transaction exists")
                analysis["notes"].append(
                    "Duplicate charge claimed but records show only one transaction"
                )
        elif dispute.reason == "subscription_canceled":
            if not transaction_metadata.get("cancellation_requested"):
                fraud_score += 30
                indicators.append("Cancellation claimed but no request in system")
                analysis["notes"].append(
                    "Customer claims cancellation but we have no record of cancellation request"
                )

        # Determine validity based on fraud score
        if fraud_score >= 60:
            analysis["validity"] = DisputeValidity.INVALID
            analysis["recommended_action"] = "contest_with_evidence"
        elif fraud_score >= 30:
            analysis["validity"] = DisputeValidity.INVALID
            analysis["recommended_action"] = "investigate_and_likely_contest"
        elif fraud_score < 15:
            analysis["validity"] = DisputeValidity.VALID
            analysis["recommended_action"] = "accept_or_resolve"
        else:
            analysis["validity"] = DisputeValidity.UNKNOWN
            analysis["recommended_action"] = "investigate_further"

        analysis["fraud_score"] = fraud_score
        analysis["fraud_indicators"] = indicators

        return analysis

    def generate_evidence_document(
        self,
        dispute: stripe.Dispute,
        transaction_metadata: Dict[str, Any],
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate evidence document for contesting a dispute.

        Args:
            dispute: Stripe Dispute object
            transaction_metadata: Original transaction metadata
            analysis: Analysis from analyze_dispute()

        Returns:
            Evidence dictionary ready for submission to Stripe
        """
        evidence = {}

        # Add customer communication
        if transaction_metadata.get("customer_email"):
            evidence["customer_email_address"] = transaction_metadata["customer_email"]

        # Add product description
        if transaction_metadata.get("description"):
            evidence["product_description"] = transaction_metadata["description"]

        # Add shipping documentation
        if transaction_metadata.get("tracking_number"):
            evidence["shipping_tracking_number"] = transaction_metadata["tracking_number"]

        # Add refund policy
        if transaction_metadata.get("refund_processed"):
            evidence["refund_policy"] = (
                f"Customer was already refunded {transaction_metadata['refund_amount']/100:.2f} "
                f"on {transaction_metadata.get('refund_date')}. "
                f"Refund ID: {transaction_metadata.get('refund_id')}"
            )

        # Add customer IP and usage logs
        if transaction_metadata.get("ip_address"):
            evidence["customer_purchase_ip"] = transaction_metadata["ip_address"]

        # Generate compelling narrative
        evidence["uncategorized_text"] = self._generate_evidence_narrative(
            dispute, transaction_metadata, analysis
        )

        return evidence

    def _generate_evidence_narrative(
        self,
        dispute: stripe.Dispute,
        transaction_metadata: Dict[str, Any],
        analysis: Dict[str, Any]
    ) -> str:
        """Generate a narrative explanation for the dispute response"""
        narrative_parts = [
            f"Dispute Response for Charge: {dispute.charge}",
            f"Amount: ${dispute.amount/100:.2f} {dispute.currency.upper()}",
            f"Dispute Reason: {dispute.reason}",
            "",
            "Our Analysis:",
        ]

        for note in analysis["notes"]:
            narrative_parts.append(f"- {note}")

        narrative_parts.append("")
        narrative_parts.append("Evidence Available:")
        for evidence in analysis["evidence_available"]:
            narrative_parts.append(f"- {evidence}")

        if analysis["fraud_indicators"]:
            narrative_parts.append("")
            narrative_parts.append("Fraud Indicators:")
            for indicator in analysis["fraud_indicators"]:
                narrative_parts.append(f"- {indicator}")

        narrative_parts.append("")
        narrative_parts.append(
            f"Fraud Score: {analysis['fraud_score']}/100 "
            f"(Validity: {analysis['validity']})"
        )

        return "\n".join(narrative_parts)

    def get_dispute_summary(self, disputes: List[stripe.Dispute]) -> Dict[str, Any]:
        """
        Generate summary statistics for a list of disputes.

        Args:
            disputes: List of Stripe Dispute objects

        Returns:
            Summary dictionary with statistics
        """
        if not disputes:
            return {
                "total_disputes": 0,
                "total_amount": 0,
                "by_reason": {},
                "by_status": {},
            }

        total_amount = sum(d.amount for d in disputes)
        by_reason = {}
        by_status = {}

        for dispute in disputes:
            # Count by reason
            reason = dispute.reason
            if reason not in by_reason:
                by_reason[reason] = {"count": 0, "amount": 0}
            by_reason[reason]["count"] += 1
            by_reason[reason]["amount"] += dispute.amount

            # Count by status
            status = dispute.status
            if status not in by_status:
                by_status[status] = {"count": 0, "amount": 0}
            by_status[status]["count"] += 1
            by_status[status]["amount"] += dispute.amount

        return {
            "total_disputes": len(disputes),
            "total_amount": total_amount,
            "total_amount_formatted": f"${total_amount/100:.2f}",
            "by_reason": by_reason,
            "by_status": by_status,
        }
