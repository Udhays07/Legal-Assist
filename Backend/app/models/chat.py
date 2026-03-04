"""
SQLAlchemy ORM models for chat and user interaction features.

Models:
- Conversation: Chat sessions between users and the RAG system
- Message: Individual messages within conversations
- UserActivity: Track user interactions and analytics

All models use UUID primary keys and timestamp fields for audit.
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Boolean, Float, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class Conversation(Base):
    """
    Conversation model for chat sessions.
    
    Represents a chat session between a user and the RAG system.
    Each conversation can have multiple messages.
    """
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=True)  # Auto-generated from first message
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
    
    # Relationships
    user = relationship("User", backref="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """
    Message model for individual chat messages.
    
    Stores both user queries and system responses within a conversation.
    Includes metadata about retrieved documents and processing time.
    """
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    
    # RAG metadata
    retrieved_documents = Column(JSONB, nullable=True)  # List of document IDs and scores
    processing_time_ms = Column(Integer, nullable=True)  # Time taken to generate response
    model_used = Column(String, nullable=True)  # LLM model name
    tokens_used = Column(Integer, nullable=True)  # Token count (if applicable)
    
    # Feedback
    rating = Column(Integer, nullable=True)  # 1-5 star rating
    feedback = Column(Text, nullable=True)  # User feedback text
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")


class UserActivity(Base):
    """
    User activity tracking for analytics and insights.
    
    Tracks user interactions with the system including:
    - Document views
    - Search queries
    - Chat interactions
    - Feature usage
    """
    __tablename__ = "user_activities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    activity_type = Column(String, nullable=False)  # 'search', 'chat', 'view_document', etc.
    
    # Activity details
    details = Column(JSONB, nullable=True)  # Flexible JSON for activity-specific data
    
    # Context
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=True)
    
    # Metadata
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", backref="activities")
    document = relationship("Document", backref="activities")
    conversation = relationship("Conversation", backref="activities")


class SearchHistory(Base):
    """
    Search history for tracking and improving search quality.
    
    Stores user search queries and results for:
    - Analytics
    - Search quality improvement
    - Popular queries tracking
    """
    __tablename__ = "search_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # Nullable for anonymous
    query = Column(Text, nullable=False)
    
    # Results
    results_count = Column(Integer, nullable=False)
    top_result_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    top_similarity = Column(Float, nullable=True)
    
    # Filters used
    filters = Column(JSONB, nullable=True)  # category_id, status, etc.
    
    # User interaction
    clicked_result_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    clicked_position = Column(Integer, nullable=True)  # Position in results (1-based)
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", backref="search_history")
    top_result = relationship("Document", foreign_keys=[top_result_id])
    clicked_result = relationship("Document", foreign_keys=[clicked_result_id])
