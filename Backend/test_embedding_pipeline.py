"""
Test script to verify the embedding pipeline is working correctly.

This script tests:
1. Model loading
2. Embedding generation
3. Database operations
4. Vector dimensions

Run this after installation to verify everything is set up correctly.

Usage:
    python test_embedding_pipeline.py
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.embedding_service import (
    get_embedding_model,
    generate_embedding,
    create_or_update_embedding,
    delete_embedding
)
from app.core.database import SessionLocal
from app.models.admin import Document, DocumentEmbedding, Category
import uuid
from datetime import datetime


def test_model_loading():
    """Test 1: Verify model can be loaded."""
    print("\n" + "="*60)
    print("TEST 1: Model Loading")
    print("="*60)
    try:
        from app.core.constants import MODEL_NAME
        model = get_embedding_model()
        dimension = model.get_sentence_embedding_dimension()
        print(f"✓ Model loaded successfully")
        print(f"✓ Model name: {MODEL_NAME}")
        print(f"✓ Embedding dimension: {dimension}")
        return True
    except Exception as e:
        print(f"✗ Failed to load model: {str(e)}")
        return False


def test_embedding_generation():
    """Test 2: Verify embedding generation."""
    print("\n" + "="*60)
    print("TEST 2: Embedding Generation")
    print("="*60)
    try:
        test_text = "This is a test document for legal assistant system."
        embedding = generate_embedding(test_text)
        
        print(f"✓ Embedding generated successfully")
        print(f"✓ Embedding dimension: {len(embedding)}")
        print(f"✓ Embedding type: {type(embedding)}")
        print(f"✓ First 5 values: {embedding[:5]}")
        
        # Verify dimension
        if len(embedding) == 768:
            print(f"✓ Correct dimension (768)")
            return True
        else:
            print(f"✗ Wrong dimension: expected 768, got {len(embedding)}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to generate embedding: {str(e)}")
        return False


def test_database_operations():
    """Test 3: Verify database operations."""
    print("\n" + "="*60)
    print("TEST 3: Database Operations")
    print("="*60)
    
    db = SessionLocal()
    test_doc_id = None
    test_category_id = None
    
    try:
        # Create a test category first
        test_category = Category(
            id=uuid.uuid4(),
            title=f"Test Category {datetime.utcnow().timestamp()}",
            description="Test category for embedding pipeline",
            is_active=True
        )
        db.add(test_category)
        db.commit()
        db.refresh(test_category)
        test_category_id = test_category.id
        print(f"✓ Test category created: {test_category_id}")
        
        # Create a test document
        test_doc = Document(
            id=uuid.uuid4(),
            category_id=test_category_id,
            title="Test Document for Embedding",
            content="This is a test document to verify the embedding pipeline works correctly.",
            status="published"
        )
        db.add(test_doc)
        db.commit()
        db.refresh(test_doc)
        test_doc_id = test_doc.id
        print(f"✓ Test document created: {test_doc_id}")
        
        # Create embedding
        embedding = create_or_update_embedding(db, test_doc_id, test_doc.content)
        print(f"✓ Embedding created for document")
        print(f"✓ Embedding updated_at: {embedding.updated_at}")
        
        # Verify embedding exists in database
        db_embedding = db.query(DocumentEmbedding).filter(
            DocumentEmbedding.document_id == test_doc_id
        ).first()
        
        if db_embedding:
            print(f"✓ Embedding found in database")
            print(f"✓ Embedding dimension in DB: {len(db_embedding.embedding)}")
        else:
            print(f"✗ Embedding not found in database")
            return False
        
        # Update embedding
        test_doc.content = "Updated content for testing embedding update."
        updated_embedding = create_or_update_embedding(db, test_doc_id, test_doc.content)
        print(f"✓ Embedding updated successfully")
        
        # Delete embedding
        deleted = delete_embedding(db, test_doc_id)
        if deleted:
            print(f"✓ Embedding deleted successfully")
        else:
            print(f"✗ Failed to delete embedding")
            return False
        
        # Cleanup: Delete test document and category
        db.delete(test_doc)
        db.delete(test_category)
        db.commit()
        print(f"✓ Test data cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ Database operation failed: {str(e)}")
        # Cleanup on error
        if test_doc_id:
            try:
                db.query(DocumentEmbedding).filter(
                    DocumentEmbedding.document_id == test_doc_id
                ).delete()
                db.query(Document).filter(Document.id == test_doc_id).delete()
                if test_category_id:
                    db.query(Category).filter(Category.id == test_category_id).delete()
                db.commit()
            except:
                pass
        return False
    finally:
        db.close()


def test_empty_content():
    """Test 4: Verify error handling for empty content."""
    print("\n" + "="*60)
    print("TEST 4: Error Handling")
    print("="*60)
    try:
        generate_embedding("")
        print(f"✗ Should have raised ValueError for empty content")
        return False
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {str(e)}")
        return True
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("EMBEDDING PIPELINE TEST SUITE")
    print("="*60)
    
    results = {
        "Model Loading": test_model_loading(),
        "Embedding Generation": test_embedding_generation(),
        "Database Operations": test_database_operations(),
        "Error Handling": test_empty_content()
    }
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print("\n" + "="*60)
    print(f"Total: {passed_tests}/{total_tests} tests passed")
    print("="*60)
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Embedding pipeline is ready to use.")
        return 0
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)