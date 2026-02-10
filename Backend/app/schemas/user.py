"""
Pydantic schemas for user-related API request and response validation.

This module defines Pydantic models for validating and serializing user data
in API requests and responses. It provides type safety, automatic validation,
and clear API documentation through schema definitions that separate concerns
between API contracts and database models.

System Dependencies:
- Depends on: models.user for type definitions and validation logic
- Depended by: API routes for request/response validation
- Depended by: Services for data transfer objects
- Depended by: FastAPI for automatic documentation generation
"""