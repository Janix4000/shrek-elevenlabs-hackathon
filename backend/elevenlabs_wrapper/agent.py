"""
Agent configuration class for ElevenLabs conversational AI.
"""

from typing import Any, Callable
from dataclasses import dataclass, field
from elevenlabs.conversational_ai.conversation import ConversationInitiationData

# from elevenlabs.types.conversation_config_client_override_input import (
#     AgentConfigOverrideInput,
# )
# from elevenlabs.types.conversation_initiation_client_data_request_input import (
#     ConversationConfigClientOverrideInput,
#     ConversationInitiationClientDataRequestInput,
#     ConversationInitiationClientDataRequestInputDynamicVariablesValue,
# )


@dataclass
class AgentPromptOverride:
    """Override for agent prompt configuration."""

    prompt: str | None = None
    """The system prompt for the agent."""

    llm: str | None = None
    """The LLM model to use."""

    temperature: float | None = None
    """Temperature for LLM generation."""

    max_tokens: int | None = None
    """Maximum tokens for LLM generation."""

    def to_dict(self) -> dict[str, Any] | None:
        """Convert to dictionary for API."""
        result = {}
        if self.prompt is not None:
            result["prompt"] = self.prompt
        if self.llm is not None:
            result["llm"] = self.llm
        if self.temperature is not None:
            result["temperature"] = self.temperature
        if self.max_tokens is not None:
            result["max_tokens"] = self.max_tokens
        return result if result else None


@dataclass
class AgentConfigOverride:
    """
    Agent-specific configuration override.
    Maps to AgentConfigOverrideInput in ElevenLabs API.
    """

    first_message: str | None = None
    """If non-empty, the first message the agent will say."""

    language: str | None = None
    """Language of the agent - used for ASR and TTS."""

    prompt: AgentPromptOverride | None = None
    """The prompt override for the agent."""

    def to_dict(self) -> dict[str, Any] | None:
        """Convert to dictionary for API."""
        result = {}
        if self.first_message is not None:
            result["first_message"] = self.first_message
        if self.language is not None:
            result["language"] = self.language
        if self.prompt is not None:
            prompt_dict = self.prompt.to_dict()
            if prompt_dict:
                result["prompt"] = prompt_dict
        return result if result else None


@dataclass
class Agent:
    """
    Configuration for an ElevenLabs conversational AI agent.

    This class encapsulates all customization options for an agent including
    dynamic variables, configuration overrides, callbacks, and tools.
    """

    # Required: Agent identification
    agent_id: str

    # Optional: User identification
    user_id: str | None = None

    # Dynamic variables for personalization
    dynamic_variables: dict[str, Any] = field(default_factory=dict)

    # Agent configuration override
    agent_override: AgentConfigOverride | None = None

    # Custom LLM extra body parameters
    custom_llm_extra_body: dict[str, Any] | None = None

    # Phone number configuration (for calls)
    phone_number_id: str | None = None

    # Callbacks for conversation events
    callback_agent_response: Callable[[str], None] | None = None
    callback_agent_response_correction: Callable[[str, str], None] | None = None
    callback_user_transcript: Callable[[str], None] | None = None
    callback_latency_measurement: Callable[[int], None] | None = None
    callback_end_session: Callable | None = None

    def add_dynamic_variable(self, key: str, value: Any) -> None:
        """Add or update a dynamic variable."""
        self.dynamic_variables[key] = value

    def set_first_message(self, message: str) -> None:
        """Set the first message the agent will say."""
        if self.agent_override is None:
            self.agent_override = AgentConfigOverride()
        self.agent_override.first_message = message

    def set_language(self, language: str) -> None:
        """Set the language for the agent."""
        if self.agent_override is None:
            self.agent_override = AgentConfigOverride()
        self.agent_override.language = language

    def set_prompt(
        self,
        prompt: str | None = None,
        llm: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> None:
        """Set the prompt override for the agent."""
        if self.agent_override is None:
            self.agent_override = AgentConfigOverride()
        self.agent_override.prompt = AgentPromptOverride(
            prompt=prompt, llm=llm, temperature=temperature, max_tokens=max_tokens
        )

    def to_conversation_config(self) -> ConversationInitiationData | None:
        """
        Convert to ConversationInitiationData format for local conversations.

        Returns:
            Dict suitable for ConversationInitiationData parameter
        """

        if not self.dynamic_variables:
            return None

        return ConversationInitiationData(dynamic_variables=self.dynamic_variables)

    def to_phone_call_config(self) -> dict[str, Any] | None:
        """
        Convert to conversation_initiation_client_data format for phone calls.

        Returns:
            Dict suitable for conversation_initiation_client_data parameter
        """

        # ConversationInitiationClientDataRequestInputDynamicVariablesValue
        # ConversationInitiationClientDataRequestInput()
        # ConversationConfigClientOverrideInput()
        # AgentConfigOverrideInput()
        # ConversationInitiationClientDataRequestInput(
        #     conversation_config_override=ConversationConfigClientOverrideInput(
        #         agent=self.agent_override.to_dict() if self.agent_override else None
        # )

        data: dict[str, Any] = {}

        # Add dynamic variables
        if self.dynamic_variables:
            data["dynamic_variables"] = self.dynamic_variables

        # Add conversation config override with agent settings
        if self.agent_override:
            agent_dict = self.agent_override.to_dict()
            if agent_dict:
                data["conversation_config_override"] = {"agent": agent_dict}

        # Add custom LLM parameters
        if self.custom_llm_extra_body:
            data["custom_llm_extra_body"] = self.custom_llm_extra_body

        # Add user ID
        if self.user_id:
            data["user_id"] = self.user_id

        return data if data else None

    def __repr__(self) -> str:
        return (
            f"Agent(agent_id={self.agent_id!r}, "
            f"user_id={self.user_id!r}, "
            f"variables={len(self.dynamic_variables)}, "
            f"has_override={self.agent_override is not None})"
        )
