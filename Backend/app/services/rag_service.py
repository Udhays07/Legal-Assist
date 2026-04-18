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
from app.services.web_search_service import perform_web_search
from app.services.llm_service_groq import get_llm_service
from app.models.chat import Conversation, Message
from app.models.admin import User
from app.core.constants import (
    RAG_SYSTEM_PROMPT,
    RAG_USER_PROMPT_TEMPLATE,
    RAG_NO_RESULTS_MESSAGE,
    INTENT_CLASSIFICATION_PROMPT,
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
            # Step 1: Classify user intent
            logger.info(f"Classifying intent for query: '{user_query[:50]}...'")
            intent = self._classify_intent(user_query, user_id, conversation_id)
            logger.info(f"Detected intent: {intent}")
            
            if intent == "GREETING":
                return self._handle_greeting(user_query, user_id, conversation_id, start_time)
            
            if intent == "CHAT":
                return self._handle_chat(user_query, user_id, conversation_id, start_time)
                
            if intent == "UNWANTED":
                return self._handle_unwanted(user_query, user_id, conversation_id, start_time)
            
            if intent == "OFF_TOPIC":
                return self._handle_off_topic(user_query, user_id, conversation_id, start_time)
            
            # Step 2: Process LEGAL_QUERY (enhanced RAG)
            # 2a: Expand query for better retrieval
            expanded_query = self._expand_query(user_query)
            logger.info(f"Expanded query: '{expanded_query[:100]}...'")
            
            # 2b: Retrieve from local database using hybrid search
            search_results = semantic_search(
                db=self.db,
                query=expanded_query, # Use expanded query for search
                top_k=top_k,
                min_similarity=min_similarity,
                category_id=category_id
            )
            
            # 2c: Perform web search for cross-verification (use original query for web)
            web_results = perform_web_search(user_query, max_results=3)
            
            if not search_results and not web_results:
                logger.warning("No relevant results found in DB or Web")
                return self._handle_no_results(user_query, user_id, conversation_id)
            
            # Step 3: Format contexts
            db_context = self._format_context(search_results) if search_results else "No relevant documents in the local database."
            web_context = self._format_web_context(web_results) if web_results else "No relevant information found on the web."
            
            # Step 4: Generate response using LLM
            user_prompt = RAG_USER_PROMPT_TEMPLATE.format(
                db_context=db_context,
                web_context=web_context,
                question=user_query
            )
            
            logger.info("Generating LLM response for legal query")
            response = self.llm.generate(
                prompt=user_prompt,
                system_prompt=RAG_SYSTEM_PROMPT,
                temperature=DEFAULT_LLM_TEMPERATURE,
                max_tokens=DEFAULT_LLM_MAX_TOKENS
            )
            
            # Step 5: Save conversation and messages
            conv_id, msg_id = self._save_conversation(
                user_id=user_id,
                conversation_id=conversation_id,
                user_query=user_query,
                assistant_response=response,
                search_results=search_results,
                processing_time_ms=int((time.time() - start_time) * 1000)
            )
            
            # Step 6: Format response
            result = {
                "answer": response,
                "sources": [self._format_source(r) for r in search_results],
                "web_sources": web_results,
                "conversation_id": str(conv_id),
                "message_id": str(msg_id),
                "processing_time_ms": int((time.time() - start_time) * 1000),
                "model_used": self.llm.model,
                "intent": intent
            }
            
            logger.info(f"RAG query completed in {result['processing_time_ms']}ms")
            return result
            
        except Exception as e:
            logger.error(f"RAG query failed: {str(e)}")
            raise
    
    def _classify_intent(self, query: str, user_id: UUID, conversation_id: Optional[UUID] = None) -> str:
        """Classify the intent of the user query with history awareness."""
        history_text = "No previous history."
        if conversation_id:
            try:
                history = self.get_conversation_history(conversation_id, user_id)
                # Format last 3 messages for context
                history_parts = []
                for msg in history[-3:]:
                    history_parts.append(f"{msg['role'].upper()}: {msg['content'][:200]}")
                if history_parts:
                    history_text = "\n".join(history_parts)
            except Exception:
                pass

        prompt = INTENT_CLASSIFICATION_PROMPT.format(history=history_text, query=query)
        response = self.llm.generate(
            prompt=prompt,
            temperature=0.0,
            max_tokens=10
        ).strip().upper()
        
        if "GREETING" in response:
            return "GREETING"
        if "CHAT" in response:
            return "CHAT"
        if "UNWANTED" in response:
            return "UNWANTED"
        if "OFF_TOPIC" in response:
            return "OFF_TOPIC"
        return "LEGAL_QUERY"

    def _expand_query(self, query: str) -> str:
        """Expand user query into a more descriptive legal search prompt."""
        expansion_prompt = f"""
        As a legal expert, expand the following short user query into a descriptive search phrase 
        that includes relevant legal keywords, acronyms, and related concepts to improve 
        document retrieval.
        
        User Query: {query}
        
        Expanded Search Phrase (return only the phrase):
        """
        try:
            expanded = self.llm.generate(
                prompt=expansion_prompt,
                temperature=0.3,
                max_tokens=60
            ).strip().strip('"')
            # Combine original and expanded for better coverage
            return f"{query} {expanded}"
        except Exception as e:
            logger.warning(f"Query expansion failed: {str(e)}, falling back to original query")
            return query

    def _handle_greeting(
        self,
        user_query: str,
        user_id: UUID,
        conversation_id: Optional[UUID],
        start_time: float
    ) -> Dict[str, Any]:
        """Handle greeting intent."""
        logger.info("Handling greeting")
        response = self.llm.generate(
            prompt=user_query,
            system_prompt=RAG_SYSTEM_PROMPT,
            temperature=DEFAULT_LLM_TEMPERATURE
        )
        
        conv_id, msg_id = self._save_conversation(
            user_id=user_id,
            conversation_id=conversation_id,
            user_query=user_query,
            assistant_response=response,
            search_results=[],
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
        
        return {
            "answer": response,
            "sources": [],
            "conversation_id": str(conv_id),
            "message_id": str(msg_id),
            "processing_time_ms": int((time.time() - start_time) * 1000),
            "model_used": self.llm.model,
            "intent": "GREETING"
        }

    def _handle_chat(
        self,
        user_query: str,
        user_id: UUID,
        conversation_id: Optional[UUID],
        start_time: float
    ) -> Dict[str, Any]:
        """Handle chat/interactive intent (small talk, acknowledgments)."""
        logger.info("Handling chat")
        response = self.llm.generate(
            prompt=user_query,
            system_prompt="You are a professional legal assistant AI. You can engage in polite small talk, acknowledge feedback, and maintain an interactive dialogue. Keep it brief and professional.",
            temperature=DEFAULT_LLM_TEMPERATURE
        )
        
        conv_id, msg_id = self._save_conversation(
            user_id=user_id,
            conversation_id=conversation_id,
            user_query=user_query,
            assistant_response=response,
            search_results=[],
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
        
        return {
            "answer": response,
            "sources": [],
            "conversation_id": str(conv_id),
            "message_id": str(msg_id),
            "processing_time_ms": int((time.time() - start_time) * 1000),
            "model_used": self.llm.model,
            "intent": "CHAT"
        }

    def _handle_unwanted(
        self,
        user_query: str,
        user_id: UUID,
        conversation_id: Optional[UUID],
        start_time: float
    ) -> Dict[str, Any]:
        """Handle unwanted (illegal/harmful) intent."""
        logger.info("Handling unwanted query")
        response = "I am a professional legal assistant specialized in legal awareness. I cannot assist with requests related to illegal activities or escaping legal consequences. My purpose is to provide general legal knowledge and promote law awareness."
        
        conv_id, msg_id = self._save_conversation(
            user_id=user_id,
            conversation_id=conversation_id,
            user_query=user_query,
            assistant_response=response,
            search_results=[],
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
        
        return {
            "answer": response,
            "sources": [],
            "conversation_id": str(conv_id),
            "message_id": str(msg_id),
            "processing_time_ms": int((time.time() - start_time) * 1000),
            "model_used": self.llm.model,
            "intent": "UNWANTED"
        }

    def _handle_off_topic(
        self,
        user_query: str,
        user_id: UUID,
        conversation_id: Optional[UUID],
        start_time: float
    ) -> Dict[str, Any]:
        """Handle off-topic intent."""
        logger.info("Handling off-topic query")
        response = "I am a professional legal assistant specialized in legal awareness. I can help you understand laws, acts, and legal procedures. I am unable to answer questions unrelated to these topics."
        
        conv_id, msg_id = self._save_conversation(
            user_id=user_id,
            conversation_id=conversation_id,
            user_query=user_query,
            assistant_response=response,
            search_results=[],
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
        
        return {
            "answer": response,
            "sources": [],
            "conversation_id": str(conv_id),
            "message_id": str(msg_id),
            "processing_time_ms": int((time.time() - start_time) * 1000),
            "model_used": self.llm.model,
            "intent": "OFF_TOPIC"
        }

    def _format_web_context(self, web_results: List[Dict[str, Any]]) -> str:
        """Format web search results into context string."""
        context_parts = []
        for idx, result in enumerate(web_results, 1):
            context_parts.append(
                f"Web Source {idx}: {result['title']}\n"
                f"Content: {result['content']}\n"
                f"Link: {result['link']}\n"
            )
        return "\n---\n".join(context_parts)

    def _format_context(self, search_results: List[SearchResult]) -> str:
        """
        Format retrieved documents into context string with enrichment.
        """
        context_parts = []
        
        for idx, result in enumerate(search_results, 1):
            # Get category title if available
            category_info = ""
            if result.document.category:
                category_info = f" | Category: {result.document.category.title}"
            
            # Prepend metadata to content for better grounding
            header = f"[Document {idx}: {result.title}{category_info}]"
            
            # Truncate content if too long
            content = result.content[:RAG_CONTEXT_PREVIEW_LENGTH]
            if len(result.content) > RAG_CONTEXT_PREVIEW_LENGTH:
                content += "..."
            
            context_parts.append(f"{header}\nContent: {content}\n")
        
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