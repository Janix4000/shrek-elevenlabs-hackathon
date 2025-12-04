# RAG Integration Setup Guide

This guide explains how to set up and run the Pinecone RAG integration for Chargeback Shield.

## What Was Added

RAG (Retrieval-Augmented Generation) gives the AI agent relevant context before each call:
- Dispute resolution scripts
- Company policies
- Customer order details
- Resolution authority guidelines
- Common customer confusions

## Prerequisites

1. **ElevenLabs Agent ID** - From your ElevenLabs dashboard
2. **Pinecone & OpenAI keys** - Already set up and shared (data already uploaded)

## Setup Steps

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This installs:
- `pinecone-client` - For vector database
- `openai` - For generating embeddings
- `python-dotenv` - For environment variables

### 2. Configure Environment Variables

Create or update your `.env` file in the `backend/` directory:

```bash
# ElevenLabs
AGENT_ID=your_elevenlabs_agent_id

# Pinecone (shared - already set up with data uploaded)
PINECONE_API_KEY=ask_bartosz_for_key

# OpenAI (shared - already set up)
OPENAI_API_KEY=ask_bartosz_for_key
```

**Note:** The Pinecone index is already created and data is already uploaded. You just need the API keys to connect.

### 3. Test RAG Works

```bash
python test_rag.py
```

This verifies Pinecone can find relevant data based on queries.

### 4. Run the Server

```bash
uvicorn main:app --reload
```

Server will start at http://localhost:8000

## How It Works

### Before RAG Integration
```
User makes API call → Agent created → Phone call made
```
Agent has no context, just basic customer info.

### With RAG Integration
```
User makes API call → RAG queries Pinecone → Retrieves relevant context →
Agent created with context → Phone call made
```
Agent has full knowledge of policies, scripts, and order details.

## Testing the Integration

### 1. Test RAG Service Directly

```bash
python test_rag.py
```

### 2. Test via API

Go to http://localhost:8000/docs and use the Swagger UI:

**POST /api/conversation/start**

Request body:
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

This will:
1. Query RAG for context about "product not received" + "Blue Wireless Headphones"
2. Create an agent with that context
3. Make a phone call with a context-aware agent

## Data Files

You can customize the knowledge base by editing these JSON files:

- `orders.json` - Customer orders (tracking, delivery status, etc.)
- `policies.json` - Company policies (refunds, shipping, returns)
- `dispute_scripts.json` - Pre-written responses for common disputes
- `resolution_authority.json` - What the agent can offer (refund limits, etc.)
- `common_confusions.json` - Common customer questions

**After editing, run `python upload_to_pinecone.py` again to update Pinecone.**

## Troubleshooting

### "Could not import module 'main'"
- Make sure you're in the `backend/` directory when running `uvicorn`

### "Index 'chargeback-rag' not found"
- Create the Pinecone index (see Step 2)
- Make sure the name is exactly `chargeback-rag`

### "PINECONE_API_KEY not set"
- Check your `.env` file exists in the `backend/` directory
- Make sure it has `PINECONE_API_KEY=...`

### "No results from RAG"
- Run `python upload_to_pinecone.py` to upload data
- Check Pinecone dashboard to verify vectors were uploaded

### "API call fails"
- Check server logs in terminal
- Verify all API keys are correct in `.env`

## Architecture

```
┌─────────────────────┐
│  API Request        │
│  (user info +       │
│   dispute reason)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  RAG Service        │
│  1. Create embedding│
│  2. Query Pinecone  │
│  3. Format context  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Conversation       │
│  Service            │
│  - Injects RAG      │
│    context into     │
│    agent prompt     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  ElevenLabs Agent   │
│  Makes phone call   │
│  with full context  │
└─────────────────────┘
```

## Cost Considerations

- **OpenAI Embeddings:** ~$0.0001 per 1K tokens (very cheap)
- **Pinecone:** Free tier includes 1 index with enough capacity for this project
- **ElevenLabs:** Depends on your plan

Each API call makes 1 embedding request (to query RAG), which costs fractions of a cent.

## Questions?

- Check `test_rag.py` for example queries
- See `rag_service.py` for implementation details
- Review `conversation/service.py` to see how RAG integrates

## Summary

✅ RAG gives your agent smart context before each call
✅ Agent can reference policies, scripts, and order details
✅ Helps resolve disputes and prevent chargebacks effectively
