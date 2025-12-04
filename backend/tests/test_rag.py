from pinecone import Pinecone
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

index = pinecone_client.Index("chargeback-rag")

def query_rag(query_text, top_k=3):
    """Query the RAG system"""
    # Get embedding for query
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=query_text
    )
    query_embedding = response.data[0].embedding
    
    # Search Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    return results

# Test 1: Find an order
print("=" * 60)
print("TEST 1: Finding order by natural language")
print("=" * 60)
results = query_rag("headphones ordered last week")
for i, match in enumerate(results['matches'], 1):
    print(f"\n{i}. Score: {match['score']:.3f}")
    print(f"   Type: {match['metadata'].get('type')}")
    print(f"   Content: {match['metadata'].get('product', match['metadata'].get('content', 'N/A')[:100])}")

# Test 2: Find a policy
print("\n" + "=" * 60)
print("TEST 2: Finding refund policy")
print("=" * 60)
results = query_rag("what is the refund policy")
for i, match in enumerate(results['matches'], 1):
    print(f"\n{i}. Score: {match['score']:.3f}")
    print(f"   Type: {match['metadata'].get('type')}")
    print(f"   Content: {match['metadata'].get('content', 'N/A')[:150]}")

# Test 3: Find dispute script
print("\n" + "=" * 60)
print("TEST 3: Customer says they never got package")
print("=" * 60)
results = query_rag("customer says they never received their order")
for i, match in enumerate(results['matches'], 1):
    print(f"\n{i}. Score: {match['score']:.3f}")
    print(f"   Type: {match['metadata'].get('type')}")
    print(f"   Content: {match['metadata'].get('content', 'N/A')[:150]}")

# Test 4: Find specific order by charge_id
print("\n" + "=" * 60)
print("TEST 4: Looking up specific charge")
print("=" * 60)
results = query_rag("charge ch_001")
for i, match in enumerate(results['matches'], 1):
    print(f"\n{i}. Score: {match['score']:.3f}")
    print(f"   Charge ID: {match['metadata'].get('charge_id', 'N/A')}")
    print(f"   Product: {match['metadata'].get('product', 'N/A')}")
    print(f"   Customer: {match['metadata'].get('customer', 'N/A')}")