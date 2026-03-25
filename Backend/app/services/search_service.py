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
    Perform semantic search to find relevant documents.
    
    Args:
        db: Database session
        query: User's search query
        top_k: Number of results to return (default: 5)
        min_similarity: Minimum similarity threshold (0.0 to 1.0)
        category_id: Optional filter by category
        status: Optional filter by status (default: "published")
    
    Returns:
        List[SearchResult]: List of search results with similarity scores
    
    Raises:
        ValueError: If query is empty
        Exception: If search fails
    """
    if not query or not query.strip():
        raise ValueError("Search query cannot be empty")
    
    try:
        # Generate query embedding (with "query:" prefix for e5 model)
        logger.info(f"Generating embedding for query: '{query[:50]}...'")
        query_embedding = generate_embedding(query, is_query=True)
        
        # Convert embedding list to PostgreSQL array format string
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"
        
        # Build SQL query - embed the vector directly in SQL since pgvector doesn't support parameterized vectors
        sql_base = f"""
            SELECT 
                d.id,
                d.category_id,
                d.title,
                d.content,
                d.tags,
                d.metadata,
                d.status,
                d.created_at,
                d.updated_at,
                1 - (e.embedding <=> '{embedding_str}'::vector) as similarity
            FROM documents d
            JOIN document_embeddings e ON d.id = e.document_id
            WHERE d.deleted_at IS NULL
        """
        
        # Build WHERE clause conditions
        where_conditions = []
        params = {}
        
        if category_id:
            where_conditions.append("d.category_id = :category_id")
            params["category_id"] = str(category_id)
        
        if status:
            where_conditions.append("d.status = :status")
            params["status"] = status
        
        if min_similarity > 0:
            where_conditions.append(f"(1 - (e.embedding <=> '{embedding_str}'::vector)) >= :min_similarity")
            params["min_similarity"] = min_similarity
        
        # Add WHERE conditions if any
        if where_conditions:
            sql_base += " AND " + " AND ".join(where_conditions)
        
        # Add ORDER BY and LIMIT
        sql_base += f"""
            ORDER BY e.embedding <=> '{embedding_str}'::vector
            LIMIT :top_k
        """
        
        params["top_k"] = top_k
        
        # Create text object
        sql_query = text(sql_base)
        
        # Execute search
        logger.info(f"Executing similarity search (top_k={top_k}, min_similarity={min_similarity})")
        
        try:
            results = db.execute(sql_query, params).fetchall()
        except Exception as pg_err:
            logger.warning("pgvector error, falling back to basic text search.")
            db.rollback()
            
            # Simple fallback SQL without embeddings
            sql_fallback = """
                SELECT 
                    id, category_id, title, content, tags, metadata, status, created_at, updated_at,
                    1.0 as similarity
                FROM documents d
                WHERE deleted_at IS NULL
                AND (title ILIKE :search_term OR content ILIKE :search_term)
            """
            params["search_term"] = f"%{query}%"
            if category_id:
                sql_fallback += " AND category_id = :category_id"
            if status:
                sql_fallback += " AND status = :status"
            sql_fallback += f" LIMIT :top_k"
            
            results = db.execute(text(sql_fallback), params).fetchall()
        
        # Convert to SearchResult objects
        search_results = []
        for row in results:
            # Create a Document object from the row
            doc = Document(
                id=row.id,
                category_id=row.category_id,
                title=row.title,
                content=row.content,
                tags=row.tags,
                metadata_json=row.metadata,
                status=row.status,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            search_results.append(SearchResult(doc, row.similarity))
        
        logger.info(f"Found {len(search_results)} relevant documents")
        
        return search_results
        
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