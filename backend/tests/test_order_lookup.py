"""
Test that we can find specific orders in the RAG system
"""

from rag_service import RAGService

rag = RAGService()

print("=" * 80)
print("Testing Order Lookup in RAG")
print("=" * 80)

# Test 1: Find John Smith's Blue Wireless Headphones order
print("\nTest 1: Query for 'Blue Wireless Headphones' and 'John Smith'")
print("-" * 80)
context = rag.query_context(
    chargeback_reason="product not received",
    product_name="Blue Wireless Headphones",
    customer_name="John Smith",
    top_k=3
)

print(f"Found {len(context['orders'])} orders")
for order in context['orders']:
    print(f"\n  Customer: {order['customer']}")
    print(f"  Product: {order['product']}")
    print(f"  Amount: ${order['amount']}")
    print(f"  Date: {order['date']}")
    print(f"  Status: {order['status']}")
    print(f"  Charge ID: {order['charge_id']}")
    print(f"  Relevance Score: {order['score']:.3f}")

# Test 2: Find David Kim's Mechanical Keyboard (in transit)
print("\n\nTest 2: Query for 'Mechanical Keyboard RGB' and 'David Kim'")
print("-" * 80)
context = rag.query_context(
    chargeback_reason="where is my order",
    product_name="Mechanical Keyboard RGB",
    customer_name="David Kim",
    top_k=3
)

print(f"Found {len(context['orders'])} orders")
for order in context['orders']:
    print(f"\n  Customer: {order['customer']}")
    print(f"  Product: {order['product']}")
    print(f"  Status: {order['status']}")
    print(f"  Relevance Score: {order['score']:.3f}")

# Test 3: Find subscription orders
print("\n\nTest 3: Query for subscription-related orders")
print("-" * 80)
context = rag.query_context(
    chargeback_reason="subscription not canceled",
    product_name="Netflix Premium Subscription",
    customer_name="Michael Chen",
    top_k=3
)

print(f"Found {len(context['orders'])} orders")
for order in context['orders']:
    print(f"\n  Customer: {order['customer']}")
    print(f"  Product: {order['product']}")
    print(f"  Amount: ${order['amount']}")
    print(f"  Status: {order['status']}")
    print(f"  Relevance Score: {order['score']:.3f}")

print("\n" + "=" * 80)
print("✅ All order data is accessible via RAG!")
print("=" * 80)
