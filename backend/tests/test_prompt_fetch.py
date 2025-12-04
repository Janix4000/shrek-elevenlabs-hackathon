"""
Test fetching agent prompt from ElevenLabs API.
"""

import os
import sys

# Add parent directory to path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from elevenlabs_wrapper.agent_config import AgentConfigFetcher

load_dotenv()


def test_fetch_agent_prompt():
    """Test fetching the agent's base prompt from ElevenLabs."""
    agent_id = os.getenv("AGENT_ID")
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

    if not agent_id:
        print("❌ AGENT_ID not set in .env")
        return

    if not elevenlabs_api_key:
        print("❌ ELEVENLABS_API_KEY not set in .env")
        return

    print(f"🔍 Fetching agent config for: {agent_id}")
    print()

    try:
        fetcher = AgentConfigFetcher()

        # Fetch full config
        print("📥 Fetching full agent config...")
        config = fetcher.get_agent_config(agent_id)
        print(f"✅ Config retrieved")
        print()

        # Extract and display prompt
        print("📥 Fetching agent prompt...")
        prompt = fetcher.get_agent_prompt(agent_id)
        print(f"✅ Prompt retrieved ({len(prompt)} characters)")
        print()

        # Display prompt preview
        print("=" * 60)
        print("AGENT BASE PROMPT PREVIEW")
        print("=" * 60)
        print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        print("=" * 60)
        print()

        # Show what will be appended
        print("📝 During a call, RAG context will be appended to this base prompt")
        print("   Structure: [BASE PROMPT] + [RAG SUPPLEMENTARY INFORMATION]")
        print()
        print("✅ Prompt fetching works correctly!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_fetch_agent_prompt()
