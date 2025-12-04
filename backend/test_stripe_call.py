#!/usr/bin/env python3
"""
Test script for making phone calls with Stripe integration.
This demonstrates the full integration: Stripe -> DisputeResponseGenerator -> RAG -> ElevenLabs call
"""
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from stripe_integration.dispute_response_generator import DisputeResponseGenerator
from elevenlabs_wrapper.agent import Agent
from elevenlabs_wrapper.phone_caller import PhoneCaller
from rag_service import RAGService

load_dotenv()


def main():
    print("=" * 80)
    print("📞 STRIPE-INTEGRATED PHONE CALL TEST")
    print("=" * 80)

    # Configuration
    charge_id = os.getenv("TEST_CHARGE_ID", "ch_3SaQFuAITa6PCFHj0dnBlMJP")
    agent_id = os.getenv("AGENT_ID")

    if not agent_id:
        raise ValueError("AGENT_ID must be set in environment variables")

    # Step 1: Fetch Stripe data
    print(f"\n💳 Step 1: Fetching Stripe charge details...")
    print(f"   Charge ID: {charge_id}")

    generator = DisputeResponseGenerator()
    charge_details = generator.get_charge_details(charge_id)

    customer_info = charge_details["customer_info"]
    product_info = charge_details["product_info"]
    charge_info = charge_details["charge_info"]

    print(f"\n✅ Stripe data fetched:")
    print(f"   Customer: {customer_info['name']}")
    print(f"   Email: {customer_info['email']}")
    print(f"   Phone: {customer_info['phone']}")
    print(f"   Product: {product_info['name']}")
    print(f"   Description: {product_info['description']}")
    print(f"   Amount: ${charge_info['amount']:.2f} {charge_info['currency']}")
    print(f"   Date: {charge_info['date']}")

    # Step 2: Generate AI response arguments
    print(f"\n🤖 Step 2: Generating AI response arguments...")
    response_arguments, phone_number, name = generator.generate_dispute_response(charge_id)

    print(f"\n✅ AI arguments generated ({len(response_arguments.split(chr(10)))} lines)")
    print(f"   Preview: {response_arguments[:200]}...")

    # Step 3: Query RAG for context
    print(f"\n🔍 Step 3: Querying RAG knowledge base...")
    rag_service = RAGService()
    rag_context = rag_service.query_context(
        chargeback_reason="subscription_canceled",
        product_name=product_info["name"],
        customer_name=customer_info["name"],
        top_k=10
    )

    context_string = rag_service.format_context_for_agent(rag_context)

    print(f"\n✅ RAG Results:")
    print(f"   - {len(rag_context['dispute_scripts'])} dispute scripts")
    print(f"   - {len(rag_context['policies'])} policies")
    print(f"   - {len(rag_context['orders'])} orders")
    print(f"   - {len(rag_context['resolution_authority'])} resolution authorities")
    print(f"   - Context length: {len(context_string)} chars")

    # Step 4: Create agent with full context
    print(f"\n🎭 Step 4: Creating ElevenLabs agent...")

    dynamic_variables = {
        "first_name": customer_info["name"].split(" ")[0],
        "last_name": customer_info["name"].split(" ")[-1] if len(customer_info["name"].split(" ")) > 1 else "",
        "phone_number": phone_number,
        "product_name": product_info["name"],
        "product_description": product_info["description"],
        "product_code": product_info["code"],
        "chargeback_reason": "subscription_canceled",
        "charge_amount": f"${charge_info['amount']:.2f}",
        "charge_date": charge_info["date"],
    }

    agent = Agent(
        agent_id=agent_id,
        dynamic_variables=dynamic_variables,
    )

    # Add supplementary information to prompt
    rag_supplement = f"""

---
SUPPLEMENTARY INFORMATION FOR THIS CALL
(Use this information to support your procedural guidance, but maintain your established tone and approach)

CUSTOMER CONTEXT:
- Name: {customer_info["name"]}
- Email: {customer_info["email"]}
- Phone: {phone_number}

PRODUCT & CHARGE DETAILS:
- Product: {product_info["name"]}
- Description: {product_info["description"]}
- Product Code: {product_info["code"]}
- Category: {product_info["category"]}
- Charge Amount: ${charge_info["amount"]:.2f} {charge_info["currency"]}
- Charge Date: {charge_info["date"]}
- Dispute Reason: subscription_canceled

RELEVANT KNOWLEDGE BASE:
{context_string}

KEY EVIDENCE-BASED ARGUMENTS TO LEVERAGE:
{response_arguments}

Note: Use the above information to support your procedural guidance. The evidence-based arguments are particularly important - they come directly from our records and can help resolve the dispute. Maintain your established tone and approach."""

    agent.set_prompt(prompt=rag_supplement)

    print(f"\n✅ Agent configured:")
    print(f"   Agent ID: {agent.agent_id}")
    print(f"   Dynamic variables: {len(dynamic_variables)} fields")
    print(f"   Prompt length: {len(rag_supplement)} chars")

    # Step 5: Make the call
    print(f"\n📞 Step 5: Making phone call...")

    # Get phone number to call (override with test number if provided)
    test_phone = os.getenv("TEST_PHONE_NUMBER")
    if test_phone:
        print(f"   ⚠️  Using TEST_PHONE_NUMBER: {test_phone} (instead of {phone_number})")
        phone_number = test_phone
    else:
        confirm = input(f"\n   ⚠️  About to call: {phone_number}\n   Continue? (yes/no): ")
        if confirm.lower() != "yes":
            print("\n❌ Call cancelled by user")
            return

    print(f"\n   Calling {phone_number}...")

    try:
        caller = PhoneCaller()
        conversation_data = caller.make_call_and_wait(
            agent=agent,
            to_number=phone_number,
            poll_interval=2,
            timeout=600,  # 10 minute timeout
            print_transcript=True,
        )

        print("\n" + "=" * 80)
        print("✅ CALL COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print(f"\n📊 Call Details:")
        print(f"   Conversation ID: {conversation_data.conversation_id}")
        print(f"   Duration: {conversation_data.metadata.call_duration_secs}s")
        print(f"   Messages: {len(conversation_data.transcript)}")
        print(f"   Cost: ${conversation_data.metadata.cost}")
        print(f"   Termination: {conversation_data.metadata.termination_reason}")

        # Print full transcript
        print("\n" + "=" * 80)
        print("📝 FULL TRANSCRIPT:")
        print("=" * 80)
        for i, msg in enumerate(conversation_data.transcript, 1):
            emoji = "👤" if msg.role == "user" else "🤖"
            time_str = f"[{msg.time_in_call_secs:.1f}s]"
            print(f"\n{i}. {emoji} {msg.role.upper()} {time_str}")
            print(f"   {msg.message}")
        print("\n" + "=" * 80)

    except Exception as e:
        print(f"\n❌ Error during call: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
