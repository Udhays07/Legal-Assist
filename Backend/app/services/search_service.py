"""
Semantic search service for document retrieval.

This service handles similarity search using vector embeddings stored in PostgreSQL
with pgvector. It retrieves the most relevant documents for a given query.

Key Features:
- Cosine similarity search using pgvector
- Configurable top-k results
- Filtering by category, status, etc.
- Relevance scoring

System Dependencies:
- Depends on: embedding_service for query vectorization
- Depends on: models.admin for Document and DocumentEmbedding
- Depended by: rag_service for document retrieval
"""

import logging
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import text, bindparam
from sqlalchemy.types import String, Integer, Float

from app.services.embedding_service import generate_embedding
from app.models.admin import Document

logger = logging.getLogger(__name__)


class SearchResult:
    """Container for search result with document and similarity score."""
    
    def __init__(self, document: Document, similarity: float):
        self.document = document
        self.similarity = similarity
        self.id = document.id
        self.title = document.title
        self.content = document.content
        self.category_id = document.category_id
        self.tags = document.tags
        self.metadata = document.metadata_json
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "id": str(self.id),
            "title": self.title,
            "content": self.content,
            "similarity": round(self.similarity, 4),
            "category_id": str(self.category_id) if self.category_id else None,
            "tags": self.tags,
            "metadata": self.metadata,
        }


def semantic_search(
    db: Session,
    query: str,
    top_k: int = 5,
    min_similarity: float = 0.0,
    category_id: Optional[UUID] = None,
    status: Optional[str] = "published"
) -> List[SearchResult]:
    """
    Perform hybrid search (Vector + Keyword) to find relevant documents.
    Uses Reciprocal Rank Fusion (RRF) to combine results.
    """
    if not query or not query.strip():
        raise ValueError("Search query cannot be empty")
    
    try:
        # 1. Vector Search (Semantic)
        logger.info(f"Generating embedding for query: '{query[:50]}...'")
        query_embedding = generate_embedding(query, is_query=True)
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"
        
        vector_sql = f"""
            SELECT d.id, 1 - (e.embedding <=> '{embedding_str}'::vector) as score
            FROM documents d
            JOIN document_embeddings e ON d.id = e.document_id
            WHERE d.deleted_at IS NULL
            {"AND d.category_id = :category_id" if category_id else ""}
            {"AND d.status = :status" if status else ""}
            ORDER BY e.embedding <=> '{embedding_str}'::vector
            LIMIT :limit
        """
        
        # 2. Keyword Search (Full-Text Search)
        keyword_sql = """
            SELECT d.id, ts_rank_cd(to_tsvector('english', d.title || ' ' || d.content), plainto_tsquery('english', :query)) as score
            FROM documents d
            WHERE d.deleted_at IS NULL
            AND to_tsvector('english', d.title || ' ' || d.content) @@ plainto_tsquery('english', :query)
            {"AND d.category_id = :category_id" if category_id else ""}
            {"AND d.status = :status" if status else ""}
            ORDER BY score DESC
            LIMIT :limit
        """
        
        # Adjust SQL for parameters
        if category_id:
            keyword_sql = keyword_sql.replace('{"AND d.category_id = :category_id" if category_id else ""}', "AND d.category_id = :category_id")
        else:
            keyword_sql = keyword_sql.replace('{"AND d.category_id = :category_id" if category_id else ""}', "")
            
        if status:
            keyword_sql = keyword_sql.replace('{"AND d.status = :status" if status else ""}', "AND d.status = :status")
        else:
            keyword_sql = keyword_sql.replace('{"AND d.status = :status" if status else ""}', "")

        params = {"query": query, "limit": top_k * 2, "category_id": str(category_id) if category_id else None, "status": status}
        
        # Execute both
        vector_results = db.execute(text(vector_sql), params).fetchall()
        keyword_results = db.execute(text(keyword_sql), params).fetchall()
        
        # 3. Reciprocal Rank Fusion (RRF)
        # RRF score = sum(1 / (k + rank))
        k = 60
        scores = {} # doc_id -> rrf_score
        
        for rank, row in enumerate(vector_results, 1):
            scores[row.id] = scores.get(row.id, 0) + (1.0 / (k + rank))
            
        for rank, row in enumerate(keyword_results, 1):
            scores[row.id] = scores.get(row.id, 0) + (1.0 / (k + rank))
            
        # Sort by RRF score
        sorted_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        if not sorted_ids:
            return []
            
        # Fetch actual documents for the top IDs
        doc_ids = [str(item[0]) for item in sorted_ids]
        id_to_rrf = {item[0]: item[1] for item in sorted_ids}
        
        docs = db.query(Document).filter(Document.id.in_(doc_ids)).all()
        
        # Map back to SearchResults and maintain RRF order
        doc_map = {doc.id: doc for doc in docs}
        results = []
        for doc_id, rrf_score in sorted_ids:
            if doc_id in doc_map:
                # We normalize RRF score back to a 0-1 range roughly for UI compatibility
                # Max possible RRF score with 2 lists is 2 * (1/61) ≈ 0.032
                normalized_score = min(rrf_score * 30, 1.0) 
                results.append(SearchResult(doc_map[doc_id], normalized_score))
        
        logger.info(f"Hybrid search found {len(results)} relevant documents using RRF")
        return results
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise


def search_by_category(
    db: Session,
    query: str,
    category_id: UUID,
    top_k: int = 5
) -> List[SearchResult]:
    """
    Search within a specific category.
    
    Args:
        db: Database session
        query: Search query
        category_id: Category to search within
        top_k: Number of results
    
    Returns:
        List[SearchResult]: Search results from the category
    """
    return semantic_search(
        db=db,
        query=query,
        top_k=top_k,
        category_id=category_id
    )


def search_with_filters(
    db: Session,
    query: str,
    filters: Dict[str, Any]
) -> List[SearchResult]:
    """
    Search with custom filters.
    
    Args:
        db: Database session
        query: Search query
        filters: Dictionary of filters (top_k, min_similarity, category_id, status)
    
    Returns:
        List[SearchResult]: Filtered search results
    """
    return semantic_search(
        db=db,
        query=query,
        top_k=filters.get("top_k", 5),
        min_similarity=filters.get("min_similarity", 0.0),
        category_id=filters.get("category_id"),
        status=filters.get("status", "published")
    )


def get_similar_documents(
    db: Session,
    document_id: UUID,
    top_k: int = 5
) -> List[SearchResult]:
    """
    Find documents similar to a given document.
    
    Args:
        db: Database session
        document_id: ID of the reference document
        top_k: Number of similar documents to return
    
    Returns:
        List[SearchResult]: Similar documents
    
    Raises:
        ValueError: If document not found
    """
    # Get the reference document
    doc = db.query(Document).filter(
        Document.id == document_id,
        Document.deleted_at == None
    ).first()
    
    if not doc:
        raise ValueError(f"Document {document_id} not found")
    
    # Use the document's content as the query
    # Note: We use the content directly, not as a query
    # So we pass is_query=False to get the same embedding type
    return semantic_search(
        db=db,
        query=doc.content[:500],  # Use first 500 chars
        top_k=top_k + 1  # +1 because the document itself will be in results
    )[1:]  # Skip the first result (the document itself)