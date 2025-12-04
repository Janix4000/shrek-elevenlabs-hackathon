from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, status
from typing import List
from conversation.models import (
    ConversationRequestLegacy,
    ConversationStartResponse,
    ConversationResult,
)
from conversation.service import ConversationService

router = APIRouter(prefix="/api/conversation", tags=["conversation"])

conversation_service = ConversationService()


@router.post(
    "/start",
    response_model=ConversationStartResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def start_conversation(
    request: ConversationRequestLegacy,
    background_tasks: BackgroundTasks,
    fake_conv: bool = Query(
        False, description="Use fake conversation for testing (no real phone call)"
    ),
    update_stripe: bool = Query(
        False, description="Actually submit evidence to Stripe (set to false for testing)"
    ),
) -> ConversationStartResponse:
    """
    Start a new phone conversation with the agent.
    The call will be made in the background and you can check the status later.

    For testing, use ?fake_conv=true to simulate a conversation without making a real phone call.
    Use ?update_stripe=true to actually submit evidence to Stripe.

    Request body only requires the Stripe charge_id - all other information
    (customer details, product info, etc.) will be fetched automatically from Stripe.
    """
    conversation_id = conversation_service.create_conversation(
        request.charge_id, phone_number_override=request.phone_number
    )

    background_tasks.add_task(
        conversation_service.run_conversation, conversation_id, fake_conv, update_stripe
    )

    return ConversationStartResponse(conversation_id=conversation_id, status="started")


@router.get("/{conversation_id}", response_model=ConversationResult)
async def get_conversation_result(conversation_id: str) -> ConversationResult:
    """
    Get the result and transcript of a conversation.
    Returns the current status and transcript if completed.
    """
    result = conversation_service.get_conversation_result(conversation_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with ID {conversation_id} not found",
        )

    return result


@router.get("/", response_model=List[dict])
async def list_saved_transcripts() -> List[dict]:
    """
    List all saved transcripts from the storage.
    """
    return conversation_service.list_saved_transcripts()
