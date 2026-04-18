"""
Pydantic schemas for authentication — login, register, token, and current-user responses.
"""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Payload for POST /auth/login."""
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    """Payload for POST /auth/register (users only, not admin)."""
    name: str
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Returned on successful login or registration."""
    access_token: str
    token_type: str = "bearer"
    role: str
    name: str
    user_id: str


class MeResponse(BaseModel):
    """Returned by GET /auth/me — DB-verified current user."""
    user_id: str
    name: str
    role: str
    email: str | None = None
