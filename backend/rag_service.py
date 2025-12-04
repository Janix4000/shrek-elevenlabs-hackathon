"""
RAG (Retrieval-Augmented Generation) service for querying Pinecone
to get relevant context before making phone calls.
"""

import os
from typing import Dict, List, Any
from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI

load_dotenv()


class RAGService:
    """Service for retrieving relevant context from Pinecone."""

    def __init__(self):
        """Initialize Pinecone and OpenAI clients."""
        self.pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.index = self.pinecone_client.Index("chargeback-rag")

    def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding for a text query using OpenAI."""
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    def query_context(
        self,
        chargeback_reason: str,
        product_name: str,
        customer_name: str = "",
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Query Pinecone for relevant context based on chargeback details.

        Args:
            chargeback_reason: The reason for the chargeback
            product_name: The product involved in the dispute
            customer_name: Optional customer name for order lookup
            top_k: Number of results to retrieve

        Returns:
            Dictionary containing relevant policies, scripts, orders, and authority info
        """
        # Create a comprehensive query
        query_text = f"{chargeback_reason} {product_name} {customer_name}"
        query_embedding = self._get_embedding(query_text)

        # Search Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        # Organize results by type
        context = {
            "policies": [],
            "dispute_scripts": [],
            "orders": [],
            "resolution_authority": [],
            "common_confusions": []
        }

        for match in results['matches']:
            metadata = match['metadata']
            result_type = metadata.get('type')

            if result_type == "policy":
                context["policies"].append({
                    "score": match['score'],
                    "policy_type": metadata.get('policy_type'),
                    "content": metadata.get('content')
                })
            elif result_type == "dispute_script":
                context["dispute_scripts"].append({
                    "score": match['score'],
                    "dispute_reason": metadata.get('dispute_reason'),
                    "content": metadata.get('content')
                })
            elif result_type == "order":
                context["orders"].append({
                    "score": match['score'],
                    "charge_id": metadata.get('charge_id'),
                    "customer": metadata.get('customer'),
                    "product": metadata.get('product'),
                    "amount": metadata.get('amount'),
                    "date": metadata.get('date'),
                    "status": metadata.get('status')
                })
            elif result_type == "resolution_authority":
                context["resolution_authority"].append({
                    "score": match['score'],
                    "authority_type": metadata.get('authority_type'),
                    "content": metadata.get('content')
                })
            elif result_type == "common_confusion":
                context["common_confusions"].append({
                    "score": match['score'],
                    "confusion_type": metadata.get('confusion_type'),
                    "content": metadata.get('content')
                })

        return context

    def format_context_for_agent(self, context: Dict[str, Any]) -> str:
        """
        Format the retrieved context into a readable string for the agent.

        Args:
            context: Dictionary of retrieved context from query_context()

        Returns:
            Formatted string to add to agent's knowledge
        """
        formatted_parts = []

        # Add dispute scripts
        if context["dispute_scripts"]:
            formatted_parts.append("## DISPUTE RESOLUTION SCRIPTS")
            for script in context["dispute_scripts"]:
                formatted_parts.append(f"- {script['content']}")

        # Add policies
        if context["policies"]:
            formatted_parts.append("\n## COMPANY POLICIES")
            for policy in context["policies"]:
                formatted_parts.append(f"- {policy['content']}")

        # Add resolution authority
        if context["resolution_authority"]:
            formatted_parts.append("\n## YOUR AUTHORITY TO RESOLVE")
            for auth in context["resolution_authority"]:
                formatted_parts.append(f"- {auth['content']}")

        # Add order details
        if context["orders"]:
            formatted_parts.append("\n## RELEVANT ORDER INFORMATION")
            for order in context["orders"]:
                formatted_parts.append(
                    f"- Order for {order['product']}: ${order['amount']} on {order['date']}, "
                    f"Status: {order['status']}, Customer: {order['customer']}"
                )

        # Add common confusions
        if context["common_confusions"]:
            formatted_parts.append("\n## COMMON CUSTOMER QUESTIONS")
            for confusion in context["common_confusions"]:
                formatted_parts.append(f"- {confusion['content']}")

        return "\n".join(formatted_parts)
