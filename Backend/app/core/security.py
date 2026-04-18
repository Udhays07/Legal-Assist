"""
Security utilities: JWT token management, password hashing, and FastAPI auth dependencies.

- create_access_token / decode_access_token  — HS256 JWT via python-jose
- hash_password / verify_password           — bcrypt via passlib
- get_current_user                          — FastAPI dependency (Bearer token → DB user)
- require_admin                             — FastAPI dependency (raises 403 for non-admins)
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db

# ---------------------------------------------------------------------------
# Password hashing (direct bcrypt — avoids passlib/bcrypt version conflicts)
# ---------------------------------------------------------------------------


def hash_password(plain: str) -> str:
    """Return a bcrypt hash of *plain*."""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Return True if *plain* matches *hashed*."""
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


# ---------------------------------------------------------------------------
# JWT
# ---------------------------------------------------------------------------

_bearer_scheme = HTTPBearer(auto_error=False)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a signed JWT.

    *data* must contain at least ``sub`` (user_id as str), ``role``, and ``name``.
    The token expires after *expires_delta* or the default configured minutes.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT.

    Raises ``HTTPException(401)`` on any failure (expired, invalid signature, etc.).
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ---------------------------------------------------------------------------
# FastAPI dependencies
# ---------------------------------------------------------------------------


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
    db: Session = Depends(get_db),
) -> dict:
    """
    FastAPI dependency — extracts Bearer token, decodes it, then verifies
    the user still exists in the DB and the stored role matches the token claim.

    Returns a dict with ``user_id``, ``name``, ``role``, ``email``.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(credentials.credentials)
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    # Lazy import to avoid circular deps
    from app.models.admin import User

    user = db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    db_role = user.role.name if user.role else "user"
    return {
        "user_id": str(user.id),
        "name": user.name,
        "role": db_role,
        "email": user.email,
    }


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """
    FastAPI dependency — raises HTTP 403 if the authenticated user is not an admin.
    Layer on top of ``get_current_user``; use on write/admin-only routes.
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user