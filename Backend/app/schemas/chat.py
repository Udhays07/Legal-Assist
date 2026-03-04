"""
Pydantic schemas for RAG and Chat operations.

Defines schemas for:
- RAG queries and responses
- Search queries and results
- Conversation management
- Message feedback
"""

from __future__ import annotations

from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


# RAG Query and Response Schemas
class RAGQuery(BaseModel):
    """Schema for RAG query requests."""
    
    query: str = Field(..., description="User's question or query", min_length=1)
    user_id: UUID = Field(..., description="UUID of the user making the query")
    conversation_id: Optional[UUID] = Field(None, description="Optional conversation ID for context")
    top_k: Optional[int] = Field(5, description="Number of documents to retrieve", ge=1, le=20)
    min_similarity: Optional[float] = Field(0.3, description="Minimum similarity threshold", ge=0.0, le=1.0)
    category_id: Optional[UUID] = Field(None, description="Optional category filter")
    include_sources: Optional[bool] = Field(True, description="Include source documents in response")
    
    model_config = ConfigDict(from_attributes=True)


class SourceDocument(BaseModel):
    """Schema for source document in RAG response."""
    
    id: UUID
    title: str
    content: str
    similarity: float = Field(..., description="Similarity score (0.0 to 1.0)")
    category_id: Optional[UUID] = None
    
    model_config = ConfigDict(from_attributes=True)


class RAGResponse(BaseModel):
    """Schema for RAG query responses."""
    
    answer: str = Field(..., description="Generated answer from LLM")
    sources: Optional[List[SourceDocument]] = Field(None, description="Source documents used")
    conversation_id: UUID = Field(..., description="Conversation ID for follow-up queries")
    message_id: UUID = Field(..., description="Message ID for feedback")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")
    model_used: str = Field(..., description="LLM model name used for generation")
    
    model_config = ConfigDict(from_attributes=True)


# Search Schemas
class SearchQuery(BaseModel):
    """Schema for semantic search requests."""
    
    query: str = Field(..., description="Search query", min_length=1)
    top_k: Optional[int] = Field(5, description="Number of results", ge=1, le=20)
    min_similarity: Optional[float] = Field(0.0, description="Minimum similarity threshold", ge=0.0, le=1.0)
    category_id: Optional[UUID] = Field(None, description="Optional category filter")
    status: Optional[str] = Field("published", description="Document status filter")
    
    model_config = ConfigDict(from_attributes=True)


class SearchResultItem(BaseModel):
    """Schema for individual search result."""
    
    id: UUID
    title: str
    content: str
    similarity: float
    category_id: Optional[UUID] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(from_attributes=True)


class SearchResponse(BaseModel):
    """Schema for search response."""
    
    query: str = Field(..., description="Original query")
    results: List[SearchResultItem]
    total_results: int = Field(..., description="Total number of results")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")
    
    model_config = ConfigDict(from_attributes=True)


# Feedback Schema
class MessageFeedback(BaseModel):
    """Schema for message feedback."""
    
    rating: Optional[int] = Field(None, description="Rating (1-5)", ge=1, le=5)
    feedback: Optional[str] = Field(None, description="Optional feedback text")
    
    model_config = ConfigDict(from_attributes=True)


# Conversation Schemas
class ConversationBase(BaseModel):
    """Base schema for conversation."""
    
    title: Optional[str] = Field(None, description="Conversation title")
    
    model_config = ConfigDict(from_attributes=True)


class ConversationRead(ConversationBase):
    """Schema for reading conversation."""
    
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    message_count: Optional[int] = Field(0, description="Number of messages in conversation")
    
    model_config = ConfigDict(from_attributes=True)


class MessageRead(BaseModel):
    """Schema for reading message."""
    
    id: UUID
    conversation_id: UUID
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str
    sources: Optional[List[Dict[str, Any]]] = None
    rating: Optional[int] = None
    feedback: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ConversationDetail(ConversationRead):
    """Schema for conversation with messages."""
    
    messages: List[MessageRead] = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)