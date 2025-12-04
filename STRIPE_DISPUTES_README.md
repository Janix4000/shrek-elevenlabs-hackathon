# Stripe Dispute Detection System

A comprehensive system for detecting and analyzing fraudulent chargebacks where customers violate terms and conditions.

## Overview

This system helps identify invalid disputes where customers:
- Claim fraud after using your service extensively
- Request duplicate refunds (refund + chargeback)
- Claim non-delivery when tracking shows delivery
- Claim cancellation without proper notice
- Are serial disputers with pattern of abuse

## Features

- **Automated Dispute Detection**: Creates test transactions with various dispute scenarios
- **Fraud Scoring**: Analyzes disputes and calculates fraud likelihood (0-100 scale)
- **Evidence Generation**: Automatically compiles evidence for contesting disputes
- **Pattern Recognition**: Identifies serial disputers and abuse patterns
- **Detailed Reporting**: Comprehensive analysis of each dispute

## Project Structure

```
stripe_integration/
├── client.py              # Stripe API client
├── models.py              # Data models and test scenarios
├── dispute_analyzer.py    # Dispute analysis logic
├── test_data_generator.py # Test data generation
└── __init__.py

scripts/
├── generate_dispute_data.py  # Generate test disputes
└── analyze_disputes.py       # Analyze existing disputes

tests/
└── test_stripe_integration.py
```

## Installation

Dependencies are already in `requirements.txt`:
```bash
venv/bin/pip install -r requirements.txt
```

## Configuration

Your Stripe test key is already configured in `.env`:
```
STRIPE_SECRET_KEY=sk_test_51SZqNa...
```

## Usage

### 1. Generate Test Data with Disputes

This creates 8 different transaction scenarios, some of which will trigger disputes:

```bash
venv/bin/python scripts/generate_dispute_data.py
```

**What this does:**
- Creates customers with different profiles
- Creates charges using special test cards that trigger disputes
- Waits for disputes to appear in Stripe
- Analyzes each dispute for fraud indicators
- Generates detailed reports

### 2. Analyze Existing Disputes

To analyze disputes already in your Stripe account:

```bash
venv/bin/python scripts/analyze_disputes.py
```

### 3. Use in Your Code

```python
from stripe_integration import StripeClient, DisputeAnalyzer

# Initialize
client = StripeClient()
analyzer = DisputeAnalyzer()

# Get disputes
disputes = client.list_disputes()

# Analyze a dispute
for dispute in disputes:
    charge = client.get_charge(dispute.charge)
    metadata = charge.metadata or {}

    analysis = analyzer.analyze_dispute(dispute, metadata)

    print(f"Fraud Score: {analysis['fraud_score']}/100")
    print(f"Validity: {analysis['validity']}")
    print(f"Action: {analysis['recommended_action']}")
```

## Test Scenarios

The system includes 8 predefined scenarios:

### Invalid Disputes (Should Contest)

1. **Fraudulent Claim After Usage**
   - Customer used service for 3 weeks, then claimed fraud
   - Evidence: 45 logins, IP logs, usage data
   - Fraud Score: 70+

2. **Serial Disputer**
   - Customer has 5 previous disputes with same pattern
   - Downloaded content 23 times, then claimed fraud
   - Fraud Score: 85+

3. **Double Refund Attempt**
   - Refund already processed, then filed chargeback
   - Evidence: Refund transaction ID and confirmation
   - Fraud Score: 60+

4. **False Duplicate Claim**
   - Only one transaction occurred
   - Evidence: Single invoice, no duplicates
   - Fraud Score: 55+

5. **False Non-Delivery**
   - Tracking shows delivered and signed for
   - Evidence: Tracking number, delivery photo, signature
   - Fraud Score: 70+

6. **False Cancellation**
   - No cancellation request on file
   - Customer continued using service after billing
   - Fraud Score: 60+

### Valid Disputes (Should Accept/Resolve)

7. **Legitimate Unrecognized Charge**
   - Customer genuinely confused by statement descriptor
   - Should improve business name on statements

8. **Legitimate Customer**
   - No disputes, clean transaction

## Fraud Scoring System

The `DisputeAnalyzer` calculates a fraud score (0-100) based on:

| Indicator | Points | Description |
|-----------|--------|-------------|
| Service delivered | +20 | Proof of service delivery |
| Service accessed | +30 | Customer used the service |
| High usage | +20 | Multiple logins/accesses |
| Tracking available | +25 | Shipment tracking exists |
| Delivered | +15 | Confirmed delivery |
| Signature | +10 | Signed for delivery |
| Refund processed | +40 | Already refunded |
| Serial disputer | +35 | Multiple previous disputes |
| Content downloaded | +25 | Digital content accessed |
| Multiple downloads | +15 | Downloaded multiple times |
| Continued usage | +30 | Still using after dispute |

**Score Interpretation:**
- **0-14**: Valid dispute (accept or resolve)
- **15-29**: Unknown (investigate further)
- **30-59**: Likely invalid (investigate and contest)
- **60-100**: Invalid/fraudulent (contest with evidence)

## Evidence Collection

The system tracks and stores evidence in transaction metadata:

```python
metadata = {
    "service_delivered": True,
    "service_accessed": True,
    "ip_address": "192.168.1.100",
    "login_count": 45,
    "last_access": "2024-11-25",
    "tracking_number": "1Z999AA10123456784",
    "delivered_date": "2024-11-20",
    "signature": "Customer Name",
    "refund_processed": True,
    "refund_date": "2024-11-10",
    "previous_disputes": 5,
}
```

## API Reference

### StripeClient

```python
# Customer operations
customer = client.create_customer(email, name)
customer = client.get_customer(customer_id)

# Charge operations
token = client.create_token(card_number)
charge = client.create_charge(amount, currency, source, metadata=metadata)
charge = client.get_charge(charge_id)

# Dispute operations
disputes = client.list_disputes(limit=100)
dispute = client.get_dispute(dispute_id)
disputes = client.get_charge_disputes(charge_id)
dispute = client.submit_dispute_evidence(dispute_id, evidence)
dispute = client.close_dispute(dispute_id)
```

### DisputeAnalyzer

```python
# Analyze dispute
analysis = analyzer.analyze_dispute(dispute, transaction_metadata)
# Returns: {validity, fraud_score, fraud_indicators, evidence_available, notes, ...}

# Generate evidence document
evidence = analyzer.generate_evidence_document(dispute, metadata, analysis)

# Get summary stats
summary = analyzer.get_dispute_summary(disputes)
```

## Testing with Stripe Test Cards

The system uses these test cards:

- `4242424242424242` - Normal successful charge
- `4000000000000259` - Triggers fraudulent dispute
- `4000000000002685` - For product_not_received scenarios
- `4000000000000002` - Card will be declined

## Dashboard Access

View your test disputes at:
https://dashboard.stripe.com/test/disputes

## Next Steps

1. Run the data generator to create test scenarios
2. Analyze the disputes to see fraud detection in action
3. Integrate the `DisputeAnalyzer` into your production code
4. Set up webhook listeners for `charge.dispute.created` events
5. Automate evidence submission for high-fraud-score disputes

## Important Notes

- This is for **TEST MODE** only (uses test API key)
- Disputes in test mode appear quickly (seconds to minutes)
- In production, collect evidence metadata with every transaction
- Set up webhooks to handle dispute events automatically
- Keep detailed logs: IP addresses, login timestamps, delivery tracking

## Support

For issues or questions, check:
- Stripe Disputes API: https://stripe.com/docs/disputes
- Stripe Test Cards: https://stripe.com/docs/testing
