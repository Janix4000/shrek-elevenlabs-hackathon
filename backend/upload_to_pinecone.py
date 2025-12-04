import json
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize clients
pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

index = pinecone_client.Index("chargeback-rag")

def get_embedding(text):
    """Generate embedding using OpenAI"""
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def upload_orders():
    """Upload orders to Pinecone"""
    with open('data/orders.json', 'r') as f:
        orders = json.load(f)
    vectors = []
    for order in orders:
        # Embed the description (natural language)
        embedding = get_embedding(order['description'])
        # Prepare vector
        vectors.append({
            "id": order['id'],
            "values": embedding,
            "metadata": {
                "type": "order",
                "charge_id": order['charge_id'],
                "customer": order['customer'],
                "product": order['product'],
                "amount": order['amount'],
                "date": order['date'],
                "status": order['status']
            }
        })
    # Upload in batch
    index.upsert(vectors=vectors)
    print(f"✅ Uploaded {len(vectors)} orders")

def upload_policies():
    """Upload policies to Pinecone"""
    with open('data/policies.json', 'r') as f:
        policies = json.load(f)
    vectors = []
    for policy in policies:
        embedding = get_embedding(policy['content'])
        vectors.append({
            "id": policy['id'],
            "values": embedding,
            "metadata": {
                "type": "policy",
                "policy_type": policy['type'],
                "content": policy['content']
            }
        })
    index.upsert(vectors=vectors)
    print(f"✅ Uploaded {len(vectors)} policies")

def upload_dispute_scripts():
    """Upload dispute scripts to Pinecone"""
    with open('data/dispute_scripts.json', 'r') as f:
        scripts = json.load(f)
    vectors = []
    for script in scripts:
        embedding = get_embedding(script['content'])
        vectors.append({
            "id": script['id'],
            "values": embedding,
            "metadata": {
                "type": "dispute_script",
                "dispute_reason": script['dispute_reason'],
                "content": script['content']
            }
        })
    index.upsert(vectors=vectors)
    print(f"✅ Uploaded {len(vectors)} dispute scripts")

def upload_resolution_authority():
    """Upload resolution authority to Pinecone"""
    with open('data/resolution_authority.json', 'r') as f:
        authorities = json.load(f)
    vectors = []
    for authority in authorities:
        embedding = get_embedding(authority['content'])
        vectors.append({
            "id": authority['id'],
            "values": embedding,
            "metadata": {
                "type": "resolution_authority",
                "authority_type": authority['type'],
                "content": authority['content']
            }
        })
    index.upsert(vectors=vectors)
    print(f"✅ Uploaded {len(vectors)} resolution authorities")

def upload_common_confusions():
    """Upload common confusions to Pinecone"""
    with open('data/common_confusions.json', 'r') as f:
        confusions = json.load(f)
    vectors = []
    for confusion in confusions:
        embedding = get_embedding(confusion['content'])
        vectors.append({
            "id": confusion['id'],
            "values": embedding,
            "metadata": {
                "type": "common_confusion",
                "confusion_type": confusion['type'],
                "content": confusion['content']
            }
        })
    index.upsert(vectors=vectors)
    print(f"✅ Uploaded {len(vectors)} common confusions")

if __name__ == "__main__":
    print("🚀 Starting upload to Pinecone...")
    upload_orders()
    upload_policies()
    upload_dispute_scripts()
    upload_resolution_authority()
    upload_common_confusions()
    print("✨ All data uploaded successfully!")