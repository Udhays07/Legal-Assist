"""
Quick test for insurance law query
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.services.rag_service import RAGService
from app.models.admin import User

# Test query about insurance
query = "What are unfair claims settlement practices?"

db = SessionLocal()
try:
    # Get user
    user = db.query(User).first()
    if not user:
        print("No user found in database")
        sys.exit(1)
    
    # Create RAG service and query
    rag_service = RAGService(db)
    
    print("\n" + "="*60)
    print(f"QUERY: {query}")
    print("="*60)
    print("\nProcessing...")
    
    result = rag_service.query(
        user_query=query,
        user_id=user.id,
        top_k=3,
        min_similarity=0.1
    )
    
    print(f"\n✓ Response generated in {result['processing_time_ms']}ms")
    print(f"✓ Model: {result['model_used']}")
    print(f"✓ Sources: {len(result['sources'])} documents")
    
    print("\n" + "-"*60)
    print("ANSWER:")
    print("-"*60)
    print(result['answer'])
    
    print("\n" + "-"*60)
    print("SOURCES:")
    print("-"*60)
    for i, source in enumerate(result['sources'], 1):
        print(f"{i}. {source['title']} (similarity: {source['similarity']:.4f})")
    
finally:
    db.close()
