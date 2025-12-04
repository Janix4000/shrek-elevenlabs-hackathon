"""
Preview the exact prompt that will be sent to the agent with RAG context.
Shows how RAG context is APPENDED to the base prompt (not overriding).
"""

from rag_service import RAGService
from conversation.models import ConversationRequest, UserInfo, ChargebackInfo

def preview_agent_prompt(request: ConversationRequest):
    """Show what the agent will see with RAG context appended."""

    print("=" * 100)
    print("PROMPT PREVIEW - What the Agent Will Receive")
    print("=" * 100)

    print(f"\nTest Case:")
    print(f"  Customer: {request.user_info.first_name} {request.user_info.last_name}")
    print(f"  Product: {request.chargeback_info.product_name}")
    print(f"  Reason: {request.chargeback_info.reason}")

    # Query RAG
    rag = RAGService()
    rag_context = rag.query_context(
        chargeback_reason=request.chargeback_info.reason,
        product_name=request.chargeback_info.product_name,
        customer_name=f"{request.user_info.first_name} {request.user_info.last_name}",
        top_k=10
    )

    context_string = rag.format_context_for_agent(rag_context)

    # This is what gets appended to the base prompt
    rag_context_addition = f"""

--- CONTEXT FOR THIS CALL ---

CUSTOMER INFORMATION:
- Name: {request.user_info.first_name} {request.user_info.last_name}
- Product: {request.chargeback_info.product_name}
- Dispute Reason: {request.chargeback_info.reason}

RELEVANT KNOWLEDGE BASE:
{context_string}

Use the above information to help resolve this specific dispute effectively."""

    print("\n" + "=" * 100)
    print("BASE PROMPT (From ElevenLabs Dashboard)")
    print("=" * 100)
    print("""
[Whatever your friend configured in the ElevenLabs dashboard will be here]
For example:
  "You are a professional customer service agent for Chargeback Shield.
   Your goal is to help customers resolve their disputes before they become
   chargebacks. Be empathetic, professional, and solution-focused."
""")

    print("\n" + "=" * 100)
    print("RAG CONTEXT (Appended to the base prompt)")
    print("=" * 100)
    print(rag_context_addition)

    print("\n" + "=" * 100)
    print("FINAL PROMPT = Base Prompt + RAG Context")
    print("=" * 100)
    print("""
The agent will receive:
1. The base prompt from ElevenLabs dashboard (defines personality, tone, goals)
2. PLUS the RAG context above (specific info for this call)

This way:
- Your friend controls the agent's core behavior via dashboard
- RAG adds call-specific knowledge (orders, policies, scripts)
- Best of both worlds!
""")

    print("=" * 100)
    print(f"RAG Context Length: {len(rag_context_addition)} characters")
    print("=" * 100)


# Test with "product not received"
print("\n")
request = ConversationRequest(
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

preview_agent_prompt(request)
