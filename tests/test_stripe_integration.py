import pytest
import os
from stripe_integration import StripeClient
import stripe


@pytest.fixture
def stripe_client():
    """Fixture to create a StripeClient instance for testing"""
    return StripeClient()


@pytest.fixture
def test_customer_email():
    """Fixture providing a test email address"""
    return "test@example.com"


class TestStripeClient:
    """Test suite for Stripe integration"""

    def test_client_initialization(self):
        """Test that StripeClient initializes correctly with API key"""
        client = StripeClient()
        assert client.api_key is not None
        assert client.api_key.startswith("sk_test_")

    def test_client_initialization_with_custom_key(self):
        """Test that StripeClient can be initialized with a custom API key"""
        custom_key = "sk_test_custom_key"
        client = StripeClient(api_key=custom_key)
        assert client.api_key == custom_key

    def test_client_initialization_without_key_raises_error(self, monkeypatch):
        """Test that StripeClient raises error when no API key is available"""
        monkeypatch.delenv("STRIPE_SECRET_KEY", raising=False)
        with pytest.raises(ValueError, match="Stripe API key is required"):
            StripeClient()

    def test_create_customer(self, stripe_client, test_customer_email):
        """Test creating a new Stripe customer"""
        customer = stripe_client.create_customer(
            email=test_customer_email,
            name="Test User"
        )

        assert customer.id is not None
        assert customer.email == test_customer_email
        assert customer.name == "Test User"

        # Cleanup: delete the test customer
        stripe.Customer.delete(customer.id)

    def test_create_customer_without_name(self, stripe_client, test_customer_email):
        """Test creating a customer without providing a name"""
        customer = stripe_client.create_customer(email=test_customer_email)

        assert customer.id is not None
        assert customer.email == test_customer_email

        # Cleanup: delete the test customer
        stripe.Customer.delete(customer.id)

    def test_get_customer(self, stripe_client, test_customer_email):
        """Test retrieving an existing customer"""
        # First create a customer
        created_customer = stripe_client.create_customer(
            email=test_customer_email,
            name="Test User"
        )

        # Retrieve the customer
        retrieved_customer = stripe_client.get_customer(created_customer.id)

        assert retrieved_customer.id == created_customer.id
        assert retrieved_customer.email == test_customer_email

        # Cleanup: delete the test customer
        stripe.Customer.delete(created_customer.id)

    def test_create_payment_intent(self, stripe_client):
        """Test creating a payment intent"""
        amount = 1000  # $10.00
        currency = "usd"

        payment_intent = stripe_client.create_payment_intent(
            amount=amount,
            currency=currency
        )

        assert payment_intent.id is not None
        assert payment_intent.amount == amount
        assert payment_intent.currency == currency
        assert payment_intent.status == "requires_payment_method"

    def test_create_payment_intent_with_customer(self, stripe_client, test_customer_email):
        """Test creating a payment intent with a customer"""
        # Create a customer first
        customer = stripe_client.create_customer(email=test_customer_email)

        # Create payment intent with customer
        payment_intent = stripe_client.create_payment_intent(
            amount=2000,  # $20.00
            currency="usd",
            customer_id=customer.id
        )

        assert payment_intent.id is not None
        assert payment_intent.customer == customer.id
        assert payment_intent.amount == 2000

        # Cleanup
        stripe.Customer.delete(customer.id)

    def test_create_payment_intent_with_metadata(self, stripe_client):
        """Test creating a payment intent with metadata"""
        metadata = {
            "order_id": "12345",
            "product": "Test Product"
        }

        payment_intent = stripe_client.create_payment_intent(
            amount=1500,
            currency="usd",
            metadata=metadata
        )

        assert payment_intent.id is not None
        assert payment_intent.metadata["order_id"] == "12345"
        assert payment_intent.metadata["product"] == "Test Product"
