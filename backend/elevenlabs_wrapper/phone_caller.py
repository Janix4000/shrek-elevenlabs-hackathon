"""
ElevenLabs Phone Caller - Initiate outbound calls to conversational AI agents.
"""

import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from .agent import Agent
from .conversation_manager import ConversationManager

load_dotenv()


class PhoneCaller:
    """Client for making outbound phone calls using ElevenLabs Twilio integration."""

    def __init__(self, api_key: str | None = None, phone_number_id: str | None = None):
        """
        Initialize the PhoneCaller.

        Args:
            api_key: ElevenLabs API key (defaults to ELEVENLABS_API_KEY env var)
            phone_number_id: Phone number ID (defaults to AGENT_PHONE_NUMBER_ID env var)
        """
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        self.phone_number_id = phone_number_id or os.getenv("AGENT_PHONE_NUMBER_ID")

        if not self.api_key:
            raise ValueError(
                "ELEVENLABS_API_KEY must be set in environment variables or passed to constructor."
            )
        if not self.phone_number_id:
            raise ValueError(
                "AGENT_PHONE_NUMBER_ID must be set in environment variables or passed to constructor."
            )

        self.client = ElevenLabs(api_key=self.api_key)
        self.conversation_manager = ConversationManager(api_key=self.api_key)

    def make_call(self, agent: Agent, to_number: str):
        """
        Make an outbound call to a phone number using agent configuration.

        Args:
            agent: Agent configuration with all customization options
            to_number: Phone number to call (format: +1234567890)

        Returns:
            TwilioOutboundCallResponse with call information

        Raises:
            ValueError: If phone_number_id is not configured
            Exception: If the call fails to initiate
        """
        phone_number_id = agent.phone_number_id or self.phone_number_id

        if not phone_number_id:
            raise ValueError(
                "Phone number ID must be configured. "
                "Set agent.phone_number_id or AGENT_PHONE_NUMBER_ID env var."
            )

        print(f"📞 Initiating call to {to_number}...")
        print(f"   Agent ID: {agent.agent_id}")
        print(f"   Phone Number ID: {phone_number_id}")

        # Get conversation config from agent
        conversation_data = agent.to_phone_call_config()
        if conversation_data:
            print(f"   Configuration: {conversation_data}")

        try:
            # Make the outbound call via Twilio
            response = self.client.conversational_ai.twilio.outbound_call(
                agent_id=agent.agent_id,
                agent_phone_number_id=phone_number_id,
                to_number=to_number,
                conversation_initiation_client_data=conversation_data,  # type: ignore
            )

            print(f"✅ Call initiated successfully!")
            if hasattr(response, "conversation_id"):
                print(f"   Conversation ID: {response.conversation_id}")
            if hasattr(response, "call_sid"):
                print(f"   Call SID: {response.call_sid}")

            return response

        except Exception as e:
            print(f"❌ Failed to initiate call: {e}")
            raise

    async def make_call_async(self, agent: Agent, to_number: str):
        """
        Make an async outbound call to a phone number using agent configuration.

        Args:
            agent: Agent configuration with all customization options
            to_number: Phone number to call (format: +1234567890)

        Returns:
            TwilioOutboundCallResponse with call information

        Raises:
            ValueError: If phone_number_id is not configured
        """

        if not self.phone_number_id:
            raise ValueError("Phone number ID must be configured.")

        from elevenlabs.client import AsyncElevenLabs

        async_client = AsyncElevenLabs(api_key=self.api_key)

        conversation_data = agent.to_phone_call_config()

        return await async_client.conversational_ai.twilio.outbound_call(
            agent_id=agent.agent_id,
            agent_phone_number_id=self.phone_number_id,
            to_number=to_number,
            conversation_initiation_client_data=conversation_data,  # type: ignore
        )

    def make_call_and_wait(
        self,
        agent: Agent,
        to_number: str,
        poll_interval: int = 2,
        timeout: int | None = None,
        print_transcript: bool = True,
        verbose: bool = False,
    ):
        """
        Make a call and wait for it to complete, then return the transcript.

        Args:
            agent: Agent configuration with all customization options
            to_number: Phone number to call (format: +1234567890)
            poll_interval: Seconds between status checks (default: 2)
            timeout: Maximum seconds to wait (default: None = no timeout)
            print_transcript: Whether to print the transcript when done (default: True)

        Returns:
            ConversationData with complete transcript

        Raises:
            TimeoutError: If timeout is reached before completion
            Exception: If the call fails
        """
        # Make the call
        response = self.make_call(agent, to_number)

        # Extract conversation_id
        conversation_id = None
        if hasattr(response, "conversation_id"):
            conversation_id = response.conversation_id
        elif isinstance(response, dict):
            conversation_id = response.get("conversation_id")

        if not conversation_id:
            raise ValueError("Could not extract conversation_id from response")

        print(f"\n⏳ Waiting for call to complete...")

        # Wait for completion
        conversation_data = self.conversation_manager.wait_for_completion(
            conversation_id=conversation_id,
            poll_interval=poll_interval,
            timeout=timeout,
            verbose=verbose,
        )

        # Print transcript if requested
        if print_transcript:
            self.conversation_manager.print_transcript(conversation_data)

        return conversation_data

    def get_conversation_transcript(self, conversation_id: str):
        """
        Get the transcript of a completed conversation.

        Args:
            conversation_id: The conversation ID

        Returns:
            ConversationData with transcript
        """
        return self.conversation_manager.get_conversation(conversation_id)
