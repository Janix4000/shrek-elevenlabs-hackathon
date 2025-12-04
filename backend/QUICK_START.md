# Quick Start - RAG Integration

## What's New?

The AI agent now has **RAG (Retrieval-Augmented Generation)** - it gets relevant context from Pinecone before each call, so it knows:
- Company policies
- Dispute resolution scripts
- Customer order details
- What it's authorized to offer

## Setup (5 minutes)

### 1. Pull the code
```bash
git pull origin dev
```

### 2. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Add API keys to `.env`
```bash
# Your ElevenLabs agent and API key
AGENT_ID=your_agent_id_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Bartosz's shared keys (ask him)
PINECONE_API_KEY=...
OPENAI_API_KEY=...
```

### 4. Test it works
```bash
python tests/test_rag.py
```

You should see it finding orders, policies, and scripts from Pinecone.

### 5. Run the server
```bash
uvicorn main:app --reload
```

### 6. Make a test call
Go to http://localhost:8000/docs

Use POST /api/conversation/start:
```json
{
  "user_info": {
    "first_name": "John",
    "last_name": "Smith",
    "phone_number": "+1234567890"
  },
  "chargeback_info": {
    "product_name": "Blue Wireless Headphones",
    "reason": "product not received"
  }
}
```

The agent will now have full context about John's order, relevant policies, and dispute scripts during the call!

## What Changed?

**Before:** Agent called customers with just their name and dispute reason

**Now:** Agent calls with:
- John Smith ordered Blue Wireless Headphones on Nov 28 for $79.99
- Delivered Dec 3 via USPS tracking 1Z999AA10123456784
- "Product not received" script: verify address, check tracking, offer replacement or refund
- Item not received policy: reship or refund customer's choice
- Agent authority: can offer refunds up to $500 without approval

## That's it!

All the data is already uploaded to Pinecone. You just need the API keys to connect.

For more details, see README_RAG_SETUP.md
