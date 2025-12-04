# Dispute Evaluator

Automatically evaluate call transcripts and submit evidence to Stripe disputes using AI-powered analysis.

## Overview

The `DisputeEvaluator` module provides a complete workflow for handling disputed charges after customer phone calls:

1. **Evaluate Transcripts** - Uses Claude AI to analyze conversation outcomes
2. **Generate Evidence** - Creates professional evidence text for Stripe submissions
3. **Submit to Stripe** - Automatically submits comprehensive evidence to dispute cases

## Installation

```bash
pip install stripe anthropic
```

Set up environment variables:
```bash
export STRIPE_API_KEY="sk_test_..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Quick Start

```python
from stripe_integration.dispute_evaluator import DisputeEvaluator

# Initialize evaluator
evaluator = DisputeEvaluator()

# Evaluate a transcript and submit evidence
result = evaluator.submit_evidence_to_stripe(
    charge_id="ch_3SaQFuAITa6PCFHj0dnBlMJP",
    transcript=conversation_transcript,
    submit_immediately=False  # Stage evidence, don't submit to bank yet
)

print(f"Dispute {result['dispute_id']} - Status: {result['status']}")
print(f"Resolved: {result['evaluation']['resolved']}")
print(f"Evidence fields: {result['evidence_generated']}")
```

## Features

### 1. Transcript Evaluation

Analyzes conversation transcripts to determine dispute resolution outcomes:

```python
evaluation = evaluator.evaluate_transcript(
    transcript=[
        {"role": "agent", "message": "Hello...", "time_in_call_secs": 0.0},
        {"role": "user", "message": "Hi...", "time_in_call_secs": 5.0},
        # ...
    ],
    charge_id="ch_xxxxx"
)

print(evaluation)
# {
#     "resolved": True,
#     "resolution_type": "renewed",  # or: canceled, partial_refund, pending, unresolved
#     "customer_sentiment": "satisfied",  # or: neutral, frustrated, angry
#     "key_points": ["Customer agreed to renew subscription", ...],
#     "recommendation": "Withdraw chargeback and maintain subscription"
# }
```

**Resolution Types:**
- `renewed` - Customer agreed to keep the subscription
- `canceled` - Customer agreed to cancel (avoiding chargeback)
- `partial_refund` - Compromise reached with partial refund
- `pending` - Needs follow-up action
- `unresolved` - No agreement, customer still disputing

### 2. Evidence Generation

Uses Claude AI (claude-sonnet-4-5) to generate professional evidence text:

```python
evidence_text = evaluator.generate_evidence_text(
    field_name="cancellation_rebuttal",
    charge_metadata=charge.metadata,
    transcript=conversation_transcript,
    evaluation=evaluation_results
)
```

**Supported Evidence Fields:**

| Field | Purpose |
|-------|---------|
| `access_activity_log` | Service usage history |
| `cancellation_rebuttal` | Why cancellation claim is invalid |
| `cancellation_policy_disclosure` | How policy was presented |
| `product_description` | Product features and billing terms |
| `refund_policy_disclosure` | How refund policy was disclosed |
| `refund_refusal_explanation` | Why refund cannot be issued |
| `uncategorized_text` | Comprehensive evidence (email history, metrics, position) |

### 3. Complete Workflow

Submit all evidence fields automatically:

```python
result = evaluator.submit_evidence_to_stripe(
    charge_id="ch_3SaQFuAITa6PCFHj0dnBlMJP",
    transcript=conversation_transcript,
    submit_immediately=False  # Stage for review
)

# Returns:
# {
#     "evaluation": {...},
#     "dispute": <Stripe Dispute Object>,
#     "evidence_generated": ["access_activity_log", "cancellation_rebuttal", ...],
#     "dispute_id": "dp_xxxxx",
#     "status": "needs_response"
# }
```

**Parameters:**
- `charge_id` - Stripe charge ID
- `transcript` - List of conversation messages with `role`, `message`, `time_in_call_secs`
- `submit_immediately` - If `True`, immediately submits to bank. If `False`, stages evidence for review.

## Evidence Submission Flow

```
1. Fetch charge metadata from Stripe
2. Evaluate conversation transcript using Claude AI
3. Generate evidence text for all key fields
4. Add customer information (email, name, address, IP)
5. Submit evidence to Stripe dispute
6. Return comprehensive results
```

## Examples

### Example 1: Evaluate Call Transcript

```python
from stripe_integration.dispute_evaluator import DisputeEvaluator

