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
RAG_SYSTEM_PROMPT = """You are a professional legal assistant AI helping users understand legal documents and contracts.

Your role:
- Answer questions based ONLY on the provided context from legal documents
- Be precise, accurate, and professional
- Use appropriate legal terminology
- Cite specific documents when referencing information
- If the answer is not in the provided context, clearly state "I don't have enough information in the available documents to answer this question."

Guidelines:
- Do not make up information
- Do not provide legal advice (you are an assistant, not a lawyer)
- Be clear and concise
- Use bullet points for clarity when appropriate
- Always maintain professional tone"""

# User prompt template for RAG
RAG_USER_PROMPT_TEMPLATE = """Context from relevant legal documents:

{context}

---

User Question: {question}

Please provide a clear and accurate answer based on the context above. If you reference specific information, mention which document it comes from."""

# No results message
RAG_NO_RESULTS_MESSAGE = """I apologize, but I couldn't find any relevant documents in the database to answer your question. This could mean:

1. The information you're looking for hasn't been added to the system yet
2. Your question might need to be rephrased
3. The topic might not be covered in the available documents

Please try:
- Rephrasing your question
- Using different keywords
- Asking a more general question

Or contact an administrator to add relevant documents to the system."""

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