"""
Dispute Evaluator - Analyzes call transcripts and submits evidence to Stripe.

This module:
1. Evaluates conversation transcripts to determine if dispute was resolved
2. Generates professional evidence text using Claude AI
3. Submits comprehensive evidence to Stripe disputes
"""

import os
from typing import Dict, Any, List, Optional, Tuple
import stripe
from anthropic import Anthropic
from .client import StripeClient


class DisputeEvaluator:
    """
    Evaluates dispute resolution calls and submits evidence to Stripe.

    Uses Claude AI to analyze transcripts and generate professional evidence documentation.
    """

    def __init__(self, stripe_api_key: Optional[str] = None, anthropic_api_key: Optional[str] = None):
        """
        Initialize the Dispute Evaluator.

        Args:
            stripe_api_key: Stripe API key (optional, reads from env if not provided)
            anthropic_api_key: Anthropic API key (optional, reads from env if not provided)
        """
        self.stripe_client = StripeClient(api_key=stripe_api_key)
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")

        if not self.anthropic_api_key:
            raise ValueError("Anthropic API key is required. Set ANTHROPIC_API_KEY env variable.")

        self.anthropic_client = Anthropic(api_key=self.anthropic_api_key)

    def evaluate_transcript(
        self,
        transcript: List[Dict[str, Any]],
        charge_id: str
    ) -> Dict[str, Any]:
        """
        Evaluate conversation transcript to determine dispute resolution outcome.

        Args:
            transcript: List of conversation messages with role, text, timestamp
            charge_id: Stripe charge ID

        Returns:
            Dictionary with:
            - resolved: bool (whether dispute was resolved during call)
            - resolution_type: str (renewed, canceled, partial_refund, pending, unresolved)
            - customer_sentiment: str (satisfied, neutral, frustrated, angry)
            - key_points: list of important points from conversation
            - recommendation: str (recommended action)
        """
        # Format transcript for Claude
        transcript_text = self._format_transcript_for_analysis(transcript)

        prompt = f"""Analyze this customer service call transcript regarding a disputed charge.

TRANSCRIPT:
{transcript_text}

Provide a JSON response with the following structure:
{{
    "resolved": true/false,
    "resolution_type": "renewed|canceled|partial_refund|pending|unresolved",
    "customer_sentiment": "satisfied|neutral|frustrated|angry",
    "key_points": ["point 1", "point 2", ...],
    "recommendation": "recommended action to take"
}}

Evaluation criteria:
- RESOLVED: Customer agreed to keep subscription, accepted refund, or issue was fully resolved
- UNRESOLVED: Customer still wants chargeback, hung up angry, or no agreement reached
- Resolution types:
  * renewed: Customer agreed to keep the subscription
  * canceled: Customer agreed to cancel (avoiding chargeback)
  * partial_refund: Compromise reached with partial refund
  * pending: Needs follow-up action
  * unresolved: No agreement, customer still disputing

Return ONLY the JSON, no other text."""

        response = self.anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse JSON response
        import json
        import re

        response_text = response.content[0].text.strip()

        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            # Extract content between ```json and ``` or between ``` and ```
            match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', response_text, re.DOTALL)
            if match:
                response_text = match.group(1).strip()

        try:
            evaluation = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response. Raw response:\n{response_text}")
            raise ValueError(f"Claude did not return valid JSON: {e}")

        return evaluation

    def generate_evidence_text(
        self,
        field_name: str,
        charge_metadata: Dict[str, Any],
        transcript: List[Dict[str, Any]],
        evaluation: Dict[str, Any]
    ) -> str:
        """
        Generate professional evidence text for a specific field using Claude AI.

        Args:
            field_name: Name of the evidence field (e.g., "cancellation_rebuttal")
            charge_metadata: Metadata from Stripe charge
            transcript: Conversation transcript
            evaluation: Evaluation results from evaluate_transcript()

        Returns:
            Professional evidence text for the field
        """
        transcript_summary = self._format_transcript_for_analysis(transcript, max_messages=10)

        # Field-specific prompts
        field_prompts = {
            "access_activity_log": "Generate a detailed access activity log showing service usage. Include dates, actions, and proof of engagement.",
            "cancellation_rebuttal": "Write a professional rebuttal explaining why the cancellation claim is invalid, using evidence from metadata and call.",
            "cancellation_policy_disclosure": "Explain how and when the cancellation policy was presented to the customer.",
            "product_description": "Write a detailed product description including features and billing terms.",
            "refund_policy_disclosure": "Explain how the refund policy was disclosed to the customer.",
            "refund_refusal_explanation": "Provide a detailed explanation of why a refund cannot be issued, citing evidence.",
            "uncategorized_text": "Generate comprehensive dispute evidence including email history, usage metrics, and merchant position."
        }

        field_prompt = field_prompts.get(
            field_name,
            f"Generate professional evidence text for the '{field_name}' field."
        )

        prompt = f"""You are a dispute evidence specialist. Generate professional, factual evidence text for Stripe dispute submission.

FIELD: {field_name}
TASK: {field_prompt}

CHARGE METADATA:
{self._format_metadata_for_prompt(charge_metadata)}

CONVERSATION OUTCOME:
- Resolved: {evaluation.get('resolved', False)}
- Resolution Type: {evaluation.get('resolution_type', 'unknown')}
- Customer Sentiment: {evaluation.get('customer_sentiment', 'unknown')}
- Key Points: {', '.join(evaluation.get('key_points', []))}

RECENT CONVERSATION EXCERPT:
{transcript_summary}

REQUIREMENTS:
- Be factual and professional
- Use specific dates, numbers, and metrics from the metadata
- Reference the conversation outcome if relevant
- Maximum 20,000 characters
- Include concrete evidence only
- Organize with clear sections if needed

Generate the evidence text now:"""

        response = self.anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def submit_evidence_to_stripe(
        self,
        charge_id: str,
        transcript: List[Dict[str, Any]],
        submit_immediately: bool = False
    ) -> Dict[str, Any]:
        """
        Complete workflow: Evaluate transcript and submit evidence to Stripe.

        Args:
            charge_id: Stripe charge ID
            transcript: Conversation transcript
            submit_immediately: If True, immediately submits to bank. If False, stages evidence.

        Returns:
            Dictionary with:
            - evaluation: Transcript evaluation results
            - dispute: Updated Stripe dispute object
            - evidence_generated: List of evidence fields generated
        """
        # Get charge and metadata
        charge = self.stripe_client.get_charge(charge_id)
        metadata = charge.metadata or {}

        # Get dispute for this charge
        disputes = self.stripe_client.get_charge_disputes(charge_id)

        if not disputes:
            raise ValueError(f"No disputes found for charge {charge_id}")

        dispute = disputes[0]  # Get the first dispute
        dispute_id = dispute.id

        print(f"📊 Evaluating transcript for dispute {dispute_id}...")

        # Evaluate transcript
        evaluation = self.evaluate_transcript(transcript, charge_id)

        print(f"✅ Evaluation complete:")
        print(f"   - Resolved: {evaluation['resolved']}")
        print(f"   - Resolution Type: {evaluation['resolution_type']}")
        print(f"   - Customer Sentiment: {evaluation['customer_sentiment']}")

        # Generate evidence for key fields
        print(f"\n📝 Generating evidence using Claude AI...")

        evidence_fields = [
            "access_activity_log",
            "cancellation_rebuttal",
            "cancellation_policy_disclosure",
            "product_description",
            "refund_policy_disclosure",
            "refund_refusal_explanation",
            "uncategorized_text"
        ]

        evidence = {}
        evidence_generated = []

        for field in evidence_fields:
            print(f"   Generating: {field}...")
            evidence[field] = self.generate_evidence_text(
                field, metadata, transcript, evaluation
            )
            evidence_generated.append(field)

        # Add simple fields from metadata
        evidence["billing_address"] = metadata.get(
            'billing_address',
            'Address on file with payment provider'
        )
        evidence["customer_email_address"] = metadata.get('customer_email', 'N/A')
        evidence["customer_name"] = metadata.get('customer_name', 'N/A')
        evidence["customer_purchase_ip"] = metadata.get('purchase_ip', 'N/A')
        evidence["service_date"] = metadata.get(
            'subscription_start',
            metadata.get('billing_period_start', 'N/A')
        )

        print(f"\n📤 Submitting evidence to Stripe...")

        # Submit evidence to Stripe
        updated_dispute = stripe.Dispute.modify(
            dispute_id,
            evidence=evidence,
            submit=submit_immediately
        )

        print(f"✅ Evidence {'submitted' if submit_immediately else 'staged'} successfully!")

        return {
            "evaluation": evaluation,
            "dispute": updated_dispute,
            "evidence_generated": evidence_generated,
            "dispute_id": dispute_id,
            "status": updated_dispute.status
        }

    def _format_transcript_for_analysis(
        self,
        transcript: List[Dict[str, Any]],
        max_messages: Optional[int] = None
    ) -> str:
        """Format transcript for Claude analysis."""
        messages = transcript[:max_messages] if max_messages else transcript

        formatted = []
        for msg in messages:
            role = msg.get('role', 'unknown').upper()
            text = msg.get('message', msg.get('text', ''))
            time = msg.get('time_in_call_secs', msg.get('timestamp', 0))
            formatted.append(f"[{time:.1f}s] {role}: {text}")

        return "\n".join(formatted)

    def _format_metadata_for_prompt(self, metadata: Dict[str, Any]) -> str:
        """Format metadata as readable string."""
        lines = []
        for key, value in sorted(metadata.items()):
            lines.append(f"  {key}: {value}")
        return "\n".join(lines)