evaluator = DisputeEvaluator()

# Mock conversation transcript
transcript = [
    {
        "role": "agent",
        "message": "Hello. I'm calling about your chargeback request.",
        "time_in_call_secs": 0.0
    },
    {
        "role": "user",
        "message": "I want to renew my subscription.",
        "time_in_call_secs": 10.0
    }
]

# Evaluate the outcome
evaluation = evaluator.evaluate_transcript(
    transcript=transcript,
    charge_id="ch_3SaQFuAITa6PCFHj0dnBlMJP"
)

if evaluation["resolved"]:
    print(f"✅ Dispute resolved: {evaluation['resolution_type']}")
else:
    print(f"❌ Dispute unresolved: {evaluation['recommendation']}")
```

### Example 2: Generate Evidence for Specific Field

```python
from stripe_integration.dispute_evaluator import DisputeEvaluator

evaluator = DisputeEvaluator()

# Fetch charge metadata
charge = evaluator.stripe_client.get_charge("ch_xxxxx")
metadata = charge.metadata

# Evaluate transcript first
evaluation = evaluator.evaluate_transcript(transcript, "ch_xxxxx")

# Generate evidence for specific field
evidence = evaluator.generate_evidence_text(
    field_name="cancellation_rebuttal",
    charge_metadata=metadata,
    transcript=transcript,
    evaluation=evaluation
)

print(f"Evidence ({len(evidence)} chars):\n{evidence}")
```

### Example 3: Complete Workflow with Staged Submission

```python
from stripe_integration.dispute_evaluator import DisputeEvaluator

evaluator = DisputeEvaluator()

# Complete workflow: evaluate + generate + submit
result = evaluator.submit_evidence_to_stripe(
    charge_id="ch_3SaQFuAITa6PCFHj0dnBlMJP",
    transcript=conversation_transcript,
    submit_immediately=False  # Stage only
)

print(f"📊 Evaluation:")
print(f"   - Resolved: {result['evaluation']['resolved']}")
print(f"   - Type: {result['evaluation']['resolution_type']}")
print(f"   - Sentiment: {result['evaluation']['customer_sentiment']}")

print(f"\n📄 Evidence generated: {len(result['evidence_generated'])} fields")
for field in result['evidence_generated']:
    print(f"   ✓ {field}")

print(f"\n💡 Review staged evidence in Stripe dashboard, then submit:")
print(f"   stripe.Dispute.modify('{result['dispute_id']}', submit=True)")
```

## Testing

Run the comprehensive test suite:

```bash
cd backend
python scripts/test_dispute_evaluator.py
```

The test suite includes:
1. **Transcript Evaluation** - Tests both resolved and unresolved scenarios
2. **Evidence Generation** - Demonstrates AI-generated evidence text
3. **Complete Workflow** - Full evidence submission (staged mode)

## Integration with ConversationService

To automatically evaluate and submit evidence after phone calls:

```python
# In conversation/service.py
from stripe_integration.dispute_evaluator import DisputeEvaluator

class ConversationService:
    def __init__(self):
        self.evaluator = DisputeEvaluator()
        # ...

    def run_conversation(self, conversation_id, request, fake_conv=False):
        # ... make phone call ...

        # After call completes, evaluate and submit evidence
        if conversation_data.status == "done":
            result = self.evaluator.submit_evidence_to_stripe(
                charge_id=request.chargeback_info.charge_id,
                transcript=[
                    {"role": msg.role, "message": msg.message, "time_in_call_secs": msg.time_in_call_secs}
                    for msg in conversation_data.transcript
                ],
                submit_immediately=False  # Stage for manual review
            )

            print(f"✅ Evidence staged for dispute {result['dispute_id']}")
