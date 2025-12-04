from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class DisputeReason(str, Enum):
    """Stripe dispute reasons"""
    FRAUDULENT = "fraudulent"
    DUPLICATE = "duplicate"
    PRODUCT_NOT_RECEIVED = "product_not_received"
    CREDIT_NOT_PROCESSED = "credit_not_processed"
    GENERAL = "general"
    SUBSCRIPTION_CANCELED = "subscription_canceled"
    UNRECOGNIZED = "unrecognized"


class DisputeValidity(str, Enum):
    """Whether a dispute is valid or represents customer abuse"""
    VALID = "valid"  # Customer has legitimate complaint
    INVALID = "invalid"  # Customer is abusing chargeback system
    UNKNOWN = "unknown"  # Need more investigation


class TestCardType(str, Enum):
    """Stripe test cards for different scenarios"""
    NORMAL = "4242424242424242"  # Normal successful charge
    DISPUTE_FRAUDULENT = "4000000000000259"  # Triggers fraudulent dispute
    DISPUTE_PRODUCT_NOT_RECEIVED = "4000000000002685"  # For simulating product not received
    DECLINE = "4000000000000002"  # Card will be declined


@dataclass
class TransactionScenario:
    """Represents a transaction scenario with expected dispute behavior"""
    customer_email: str
    customer_name: str
    amount: int  # in cents
    description: str
    card_number: str
    will_dispute: bool
    dispute_reason: Optional[DisputeReason]
    dispute_validity: DisputeValidity
    notes: str  # Why this dispute is valid/invalid
    metadata: dict


# Predefined scenarios for testing
TRANSACTION_SCENARIOS = [
    TransactionScenario(
        customer_email="honest.customer@example.com",
        customer_name="Honest Customer",
        amount=5000,  # $50.00
        description="Premium subscription - 1 month",
        card_number=TestCardType.NORMAL,
        will_dispute=False,
        dispute_reason=None,
        dispute_validity=DisputeValidity.UNKNOWN,
        notes="Legitimate customer, no dispute expected",
        metadata={"scenario": "legitimate_purchase", "service_delivered": True}
    ),
    TransactionScenario(
        customer_email="fraudster1@example.com",
        customer_name="John Fraudster",
        amount=10000,  # $100.00
        description="Premium service access",
        card_number=TestCardType.DISPUTE_FRAUDULENT,
        will_dispute=True,
        dispute_reason=DisputeReason.FRAUDULENT,
        dispute_validity=DisputeValidity.INVALID,
        notes="Customer received service, used it for 3 weeks, then claimed fraud. "
              "We have IP logs and usage data proving they accessed the service.",
        metadata={
            "scenario": "invalid_fraud_claim",
            "service_delivered": True,
            "service_accessed": True,
            "ip_address": "192.168.1.100",
            "login_count": 45,
            "last_access": "2024-11-25"
        }
    ),
    TransactionScenario(
        customer_email="serial.disputer@example.com",
        customer_name="Sarah Disputer",
        amount=7500,  # $75.00
        description="Digital course access",
        card_number=TestCardType.DISPUTE_FRAUDULENT,
        will_dispute=True,
        dispute_reason=DisputeReason.FRAUDULENT,
        dispute_validity=DisputeValidity.INVALID,
        notes="Customer has 5 previous disputes with same pattern: purchase, download content, "
              "then claim card was stolen. Clear pattern of abuse.",
        metadata={
            "scenario": "serial_fraudster",
            "service_delivered": True,
            "content_downloaded": True,
            "download_count": 23,
            "previous_disputes": 5,
            "customer_risk_score": "high"
        }
    ),
    TransactionScenario(
        customer_email="refund.abuser@example.com",
        customer_name="Mike Abuser",
        amount=15000,  # $150.00
        description="Annual subscription",
        card_number=TestCardType.DISPUTE_FRAUDULENT,
        will_dispute=True,
        dispute_reason=DisputeReason.CREDIT_NOT_PROCESSED,
        dispute_validity=DisputeValidity.INVALID,
        notes="Customer requested refund, we processed it successfully 2 weeks ago. "
              "Customer then filed chargeback claiming refund wasn't received. "
              "We have refund transaction ID and bank confirmation.",
        metadata={
            "scenario": "double_refund_attempt",
            "service_delivered": True,
            "refund_processed": True,
            "refund_date": "2024-11-10",
            "refund_amount": 15000,
            "refund_id": "re_1234567890"
        }
    ),
    TransactionScenario(
        customer_email="duplicate.claimer@example.com",
        customer_name="Lisa Duplicate",
        amount=3000,  # $30.00
        description="Monthly subscription",
        card_number=TestCardType.DISPUTE_FRAUDULENT,
        will_dispute=True,
        dispute_reason=DisputeReason.DUPLICATE,
        dispute_validity=DisputeValidity.INVALID,
        notes="Customer claims duplicate charge but only one transaction occurred. "
              "Customer may be confusing our charge with another merchant or attempting fraud.",
        metadata={
            "scenario": "false_duplicate_claim",
            "service_delivered": True,
            "transaction_count": 1,
            "invoice_sent": True,
            "invoice_id": "inv_1234567890"
        }
    ),
    TransactionScenario(
        customer_email="legitimately.confused@example.com",
        customer_name="Tom Confused",
        amount=9999,  # $99.99
        description="One-time purchase",
        card_number=TestCardType.DISPUTE_FRAUDULENT,
        will_dispute=True,
        dispute_reason=DisputeReason.UNRECOGNIZED,
        dispute_validity=DisputeValidity.VALID,
        notes="Customer genuinely doesn't recognize charge on statement. "
              "Our business name on statement is different from our brand name. "
              "This is a valid dispute - we should improve our statement descriptor.",
        metadata={
            "scenario": "legitimate_unrecognized",
            "service_delivered": True,
            "statement_descriptor": "XYZ*CRYPTIC123",
            "brand_name": "ShrekApp",
            "customer_contacted": False
        }
    ),
    TransactionScenario(
        customer_email="never.received@example.com",
        customer_name="Emma NoProduct",
        amount=12500,  # $125.00
        description="Physical product order",
        card_number=TestCardType.DISPUTE_FRAUDULENT,
        will_dispute=True,
        dispute_reason=DisputeReason.PRODUCT_NOT_RECEIVED,
        dispute_validity=DisputeValidity.INVALID,
        notes="Customer claims product not received but tracking shows delivered and signed for "
              "at their address. Customer attempting to get free product.",
        metadata={
            "scenario": "false_not_received",
            "service_delivered": True,
            "tracking_number": "1Z999AA10123456784",
            "delivered_date": "2024-11-20",
            "signature": "E.NOPRODUCT",
            "delivery_photo": "available"
        }
    ),
    TransactionScenario(
        customer_email="subscription.canceler@example.com",
        customer_name="Robert Cancel",
        amount=2999,  # $29.99
        description="Monthly SaaS subscription",
        card_number=TestCardType.DISPUTE_FRAUDULENT,
        will_dispute=True,
        dispute_reason=DisputeReason.SUBSCRIPTION_CANCELED,
        dispute_validity=DisputeValidity.INVALID,
        notes="Customer claims they canceled subscription but our records show no cancellation request. "
              "Terms clearly state cancellation must be done 5 days before billing. "
              "Customer continued using service after billing date.",
        metadata={
            "scenario": "false_cancellation_claim",
            "service_delivered": True,
            "cancellation_requested": False,
            "terms_agreed": True,
            "continued_usage": True,
            "billing_date": "2024-12-01",
            "last_login": "2024-12-02"
        }
    ),
]
