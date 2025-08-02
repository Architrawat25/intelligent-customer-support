import asyncio
from app.ai.semantic_search_service import get_search_service

def test_ai_integration():
    """Test the AI integration"""
    search_service = get_search_service()

    if not search_service.is_available():
        print("AI services not available")
        return

    print("AI services available")

    # Test queries
    test_queries = [
        "I forgot my password",
        "How do I contact support?",
        "What are your hours?",
        "Cancel my subscription",
        "Is my data safe?"
    ]

    for query in test_queries:
        print(f"\n Query: {query}")
        result = search_service.get_best_answer(query)
        print(f"   Confidence: {result['confidence']:.3f}")
        print(f"   Source: {result['source']}")
        print(f"   Answer: {result['answer'][:100]}...")

if __name__ == "__main__":
    test_ai_integration()
