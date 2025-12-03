import time
import threading
from typing import List, Literal
from conversation.models import TranscriptEntry


class TranscriptManager:
    def __init__(self):
        self._transcript: List[TranscriptEntry] = []
        self._lock = threading.Lock()
        self._start_time: float | None = None

    def _get_timestamp(self) -> float:
        if self._start_time is None:
            self._start_time = time.time()
            return 0.0
        return time.time() - self._start_time

    def add_user_message(self, text: str) -> None:
        with self._lock:
            timestamp = self._get_timestamp()
            entry = TranscriptEntry(
                speaker="user",
                text=text,
                timestamp=timestamp
            )
            self._transcript.append(entry)

    def add_agent_message(self, text: str) -> None:
        with self._lock:
            timestamp = self._get_timestamp()
            entry = TranscriptEntry(
                speaker="agent",
                text=text,
                timestamp=timestamp
            )
            self._transcript.append(entry)

    def correct_last_agent_message(self, original_text: str, corrected_text: str) -> None:
        with self._lock:
            for i in range(len(self._transcript) - 1, -1, -1):
                if self._transcript[i].speaker == "agent" and self._transcript[i].text == original_text:
                    self._transcript[i] = TranscriptEntry(
                        speaker="agent",
                        text=corrected_text,
                        timestamp=self._transcript[i].timestamp
                    )
                    return
            raise ValueError(f"Could not find agent message with text: {original_text}")

    def get_transcript(self) -> List[TranscriptEntry]:
        with self._lock:
            return self._transcript.copy()

    def reset(self) -> None:
        with self._lock:
            self._transcript.clear()
            self._start_time = None