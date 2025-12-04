import os
import stripe
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class StripeClient:
    """Client for interacting with Stripe API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Stripe client with API key.

        Args:
            api_key: Stripe API key. If not provided, reads from STRIPE_SECRET_KEY env variable.
        """
        self.api_key = api_key or os.getenv("STRIPE_SECRET_KEY")
        if not self.api_key:
            raise ValueError("Stripe API key is required")
        stripe.api_key = self.api_key

    def create_customer(self, email: str, name: Optional[str] = None) -> stripe.Customer:
        """
        Create a new Stripe customer.

        Args:
            email: Customer email address
            name: Customer name (optional)

        Returns:
            Created Stripe Customer object
        """
        customer_data = {"email": email}
        if name:
            customer_data["name"] = name

        return stripe.Customer.create(**customer_data)

    def get_customer(self, customer_id: str) -> stripe.Customer:
        """
        Retrieve a Stripe customer by ID.

        Args:
            customer_id: Stripe customer ID

        Returns:
            Stripe Customer object
        """
        return stripe.Customer.retrieve(customer_id)

    def create_payment_intent(
        self,
        amount: int,
        currency: str = "usd",
        customer_id: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> stripe.PaymentIntent:
        """
        Create a payment intent.

        Args:
            amount: Amount in cents (e.g., 1000 for $10.00)
            currency: Three-letter ISO currency code
            customer_id: Optional Stripe customer ID
            metadata: Optional metadata dictionary

        Returns:
            Created PaymentIntent object
        """
        payment_intent_data = {
            "amount": amount,
            "currency": currency,
        }

        if customer_id:
            payment_intent_data["customer"] = customer_id

        if metadata:
            payment_intent_data["metadata"] = metadata

        return stripe.PaymentIntent.create(**payment_intent_data)

    def create_charge(
        self,
        amount: int,
        currency: str,
        source: str,
        customer_id: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        billing_details: Optional[Dict[str, Any]] = None
    ) -> stripe.Charge:
        """
        Create a charge (direct charge, can trigger disputes with test cards).

        Args:
            amount: Amount in cents
            currency: Three-letter ISO currency code
            source: Payment source (token or test card number)
            customer_id: Optional customer ID
            description: Optional description
            metadata: Optional metadata
            billing_details: Optional billing details (address, email, name, phone)

        Returns:
            Created Charge object
        """
        charge_data = {
            "amount": amount,
            "currency": currency,
            "source": source,
        }

        if customer_id:
            charge_data["customer"] = customer_id

        if description:
            charge_data["description"] = description

        if metadata:
            charge_data["metadata"] = metadata

        if billing_details:
            charge_data["billing_details"] = billing_details

        return stripe.Charge.create(**charge_data)

    def create_token(self, card_number: str, exp_month: int = 12, exp_year: int = 2025) -> stripe.Token:
        """
        Create a card token from a card number (for testing).

        Args:
            card_number: Card number (can be test card)
            exp_month: Expiration month
            exp_year: Expiration year

        Returns:
            Created Token object
        """
        return stripe.Token.create(
            card={
                "number": card_number,
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvc": "123",
            },
        )

    def get_charge(self, charge_id: str) -> stripe.Charge:
        """
        Retrieve a charge by ID.

        Args:
            charge_id: Stripe charge ID

        Returns:
            Charge object
        """
        return stripe.Charge.retrieve(charge_id)

    def list_charges(self, limit: int = 100) -> List[stripe.Charge]:
        """
        List all charges.

        Args:
            limit: Maximum number of charges to return

        Returns:
            List of Charge objects
        """
        return stripe.Charge.list(limit=limit).data

    def list_disputes(self, limit: int = 100) -> List[stripe.Dispute]:
        """
        List all disputes.

        Args:
            limit: Maximum number of disputes to return

        Returns:
            List of Dispute objects
        """
        return stripe.Dispute.list(limit=limit).data

    def get_dispute(self, dispute_id: str) -> stripe.Dispute:
        """
        Retrieve a dispute by ID.

        Args:
            dispute_id: Stripe dispute ID

        Returns:
            Dispute object
        """
        return stripe.Dispute.retrieve(dispute_id)

    def get_charge_disputes(self, charge_id: str) -> List[stripe.Dispute]:
        """
        Get all disputes for a specific charge.

        Args:
            charge_id: Stripe charge ID

        Returns:
            List of disputes for the charge
        """
        disputes = stripe.Dispute.list(charge=charge_id)
        return disputes.data

    def submit_dispute_evidence(
        self,
        dispute_id: str,
        evidence: Dict[str, Any]
    ) -> stripe.Dispute:
        """
        Submit evidence for a dispute.

        Args:
            dispute_id: Stripe dispute ID
            evidence: Dictionary of evidence fields

        Returns:
            Updated Dispute object
        """
        return stripe.Dispute.modify(dispute_id, evidence=evidence)

    def close_dispute(self, dispute_id: str) -> stripe.Dispute:
        """
        Close a dispute (accept the loss).

        Args:
            dispute_id: Stripe dispute ID

        Returns:
            Updated Dispute object
        """
        return stripe.Dispute.close(dispute_id)
