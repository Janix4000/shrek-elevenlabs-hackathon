"""
Agent Configuration Fetcher - Retrieve agent config from ElevenLabs API.
"""

import os
import httpx
from typing import Any


class AgentConfigFetcher:
    """Fetches agent configuration from ElevenLabs API."""

    def __init__(self, api_key: str | None = None):
        """
        Initialize the AgentConfigFetcher.

        Args:
            api_key: ElevenLabs API key (defaults to ELEVENLABS_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY must be set in environment variables")
        self.base_url = "https://api.elevenlabs.io/v1"

    def get_agent_config(self, agent_id: str) -> dict[str, Any]:
        """
        Get agent configuration from ElevenLabs API.

        Args:
            agent_id: The agent ID to retrieve

        Returns:
            Dict with agent configuration

        Raises:
            httpx.HTTPStatusError: If the API request fails
        """
        url = f"{self.base_url}/convai/agents/{agent_id}"
        headers = {"xi-api-key": self.api_key}

        with httpx.Client() as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

    def get_agent_prompt(self, agent_id: str) -> str:
        """
        Get the agent's base prompt from ElevenLabs API.

        Args:
            agent_id: The agent ID to retrieve

        Returns:
            The agent's configured prompt text

        Raises:
            httpx.HTTPStatusError: If the API request fails
            KeyError: If prompt is not found in config
        """
        config = self.get_agent_config(agent_id)

        # Navigate to the prompt in the config structure
        # Structure: config["conversation_config"]["agent"]["prompt"]["prompt"]
        try:
            prompt = config["conversation_config"]["agent"]["prompt"]["prompt"]
            return prompt
        except (KeyError, TypeError) as e:
            raise KeyError(
                f"Could not find prompt in agent config. "
                f"Config structure: {list(config.keys())}"
            ) from e
