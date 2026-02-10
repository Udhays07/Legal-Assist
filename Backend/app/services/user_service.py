"""
User service layer for user management and authentication operations.

This module implements comprehensive business logic for user management including
account creation, authentication, profile management, session handling, and
security operations. It serves as the primary interface between API routes
and user-related data models with proper security measures.

System Dependencies:
- Depends on: models.user for data access and user entities
- Depends on: core.security for password hashing and token operations
- Depends on: core.database for database session management
- Depended by: API routes (auth, admin) for user operations
- Depended by: Authentication middleware for user validation
"""