import os
import time
import uuid
import threading
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from anthropic import AsyncAnthropic
from conversation.models import (
    ConversationResult,
    ConversationStatus,
    TranscriptEntry,
    EvidenceResult,
    DisputeEvaluation,
)
from elevenlabs_wrapper.phone_caller import PhoneCaller
from elevenlabs_wrapper.agent import Agent, AgentPromptOverride, AgentConfigOverride
from elevenlabs_wrapper.transcript_storage import TranscriptStorage
from elevenlabs_wrapper.transcript_summarizer import TranscriptSummarizer
from elevenlabs_wrapper.conversation_manager import (
    ConversationData,
    TranscriptMessage,
    ConversationMetadata,
)
from rag_service import RAGService
from stripe_integration.dispute_response_generator import DisputeResponseGenerator
from stripe_integration.dispute_evaluator import DisputeEvaluator

load_dotenv()

agent_id = os.getenv("AGENT_ID")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")


class ConversationService:
    def __init__(self, storage_dir: str = "transcripts"):
        self._conversations: dict[str, ConversationResult] = {}
        self._charge_ids: dict[str, str] = {}  # Maps conversation_id -> charge_id
        self._lock = threading.Lock()
        self.storage = TranscriptStorage(storage_dir=storage_dir)
        self.rag_service = RAGService()
        self.dispute_response_generator = DisputeResponseGenerator()
        self.dispute_evaluator = DisputeEvaluator()

    def _create_fake_conversation(
        self, product_name: str, first_name: str, reason: str
    ) -> ConversationData:
        """Create a fake conversation for testing purposes."""

        mock_transcript = [
            TranscriptMessage(
                role="agent",
                message=f"Hello. I'm Ethan, calling about your recent chargeback request for the subscription of {product_name}.",
                time_in_call_secs=0.0,
            ),
            TranscriptMessage(
                role="user",
                message="Hello.",
                time_in_call_secs=7.0,
            ),
            TranscriptMessage(
                role="agent",
                message=f"I need to inform you that a chargeback is not a valid method for canceling your {product_name} subscription. That action will not be accepted.",
                time_in_call_secs=11.0,
            ),
            TranscriptMessage(
                role="user",
                message="Oh no, really? How do I fix it?",
                time_in_call_secs=20.0,
            ),
            TranscriptMessage(
                role="agent",
                message=f"You have two options to resolve this. We can proceed with an official cancellation of your {product_name} subscription according to the terms, or you can choose to renew your subscription. Which option would you prefer?",
                time_in_call_secs=23.0,
            ),
            TranscriptMessage(
                role="user",
                message="I want to renew my subscription.",
                time_in_call_secs=36.0,
            ),
            TranscriptMessage(
                role="agent",
                message=f"Thank you for confirming. Your {product_name} subscription will be renewed.",
                time_in_call_secs=39.0,
            ),
        ]

        mock_metadata = ConversationMetadata(
            start_time_unix_secs=int(time.time()),
            call_duration_secs=45,
            cost=0,
            termination_reason="user_ended_call",
        )

        return ConversationData(
            conversation_id=f"fake_{uuid.uuid4().hex[:8]}",
            agent_id=agent_id or "fake_agent",
            status="done",
            transcript=mock_transcript,
            metadata=mock_metadata,
        )

    def create_conversation(self, charge_id: str) -> str:
        conversation_id = f"conv_{uuid.uuid4().hex[:12]}"

        with self._lock:
            self._conversations[conversation_id] = ConversationResult(
                conversation_id=conversation_id,
                status=ConversationStatus.IN_PROGRESS,
            )
            self._charge_ids[conversation_id] = charge_id

        return conversation_id

    def run_conversation(
        self,
        conversation_id: str,
        fake_conv: bool = False,
    ) -> None:
        if not agent_id:
            raise ValueError("AGENT_ID must be set in environment variables")

        # Get charge_id from the stored mapping
        with self._lock:
            charge_id = self._charge_ids.get(conversation_id)

        if not charge_id:
            raise ValueError(f"No charge_id found for conversation {conversation_id}")

        phone_caller = PhoneCaller()

        # Fetch comprehensive charge details from Stripe
        print(f"💳 Fetching Stripe charge details: {charge_id}")
        charge_details = self.dispute_response_generator.get_charge_details(charge_id)

        # Generate AI-powered response arguments
        response_arguments, phone_number, name = (
            self.dispute_response_generator.generate_dispute_response(charge_id)
        )

        # Check for phone number override from environment
        phone_number_override = os.getenv("PHONE_NUMBER_OVERRIDE")
        if phone_number_override:
            print(f"📞 Using phone number override from .env: {phone_number_override}")
            phone_number = phone_number_override

        # Extract product and customer information from Stripe
        product_info = charge_details["product_info"]
        customer_info = charge_details["customer_info"]
        charge_info = charge_details["charge_info"]

        print(f"✅ Stripe data fetched:")
        print(f"   - Customer: {customer_info['name']}")
        print(f"   - Product: {product_info['name']}")
        print(f"   - Amount: ${charge_info['amount']:.2f}")
        print(f"   - Phone: {phone_number}")

        # Get dispute reason from charge details (if available, otherwise use generic)
        dispute_reason = charge_details.get("dispute_reason", "subscription_canceled")

        # Query RAG for relevant context before making the call
        print(f"🔍 Querying RAG for: {dispute_reason} - {product_info['name']}")
        rag_context = self.rag_service.query_context(
            chargeback_reason=dispute_reason,
            product_name=product_info["name"],  # Use actual product name from Stripe
            customer_name=customer_info["name"],  # Use actual customer name from Stripe
            top_k=10,  # Get top 10 most relevant results
        )

        # Format the context for the agent
        context_string = self.rag_service.format_context_for_agent(rag_context)

        # Log what RAG found
        print(f"✅ RAG Results:")
        print(f"   - {len(rag_context['dispute_scripts'])} dispute scripts")
        print(f"   - {len(rag_context['policies'])} policies")
        print(f"   - {len(rag_context['orders'])} orders")
        print(f"   - {len(rag_context['resolution_authority'])} resolution authorities")
        print(f"   - Context length: {len(context_string)} chars")

        # Create dynamic variables with actual Stripe data
        dynamic_variables = {
            "first_name": customer_info["name"].split(" ")[0],
            "last_name": (
                customer_info["name"].split(" ")[-1]
                if len(customer_info["name"].split(" ")) > 1
                else ""
            ),
            "phone_number": phone_number,
            "product_name": product_info["name"],
            "product_description": product_info["description"],
            "product_code": product_info["code"],
            "chargeback_reason": dispute_reason,
            "charge_amount": f"${charge_info['amount']:.2f}",
            "charge_date": charge_info["date"],
        }

        # Create agent with RAG context injected into the prompt
        agent = Agent(
            agent_id=agent_id,
            dynamic_variables=dynamic_variables,
        )

        # Add RAG context as supplementary information to the agent
        # This appends to the base prompt configured in ElevenLabs dashboard
        if context_string:
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
- Dispute Reason: {dispute_reason}