```

## API Reference

### `DisputeEvaluator`

#### `__init__(stripe_api_key=None, anthropic_api_key=None)`

Initialize the evaluator.

**Parameters:**
- `stripe_api_key` (str, optional) - Stripe API key (reads from `STRIPE_API_KEY` env if not provided)
- `anthropic_api_key` (str, optional) - Anthropic API key (reads from `ANTHROPIC_API_KEY` env if not provided)

---

#### `evaluate_transcript(transcript, charge_id)`

Evaluate conversation transcript to determine dispute resolution outcome.

**Parameters:**
- `transcript` (List[Dict]) - Conversation messages with `role`, `message`, `time_in_call_secs`
- `charge_id` (str) - Stripe charge ID

**Returns:**
```python
{
    "resolved": bool,
    "resolution_type": str,  # renewed|canceled|partial_refund|pending|unresolved
    "customer_sentiment": str,  # satisfied|neutral|frustrated|angry
    "key_points": List[str],
    "recommendation": str
}
```

---

#### `generate_evidence_text(field_name, charge_metadata, transcript, evaluation)`

Generate professional evidence text for a specific field using Claude AI.

**Parameters:**
- `field_name` (str) - Evidence field name
- `charge_metadata` (Dict) - Metadata from Stripe charge
- `transcript` (List[Dict]) - Conversation transcript
- `evaluation` (Dict) - Evaluation results from `evaluate_transcript()`

**Returns:** (str) Professional evidence text (max 20,000 characters)

---

#### `submit_evidence_to_stripe(charge_id, transcript, submit_immediately=False)`

Complete workflow: Evaluate transcript and submit evidence to Stripe.

**Parameters:**
- `charge_id` (str) - Stripe charge ID
- `transcript` (List[Dict]) - Conversation transcript
- `submit_immediately` (bool) - If True, immediately submits to bank. If False, stages evidence.

**Returns:**
```python
{
    "evaluation": Dict,  # Transcript evaluation results
    "dispute": StripeDispute,  # Updated Stripe dispute object
    "evidence_generated": List[str],  # Evidence fields generated
    "dispute_id": str,  # Stripe dispute ID
    "status": str  # Dispute status
}
```

## Error Handling

```python
try:
    result = evaluator.submit_evidence_to_stripe(
        charge_id="ch_xxxxx",
        transcript=transcript
    )
except ValueError as e:
    print(f"No disputes found: {e}")
except Exception as e:
    print(f"Error: {e}")
```

**Common Errors:**
- `ValueError: No disputes found for charge` - Charge has no associated disputes
- `ValueError: Anthropic API key is required` - Missing `ANTHROPIC_API_KEY` environment variable
- API errors from Stripe or Anthropic services

## Best Practices

1. **Always review staged evidence** before submitting to bank:
   ```python
   result = evaluator.submit_evidence_to_stripe(
       charge_id=charge_id,
       transcript=transcript,
       submit_immediately=False  # Stage first
   )
   # Review in Stripe dashboard, then submit manually
   ```

2. **Include complete transcripts** - More context = better evaluation:
   ```python
   # Include ALL messages, not just a summary
   transcript = [msg for msg in full_conversation]
   ```

3. **Use real charge metadata** - Richer metadata = stronger evidence:
   ```python
   # Populate Stripe charges with 44 metadata fields
   # See: scripts/populate_test_data.py
   ```

4. **Monitor evaluation accuracy** - Review AI evaluations to ensure correctness:
   ```python
   evaluation = evaluator.evaluate_transcript(transcript, charge_id)
   if evaluation["resolved"] != expected_outcome:
       print(f"⚠️ AI evaluation may be incorrect: {evaluation}")
   ```

## Stripe Dashboard

After staging evidence, review in Stripe:

1. Go to: https://dashboard.stripe.com/test/disputes
2. Find dispute by charge ID
3. Review generated evidence
4. Submit to bank if satisfied

## Limitations

- Evidence text limited to 20,000 characters per field
- Requires Stripe charge to have associated dispute
- Claude AI evaluation may occasionally misinterpret transcripts
- Metadata quality impacts evidence strength

## Related Modules

- `DisputeResponseGenerator` - Generates AI-powered response arguments for phone calls
- `ConversationService` - Orchestrates phone calls with Stripe integration
- `StripeClient` - Low-level Stripe API wrapper

## Support

For issues or questions, see:
- Stripe Disputes API: https://stripe.com/docs/api/disputes
- Anthropic Claude API: https://docs.anthropic.com/
