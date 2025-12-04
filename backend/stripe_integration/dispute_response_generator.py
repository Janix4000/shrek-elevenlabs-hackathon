"""
Dispute Response Generator - Generate human-readable arguments for responding to disputing customers.
Uses Anthropic Claude to analyze charge metadata and create compelling response text.
"""

import os
from typing import Dict, Any, Tuple, Optional
from anthropic import Anthropic
from .client import StripeClient


class DisputeResponseGenerator:
    """
    Generate response arguments for disputed charges using AI.

    This class fetches charge metadata from Stripe and uses Claude AI to generate
    human-readable text that can be used when communicating with disputing customers.
    """

    def __init__(self, stripe_api_key: Optional[str] = None, anthropic_api_key: Optional[str] = None):
        """
        Initialize the Dispute Response Generator.

        Args:
            stripe_api_key: Stripe API key (optional, reads from env if not provided)
            anthropic_api_key: Anthropic API key (optional, reads from env if not provided)
        """
        self.stripe_client = StripeClient(api_key=stripe_api_key)
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")

        if not self.anthropic_api_key:
            raise ValueError("Anthropic API key is required. Set ANTHROPIC_API_KEY env variable or pass it directly.")

        self.anthropic_client = Anthropic(api_key=self.anthropic_api_key)

    def fetch_charge_metadata(self, charge_id: str) -> Dict[str, Any]:
        """
        Fetch charge metadata from Stripe.

        Args:
            charge_id: Stripe charge ID (e.g., ch_xxxxx)

        Returns:
            Dictionary containing charge metadata
        """
        charge = self.stripe_client.get_charge(charge_id)
        return charge.metadata or {}

    def generate_response_arguments(self, metadata: Dict[str, Any]) -> str:
        """
        Use Claude AI to generate response arguments from metadata.

        Args:
            metadata: Charge metadata dictionary

        Returns:
            Human-readable text with arguments to use when responding to the disputer
        """
        # Build the prompt for Claude
        prompt = f"""Analyze the following charge metadata and extract all arguments we can leverage when communicating with a customer who disputed this charge.

Charge Metadata:
{self._format_metadata_for_prompt(metadata)}

Output ONLY a numbered list of arguments/evidence points. Each point should be:
- Clear and factual
- Based directly on the metadata
- Actionable for use in customer communication

Format: Simple numbered list, nothing more, nothing less. No introduction, no conclusion, just the arguments."""

        # Call Claude API
        message = self.anthropic_client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the text response
        response_text = message.content[0].text
        return response_text

    def _format_metadata_for_prompt(self, metadata: Dict[str, Any]) -> str:
        """Format metadata as a readable string for the prompt."""
        lines = []
        for key, value in sorted(metadata.items()):
            lines.append(f"  {key}: {value}")
        return "\n".join(lines)

    def generate_dispute_response(self, charge_id: str) -> Tuple[str, str, str]:
        """
        Complete workflow: Fetch metadata and generate response.

        Args:
            charge_id: Stripe charge ID

        Returns:
            Tuple of (prepared_text, phone_number, customer_name)
        """
        # Fetch metadata
        metadata = self.fetch_charge_metadata(charge_id)

        if not metadata:
            raise ValueError(f"No metadata found for charge {charge_id}")

        # Extract customer info
        customer_name = metadata.get('customer_name', 'Unknown Customer')
        customer_phone = metadata.get('customer_phone', 'No phone number on file')

        # Generate response text
        response_text = self.generate_response_arguments(metadata)

        return (response_text, customer_phone, customer_name)

    def get_customer_info(self, charge_id: str) -> Dict[str, str]:
        """
        Get customer information from charge metadata.

        Args:
            charge_id: Stripe charge ID

        Returns:
            Dictionary with customer details
        """
        metadata = self.fetch_charge_metadata(charge_id)

        return {
            "name": metadata.get('customer_name', 'Unknown'),
            "email": metadata.get('customer_email', 'Unknown'),
            "phone": metadata.get('customer_phone', 'Unknown'),
            "customer_id": metadata.get('customer_id', 'Unknown'),
        }

    def get_charge_details(self, charge_id: str) -> Dict[str, Any]:
        """
        Get comprehensive charge details including product information.

        Args:
            charge_id: Stripe charge ID

        Returns:
            Dictionary with complete charge details including:
            - customer_info: name, email, phone, customer_id
            - product_info: name, description, code/sku, category, price
            - charge_info: amount, currency, date, status
            - metadata: all metadata fields
        """
        charge = self.stripe_client.get_charge(charge_id)
        metadata = charge.metadata or {}

        # Extract customer information
        customer_info = {
            "name": metadata.get('customer_name', 'Unknown'),
            "email": metadata.get('customer_email', 'Unknown'),
            "phone": metadata.get('customer_phone', 'Unknown'),
            "customer_id": metadata.get('customer_id', 'Unknown'),
        }

        # Extract product information from metadata
        product_info = {
            "name": metadata.get('product_name', charge.description or 'Unknown Product'),
            "description": charge.description or metadata.get('product_type', 'No description available'),
            "code": metadata.get('subscription_tier', metadata.get('product_code', 'N/A')),
            "category": metadata.get('product_type', 'N/A'),
            "price": charge.amount / 100,  # Convert cents to dollars
        }

        # Extract charge information
        charge_info = {
            "amount": charge.amount / 100,
            "currency": charge.currency.upper(),
            "date": metadata.get('subscription_start', metadata.get('billing_period_start', 'N/A')),
            "status": charge.status,
            "charge_id": charge_id,
        }

        return {
            "customer_info": customer_info,
            "product_info": product_info,
            "charge_info": charge_info,
            "metadata": metadata,
        }
