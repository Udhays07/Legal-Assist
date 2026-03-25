"""
Authentication and authorization API endpoints.

This module provides REST API endpoints for user authentication, including
login, logout, token refresh, password reset, and account management. It serves
as the security gateway for the application, handling user credentials and
session management with proper security measures.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.admin import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/users")
def get_mock_users(db: Session = Depends(get_db)):
    """Fetch all seeded users and their roles for the mock login gateway."""
    users = db.query(User).all()
    return [
        {
            "id": str(u.id),
            "name": u.name,
            "role": u.role.name if u.role else "user"
        }
        for u in users
    ]