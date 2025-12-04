#!/bin/bash

# Script to test the RAG-enabled API without making actual phone calls
# This shows you the API request/response flow

echo "================================================================================"
echo "Testing Chargeback Shield API with RAG Integration"
echo "================================================================================"

# Check if server is running
echo ""
echo "1. Starting FastAPI server..."
echo "   Run this in a separate terminal: uvicorn main:app --reload"
echo ""
read -p "Press Enter once the server is running on http://localhost:8000..."

# Test health endpoint
echo ""
echo "2. Testing health endpoint..."
curl -s http://localhost:8000/health | python -m json.tool

# Show the conversation start endpoint
echo ""
echo ""
echo "3. To test RAG-enabled conversation (without making real call):"
echo "   You would use this endpoint, but it will make a REAL phone call:"
echo ""
echo "   POST http://localhost:8000/api/conversation/start"
echo ""
echo "   Example request body:"
cat <<'EOF'
{
  "user_info": {
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890"
  },
  "chargeback_info": {
    "product_name": "Blue Wireless Headphones",
    "reason": "product not received"
  }
}
EOF

echo ""
echo ""
echo "================================================================================"
echo "RAG Integration Summary"
echo "================================================================================"
echo ""
echo "✅ What happens when you call POST /api/conversation/start:"
echo ""
echo "   1. API receives customer info and chargeback reason"
echo "   2. ConversationService queries Pinecone RAG with:"
echo "      - Chargeback reason: 'product not received'"
echo "      - Product name: 'Blue Wireless Headphones'"
echo "      - Customer name: 'John Doe'"
echo ""
echo "   3. RAG returns relevant context:"
echo "      - Dispute resolution scripts"
echo "      - Company policies"
echo "      - Order information"
echo "      - Resolution authority guidelines"
echo ""
echo "   4. Agent is created with RAG context injected into prompt"
echo ""
echo "   5. Phone call is made with context-aware agent"
echo ""
echo "   6. Agent can now:"
echo "      - Reference specific policies during the call"
echo "      - Use pre-written dispute scripts"
echo "      - Offer solutions within their authority"
echo "      - Look up order details to help resolve the issue"
echo ""
echo "================================================================================"
echo "⚠️  To make an actual test call, update the phone number to a real one"
echo "    and use curl or the Swagger UI at http://localhost:8000/docs"
echo "================================================================================"
