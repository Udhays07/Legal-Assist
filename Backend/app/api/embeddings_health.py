"""
Embeddings Health Check API Router.

Provides endpoints to check the status and health of the embedding service.
Useful for monitoring and debugging.

Routes:
 - GET /embeddings/health - Check if embedding service is operational
 - GET /embeddings/stats - Get statistics about embeddings
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text, func

from app.core.database import get_db
from app.models.admin import Document, DocumentEmbedding
from app.services.embedding_service import get_embedding_model
from app.core.constants import MODEL_NAME, EMBEDDING_DIMENSION

router = APIRouter(prefix="/embeddings", tags=["embeddings"])


@router.get("/health")
def embedding_health_check():
    """
    Check if the embedding service is operational.
    
    Returns:
        - status: "healthy" or "error"
        - model_name: Name of the embedding model
        - model_dimension: Expected embedding dimension
        - model_loaded: Whether the model is currently loaded in memory
    """
    try:
        # Try to get the model (will load if not already loaded)
        model = get_embedding_model()
        model_dimension = model.get_sentence_embedding_dimension()
        
        return {
            "status": "healthy",
            "model_name": MODEL_NAME,
            "expected_dimension": EMBEDDING_DIMENSION,
            "actual_dimension": model_dimension,
            "model_loaded": True,
            "message": "Embedding service is operational"
        }
    except Exception as e:
        return {
            "status": "error",
            "model_name": MODEL_NAME,
            "expected_dimension": EMBEDDING_DIMENSION,
            "model_loaded": False,
            "error": str(e),
            "message": "Embedding service is not operational"
        }


@router.get("/stats")
def embedding_statistics(db: Session = Depends(get_db)):
    """
    Get statistics about document embeddings.
    
    Returns:
        - total_documents: Total number of non-deleted documents
        - documents_with_embeddings: Number of documents that have embeddings
        - documents_without_embeddings: Number of documents missing embeddings
        - coverage_percentage: Percentage of documents with embeddings
        - stale_embeddings: Number of embeddings older than their documents
    """
    try:
        # Total non-deleted documents
        total_docs = db.query(func.count(Document.id)).filter(
            Document.deleted_at == None
        ).scalar()
        
        # Documents with embeddings
        docs_with_embeddings = db.query(func.count(DocumentEmbedding.document_id)).join(
            Document, Document.id == DocumentEmbedding.document_id
        ).filter(
            Document.deleted_at == None
        ).scalar()
        
        # Documents without embeddings
        docs_without_embeddings = total_docs - docs_with_embeddings
        
        # Coverage percentage
        coverage_pct = (docs_with_embeddings / total_docs * 100) if total_docs > 0 else 0
        
        # Stale embeddings (document updated after embedding)
        stale_embeddings = db.query(func.count(Document.id)).join(
            DocumentEmbedding, Document.id == DocumentEmbedding.document_id
        ).filter(
            Document.deleted_at == None,
            Document.updated_at > DocumentEmbedding.updated_at
        ).scalar()
        
        return {
            "status": "success",
            "total_documents": total_docs,
            "documents_with_embeddings": docs_with_embeddings,
            "documents_without_embeddings": docs_without_embeddings,
            "coverage_percentage": round(coverage_pct, 2),
            "stale_embeddings": stale_embeddings,
            "message": f"{coverage_pct:.1f}% of documents have embeddings"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to retrieve embedding statistics"
        }


@router.get("/missing")
def list_documents_without_embeddings(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    List documents that don't have embeddings.
    
    Args:
        limit: Maximum number of documents to return (default: 10)
    
    Returns:
        List of documents without embeddings
    """
    try:
        # Query documents without embeddings
        docs_without_embeddings = db.query(Document).outerjoin(
            DocumentEmbedding, Document.id == DocumentEmbedding.document_id
        ).filter(
            Document.deleted_at == None,
            DocumentEmbedding.document_id == None
        ).limit(limit).all()
        
        result = [
            {
                "id": str(doc.id),
                "title": doc.title,
                "created_at": doc.created_at.isoformat() if doc.created_at else None,
                "content_length": len(doc.content) if doc.content else 0
            }
            for doc in docs_without_embeddings
        ]
        
        return {
            "status": "success",
            "count": len(result),
            "documents": result
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to retrieve documents without embeddings"
        }


@router.get("/stale")
def list_stale_embeddings(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    List documents with stale embeddings (document updated after embedding).
    
    Args:
        limit: Maximum number of documents to return (default: 10)
    
    Returns:
        List of documents with stale embeddings
    """
    try:
        # Query documents with stale embeddings
        stale_docs = db.query(Document, DocumentEmbedding).join(
            DocumentEmbedding, Document.id == DocumentEmbedding.document_id
        ).filter(
            Document.deleted_at == None,
            Document.updated_at > DocumentEmbedding.updated_at
        ).limit(limit).all()
        
        result = [
            {
                "id": str(doc.id),
                "title": doc.title,
                "document_updated_at": doc.updated_at.isoformat() if doc.updated_at else None,
                "embedding_updated_at": embedding.updated_at.isoformat() if embedding.updated_at else None,
                "staleness_seconds": (doc.updated_at - embedding.updated_at).total_seconds() if doc.updated_at and embedding.updated_at else None
            }
            for doc, embedding in stale_docs
        ]
        
        return {
            "status": "success",
            "count": len(result),
            "documents": result
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to retrieve stale embeddings"
        }
