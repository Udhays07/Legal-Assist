"""
Quick test script for RAG API endpoint.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_rag_query():
    """Test RAG query endpoint."""
    
    print("Testing RAG Query Endpoint...")
    print("=" * 60)
    
    # Test data
    payload = {
        "query": "What is the punishment for murder under IPC?",
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "conversation_id": None,
        "top_k": 5,
        "min_similarity": 0.3,
        "category_id": None,
        "include_sources": True
    }
    
    print(f"\nRequest URL: {BASE_URL}/rag/query")
    print(f"Request Body:")
    print(json.dumps(payload, indent=2))
    print("\nSending request...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/rag/query",
            json=payload,
            timeout=30
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✓ SUCCESS!")
            print("=" * 60)
            print(f"\nAnswer: {data['answer'][:200]}...")
            print(f"\nConversation ID: {data['conversation_id']}")
            print(f"Message ID: {data['message_id']}")
            print(f"Processing Time: {data['processing_time_ms']}ms")
            print(f"Model Used: {data['model_used']}")
            print(f"\nNumber of Sources: {len(data.get('sources', []))}")
            
            if data.get('sources'):
                print("\nTop Source:")
                source = data['sources'][0]
                print(f"  - Title: {source['title']}")
                print(f"  - Similarity: {source['similarity']}")
        else:
            print("\n✗ FAILED!")
            print("=" * 60)
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n✗ CONNECTION ERROR!")
        print("=" * 60)
        print("Make sure the server is running:")
        print("  cd Backend")
        print("  python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")


def test_health():
    """Test health endpoints."""
    
    print("\nTesting Health Endpoints...")
    print("=" * 60)
    
    # Test app health
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"\nApp Health: {response.json()}")
    except Exception as e:
        print(f"App Health Error: {str(e)}")
    
    # Test RAG health
    try:
        response = requests.get(f"{BASE_URL}/rag/health")
        print(f"RAG Health: {response.json()}")
    except Exception as e:
        print(f"RAG Health Error: {str(e)}")


if __name__ == "__main__":
    test_health()
    print("\n")
    test_rag_query()
