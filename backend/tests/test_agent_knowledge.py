"""
Show exactly what knowledge the agent receives from RAG.
This simulates what happens when the conversation service creates an agent.
"""

from rag_service import RAGService
from conversation.models import ConversationRequest, UserInfo, ChargebackInfo

def show_agent_knowledge(request: ConversationRequest):
    """Show the exact prompt and knowledge the agent will receive."""

    print("=" * 100)
    print(f"SIMULATING AGENT KNOWLEDGE FOR CALL")
    print("=" * 100)

    print(f"\nCustomer: {request.user_info.first_name} {request.user_info.last_name}")
    print(f"Phone: {request.user_info.phone_number}")
    print(f"Product: {request.chargeback_info.product_name}")
    print(f"Dispute Reason: {request.chargeback_info.reason}")

    # Query RAG (this is what the service does)
    print("\n" + "-" * 100)
    print("QUERYING RAG FOR CONTEXT...")
    print("-" * 100)

    rag = RAGService()
    rag_context = rag.query_context(
        chargeback_reason=request.chargeback_info.reason,
        product_name=request.chargeback_info.product_name,
        customer_name=f"{request.user_info.first_name} {request.user_info.last_name}",
        top_k=10
    )

    print(f"\nRAG Results:")
    print(f"  - {len(rag_context['dispute_scripts'])} dispute scripts")
    print(f"  - {len(rag_context['policies'])} policies")
    print(f"  - {len(rag_context['orders'])} orders")
    print(f"  - {len(rag_context['resolution_authority'])} resolution authorities")
    print(f"  - {len(rag_context['common_confusions'])} common confusions")

    # Format the context
    context_string = rag.format_context_for_agent(rag_context)

    # Build the full agent prompt (this is what the agent sees)
    agent_prompt = f"""You are a helpful customer service agent for Chargeback Shield, calling to resolve a customer dispute before it becomes a chargeback.

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

    print("\n" + "=" * 100)
    print("FULL AGENT PROMPT (What the AI will see and use)")
    print("=" * 100)
    print(agent_prompt)
    print("\n" + "=" * 100)
    print(f"Total prompt length: {len(agent_prompt)} characters")
    print("=" * 100)

    return agent_prompt


# Test Case 1: Product Not Received
print("\n\n")
print("#" * 100)
print("TEST CASE 1: Customer says they never received their Blue Wireless Headphones")
print("#" * 100)

request1 = ConversationRequest(
    user_info=UserInfo(
        first_name="John",
        last_name="Smith",
        phone_number="+1234567890"
    ),
    chargeback_info=ChargebackInfo(
        product_name="Blue Wireless Headphones",
        reason="product not received"
    )
)

prompt1 = show_agent_knowledge(request1)


# Test Case 2: Subscription not canceled
print("\n\n\n")
print("#" * 100)
print("TEST CASE 2: Customer says they canceled their Netflix subscription but were charged")
print("#" * 100)

request2 = ConversationRequest(
    user_info=UserInfo(
        first_name="Michael",
        last_name="Chen",
        phone_number="+1234567890"
    ),
    chargeback_info=ChargebackInfo(
        product_name="Netflix Premium Subscription",
        reason="subscription not canceled"
    )
)

prompt2 = show_agent_knowledge(request2)


# Test Case 3: Where is my order (In Transit)
print("\n\n\n")
print("#" * 100)
print("TEST CASE 3: Customer asking where their Mechanical Keyboard is")
print("#" * 100)

request3 = ConversationRequest(
    user_info=UserInfo(
        first_name="David",
        last_name="Kim",
        phone_number="+1234567890"
    ),
    chargeback_info=ChargebackInfo(
        product_name="Mechanical Keyboard RGB",
        reason="where is my order"
    )
)

prompt3 = show_agent_knowledge(request3)


print("\n\n")
print("=" * 100)
print("SUMMARY: What the Agent Can Do")
print("=" * 100)
print("""
✅ The agent will have access to:

1. DISPUTE SCRIPTS - Pre-written responses for common disputes:
   - Product not received
   - Unrecognized charges
   - Fraudulent charges
   - Product not as described
   - Subscription issues
   - Duplicate charges

2. COMPANY POLICIES - Official policies to reference:
   - Refund policy (30 days, no questions asked)
   - Shipping policy (2-3 days processing, 5-7 days delivery)
   - Item not received policy (reship or refund)
   - Subscription cancellation (immediate, prorated refund)
   - Defective product policy (replacement without return for <$100)
   - Return policy (30 days, no restocking fees)
   - Warranty policy (1-year on electronics)

3. ORDER DETAILS - Specific information about the customer's order:
   - Order date, amount, status
   - Tracking number and carrier
   - Shipping address
   - Delivery dates
   - Current status (Delivered, In Transit, etc.)

4. RESOLUTION AUTHORITY - What the agent can offer:
   - Full refunds up to certain amounts
   - Free replacement shipping
   - Discount codes for future purchases
   - Immediate solutions without escalation

5. COMMON CONFUSIONS - Proactive answers to common questions

The agent can intelligently use all this information during the live conversation
to resolve disputes and prevent chargebacks!
""")
