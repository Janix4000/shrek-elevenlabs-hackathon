"""
LLM Agent - Configurable Claude AI agent for specific tasks
"""

import logging
from typing import Any, Optional
from anthropic import AsyncAnthropic
from anthropic.types import MessageParam

logger = logging.getLogger(__name__)


class LLMAgent:
    """
    Configurable LLM agent that constructs prompts from role, context, and output format.
    Task is provided when running the agent.

    Example:
        agent = LLMAgent(
            role_description="You are an expert customer service analyst",
            context="Customer had a chargeback for Shrek Premium subscription",
            output_format="Return JSON with fields: resolved (bool), reason (string)"
        )

        result = await agent.run(
            client=anthropic_client,
            task="Analyze the conversation and determine if the issue was resolved"
        )
    """

    def __init__(
        self,
        role_description: str,
        context: str,
        output_format: str,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ):
        """
        Initialize the LLM agent with configuration.

        Args:
            role_description: Description of the agent's role/persona
            context: Background information and context for the task
            output_format: Expected format of the output
            model: Claude model to use (default: claude-sonnet-4-20250514)
            max_tokens: Maximum tokens in response (default: 4096)
            temperature: Sampling temperature (default: 0.7)
        """
        self.role_description = role_description
        self.context = context
        self.output_format = output_format
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def _build_system_prompt(self, task: str) -> str:
        """Build the complete system prompt from components."""
        prompt_parts = []

        # Add role description
        if self.role_description:
            prompt_parts.append(f"# Role\n{self.role_description}")

        # Add context
        if self.context:
            prompt_parts.append(f"# Context\n{self.context}")

        # Add task
        if task:
            prompt_parts.append(f"# Task\n{task}")

        # Add output format
        if self.output_format:
            prompt_parts.append(f"# Output Format\n{self.output_format}")

        return "\n\n".join(prompt_parts)

    async def run(
        self,
        client: AsyncAnthropic,
        task: str,
        user_input: Optional[str] = None,
        additional_context: Optional[dict[str, Any]] = None,
    ) -> str:
        """
        Run the agent with the given task.

        Args:
            client: Initialized Anthropic client
            task: Specific task the agent should perform
            user_input: Optional user input/query for the agent
            additional_context: Optional additional context to inject

        Returns:
            Agent's response as string

        Raises:
            Exception: If the API call fails
        """
        # Build system prompt with task
        system_prompt = self._build_system_prompt(task)

        # Build user message
        user_message = self._build_user_message(user_input, additional_context)

        logger.info(f"🤖 Running LLM agent: {self.role_description[:50]}...")
        logger.debug(f"Task: {task}")
        logger.debug(f"System prompt: {system_prompt}")
        logger.debug(f"User message: {user_message}")

        try:
            # Call Claude API
            response = await client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )

            # Extract text from response
            result = response.content[0].text

            logger.info(f"✅ Agent completed successfully")
            logger.debug(f"Response: {result[:200]}...")

            return result

        except Exception as e:
            logger.error(f"❌ Agent execution failed: {e}")
            raise

    def _build_user_message(
        self,
        user_input: Optional[str] = None,
        additional_context: Optional[dict[str, Any]] = None,
    ) -> str:
        """Build the user message with optional input and context."""
        message_parts = []

        # Add additional context if provided
        if additional_context:
            context_str = "\n".join(
                f"- {key}: {value}" for key, value in additional_context.items()
            )
            message_parts.append(f"Additional Context:\n{context_str}")

        # Add user input if provided
        if user_input:
            message_parts.append(f"Input:\n{user_input}")

        # If no input provided, use a default prompt
        if not message_parts:
            message_parts.append("Please proceed with the task described above.")

        return "\n\n".join(message_parts)

    async def run_with_messages(
        self,
        client: AsyncAnthropic,
        task: str,
        messages: list[MessageParam],
    ) -> str:
        """
        Run the agent with custom message history.

        Args:
            client: Initialized Anthropic client
            task: Specific task the agent should perform
            messages: List of message dicts with 'role' and 'content'

        Returns:
            Agent's response as string
        """
        # Build system prompt with task
        system_prompt = self._build_system_prompt(task)

        logger.info(f"🤖 Running LLM agent with {len(messages)} messages")

        try:
            response = await client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=messages,
            )

            result = response.content[0].text
            logger.info(f"✅ Agent completed successfully")

            return result

        except Exception as e:
            logger.error(f"❌ Agent execution failed: {e}")
            raise

    def update_context(self, new_context: str) -> None:
        """Update the context."""
        self.context = new_context
        logger.info("🔄 Agent context updated")

    def __repr__(self) -> str:
        return (
            f"LLMAgent(role={self.role_description[:30]}..., "
            f"model={self.model}, "
            f"temperature={self.temperature})"
        )
