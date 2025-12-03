# Chargeback Shield - Knowledge Base

RAG (Retrieval-Augmented Generation) knowledge base for the Chargeback Shield AI voice assistant.

## Overview

This repository contains the knowledge base data for our AI agent that calls customers to resolve chargebacks before they're finalized.

## Directory Structure

```
chargeback-mock-data/
├── source_data/              # Source JSON files
│   ├── orders.json
│   ├── policies.json
│   ├── dispute_scripts.json
│   ├── resolution_authority.json
│   └── common_confusions.json
├── knowledge_base/           # ElevenLabs knowledge base documents (UPLOAD THESE)
│   ├── elevenlabs_kb_orders.txt
│   ├── elevenlabs_kb_policies.txt
│   ├── elevenlabs_kb_dispute_scripts.txt
│   ├── elevenlabs_kb_resolution_authority.txt
│   └── elevenlabs_kb_common_confusions.txt
├── scripts/                  # Utility scripts
│   └── upload_to_elevenlabs.py
└── README.md
```

## Files

### Source Data (`source_data/`)
- `orders.json` - Sample customer order data
- `policies.json` - Company refund/return policies
- `dispute_scripts.json` - Resolution scripts for different dispute reasons
- `resolution_authority.json` - Guidelines for resolution authority limits
- `common_confusions.json` - Common customer confusion scenarios

### Knowledge Base Documents (`knowledge_base/`)
**These are the files to upload to ElevenLabs:**
- `elevenlabs_kb_orders.txt`
- `elevenlabs_kb_policies.txt`
- `elevenlabs_kb_dispute_scripts.txt`
- `elevenlabs_kb_resolution_authority.txt`
- `elevenlabs_kb_common_confusions.txt`

## Setup

### 1. Install Dependencies
```bash
pip install elevenlabs python-dotenv
```

### 2. Configure Environment Variables
Create a `.env` file:
```
ELEVENLABS_API_KEY=your_api_key_here
```

### 3. Generate Knowledge Base Files
```bash
python scripts/upload_to_elevenlabs.py
```

## Integration with ElevenLabs Agent

### Upload to Agent's Knowledge Base

1. Go to https://elevenlabs.io/app/conversational-ai
2. Select your agent
3. Navigate to **Knowledge Base** section
4. Upload each `elevenlabs_kb_*.txt` file
5. Enable **RAG** in agent settings:
   - Embedding model: `e5_mistral_7b_instruct`
   - Max document chunks: `5-10`
   - Max vector distance: `0.5`

### Recommended System Prompt Addition

```
You are a helpful customer service representative resolving chargeback disputes.

When a customer initiates a chargeback:
1. Listen with empathy to their concern
2. Look up their order details in the knowledge base
3. Clarify any confusion (subscription renewal, shipping, etc.)
4. Offer immediate solutions: refund, reshipment, or cancellation
5. Resolve before the chargeback is finalized

Guidelines:
- Be warm and solution-focused
- Never argue or sound defensive
- Offer refunds immediately if requested
- Reference specific order details from knowledge base
- Preserve customer relationships

Use the knowledge base to retrieve:
- Order history and tracking
- Refund/return policies
- Common confusion scenarios
- Resolution authority limits
```

## API Integration (Optional)

To programmatically upload and configure RAG, uncomment lines 127-128 in `upload_to_elevenlabs.py` and add your agent ID:

```python
agent_id = "your-agent-id-here"
configure_agent_rag(agent_id)
```

## Next Steps

1. Upload all knowledge base `.txt` files to the ElevenLabs agent
2. Enable RAG in agent settings
3. Test the agent with sample chargeback scenarios
4. Update system prompt with chargeback-specific instructions
5. Integrate with Verifi/Ethoca chargeback alerts

## Questions?

Contact the team for agent access or integration help.
