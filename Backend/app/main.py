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

from fastapi import FastAPI

app = FastAPI(
    title="Backend API System",
    description="Role-based backend system with resource management and intelligent interactions",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {"status": "healthy"}