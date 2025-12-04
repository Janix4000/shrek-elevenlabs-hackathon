from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional
from enum import Enum


class UserInfo(BaseModel):
    first_name: str = Field(..., min_length=1, description="User's first name")
    last_name: str = Field(..., min_length=1, description="User's last name")
    phone_number: str = Field(..., min_length=1, description="User's phone number")

    @field_validator("first_name", "last_name", "phone_number")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace only")
        return v.strip()


class ChargebackInfo(BaseModel):
    charge_id: str = Field(
        ..., min_length=1, description="Stripe charge ID (e.g., ch_xxxxx)"
    )
    product_name: str = Field(..., min_length=1, description="Name of the product")
    reason: str = Field(..., min_length=1, description="Reason for chargeback")

    @field_validator("charge_id", "product_name", "reason")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace only")
        return v.strip()


class ConversationRequestLegacy(BaseModel):
    """Legacy request format - kept for backwards compatibility."""

    user_info: Optional[UserInfo] = (
        None  # Optional - will be fetched from Stripe if not provided
    )
    charge_id: str = Field(
        ..., min_length=1, description="Stripe charge ID (e.g., ch_xxxxx)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_info": {
                        "first_name": "John",
                        "last_name": "Doe",
                        "phone_number": "+1234567890",
                    },
                    "charge_id": "ch_3SaQFuAITa6PCFHj0dnBlMJP",
                }
            ]
        }
    }


class ConversationStartResponse(BaseModel):
    conversation_id: str = Field(
        ..., description="Unique ID to track this conversation"
    )
    status: Literal["started"] = "started"


class TranscriptEntry(BaseModel):
    speaker: Literal["agent", "user"]
    text: str
    timestamp: float = Field(
        ..., description="Timestamp in seconds from conversation start"
    )


class ConversationStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class DisputeEvaluation(BaseModel):
    """Evaluation of the conversation outcome."""
    resolved: bool = Field(..., description="Whether the dispute was resolved")
    resolution_type: Optional[str] = Field(None, description="Type of resolution (e.g., 'renewed', 'canceled', 'partial_refund')")
    confidence: Optional[float] = Field(None, description="Confidence score of the evaluation")
    reasoning: Optional[str] = Field(None, description="Reasoning behind the evaluation")


class EvidenceResult(BaseModel):
    """Result of evidence generation and submission."""
    dispute_id: str = Field(..., description="Stripe dispute ID")
    evaluation: DisputeEvaluation
    evidence_generated: dict = Field(..., description="Generated evidence fields")
    status: str = Field(..., description="Submission status")
    submitted_to_stripe: bool = Field(..., description="Whether evidence was actually submitted to Stripe")


class ConversationResult(BaseModel):
    conversation_id: str
    status: ConversationStatus
    transcript: Optional[List[TranscriptEntry]] = None
    duration_seconds: Optional[float] = None
    summary: Optional[str] = None
    evidence_result: Optional[EvidenceResult] = None
    error: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "conversation_id": "conv_abc123",
                    "status": "completed",
                    "transcript": [
                        {
                            "speaker": "agent",
                            "text": "Hello, this is regarding your recent chargeback.",
                            "timestamp": 0.0,
                        },
                        {
                            "speaker": "user",
                            "text": "Yes, I'd like to discuss that.",
                            "timestamp": 2.5,
                        },
                    ],
                    "duration_seconds": 120.5,
                    "summary": "Customer agreed to renew subscription.",
                    "evidence_result": {
                        "dispute_id": "du_1234567890",
                        "evaluation": {
                            "resolved": True,
                            "resolution_type": "renewed",
                            "confidence": 0.95,
                            "reasoning": "Customer explicitly agreed to renew"
                        },
                        "evidence_generated": {
                            "cancellation_rebuttal": "...",
                            "product_description": "..."
                        },
                        "status": "submitted",
                        "submitted_to_stripe": True
                    },
                    "error": None,
                }
            ]
        }
    }
