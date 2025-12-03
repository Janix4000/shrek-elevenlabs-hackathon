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

    def create_conversation(self, request: ConversationRequest) -> str:
        conversation_id = f"conv_{uuid.uuid4().hex[:12]}"

        with self._lock:
            self._conversations[conversation_id] = ConversationResult(
                conversation_id=conversation_id,
                status=ConversationStatus.IN_PROGRESS,
            )

        return conversation_id

    def run_conversation(
        self, conversation_id: str, request: ConversationRequest
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
            # Make phone call and wait for completion
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
