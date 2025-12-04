"""
Conversation Manager - Retrieve and monitor ElevenLabs conversations.
"""

import time
from typing import Any, Literal
from dataclasses import dataclass
import httpx
from elevenlabs.client import ElevenLabs


ConversationStatus = Literal["initiated", "in-progress", "processing", "done", "failed"]


@dataclass
class TranscriptMessage:
    """Single message in a conversation transcript."""

    role: str  # "user" or "agent"
    message: str
    time_in_call_secs: float
    tool_calls: Any | None = None
    tool_results: Any | None = None


@dataclass
class ConversationMetadata:
    """Metadata about a conversation."""

    start_time_unix_secs: int
    call_duration_secs: int
    cost: int
    termination_reason: str | None = None


@dataclass
class ConversationData:
    """Complete conversation data including transcript and metadata."""

    conversation_id: str
    agent_id: str
    status: ConversationStatus
    transcript: list[TranscriptMessage]
    metadata: ConversationMetadata
    user_id: str | None = None
    transcript_summary: str | None = None


class ConversationManager:
    """Manager for retrieving and monitoring ElevenLabs conversations."""

    def __init__(self, api_key: str):
        """
        Initialize the ConversationManager.

        Args:
            api_key: ElevenLabs API key
        """
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"

    def get_conversation(self, conversation_id: str) -> ConversationData:
        """
        Get complete conversation details including transcript.

        Args:
            conversation_id: The conversation ID to retrieve

        Returns:
            ConversationData with full details

        Raises:
            httpx.HTTPStatusError: If the API request fails
        """
        url = f"{self.base_url}/convai/conversations/{conversation_id}"
        headers = {"xi-api-key": self.api_key}

        with httpx.Client() as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

        return self._parse_conversation_data(data)

    async def get_conversation_async(self, conversation_id: str) -> ConversationData:
        """
        Async version of get_conversation.

        Args:
            conversation_id: The conversation ID to retrieve

        Returns:
            ConversationData with full details
        """
        url = f"{self.base_url}/convai/conversations/{conversation_id}"
        headers = {"xi-api-key": self.api_key}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

        return self._parse_conversation_data(data)

    def wait_for_completion(
        self,
        conversation_id: str,
        poll_interval: int = 2,
        timeout: int | None = None,
        verbose: bool = True,
    ) -> ConversationData:
        """
        Wait for a conversation to complete by polling.

        Args:
            conversation_id: The conversation ID to monitor
            poll_interval: Seconds between status checks (default: 2)
            timeout: Maximum seconds to wait (default: None = no timeout)
            verbose: Print status updates (default: True)

        Returns:
            ConversationData when conversation is complete

        Raises:
            TimeoutError: If timeout is reached before completion
            Exception: If conversation fails
        """
        start_time = time.time()

        if verbose:
            print(f"⏳ Waiting for conversation {conversation_id} to complete...")

        while True:
            elapsed = time.time() - start_time

            # Check timeout
            if timeout and elapsed > timeout:
                raise TimeoutError(
                    f"Conversation did not complete within {timeout} seconds"
                )

            # Get current status
            try:
                data = self.get_conversation(conversation_id)
            except httpx.HTTPStatusError as e:
                if verbose:
                    print(f"⚠️  Error fetching conversation: {e}")
                time.sleep(poll_interval)
                continue

            status = data.status

            if verbose:
                print(f"   Status: {status} (elapsed: {elapsed:.1f}s)")

            if status == "done":
                if verbose:
                    print(f"✅ Conversation completed!")
                return data

            if status == "failed":
                raise Exception(f"Conversation failed: {data}")

            # Still processing - wait and try again
            time.sleep(poll_interval)

    def list_conversations(
        self,
        agent_id: str | None = None,
        page_size: int = 30,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """
        List conversations with optional filtering.

        Args:
            agent_id: Optional agent ID filter
            page_size: Number of results per page (max 100)
            cursor: Pagination cursor from previous response

        Returns:
            Dict with conversations list and pagination info
        """
        url = f"{self.base_url}/convai/conversations"
        headers = {"xi-api-key": self.api_key}
        params: dict[str, Any] = {"page_size": min(page_size, 100)}

        if agent_id:
            params["agent_id"] = agent_id
        if cursor:
            params["cursor"] = cursor

        with httpx.Client() as client:
            response = client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()

    def _parse_conversation_data(self, data: dict[str, Any]) -> ConversationData:
        """Parse API response into ConversationData."""
        # Parse transcript messages
        transcript = []
        for msg in data.get("transcript", []):
            # Skip messages with None content
            if msg.get("message") is None:
                continue

            transcript.append(
                TranscriptMessage(
                    role=msg["role"],
                    message=msg["message"],
                    time_in_call_secs=msg.get("time_in_call_secs", 0),
                    tool_calls=msg.get("tool_calls"),
                    tool_results=msg.get("tool_results"),
                )
            )

        # Parse metadata
        meta = data.get("metadata", {})
        metadata = ConversationMetadata(
            start_time_unix_secs=meta.get("start_time_unix_secs", 0),
            call_duration_secs=meta.get("call_duration_secs", 0),
            cost=meta.get("cost", 0),
            termination_reason=meta.get("termination_reason"),
        )

        # Get summary if available
        analysis = data.get("analysis") or {}
        transcript_summary = analysis.get("transcript_summary") if analysis else None

        return ConversationData(
            conversation_id=data["conversation_id"],
            agent_id=data["agent_id"],
            status=data["status"],
            transcript=transcript,
            metadata=metadata,
            user_id=data.get("user_id"),
            transcript_summary=transcript_summary,
        )

    def print_transcript(self, conversation_data: ConversationData) -> None:
        """
        Print a formatted transcript of the conversation.

        Args:
            conversation_data: The conversation data to print
        """
        print("\n" + "=" * 60)
        print(f"📝 Conversation Transcript")
        print("=" * 60)
        print(f"Conversation ID: {conversation_data.conversation_id}")
        print(f"Agent ID: {conversation_data.agent_id}")
        print(f"Status: {conversation_data.status}")
        print(f"Duration: {conversation_data.metadata.call_duration_secs}s")

        if conversation_data.transcript_summary:
            print(f"\n📊 Summary:")
            print(f"   {conversation_data.transcript_summary}")

        print(f"\n💬 Messages:")
        print("-" * 60)

        for i, msg in enumerate(conversation_data.transcript, 1):
            emoji = "👤" if msg.role == "user" else "🤖"
            time_str = f"[{msg.time_in_call_secs:.1f}s]"
            print(f"{i}. {emoji} {msg.role.title()} {time_str}")
            print(f"   {msg.message}")
            if i < len(conversation_data.transcript):
                print()

        print("-" * 60)
        print(f"Total messages: {len(conversation_data.transcript)}")
        print("=" * 60)
