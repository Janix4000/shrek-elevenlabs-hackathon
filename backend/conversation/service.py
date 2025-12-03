import time
import uuid
import threading
from typing import Dict
from conversation.models import (
    ConversationRequest,
    ConversationResult,
    ConversationStatus,
)
from elevenlabs.client import ElevenLabsClient
from elevenlabs.transcript_manager import TranscriptManager


class ConversationService:
    def __init__(self):
        self._conversations: Dict[str, ConversationResult] = {}
        self._lock = threading.Lock()

    def _create_dynamic_variables(self, request: ConversationRequest) -> Dict[str, str]:
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

    def run_conversation(self, conversation_id: str, request: ConversationRequest) -> None:
        transcript_manager = TranscriptManager()
        elevenlabs_client = ElevenLabsClient(transcript_manager=transcript_manager)

        dynamic_variables = self._create_dynamic_variables(request)

        start_time = time.time()

        try:
            elevenlabs_conversation_id = elevenlabs_client.start_conversation(dynamic_variables)

            end_time = time.time()
            duration = end_time - start_time

            transcript = transcript_manager.get_transcript()

            with self._lock:
                self._conversations[conversation_id] = ConversationResult(
                    conversation_id=conversation_id,
                    status=ConversationStatus.COMPLETED,
                    transcript=transcript,
                    duration_seconds=duration,
                )

        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time

            transcript = transcript_manager.get_transcript()

            with self._lock:
                self._conversations[conversation_id] = ConversationResult(
                    conversation_id=conversation_id,
                    status=ConversationStatus.FAILED,
                    transcript=transcript if transcript else None,
                    duration_seconds=duration,
                    error=str(e)
                )

    def get_conversation_result(self, conversation_id: str) -> ConversationResult | None:
        with self._lock:
            return self._conversations.get(conversation_id)