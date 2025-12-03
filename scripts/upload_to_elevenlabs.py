import json
import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
import time

# Load environment variables
load_dotenv()

# Initialize ElevenLabs client
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def create_document_from_json(file_path, doc_name, doc_type):
    """
    Upload a JSON file as a document to ElevenLabs Knowledge Base
    Returns the document ID
    """
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Convert JSON to readable text format for the knowledge base
    if isinstance(data, list):
        content = "\n\n".join([
            f"{doc_type.upper()} {i+1}:\n" +
            "\n".join([f"{k}: {v}" for k, v in item.items()])
            for i, item in enumerate(data)
        ])
    else:
        content = json.dumps(data, indent=2)

    print(f"📄 Uploading {doc_name}...")

    # Create document in knowledge base
    # Note: You'll need to first create these documents via the ElevenLabs dashboard
    # or use the knowledge base API endpoint

    return content

def upload_all_documents():
    """
    Upload all JSON files to ElevenLabs Knowledge Base
    """
    documents = [
        {
            "file": "orders.json",
            "name": "Customer Orders",
            "type": "order"
        },
        {
            "file": "policies.json",
            "name": "Company Policies",
            "type": "policy"
        },
        {
            "file": "dispute_scripts.json",
            "name": "Dispute Resolution Scripts",
            "type": "script"
        },
        {
            "file": "resolution_authority.json",
            "name": "Resolution Authority Guidelines",
            "type": "authority"
        },
        {
            "file": "common_confusions.json",
            "name": "Common Customer Confusions",
            "type": "confusion"
        }
    ]

    print("🚀 Starting upload to ElevenLabs Knowledge Base...\n")

    for doc in documents:
        if os.path.exists(doc["file"]):
            content = create_document_from_json(
                doc["file"],
                doc["name"],
                doc["type"]
            )

            # Save as text file for manual upload to ElevenLabs dashboard
            output_file = f"elevenlabs_kb_{doc['file'].replace('.json', '.txt')}"
            with open(output_file, 'w') as f:
                f.write(content)

            print(f"✅ Saved {output_file} for upload to ElevenLabs\n")
        else:
            print(f"⚠️  {doc['file']} not found, skipping...\n")

    print("\n📋 Next steps:")
    print("1. Go to https://elevenlabs.io/app/conversational-ai")
    print("2. Create or select your Chargeback Shield agent")
    print("3. Navigate to Knowledge Base section")
    print("4. Upload each .txt file generated above")
    print("5. Enable RAG in agent settings")
    print("6. Configure embedding model (e5_mistral_7b_instruct recommended)")

def configure_agent_rag(agent_id):
    """
    Configure an existing ElevenLabs agent to use RAG

    Args:
        agent_id: The ID of your ElevenLabs conversational agent
    """
    print(f"\n🔧 Configuring RAG for agent {agent_id}...")

    try:
        # Get current agent configuration
        agent_config = client.conversational_ai.agents.get(agent_id=agent_id)

        # Enable RAG
        agent_config.agent.prompt.rag = {
            "enabled": True,
            "embedding_model": "e5_mistral_7b_instruct",
            "max_documents_length": 10000,
            "max_distance": 0.5
        }

        # Update agent
        client.conversational_ai.agents.update(
            agent_id=agent_id,
            conversation_config=agent_config.agent
        )

        print("✅ RAG configuration updated successfully!")

    except Exception as e:
        print(f"❌ Error configuring RAG: {e}")
        print("You may need to configure RAG manually in the ElevenLabs dashboard")

if __name__ == "__main__":
    # Step 1: Generate knowledge base documents
    upload_all_documents()

    # Step 2: Optionally configure agent RAG (uncomment and add your agent ID)
    # agent_id = "your-agent-id-here"
    # configure_agent_rag(agent_id)

    print("\n✨ Setup complete!")
