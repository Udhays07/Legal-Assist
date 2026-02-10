"""
User API endpoints for interactive content engagement and AI-powered interactions.

This module provides user-facing REST API endpoints for content interaction,
search functionality, AI-powered Q&A, and personalized content recommendations.
It focuses on the end-user experience with content consumption, engagement
tracking, and intelligent assistance features.

System Dependencies:
- Depends on: api.auth for user authentication
- Depends on: services.interaction_service for AI/RAG functionality  
- Depends on: services.resource_service for content access
- Depends on: rag.retriever for semantic search and content retrieval
- Depended by: Frontend applications and client interfaces
- Depended by: Mobile applications and third-party integrations
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db_session
from app.api.auth import get_current_active_user
from app.services.interaction_service import InteractionService
from app.services.resource_service import ResourceService
from app.schemas.user import User
from app.schemas.resource import (
    Resource,
    ResourceList,
    ResourceSearchQuery,
    ResourceSearchResults,
    ResourceInteractionCreate,
    ResourceInteraction
)

router = APIRouter()


# Request/Response schemas for interactions
class ChatMessage(BaseModel):
    """Schema for chat message requests."""
    message: str
    context_resource_ids: Optional[List[int]] = []
    conversation_id: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "message": "What are the key points about contract law?",
                "context_resource_ids": [1, 2, 3],
                "conversation_id": "conv_123"
            }
        }


class ChatResponse(BaseModel):
    """Schema for chat response."""
    response: str
    sources: List[Dict[str, Any]]
    conversation_id: str
    confidence_score: Optional[float] = None
    
    class Config:
        schema_extra = {
            "example": {
                "response": "Contract law involves several key principles...",
                "sources": [
                    {
                        "resource_id": 1,
                        "title": "Contract Law Basics",
                        "relevance_score": 0.95,
                        "excerpt": "Key principles include..."
                    }
                ],
                "conversation_id": "conv_123",
                "confidence_score": 0.87
            }
        }


class RecommendationRequest(BaseModel):
    """Schema for content recommendation requests."""
    query: Optional[str] = None
    categories: Optional[List[str]] = []
    limit: int = 10
    
    class Config:
        schema_extra = {
            "example": {
                "query": "contract negotiation tips",
                "categories": ["legal", "business"],
                "limit": 5
            }
        }


class ContentRecommendation(BaseModel):
    """Schema for content recommendations."""
    resource: Resource
    relevance_score: float
    reason: str
    
    class Config:
        schema_extra = {
            "example": {
                "resource": "...",
                "relevance_score": 0.92,
                "reason": "Based on your recent activity and interests"
            }
        }


# Content Discovery and Search
@router.get("/resources", response_model=ResourceList)
async def list_available_resources(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=50, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    resource_type: Optional[str] = Query(None, description="Filter by type"),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    List available resources for the current user.
    
    Returns published and accessible resources based on user permissions
    and access levels, with filtering and pagination support.
    """
    resource_service = ResourceService(db)
    
    # Build filters based on user access level
    filters = {
        "status": "published",
        "user_role": current_user.role
    }
    
    if category:
        filters["category"] = category
    if resource_type:
        filters["resource_type"] = resource_type
    if tags:
        filters["tags"] = [tag.strip() for tag in tags.split(",")]
    
    resources = await resource_service.list_resources(
        page=page,
        per_page=per_page,
        filters=filters,
        user_context=current_user
    )
    
    return resources


