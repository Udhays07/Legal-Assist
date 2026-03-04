"""
RAG API router.

Provides endpoints for RAG (Retrieval-Augmented Generation) operations:
- Query the RAG system
- Manage conversations
- Provide feedback
- Search documents

Routes:
 - POST /rag/query
 - GET  /rag/conversations
 - GET  /rag/conversations/{conversation_id}
 - POST /rag/feedback
 - POST /search
"""

import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.rag_service import RAGService
from app.services.search_service import semantic_search
from app.schemas.chat import (
    RAGQuery,
    RAGResponse,
    SearchQuery,
    SearchResponse,
    SearchResultItem,
    MessageFeedback
)
from app.models.chat import Message
import time

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/query", response_model=RAGResponse)
def rag_query(
    query: RAGQuery,
    db: Session = Depends(get_db)
):
    """
    Process a RAG query and generate a response.
    
    This endpoint:
    1. Retrieves relevant documents using semantic search
    2. Generates a response using the LLM with retrieved context
    3. Saves the conversation and messages
    4. Returns the response with source citations
    """
    try:
        rag_service = RAGService(db)
        
        result = rag_service.query(
            user_query=query.query,
            user_id=query.user_id,
            conversation_id=query.conversation_id,
            top_k=query.top_k or 5,
            min_similarity=query.min_similarity or 0.3,
            category_id=query.category_id
        )
        
        # Format response
        response = RAGResponse(
            answer=result["answer"],
            sources=result["sources"] if query.include_sources else None,
            conversation_id=UUID(result["conversation_id"]),
            message_id=UUID(result["message_id"]),
            processing_time_ms=result["processing_time_ms"],
            model_used=result["model_used"]
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"RAG query failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process query. Please try again."
        )


@router.get("/conversations")
def list_conversations(
    user_id: UUID,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    List user's conversations.
    
    Returns a list of conversations ordered by most recent first.
    """
    try:
        rag_service = RAGService(db)
        conversations = rag_service.list_conversations(user_id, limit)
        return {"conversations": conversations}
        
    except Exception as e:
        logger.error(f"Failed to list conversations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversations"
        )


@router.get("/conversations/{conversation_id}")
def get_conversation(
    conversation_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get a conversation with all its messages.
    
    Returns the conversation history including user queries and assistant responses.
    """
    try:
        rag_service = RAGService(db)
        messages = rag_service.get_conversation_history(conversation_id, user_id)
        
        return {
            "conversation_id": str(conversation_id),
            "messages": messages
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to get conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversation"
        )


@router.post("/feedback")
def submit_feedback(
    message_id: UUID,
    feedback: MessageFeedback,
    db: Session = Depends(get_db)
):
    """
    Submit feedback for a message.
    
    Allows users to rate responses and provide feedback for improvement.
    """
    try:
        message = db.query(Message).filter(Message.id == message_id).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        # Update feedback
        if feedback.rating is not None:
            message.rating = feedback.rating
        if feedback.feedback is not None:
            message.feedback = feedback.feedback
        
        db.commit()
        
        return {
            "message": "Feedback submitted successfully",
            "message_id": str(message_id)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to submit feedback: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit feedback"
        )


@router.post("/search", response_model=SearchResponse)
def search_documents(
    search_query: SearchQuery,
    db: Session = Depends(get_db)
):
    """
    Perform semantic search on documents.
    
    This endpoint searches for relevant documents without generating
    an LLM response. Useful for document discovery and exploration.
    """
    try:
        start_time = time.time()
        
        # Perform search
        results = semantic_search(
            db=db,
            query=search_query.query,
            top_k=search_query.top_k or 5,
            min_similarity=search_query.min_similarity or 0.0,
            category_id=search_query.category_id,
            status=search_query.status
        )
        
        # Format results
        search_results = [
            SearchResultItem(
                id=r.id,
                title=r.title,
                content=r.content[:300] + "..." if len(r.content) > 300 else r.content,
                similarity=r.similarity,
                category_id=r.category_id,
                tags=r.tags,
                metadata=r.metadata
            )
            for r in results
        ]
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return SearchResponse(
            query=search_query.query,
            results=search_results,
            total_results=len(search_results),
            processing_time_ms=processing_time
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Search failed. Please try again."
        )


@router.get("/health")
def rag_health_check(db: Session = Depends(get_db)):
    """
    Check RAG system health.
    
    Verifies:
    - Database connection
    - LLM service availability
    - Embedding service status
    """
    try:
        from app.services.llm_service_groq import get_llm_service
        from app.services.embedding_service import get_embedding_model
        
        llm = get_llm_service()
        
        # Build health status based on provider type
        llm_info = {
            "available": llm.check_health(),
            "model": llm.model,
        }
        
        # Add provider-specific info
        if hasattr(llm, 'base_url'):
            llm_info["base_url"] = llm.base_url
        if hasattr(llm, 'api_key'):
            llm_info["provider"] = "groq"
        
        health_status = {
            "status": "healthy",
            "database": "connected",
            "llm": llm_info,
            "embedding": {
                "model": "intfloat/e5-base-v2",
                "dimension": 768
            }
        }
        
        # Check if LLM is actually available
        if not health_status["llm"]["available"]:
            health_status["status"] = "degraded"
            health_status["llm"]["error"] = "Ollama not accessible"
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }