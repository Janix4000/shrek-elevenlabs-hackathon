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
    charge_id: str = Field(..., min_length=1, description="Stripe charge ID (e.g., ch_xxxxx)")
    product_name: str = Field(..., min_length=1, description="Name of the product")
    reason: str = Field(..., min_length=1, description="Reason for chargeback")

    @field_validator("charge_id", "product_name", "reason")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace only")
        return v.strip()


class ConversationRequest(BaseModel):
    user_info: Optional[UserInfo] = None  # Optional - will be fetched from Stripe if not provided
    chargeback_info: ChargebackInfo

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_info": {
                        "first_name": "John",
                        "last_name": "Doe",
                        "phone_number": "+1234567890"
                    },
                    "chargeback_info": {
                        "charge_id": "ch_3SaQFuAITa6PCFHj0dnBlMJP",
                        "product_name": "Shrek Premium Subscription",
                        "reason": "Unauthorized charge"
                    }
                }
            ]
        }
    }


class ConversationStartResponse(BaseModel):
    conversation_id: str = Field(..., description="Unique ID to track this conversation")
    status: Literal["started"] = "started"


class TranscriptEntry(BaseModel):
    speaker: Literal["agent", "user"]
    text: str
    timestamp: float = Field(..., description="Timestamp in seconds from conversation start")


class ConversationStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ConversationResult(BaseModel):
    conversation_id: str
    status: ConversationStatus
    transcript: Optional[List[TranscriptEntry]] = None
    duration_seconds: Optional[float] = None
    summary: Optional[str] = None
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
                            "timestamp": 0.0
                        },
                        {
                            "speaker": "user",
                            "text": "Yes, I'd like to discuss that.",
                            "timestamp": 2.5
                        }
                    ],
                    "duration_seconds": 120.5,
                    "error": None
                }
            ]
        }
    }