RELEVANT KNOWLEDGE BASE:
{context_string}

KEY EVIDENCE-BASED ARGUMENTS TO LEVERAGE:
{response_arguments}

Note: Use the above information to support your procedural guidance. The evidence-based arguments are particularly important - they come directly from our records and can help resolve the dispute. Maintain your established tone and approach."""

            agent.set_prompt(prompt=rag_supplement)

        start_time = time.time()

        try:
            if fake_conv:
                # Use fake conversation for testing
                print(f"🎭 Starting fake conversation (5 second delay)...")
                time.sleep(5)  # Simulate conversation delay
                conversation_data = self._create_fake_conversation(
                    product_name=product_info["name"],
                    first_name=customer_info["name"].split(" ")[0],
                    reason=dispute_reason,
                )
                print(f"✅ Fake conversation completed")
            else:
                # Make real phone call and wait for completion
                conversation_data = phone_caller.make_call_and_wait(
                    agent=agent,
                    to_number=phone_number,  # Use phone number from Stripe
                    poll_interval=1.5,
                    timeout=600,  # 10 minute timeout
                    print_transcript=False,  # Don't print to console in background task
                )

            end_time = time.time()
            duration = end_time - start_time

            # Convert transcript to API format
            transcript = [
                TranscriptEntry(
                    speaker=(
                        msg.role if msg.role in ("user", "agent") else "agent"
                    ),  # Ensure valid literal type
                    text=msg.message,
                    timestamp=msg.time_in_call_secs,
                )
                for msg in conversation_data.transcript
            ]

            # Save transcript to storage
            self.storage.save_transcript(conversation_data, filename=conversation_id)

            # Generate summary using TranscriptSummarizer
            summary = None
            if anthropic_api_key:
                try:
                    summarizer = TranscriptSummarizer()
                    anthropic_client = AsyncAnthropic(api_key=anthropic_api_key)
                    summary = asyncio.run(
                        summarizer.summarize(
                            client=anthropic_client,
                            transcript=conversation_data.transcript,
                        )
                    )
                except Exception as e:
                    # Log error but don't fail the whole conversation
                    print(f"Warning: Failed to generate summary: {e}")

            # Evaluate transcript and submit evidence to Stripe
            print("\n🔍 Evaluating transcript and submitting evidence to Stripe...")
            evidence_result_data = None
            try:
                # Convert transcript to format expected by DisputeEvaluator
                evaluator_transcript = [
                    {
                        "role": msg.role,
                        "message": msg.message,
                        "time_in_call_secs": msg.time_in_call_secs,
                    }
                    for msg in conversation_data.transcript
                ]

                # Submit evidence immediately to Stripe
                evidence_dict = self.dispute_evaluator.submit_evidence_to_stripe(
                    charge_id=charge_id,
                    transcript=evaluator_transcript,
                    submit_immediately=True,  # Submit to bank immediately
                    send_to_stripe=not fake_conv,  # Actually send to Stripe
                )

                print("✅ Evidence submitted successfully!")
                print(f"   - Dispute ID: {evidence_dict['dispute_id']}")
                print(f"   - Resolved: {evidence_dict['evaluation']['resolved']}")
                print(
                    f"   - Resolution Type: {evidence_dict['evaluation']['resolution_type']}"
                )
                print(
                    f"   - Evidence Fields: {len(evidence_dict.get('evidence_generated', {}))}"
                )
                print(f"   - Status: {evidence_dict['status']}")

                # Convert evidence_generated to dict if it's a list
                evidence_generated = evidence_dict.get('evidence_generated', {})
                if isinstance(evidence_generated, list):
                    # If it's a list of field names, convert to dict with empty values
                    evidence_generated = {field: "" for field in evidence_generated}

                # Convert to Pydantic model
                evidence_result_data = EvidenceResult(
                    dispute_id=evidence_dict['dispute_id'],
                    evaluation=DisputeEvaluation(
                        resolved=evidence_dict['evaluation']['resolved'],
                        resolution_type=evidence_dict['evaluation'].get('resolution_type'),
                        confidence=evidence_dict['evaluation'].get('confidence'),
                        reasoning=evidence_dict['evaluation'].get('reasoning')
                    ),
                    evidence_generated=evidence_generated,
                    status=evidence_dict['status'],
                    submitted_to_stripe=not fake_conv
                )
            except Exception as e:
                # Log error but don't fail the whole conversation
                print(f"⚠️  Warning: Failed to submit evidence to Stripe: {e}")
                import traceback

                traceback.print_exc()

            with self._lock:
                self._conversations[conversation_id] = ConversationResult(
                    conversation_id=conversation_id,
                    status=ConversationStatus.COMPLETED,
                    transcript=transcript,
                    duration_seconds=conversation_data.metadata.call_duration_secs,
                    summary=summary,
                    evidence_result=evidence_result_data,
                )

        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time

            with self._lock:
                self._conversations[conversation_id] = ConversationResult(
                    conversation_id=conversation_id,
                    status=ConversationStatus.FAILED,
                    transcript=None,
                    duration_seconds=duration,
                    error=str(e),
                )

    def get_conversation_result(
        self, conversation_id: str
    ) -> ConversationResult | None:
        with self._lock:
            return self._conversations.get(conversation_id)

    def list_saved_transcripts(self) -> list[dict]:
        """List all saved transcripts from storage."""
        return self.storage.list_transcripts()