@router.get("/resources/{resource_id}", response_model=Resource)
async def get_resource(
    resource_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a specific resource by ID.
    
    Returns resource details if user has access, and tracks
    the interaction for analytics and recommendations.
    """
    resource_service = ResourceService(db)
    interaction_service = InteractionService(db)
    
    resource = await resource_service.get_by_id(
        resource_id=resource_id,
        user_context=current_user
    )
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found or access denied"
        )
    
    # Track view interaction
    await interaction_service.track_interaction(
        user_id=current_user.id,
        resource_id=resource_id,
        interaction_type="view"
    )
    
    return resource


@router.post("/search", response_model=ResourceSearchResults)
async def search_resources(
    search_query: ResourceSearchQuery,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Perform semantic search across available resources.
    
    Uses both text-based search and semantic similarity to find
    relevant content based on the user's query and access permissions.
    """
    interaction_service = InteractionService(db)
    
    # Perform semantic search with user context
    results = await interaction_service.semantic_search(
        query=search_query.query,
        user_context=current_user,
        filters={
            "resource_type": search_query.resource_type,
            "category": search_query.category,
            "tags": search_query.tags,
            "created_after": search_query.created_after,
            "created_before": search_query.created_before
        }
    )
    
    # Track search interaction
    await interaction_service.track_search(
        user_id=current_user.id,
        query=search_query.query,
        results_count=len(results.results)
    )
    
    return results


# AI-Powered Interactions
@router.post("/chat", response_model=ChatResponse)
async def chat_with_content(
    chat_request: ChatMessage,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Engage in AI-powered conversation with content context.
    
    Uses RAG (Retrieval-Augmented Generation) to provide intelligent
    responses based on available resources and conversation history.
    """
    interaction_service = InteractionService(db)
    
    try:
        response = await interaction_service.generate_response(
            user_id=current_user.id,
            message=chat_request.message,
            context_resource_ids=chat_request.context_resource_ids,
            conversation_id=chat_request.conversation_id
        )
        
        # Track chat interaction
        await interaction_service.track_interaction(
            user_id=current_user.id,
            resource_id=None,
            interaction_type="chat",
            metadata={
                "message_length": len(chat_request.message),
                "context_resources": len(chat_request.context_resource_ids or []),
                "conversation_id": response.conversation_id
            }
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate response: {str(e)}"
        )


@router.get("/recommendations", response_model=List[ContentRecommendation])
async def get_content_recommendations(
    recommendation_request: RecommendationRequest = Depends(),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get personalized content recommendations.
    
    Provides intelligent content suggestions based on user behavior,
    preferences, and similarity to other users with similar interests.
    """
    interaction_service = InteractionService(db)
    
    recommendations = await interaction_service.get_recommendations(
        user_id=current_user.id,
        query=recommendation_request.query,
        categories=recommendation_request.categories,
        limit=recommendation_request.limit
    )
    
    return recommendations


@router.get("/trending", response_model=ResourceList)
async def get_trending_resources(
    days: int = Query(7, ge=1, le=30, description="Number of days to consider"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(10, ge=1, le=20, description="Number of trending items"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get trending resources based on user engagement.
    
    Returns popular content based on views, downloads, ratings,
    and other engagement metrics within the specified timeframe.
    """
    interaction_service = InteractionService(db)
    
    trending = await interaction_service.get_trending_content(
        user_context=current_user,
        days=days,
        category=category,
        limit=limit
    )
    
    return trending


# User Interaction Tracking
@router.post("/interactions", response_model=ResourceInteraction, status_code=status.HTTP_201_CREATED)
async def track_resource_interaction(
    interaction_data: ResourceInteractionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Track user interaction with a resource.
    
    Records user engagement activities like downloads, ratings,
    bookmarks, and other interactions for analytics and recommendations.
    """
    interaction_service = InteractionService(db)
    
    # Verify user has access to the resource
    resource_service = ResourceService(db)
    resource = await resource_service.get_by_id(
        resource_id=interaction_data.resource_id,
        user_context=current_user
    )
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found or access denied"
        )
    
    interaction = await interaction_service.track_interaction(
        user_id=current_user.id,
        resource_id=interaction_data.resource_id,
        interaction_type=interaction_data.interaction_type,
        duration_seconds=interaction_data.duration_seconds,
        rating=interaction_data.rating,
        metadata=interaction_data.metadata
    )
    
    return interaction


@router.get("/interactions/history")
async def get_interaction_history(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=50, description="Items per page"),
    interaction_type: Optional[str] = Query(None, description="Filter by interaction type"),
    days: int = Query(30, ge=1, le=365, description="Number of days to include"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get user's interaction history.
    
    Returns the user's past interactions with resources for
    tracking progress and providing personalized insights.
    """
    interaction_service = InteractionService(db)
    
    history = await interaction_service.get_user_interaction_history(
        user_id=current_user.id,
        page=page,
        per_page=per_page,
        interaction_type=interaction_type,
        days=days
    )
    
    return history


# Bookmarks and Favorites
@router.post("/bookmarks/{resource_id}")
async def bookmark_resource(
    resource_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Bookmark a resource for later access.
    
    Adds resource to user's bookmark list for easy retrieval
    and quick access to frequently used content.
    """
    interaction_service = InteractionService(db)
    
    success = await interaction_service.bookmark_resource(
        user_id=current_user.id,
        resource_id=resource_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found or already bookmarked"
        )
    
    return {"message": "Resource bookmarked successfully"}


@router.delete("/bookmarks/{resource_id}")
async def remove_bookmark(
    resource_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Remove a resource from bookmarks.
    
    Removes the specified resource from user's bookmark list.
    """
    interaction_service = InteractionService(db)
    
    success = await interaction_service.remove_bookmark(
        user_id=current_user.id,
        resource_id=resource_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )
    
    return {"message": "Bookmark removed successfully"}


@router.get("/bookmarks", response_model=ResourceList)
async def get_bookmarks(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=50, description="Items per page"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get user's bookmarked resources.
    
    Returns paginated list of user's bookmarked resources
    with current access permissions applied.
    """
    interaction_service = InteractionService(db)
    
    bookmarks = await interaction_service.get_user_bookmarks(
        user_id=current_user.id,
        page=page,
        per_page=per_page
    )
    
    return bookmarks


# Conversation Management
@router.get("/conversations")
async def get_conversation_history(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=20, description="Items per page"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get user's conversation history.
    
    Returns list of previous AI conversations for continuity
    and context in future interactions.
    """
    interaction_service = InteractionService(db)
    
    conversations = await interaction_service.get_user_conversations(
        user_id=current_user.id,
        page=page,
        per_page=per_page
    )
    
    return conversations


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get messages from a specific conversation.
    
    Returns the complete message history for a conversation,
    allowing users to review previous AI interactions.
    """
    interaction_service = InteractionService(db)
    
    messages = await interaction_service.get_conversation_messages(
        user_id=current_user.id,
        conversation_id=conversation_id
    )
    
    if messages is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )
    
    return messages