#!/usr/bin/env python3
"""
View saved conversation transcripts and their evaluation status.
"""
import os
import sys
import json
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from conversation.service import ConversationService


def main():
    service = ConversationService()

    print("=" * 80)
    print("SAVED CONVERSATION TRANSCRIPTS")
    print("=" * 80 + "\n")

    # List all saved transcripts
    transcripts = service.list_saved_transcripts()

    if not transcripts:
        print("No transcripts found.\n")
        return

    print(f"Found {len(transcripts)} transcript(s):\n")

    for i, transcript in enumerate(transcripts, 1):
        print(f"[{i}] {transcript['filename']}")
        print(f"    Date: {transcript['modified']}")
        print(f"    Size: {transcript['size']} bytes")
        print()

    # Show details of the most recent transcript
    if transcripts:
        recent = transcripts[0]
        print("=" * 80)
        print(f"MOST RECENT TRANSCRIPT: {recent['filename']}")
        print("=" * 80 + "\n")

        transcript_path = Path("transcripts") / recent['filename']
        if transcript_path.exists():
            with open(transcript_path, 'r') as f:
                data = json.load(f)

            print(f"Conversation ID: {data.get('conversation_id', 'N/A')}")
            print(f"Status: {data.get('status', 'N/A')}")
            print(f"Agent ID: {data.get('agent_id', 'N/A')}")

            metadata = data.get('metadata', {})
            print(f"\nCall Metadata:")
            print(f"  Duration: {metadata.get('call_duration_secs', 0):.1f} seconds")
            print(f"  Cost: ${metadata.get('cost', 0):.4f}")
            print(f"  Termination Reason: {metadata.get('termination_reason', 'N/A')}")

            transcript = data.get('transcript', [])
            print(f"\nTranscript ({len(transcript)} messages):")

            for j, msg in enumerate(transcript[:10], 1):  # Show first 10 messages
                emoji = "👤" if msg.get('role') == 'user' else "🤖"
                time_str = f"[{msg.get('time_in_call_secs', 0):.1f}s]"
                role = msg.get('role', 'unknown').upper()
                message = msg.get('message', '')

                print(f"\n{j}. {emoji} {role} {time_str}")
                print(f"   {message}")

            if len(transcript) > 10:
                print(f"\n... and {len(transcript) - 10} more messages")

    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
