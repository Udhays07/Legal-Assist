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
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Backend API System",
    description="Role-based backend system with resource management and intelligent interactions",
    version="1.0.0"
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



# Register routers
app.include_router(category.router)
app.include_router(document.router)


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