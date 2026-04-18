"""
Application constants and configuration values.

This module centralizes all constant values used across the application
to ensure consistency and easy maintenance.
"""

# ============================================================
# Embedding Model Configuration
# ============================================================

MODEL_NAME = "intfloat/e5-base-v2"
EMBEDDING_DIMENSION = 768

# Model Information
MODEL_INFO = {
    "name": MODEL_NAME,
    "dimension": EMBEDDING_DIMENSION,
    "description": "E5-base-v2 model for high-quality semantic embeddings",
    "license": "MIT",
    "size_mb": 411,
    "requires_prefix": True,
    "query_prefix": "query: ",
    "passage_prefix": "passage: ",
}

# ============================================================
# LLM Configuration
# ============================================================

# Default LLM settings
DEFAULT_LLM_TEMPERATURE = 0.7
DEFAULT_LLM_MAX_TOKENS = 2000
DEFAULT_LLM_MODEL = "llama-3.1-8b-instant"  # Groq model

# Ollama settings (if using Ollama instead of Groq)
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_DEFAULT_MODEL = "llama3"

# ============================================================
# RAG Configuration
# ============================================================

# Search settings
RAG_DEFAULT_TOP_K = 5
RAG_DEFAULT_MIN_SIMILARITY = 0.3
RAG_MAX_CONTEXT_LENGTH = 4000

# Content truncation
RAG_CONTEXT_PREVIEW_LENGTH = 500  # Characters per document in context
RAG_SOURCE_CONTENT_LENGTH = 300   # Characters per source in response

# System prompt for RAG
RAG_SYSTEM_PROMPT = """You are a professional legal assistant AI. Your goal is to provide accurate legal information and situational awareness for educational and awareness purposes only.

Guidelines:
1.  **Greetings**: If the user says "hi", "hello", or similar greetings, respond in a friendly, professional, and welcoming manner.
2.  **Legal Awareness**: Provide information about laws, acts, and legal procedures clearly and concisely.
3.  **No Advice**: Never provide specific legal advice, suggestions, or recommendations for a particular situation. Always maintain that you are for awareness only.
4.  **Guardrails**: If the user asks about unrelated topics (e.g., sports, cooking, personal questions), politely inform them that you are specialized in legal awareness and cannot answer those questions.
5.  **Professional Tone**: Maintain a helpful, objective, and professional tone at all times."""

# Intent Classification Prompt
INTENT_CLASSIFICATION_PROMPT = """Analyze the user's message and the conversation history to classify the intent into one of the following categories:

- GREETING: The user is saying hi, hello, or other introductory remarks.
- LEGAL_QUERY: The user is asking about laws, acts, legal procedures, or a legal concept.
- CHAT: The user is providing an acknowledgment ("cool", "okay", "thanks", "I see"), making small talk, or continuing a conversation in a natural way.
- OFF_TOPIC: The user is asking about unrelated general topics (e.g., "who is Dhoni?", "how to bake a cake").
- UNWANTED: The user is asking for assistance with illegal activities, how to commit a crime, or how to escape the consequences of a crime (e.g., "how to escape from crime", "how to commit fraud").

Respond with only the category name (GREETING, LEGAL_QUERY, CHAT, OFF_TOPIC, or UNWANTED).

CONVERSATION HISTORY:
{history}

USER MESSAGE:
{query}"""

# User prompt template for RAG (Enhanced with awareness)
RAG_USER_PROMPT_TEMPLATE = """You are a legal awareness assistant. Your task is to answer the user's question using the provided context in a clear, practical, and easy-to-understand manner.

---
LOCAL DATABASE CONTEXT:
{db_context}

---
WEB SEARCH CONTEXT:
{web_context}

---
USER QUESTION: {question}

Instructions:
1. Understand the user's scenario and respond specifically to their situation (not generic explanation).
2. First, briefly explain the situation in simple terms.
3. Then clearly mention the relevant legal rights, acts, or sections (if available).
4. Provide step-by-step actions the user can take.
5. Use simple, non-technical language so that a common person can understand.
6. Do NOT make up laws. Only use information from the provided context.
7. If information is insufficient, say "Based on available information".
8. Include a small "Citations" section referencing the source context (acts, sections, or sources).
9. End the response with:
   "This information is for legal awareness only and not legal advice."

Output Format:
- Explanation:
- Your Rights:
- What You Can Do:
- Citations:
- Disclaimer:
"""

# No results message
RAG_NO_RESULTS_MESSAGE = """I apologize, but I couldn't find any specific information in our database or via web search to answer your question accurately. 

This could be because the topic is very specific or not covered in available legal resources. Please try rephrasing your question or asking a more general legal question."""

# ============================================================
# API Response Configuration
# ============================================================

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Rate limiting (requests per minute)
RATE_LIMIT_PER_MINUTE = 60

# ============================================================
# File Upload Configuration
# ============================================================

# Supported file types
SUPPORTED_FILE_TYPES = [".pdf", ".docx", ".txt"]
MAX_FILE_SIZE_MB = 10

# Content validation
MIN_CONTENT_LENGTH = 50  # Minimum characters for document content
MAX_CONTENT_LENGTH = 1000000  # Maximum characters (1M)

# ============================================================
# Database Configuration
# ============================================================

# Soft delete
SOFT_DELETE_ENABLED = True

# Timestamp format
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# ============================================================
# Logging Configuration
# ============================================================

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"