"""
Test that the conversation service can initialize RAG and create agents with context.
This does NOT make actual phone calls, just tests the RAG integration.
"""

import os
from dotenv import load_dotenv
from conversation.service import ConversationService
from conversation.models import ConversationRequest, UserInfo, ChargebackInfo

load_dotenv()

def test_conversation_service_rag():
    """Test that conversation service can initialize and use RAG."""
    print("=" * 80)
    print("Testing Conversation Service RAG Integration")
    print("=" * 80)

    # Create conversation service (this initializes RAG)
    print("\n1. Initializing ConversationService...")
    try:
        service = ConversationService()
        print("   ✅ ConversationService initialized successfully")
        print(f"   ✅ RAG service initialized: {service.rag_service is not None}")
    except Exception as e:
        print(f"   ❌ Failed to initialize: {e}")
        raise

    # Create a test conversation request
    print("\n2. Creating test conversation request...")
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
    print(f"   Customer: {request.user_info.first_name} {request.user_info.last_name}")
    print(f"   Product: {request.chargeback_info.product_name}")
    print(f"   Reason: {request.chargeback_info.reason}")

    # Test RAG query (what the service does before calling)
    print("\n3. Testing RAG query...")
    try:
        rag_context = service.rag_service.query_context(
            chargeback_reason=request.chargeback_info.reason,
            product_name=request.chargeback_info.product_name,
            customer_name=f"{request.user_info.first_name} {request.user_info.last_name}",
            top_k=10
        )
        print(f"   ✅ RAG query successful")
        print(f"   Found {len(rag_context['dispute_scripts'])} dispute scripts")
        print(f"   Found {len(rag_context['policies'])} policies")
        print(f"   Found {len(rag_context['orders'])} orders")
        print(f"   Found {len(rag_context['resolution_authority'])} resolution authorities")
    except Exception as e:
        print(f"   ❌ RAG query failed: {e}")
        raise

    # Test context formatting
    print("\n4. Testing context formatting...")
    try:
        context_string = service.rag_service.format_context_for_agent(rag_context)
        print(f"   ✅ Context formatted successfully")
        print(f"   Context length: {len(context_string)} characters")

        # Show preview of context
        print("\n   Preview of formatted context:")
        print("   " + "-" * 76)
        preview = context_string[:400] + "..." if len(context_string) > 400 else context_string
        for line in preview.split('\n'):
            print(f"   {line}")
        print("   " + "-" * 76)
    except Exception as e:
        print(f"   ❌ Context formatting failed: {e}")
        raise

    # Test dynamic variables
    print("\n5. Testing dynamic variables creation...")
    try:
        dynamic_vars = service._create_dynamic_variables(request)
        print(f"   ✅ Dynamic variables created successfully")
        print(f"   Variables: {dynamic_vars}")
    except Exception as e:
        print(f"   ❌ Dynamic variables creation failed: {e}")
        raise

    print("\n" + "=" * 80)
    print("✅ All Conversation Service RAG Integration Tests Passed!")
    print("=" * 80)
    print("\nThe conversation service will:")
    print("  1. Query RAG for relevant context based on chargeback reason")
    print("  2. Format the context into a readable prompt")
    print("  3. Create an agent with the RAG context injected")
    print("  4. Make the phone call with the context-aware agent")
    print("\n⚠️  Note: To test actual phone calls, you need:")
    print("     - Valid AGENT_ID in .env")
    print("     - Valid phone number")
    print("     - Use the FastAPI endpoint: POST /api/conversation/start")


if __name__ == "__main__":
    try:
        test_conversation_service_rag()
    except Exception as e:
        print(f"\n\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
