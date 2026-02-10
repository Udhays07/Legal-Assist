"""
Interaction service for AI-powered user engagement and RAG functionality.

This module implements business logic for intelligent user interactions including
AI-powered Q&A, semantic search, content recommendations, conversation management,
and user engagement tracking. It serves as the bridge between user requests
and AI/RAG systems while maintaining context and personalization.

System Dependencies:
- Depends on: models.resource for content access and chunking
- Depends on: models.user for user context and preferences  
- Depends on: rag.retriever for semantic search capabilities
- Depends on: rag.embeddings for content understanding
- Depends on: services.resource_service for content management
- Depended by: API routes (user/interaction) for user-facing features
- Depended by: AI agents and chatbot interfaces
"""