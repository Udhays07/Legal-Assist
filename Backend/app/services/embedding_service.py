"""
Embedding service for document vectorization using sentence-transformers.

This service handles the generation and management of document embeddings
for semantic search capabilities. It uses the intfloat/e5-base-v2 model
which produces 768-dimensional vectors with superior retrieval quality.

Key Features:
- Lazy loading of the embedding model (loaded once on first use)
- Automatic embedding generation for document content
- Automatic prefix handling for e5 model (passage: for documents, query: for searches)
- Batch processing support for multiple documents
- Integration with DocumentEmbedding table via SQLAlchemy

System Dependencies:
- Depends on: sentence-transformers for embedding generation
- Depends on: models.admin for DocumentEmbedding ORM
- Depended by: api.document for automatic embedding on create/update

Note: e5-base-v2 requires prefixes for optimal performance:
- Documents: "passage: " prefix (automatically added)
- Search queries: "query: " prefix (must be added by search function)
"""

import logging
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer

from app.models.admin import DocumentEmbedding
from app.core.constants import MODEL_NAME, EMBEDDING_DIMENSION, MODEL_INFO

logger = logging.getLogger(__name__)

# Global model instance (lazy loaded)
_embedding_model: Optional[SentenceTransformer] = None


def get_embedding_model() -> SentenceTransformer:
    """
    Get or initialize the embedding model (singleton pattern).
    
    The model is loaded once and cached for subsequent calls to improve performance.
    
    Returns:
        SentenceTransformer: The loaded embedding model
    """
    global _embedding_model
    if _embedding_model is None:
        logger.info(f"Loading embedding model: {MODEL_NAME}")
        _embedding_model = SentenceTransformer(MODEL_NAME)
        logger.info("Embedding model loaded successfully")
    return _embedding_model


def generate_embedding(text: str, is_query: bool = False) -> List[float]:
    """
    Generate embedding vector for a given text.
    
    For e5-base-v2 model, automatically adds appropriate prefix:
    - Documents: "passage: " prefix
    - Search queries: "query: " prefix
    
    Args:
        text: The text content to embed
        is_query: If True, adds "query: " prefix; if False, adds "passage: " prefix
        
    Returns:
        List[float]: 768-dimensional embedding vector
        
    Raises:
        ValueError: If text is empty
        Exception: If embedding generation fails
    """
    if not text or not text.strip():
        raise ValueError("Cannot generate embedding for empty text")
    
    model = get_embedding_model()
    
    # Add appropriate prefix for e5 model
    if MODEL_INFO.get("requires_prefix", False):
        if is_query:
            prefixed_text = MODEL_INFO["query_prefix"] + text
        else:
            prefixed_text = MODEL_INFO["passage_prefix"] + text
    else:
        prefixed_text = text
    
    # Generate embedding (returns numpy array)
    embedding = model.encode(prefixed_text, convert_to_numpy=True)
    
    # Convert to Python list for database storage
    return embedding.tolist()


def create_or_update_embedding(
    db: Session,
    document_id: UUID,
    content: str
) -> DocumentEmbedding:
    """
    Create or update embedding for a document.
    
    This function generates an embedding for the document content and either
    creates a new DocumentEmbedding record or updates an existing one.
    
    Args:
        db: SQLAlchemy database session
        document_id: UUID of the document
        content: Text content to embed
        
    Returns:
        DocumentEmbedding: The created or updated embedding record
        
    Raises:
        ValueError: If content is empty
        Exception: If embedding generation or database operation fails
    """
    try:
        # Generate embedding (with passage prefix for documents)
        logger.info(f"Generating embedding for document {document_id}")
        embedding_vector = generate_embedding(content, is_query=False)
        
        # Check if embedding already exists
        existing_embedding = db.query(DocumentEmbedding).filter(
            DocumentEmbedding.document_id == document_id
        ).first()
        
        if existing_embedding:
            # Update existing embedding
            logger.info(f"Updating existing embedding for document {document_id}")
            existing_embedding.embedding = embedding_vector
            db.add(existing_embedding)
        else:
            # Create new embedding
            logger.info(f"Creating new embedding for document {document_id}")
            new_embedding = DocumentEmbedding(
                document_id=document_id,
                embedding=embedding_vector
            )
            db.add(new_embedding)
        
        db.commit()
        
        # Refresh to get updated timestamp
        if existing_embedding:
            db.refresh(existing_embedding)
            return existing_embedding
        else:
            db.refresh(new_embedding)
            return new_embedding
            
    except ValueError as e:
        logger.error(f"Validation error for document {document_id}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Failed to create/update embedding for document {document_id}: {str(e)}")
        db.rollback()
        raise


def delete_embedding(db: Session, document_id: UUID) -> bool:
    """
    Delete embedding for a document (called on document soft delete).
    
    Args:
        db: SQLAlchemy database session
        document_id: UUID of the document
        
    Returns:
        bool: True if embedding was deleted, False if not found
    """
    try:
        embedding = db.query(DocumentEmbedding).filter(
            DocumentEmbedding.document_id == document_id
        ).first()
        
        if embedding:
            logger.info(f"Deleting embedding for document {document_id}")
            db.delete(embedding)
            db.commit()
            return True
        else:
            logger.warning(f"No embedding found for document {document_id}")
            return False
            
    except Exception as e:
        logger.error(f"Failed to delete embedding for document {document_id}: {str(e)}")
        db.rollback()
        raise


def batch_generate_embeddings(
    db: Session,
    document_ids_and_contents: List[tuple[UUID, str]]
) -> int:
    """
    Generate embeddings for multiple documents in batch.
    
    Useful for initial population or bulk updates of embeddings.
    
    Args:
        db: SQLAlchemy database session
        document_ids_and_contents: List of (document_id, content) tuples
        
    Returns:
        int: Number of embeddings successfully created/updated
    """
    success_count = 0
    
    for document_id, content in document_ids_and_contents:
        try:
            create_or_update_embedding(db, document_id, content)
            success_count += 1
        except Exception as e:
            logger.error(f"Failed to process document {document_id} in batch: {str(e)}")
            continue
    
    logger.info(f"Batch processing complete: {success_count}/{len(document_ids_and_contents)} successful")
    return success_count