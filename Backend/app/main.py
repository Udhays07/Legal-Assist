"""
Main application entry point for the FastAPI backend system.

This module serves as the central hub that bootstraps the entire application,
configures middleware, registers API routes, and sets up the FastAPI instance.
It orchestrates the integration of all system components including authentication,
database connections, and API endpoints.

System Dependencies:
- Depends on: core.config for application settings
- Depends on: core.database for database initialization
- Depends on: api routers for endpoint registration
- Depended by: ASGI server (uvicorn, gunicorn) for application serving
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api import category, document
from app.api import embeddings_health
from app.api import rag
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    Preloads the embedding model on startup for faster first request.
    """
    # Startup: Preload embedding model
    logger.info("🚀 Starting application...")
    logger.info("📦 Preloading embedding model...")
    
    try:
        from app.services.embedding_service import get_embedding_model
        model = get_embedding_model()
        logger.info(f"✓ Embedding model loaded successfully: {model.get_sentence_embedding_dimension()} dimensions")
    except Exception as e:
        logger.error(f"✗ Failed to preload embedding model: {str(e)}")
        logger.warning("⚠️  Model will be loaded on first use")
    
    logger.info("✓ Application startup complete")
    
    yield
    
    # Shutdown: Cleanup if needed
    logger.info("👋 Shutting down application...")


app = FastAPI(
    title="Legal Assistant Backend API",
    description="""
    Complete API for Legal Assistant system with RAG capabilities.
    
    ## Features
    
    * **RAG System**: Intelligent Q&A using Retrieval-Augmented Generation
    * **Document Management**: Upload and manage legal documents with automatic embedding generation
    * **Semantic Search**: Find relevant documents using vector similarity
    * **Conversation History**: Track and manage user conversations
    * **Category Organization**: Organize documents by categories
    
    ## Tech Stack
    
    * FastAPI + PostgreSQL + pgvector
    * Groq LLM (Llama 3.1-8b-instant)
    * E5-base-v2 embeddings (768 dimensions)
    * Sentence Transformers
    
    ## Quick Start
    
    1. Create a category: `POST /categories/`
    2. Upload a document: `POST /documents/`
    3. Ask a question: `POST /rag/query`
    
    ## Documentation
    
    * **Swagger UI**: `/docs` (this page)
    * **ReDoc**: `/redoc`
    * **OpenAPI Spec**: Download from `/openapi.json`
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "API Support",
        "email": "support@legalassist.com",
    },
    license_info={
        "name": "MIT",
    }
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Log validation errors and return them to the client for debugging."""
    content_type = request.headers.get("Content-Type", "Missing")
    logger.error(f"Validation error: {exc.errors()} | Content-Type: {content_type}")
    # Using str() on exc.body is safer than indexing for some linters
    body_str = str(exc.body)
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(), 
            "content_type": content_type,
            "body_preview": body_str
        },
    )


from app.api import auth

# Register routers
app.include_router(auth.router)
app.include_router(category.router)
app.include_router(document.router)
app.include_router(embeddings_health.router)
app.include_router(rag.router)


# Minimal CORS for development (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {"status": "healthy"}