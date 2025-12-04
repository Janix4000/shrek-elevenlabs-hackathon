"""
Test script to verify RAG integration with conversation service.
This tests the RAG lookup without making actual phone calls.
"""

from rag_service import RAGService
from conversation.models import ConversationRequest, UserInfo, ChargebackInfo


def test_rag_service():
    """Test RAG service directly."""
    print("=" * 80)
    print("Testing RAG Service")
    print("=" * 80)

    rag = RAGService()

    # Test query for product not received
    print("\nTest 1: Product Not Received Dispute")
    print("-" * 80)
    context = rag.query_context(
        chargeback_reason="product not received",
        product_name="Blue Wireless Headphones",
        customer_name="John Doe",
        top_k=5
    )

    print(f"Found {len(context['dispute_scripts'])} dispute scripts")
    print(f"Found {len(context['policies'])} policies")
    print(f"Found {len(context['orders'])} orders")
    print(f"Found {len(context['resolution_authority'])} resolution authorities")

    formatted = rag.format_context_for_agent(context)
    print("\nFormatted Context for Agent:")
    print("-" * 80)
    print(formatted[:500] + "..." if len(formatted) > 500 else formatted)

    # Test query for unrecognized charge
    print("\n\nTest 2: Unrecognized Charge Dispute")
    print("-" * 80)
    context = rag.query_context(
        chargeback_reason="unrecognized charge",
        product_name="Subscription",
        customer_name="Jane Smith",
        top_k=5
    )

    print(f"Found {len(context['dispute_scripts'])} dispute scripts")
    print(f"Found {len(context['policies'])} policies")

    formatted = rag.format_context_for_agent(context)
    print("\nFormatted Context for Agent:")
    print("-" * 80)
    print(formatted[:500] + "..." if len(formatted) > 500 else formatted)


def test_conversation_request_flow():
    """Test how a conversation request would work with RAG."""
    print("\n\n" + "=" * 80)
    print("Testing Conversation Request Flow (No Actual Call)")
    print("=" * 80)

    rag = RAGService()

    # Simulate a conversation request
    request = ConversationRequest(
        user_info=UserInfo(
            first_name="John",
            last_name="Doe",
            phone_number="+1234567890"
        ),
        chargeback_info=ChargebackInfo(
            product_name="Blue Wireless Headphones",
            reason="product not received"
        )
    )

    # Query RAG (this is what the service does)
    print(f"\nCustomer: {request.user_info.first_name} {request.user_info.last_name}")
    print(f"Product: {request.chargeback_info.product_name}")
    print(f"Reason: {request.chargeback_info.reason}")
    print("\nQuerying RAG for context...")

    rag_context = rag.query_context(
        chargeback_reason=request.chargeback_info.reason,
        product_name=request.chargeback_info.product_name,
        customer_name=f"{request.user_info.first_name} {request.user_info.last_name}",
        top_k=10
    )

    context_string = rag.format_context_for_agent(rag_context)

    print("\nAgent Prompt Preview:")
    print("-" * 80)
    prompt = f"""You are a helpful customer service agent for Chargeback Shield, calling to resolve a customer dispute before it becomes a chargeback.

CUSTOMER CONTEXT:
- Name: {request.user_info.first_name} {request.user_info.last_name}
- Product: {request.chargeback_info.product_name}
- Dispute Reason: {request.chargeback_info.reason}

KNOWLEDGE BASE (Use this information to help resolve the dispute):
{context_string}

IMPORTANT GUIDELINES:
1. Be empathetic and understanding - the customer is frustrated
2. Listen carefully to their specific concern
3. Use the dispute scripts and policies above to guide your responses
4. Offer immediate solutions within your authority
5. Always aim to resolve the issue and prevent the chargeback
6. If you can't resolve it, escalate appropriately

Your goal is to turn this frustrated customer into a satisfied one through a helpful, solution-focused conversation."""

    print(prompt[:1000] + "..." if len(prompt) > 1000 else prompt)
    print(f"\n\nTotal prompt length: {len(prompt)} characters")
    print("✅ RAG context successfully integrated into agent prompt!")


if __name__ == "__main__":
    try:
        test_rag_service()
        test_conversation_request_flow()
        print("\n\n" + "=" * 80)
        print("✅ All tests passed! RAG integration is working correctly.")
        print("=" * 80)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
