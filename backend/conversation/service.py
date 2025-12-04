import os
import time
import uuid
import threading
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from anthropic import AsyncAnthropic
from conversation.models import (
    ConversationRequest,
    ConversationResult,
    ConversationStatus,
    TranscriptEntry,
)
from elevenlabs_wrapper.phone_caller import PhoneCaller
from elevenlabs_wrapper.agent import Agent
from elevenlabs_wrapper.transcript_storage import TranscriptStorage
from elevenlabs_wrapper.transcript_summarizer import TranscriptSummarizer
from elevenlabs_wrapper.conversation_manager import (
    ConversationData,
    TranscriptMessage,
    ConversationMetadata,
)

load_dotenv()

agent_id = os.getenv("AGENT_ID")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")


class ConversationService:
    def __init__(self, storage_dir: str = "transcripts"):
        self._conversations: dict[str, ConversationResult] = {}
        self._lock = threading.Lock()
        self.storage = TranscriptStorage(storage_dir=storage_dir)

    def _create_dynamic_variables(self, request: ConversationRequest) -> dict[str, str]:
        return {
            "first_name": request.user_info.first_name,
            "last_name": request.user_info.last_name,
            "phone_number": request.user_info.phone_number,
            "product_name": request.chargeback_info.product_name,
            "chargeback_reason": request.chargeback_info.reason,
        }

    def _create_fake_conversation(
        self, request: ConversationRequest
    ) -> ConversationData:
        """Create a fake conversation for testing purposes."""
        product_name = request.chargeback_info.product_name
        first_name = request.user_info.first_name
        reason = request.chargeback_info.reason

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

    def create_conversation(self, request: ConversationRequest) -> str:
        conversation_id = f"conv_{uuid.uuid4().hex[:12]}"

        with self._lock:
            self._conversations[conversation_id] = ConversationResult(
                conversation_id=conversation_id,
                status=ConversationStatus.IN_PROGRESS,
            )

        return conversation_id

    def run_conversation(
        self, conversation_id: str, request: ConversationRequest, fake_conv: bool = False
    ) -> None:
        if not agent_id:
            raise ValueError("AGENT_ID must be set in environment variables")

        phone_caller = PhoneCaller()

        dynamic_variables = self._create_dynamic_variables(request)
        agent = Agent(
            agent_id=agent_id,
            dynamic_variables=dynamic_variables,
        )

        start_time = time.time()

        try:
            if fake_conv:
                # Use fake conversation for testing
                print(f"🎭 Starting fake conversation (5 second delay)...")
                time.sleep(5)  # Simulate conversation delay
                conversation_data = self._create_fake_conversation(request)
                print(f"✅ Fake conversation completed")
            else:
                # Make real phone call and wait for completion
                conversation_data = phone_caller.make_call_and_wait(
                    agent=agent,
                    to_number=request.user_info.phone_number,
                    poll_interval=2,
                    timeout=600,  # 10 minute timeout
                    print_transcript=False,  # Don't print to console in background task
                )

            end_time = time.time()
            duration = end_time - start_time

            # Convert transcript to API format
            transcript = [
                TranscriptEntry(
                    speaker=msg.role,  # "user" or "agent"
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

            with self._lock:
                self._conversations[conversation_id] = ConversationResult(
                    conversation_id=conversation_id,
                    status=ConversationStatus.COMPLETED,
                    transcript=transcript,
                    duration_seconds=conversation_data.metadata.call_duration_secs,
                    summary=summary,
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
