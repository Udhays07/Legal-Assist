"""
RAG (Retrieval-Augmented Generation) service.

This service orchestrates the complete RAG pipeline:
1. User query → Embedding
2. Similarity search → Retrieve relevant documents
3. Format context + query → LLM → Generate response

Key Features:
- Complete RAG pipeline
- Conversation management
- Source citation
- Performance tracking
- Error handling

System Dependencies:
- Depends on: search_service for document retrieval
- Depends on: llm_service for response generation
- Depends on: models.chat for conversation storage
- Depended by: api.rag for API endpoints
"""

import logging
import time
from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.services.search_service import semantic_search, SearchResult
from app.services.llm_service_groq import get_llm_service
from app.models.chat import Conversation, Message
from app.models.admin import User
from app.core.constants import (
    RAG_SYSTEM_PROMPT,
    RAG_USER_PROMPT_TEMPLATE,
    RAG_NO_RESULTS_MESSAGE,
    RAG_CONTEXT_PREVIEW_LENGTH,
    RAG_SOURCE_CONTENT_LENGTH,
    DEFAULT_LLM_TEMPERATURE,
    DEFAULT_LLM_MAX_TOKENS,
)

logger = logging.getLogger(__name__)


class RAGService:
    """Service for RAG operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.llm = get_llm_service()
    
    def query(
        self,
        user_query: str,
        user_id: UUID,
        conversation_id: Optional[UUID] = None,
        top_k: int = 5,
        min_similarity: float = 0.3,
        category_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """
        Process a RAG query and generate a response.
        
        Args:
            user_query: The user's question
            user_id: ID of the user making the query
            conversation_id: Optional existing conversation ID
            top_k: Number of documents to retrieve
            min_similarity: Minimum similarity threshold
            category_id: Optional category filter
        
        Returns:
            Dict containing:
                - answer: Generated response
                - sources: List of source documents
                - conversation_id: Conversation ID
                - message_id: Message ID
                - processing_time_ms: Time taken
                - model_used: LLM model name
        """
        start_time = time.time()
        
        try:
            # Step 1: Retrieve relevant documents
            logger.info(f"Processing RAG query: '{user_query[:50]}...'")
            search_results = semantic_search(
                db=self.db,
                query=user_query,
                top_k=top_k,
                min_similarity=min_similarity,
                category_id=category_id
            )
            
            if not search_results:
                logger.warning("No relevant documents found")
                return self._handle_no_results(user_query, user_id, conversation_id)
            
            logger.info(f"Retrieved {len(search_results)} relevant documents")
            
            # Step 2: Format context from retrieved documents
            context = self._format_context(search_results)
            
            # Step 3: Generate response using LLM
            user_prompt = RAG_USER_PROMPT_TEMPLATE.format(
                context=context,
                question=user_query
            )
            
            logger.info("Generating LLM response")
            response = self.llm.generate(
                prompt=user_prompt,
                system_prompt=RAG_SYSTEM_PROMPT,
                temperature=DEFAULT_LLM_TEMPERATURE,
                max_tokens=DEFAULT_LLM_MAX_TOKENS
            )
            
            # Step 4: Save conversation and messages
            conv_id, msg_id = self._save_conversation(
                user_id=user_id,
                conversation_id=conversation_id,
                user_query=user_query,
                assistant_response=response,
                search_results=search_results,
                processing_time_ms=int((time.time() - start_time) * 1000)
            )
            
            # Step 5: Format response
            result = {
                "answer": response,
                "sources": [self._format_source(r) for r in search_results],
                "conversation_id": str(conv_id),
                "message_id": str(msg_id),
                "processing_time_ms": int((time.time() - start_time) * 1000),
                "model_used": self.llm.model,
            }
            
            logger.info(f"RAG query completed in {result['processing_time_ms']}ms")
            return result
            
        except Exception as e:
            logger.error(f"RAG query failed: {str(e)}")
            raise
    
    def _format_context(self, search_results: List[SearchResult]) -> str:
        """
        Format retrieved documents into context string.
        
        Args:
            search_results: List of search results
        
        Returns:
            str: Formatted context
        """
        context_parts = []
        
        for idx, result in enumerate(search_results, 1):
            # Truncate content if too long (use constant)
            content = result.content[:RAG_CONTEXT_PREVIEW_LENGTH]
            if len(result.content) > RAG_CONTEXT_PREVIEW_LENGTH:
                content += "..."
            
            context_parts.append(
                f"Document {idx}: {result.title}\n"
                f"Relevance: {result.similarity:.2%}\n"
                f"Content: {content}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    def _format_source(self, result: SearchResult) -> Dict[str, Any]:
        """
        Format a search result as a source citation.
        
        Args:
            result: Search result
        
        Returns:
            Dict: Formatted source matching SourceDocument schema
        """
        return {
            "id": str(result.id),
            "title": result.title,
            "content": result.content[:RAG_SOURCE_CONTENT_LENGTH] + "..." if len(result.content) > RAG_SOURCE_CONTENT_LENGTH else result.content,
            "similarity": round(result.similarity, 4),
            "category_id": str(result.category_id) if result.category_id else None,
        }
    
    def _save_conversation(
        self,
        user_id: UUID,
        user_query: str,
        assistant_response: str,
        search_results: List[SearchResult],
        conversation_id: Optional[UUID] = None,
        processing_time_ms: int = 0
    ) -> tuple[UUID, UUID]:
        """
        Save conversation and messages to database.
        
        Args:
            user_id: User ID
            user_query: User's question
            assistant_response: Generated response
            search_results: Retrieved documents
            conversation_id: Optional existing conversation
            processing_time_ms: Processing time
        
        Returns:
            tuple: (conversation_id, message_id)
        """
        try:
            # Get or create conversation
            if conversation_id:
                conversation = self.db.query(Conversation).filter(
                    Conversation.id == conversation_id
                ).first()
                if not conversation:
                    raise ValueError(f"Conversation {conversation_id} not found")
            else:
                # Create new conversation with title from first query
                title = user_query[:50] + "..." if len(user_query) > 50 else user_query
                conversation = Conversation(
                    user_id=user_id,
                    title=title
                )
                self.db.add(conversation)
                self.db.flush()  # Get the ID
            
            # Save user message
            user_message = Message(
                conversation_id=conversation.id,
                role="user",
                content=user_query
            )
            self.db.add(user_message)
            
            # Save assistant message with metadata
            retrieved_docs = [
                {
                    "document_id": str(r.id),
                    "title": r.title,
                    "similarity": round(r.similarity, 4)
                }
                for r in search_results
            ]
            
            assistant_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=assistant_response,
                retrieved_documents=retrieved_docs,
                processing_time_ms=processing_time_ms,
                model_used=self.llm.model
            )
            self.db.add(assistant_message)
            
            self.db.commit()
            
            return conversation.id, assistant_message.id
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to save conversation: {str(e)}")
            raise
    
    def _handle_no_results(
        self,
        user_query: str,
        user_id: UUID,
        conversation_id: Optional[UUID]
    ) -> Dict[str, Any]:
        """
        Handle case when no relevant documents are found.
        
        Args:
            user_query: User's question
            user_id: User ID
            conversation_id: Optional conversation ID
        
        Returns:
            Dict: Response indicating no results
        """
        response = RAG_NO_RESULTS_MESSAGE
        
        # Still save the conversation
        conv_id, msg_id = self._save_conversation(
            user_id=user_id,
            conversation_id=conversation_id,
            user_query=user_query,
            assistant_response=response,
            search_results=[],
            processing_time_ms=0
        )
        
        return {
            "answer": response,
            "sources": [],
            "conversation_id": str(conv_id),
            "message_id": str(msg_id),
            "processing_time_ms": 0,
            "model_used": self.llm.model,
        }
    
    def get_conversation_history(
        self,
        conversation_id: UUID,
        user_id: UUID
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history with messages.
        
        Args:
            conversation_id: Conversation ID
            user_id: User ID (for authorization)
        
        Returns:
            List[Dict]: List of messages
        """
        conversation = self.db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
            Conversation.deleted_at == None
        ).first()
        
        if not conversation:
            raise ValueError("Conversation not found")
        
        messages = self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
        
        return [
            {
                "id": str(msg.id),
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
                "sources": msg.retrieved_documents if msg.role == "assistant" else None
            }
            for msg in messages
        ]
    
    def list_conversations(
        self,
        user_id: UUID,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        List user's conversations.
        
        Args:
            user_id: User ID
            limit: Maximum number of conversations
        
        Returns:
            List[Dict]: List of conversations
        """
        conversations = self.db.query(Conversation).filter(
            Conversation.user_id == user_id,
            Conversation.deleted_at == None
        ).order_by(Conversation.updated_at.desc()).limit(limit).all()
        
        return [
            {
                "id": str(conv.id),
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat() if conv.updated_at else None,
                "message_count": len(conv.messages)
            }
            for conv in conversations
        ]