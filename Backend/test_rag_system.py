"""
Test script for RAG system.

Tests:
1. LLM service (Ollama)
2. Search service
3. RAG pipeline end-to-end

Usage:
    python test_rag_system.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.llm_service_groq import get_llm_service
from app.services.search_service import semantic_search
from app.services.rag_service import RAGService
from app.core.database import SessionLocal
from app.models.admin import User
import uuid


def test_llm_service():
    """Test 1: LLM Service"""
    print("\n" + "="*60)
    print("TEST 1: LLM Service")
    print("="*60)
    
    try:
        llm = get_llm_service()
        
        # Check health
        if not llm.check_health():
            print("✗ LLM service is not available!")
            return False
        
        print(f"✓ LLM service is running")
        print(f"✓ Model: {llm.model}")
        
        # Check provider type
        if hasattr(llm, 'base_url'):
            print(f"✓ Provider: Ollama")
            print(f"✓ Base URL: {llm.base_url}")
        else:
            print(f"✓ Provider: Groq")
        
        # List models if available
        try:
            models = llm.list_models()
            if models:
                print(f"✓ Available models: {', '.join(models[:3])}...")
        except:
            pass
        
        # Test generation with legal context
        print("\nTesting response generation...")
        response = llm.generate(
            prompt="What is Section 302 IPC?",
            system_prompt="You are a legal assistant specializing in criminal and insurance law. Answer briefly.",
            max_tokens=100
        )
        print(f"✓ Response generated ({len(response)} chars)")
        print(f"  Preview: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ LLM test failed: {str(e)}")
        return False


def test_search_service():
    """Test 2: Search Service"""
    print("\n" + "="*60)
    print("TEST 2: Search Service")
    print("="*60)
    
    db = SessionLocal()
    try:
        # Test search with criminal law query
        query = "What is the punishment for murder under IPC?"
        print(f"Searching for: '{query}'")
        
        results = semantic_search(
            db=db,
            query=query,
            top_k=3,
            min_similarity=0.0
        )
        
        print(f"✓ Found {len(results)} results")
        
        for i, result in enumerate(results, 1):
            print(f"\n  {i}. {result.title}")
            print(f"     Similarity: {result.similarity:.4f}")
            print(f"     Preview: {result.content[:80]}...")
        
        return len(results) > 0
        
    except Exception as e:
        print(f"✗ Search test failed: {str(e)}")
        return False
    finally:
        db.close()


def test_rag_pipeline():
    """Test 3: Complete RAG Pipeline"""
    print("\n" + "="*60)
    print("TEST 3: RAG Pipeline (End-to-End)")
    print("="*60)
    
    db = SessionLocal()
    try:
        # Get or create test user
        test_user = db.query(User).first()
        if not test_user:
            print("✗ No users in database. Create a user first.")
            return False
        
        print(f"✓ Using user: {test_user.name}")
        
        # Create RAG service
        rag_service = RAGService(db)
        
        # Test query - criminal law related
        query = "What is Section 302 of the Indian Penal Code?"
        print(f"\nQuery: '{query}'")
        print("Processing...")
        
        result = rag_service.query(
            user_query=query,
            user_id=test_user.id,
            top_k=3,
            min_similarity=0.2
        )
        
        print(f"\n✓ Response generated in {result['processing_time_ms']}ms")
        print(f"✓ Model used: {result['model_used']}")
        print(f"✓ Sources: {len(result['sources'])} documents")
        print(f"✓ Conversation ID: {result['conversation_id']}")
        
        print("\n" + "-"*60)
        print("ANSWER:")
        print("-"*60)
        print(result['answer'])
        
        print("\n" + "-"*60)
        print("SOURCES:")
        print("-"*60)
        for i, source in enumerate(result['sources'], 1):
            print(f"{i}. {source['title']} (similarity: {source['similarity']})")
        
        return True
        
    except Exception as e:
        print(f"✗ RAG test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("RAG SYSTEM TEST SUITE")
    print("="*60)
    
    results = {
        "LLM Service": test_llm_service(),
        "Search Service": test_search_service(),
        "RAG Pipeline": test_rag_pipeline()
    }
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! RAG system is ready!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
