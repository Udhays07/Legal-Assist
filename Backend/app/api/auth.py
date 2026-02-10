"""
Authentication and authorization API endpoints.

This module provides REST API endpoints for user authentication, including
login, logout, token refresh, password reset, and account management. It serves
as the security gateway for the application, handling user credentials and
session management with proper security measures.

System Dependencies:
- Depends on: core.security for authentication logic
- Depends on: services.user_service for user operations
- Depends on: schemas.user for request/response validation
- Depended by: All protected API endpoints for authentication
- Depended by: Frontend applications for user authentication
"""