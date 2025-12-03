"""
Transcript Storage - Save and load conversation transcripts to/from JSON files.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from .conversation_manager import ConversationData, TranscriptMessage, ConversationMetadata


class TranscriptStorage:
    """Storage for conversation transcripts using JSON files."""

    def __init__(self, storage_dir: str = "transcripts"):
        """
        Initialize the transcript storage.

        Args:
            storage_dir: Directory to store transcript files (default: "transcripts")
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True, parents=True)

    def save_transcript(
        self, conversation_data: ConversationData, filename: str | None = None
    ) -> str:
        """
        Save a conversation transcript to a JSON file.

        Args:
            conversation_data: The conversation data to save
            filename: Optional custom filename (without extension)

        Returns:
            Path to the saved file
        """
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{conversation_data.conversation_id}_{timestamp}"

        # Ensure .json extension
        if not filename.endswith(".json"):
            filename = f"{filename}.json"

        filepath = self.storage_dir / filename

        # Convert to dict for JSON serialization
        data = {
            "conversation_id": conversation_data.conversation_id,
            "agent_id": conversation_data.agent_id,
            "status": conversation_data.status,
            "user_id": conversation_data.user_id,
            "transcript_summary": conversation_data.transcript_summary,
            "metadata": {
                "start_time_unix_secs": conversation_data.metadata.start_time_unix_secs,
                "call_duration_secs": conversation_data.metadata.call_duration_secs,
                "cost": conversation_data.metadata.cost,
                "termination_reason": conversation_data.metadata.termination_reason,
            },
            "transcript": [
                {
                    "role": msg.role,
                    "message": msg.message,
                    "time_in_call_secs": msg.time_in_call_secs,
                    "tool_calls": msg.tool_calls,
                    "tool_results": msg.tool_results,
                }
                for msg in conversation_data.transcript
            ],
            "saved_at": datetime.now().isoformat(),
        }

        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"💾 Transcript saved to: {filepath}")
        return str(filepath)

    def load_transcript(self, filename: str) -> ConversationData:
        """
        Load a conversation transcript from a JSON file.

        Args:
            filename: Name of the file to load (with or without .json extension)

        Returns:
            ConversationData object

        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        # Add .json extension if not present
        if not filename.endswith(".json"):
            filename = f"{filename}.json"

        filepath = self.storage_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Transcript file not found: {filepath}")

        # Load from file
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Reconstruct objects
        metadata = ConversationMetadata(
            start_time_unix_secs=data["metadata"]["start_time_unix_secs"],
            call_duration_secs=data["metadata"]["call_duration_secs"],
            cost=data["metadata"]["cost"],
            termination_reason=data["metadata"].get("termination_reason"),
        )

        transcript = [
            TranscriptMessage(
                role=msg["role"],
                message=msg["message"],
                time_in_call_secs=msg["time_in_call_secs"],
                tool_calls=msg.get("tool_calls"),
                tool_results=msg.get("tool_results"),
            )
            for msg in data["transcript"]
        ]

        return ConversationData(
            conversation_id=data["conversation_id"],
            agent_id=data["agent_id"],
            status=data["status"],
            transcript=transcript,
            metadata=metadata,
            user_id=data.get("user_id"),
            transcript_summary=data.get("transcript_summary"),
        )

    def list_transcripts(self) -> list[dict[str, str]]:
        """
        List all saved transcripts.

        Returns:
            List of dicts with file info (filename, conversation_id, saved_at)
        """
        transcripts = []

        for filepath in self.storage_dir.glob("*.json"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                transcripts.append(
                    {
                        "filename": filepath.name,
                        "conversation_id": data.get("conversation_id", "unknown"),
                        "saved_at": data.get("saved_at", "unknown"),
                        "duration_secs": data.get("metadata", {}).get(
                            "call_duration_secs", 0
                        ),
                        "message_count": len(data.get("transcript", [])),
                    }
                )
            except Exception as e:
                print(f"⚠️  Error reading {filepath.name}: {e}")

        # Sort by saved_at (newest first)
        transcripts.sort(key=lambda x: x["saved_at"], reverse=True)

        return transcripts

    def find_by_conversation_id(self, conversation_id: str) -> Optional[str]:
        """
        Find a transcript file by conversation ID.

        Args:
            conversation_id: The conversation ID to search for

        Returns:
            Filename if found, None otherwise
        """
        for filepath in self.storage_dir.glob("*.json"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("conversation_id") == conversation_id:
                        return filepath.name
            except Exception:
                continue

        return None

    def delete_transcript(self, filename: str) -> bool:
        """
        Delete a transcript file.

        Args:
            filename: Name of the file to delete

        Returns:
            True if deleted, False if not found
        """
        if not filename.endswith(".json"):
            filename = f"{filename}.json"

        filepath = self.storage_dir / filename

        if filepath.exists():
            filepath.unlink()
            print(f"🗑️  Deleted transcript: {filename}")
            return True

        return False