"""
Transcript Summarizer - Agent that extracts customer decisions and actions from conversations.
"""

from anthropic import AsyncAnthropic
from elevenlabs_wrapper.conversation_manager import TranscriptMessage
from .llm_agent import LLMAgent


class TranscriptSummarizer(LLMAgent):
    """
    Specialized agent that summarizes conversation transcripts.
    Focuses ONLY on customer decisions and actions, ignoring agent statements.

    Output format: "user [action]; user [decision]"
    Example: "user forgotten to cancel subscription; user decided to renew"
    """

    def __init__(
        self,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 1024,
        temperature: float = 0.3,
    ):
        """
        Initialize the TranscriptSummarizer.

        Args:
            model: Claude model to use (default: claude-sonnet-4-20250514)
            max_tokens: Maximum tokens in response (default: 1024)
            temperature: Sampling temperature (default: 0.3 for more focused output)
        """
        role_description = (
            "You are an expert at analyzing customer service conversations. "
            "Your role is to extract ONLY customer decisions and actions from transcripts."
        )

        context = (
            "You will receive a conversation transcript between a customer (user) and an agent. "
            "Focus EXCLUSIVELY on what the customer said, did, or decided. "
            "COMPLETELY IGNORE everything the agent said."
        )

        output_format = (
            "Output format: 'user [action]; user [decision]; user [action]'\n\n"
            "Examples:\n"
            "- 'user forgotten to cancel subscription; user decided to renew'\n"
            "- 'user had chargeback issue; user wants refund'\n"
            "- 'user never used product; user agreed to keep subscription'\n\n"
            "Be EXTREMELY concise. Only include what the USER said, decided, or did. "
            "No agent statements, no explanations, no extra words."
        )

        super().__init__(
            role_description=role_description,
            context=context,
            output_format=output_format,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
        )

    async def summarize(
        self,
        client: AsyncAnthropic,
        transcript: list[TranscriptMessage],
    ) -> str:
        """
        Summarize a conversation transcript focusing on customer decisions and actions.

        Args:
            client: Initialized Anthropic client
            transcript: List of transcript messages from the conversation

        Returns:
            Concise summary in format: "user [action]; user [decision]"
        """
        task = (
            "Analyze the transcript below and extract ONLY the customer's (user's) "
            "decisions, actions, and statements. Ignore everything the agent said."
        )

        # Format transcript for the LLM
        formatted_transcript = self._format_transcript(transcript)

        # Run the agent with the formatted transcript as user input
        summary = await self.run(
            client=client,
            task=task,
            user_input=formatted_transcript,
        )

        return summary.strip()

    def _format_transcript(self, transcript: list[TranscriptMessage]) -> str:
        """
        Format transcript messages into a readable string.

        Args:
            transcript: List of TranscriptMessage objects

        Returns:
            Formatted transcript string
        """
        lines = []
        for msg in transcript:
            role = msg.role.upper()
            text = msg.message.strip()
            timestamp = f"[{msg.time_in_call_secs:.1f}s]"

            if text:  # Skip empty messages
                lines.append(f"{role} {timestamp}: {text}")

        return "\n".join(lines)
