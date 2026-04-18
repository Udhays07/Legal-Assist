"""
Authentication and authorization API endpoints.

Provides REST API endpoints for:
- POST /auth/login     — credential-based login, returns JWT
- POST /auth/register  — user self-registration, returns JWT
- GET  /auth/me        — returns DB-verified current user from Bearer token
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
    get_current_user,
)
from app.models.admin import Role, User
from app.schemas.auth import LoginRequest, MeResponse, RegisterRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# ---------------------------------------------------------------------------
# Fixed admin credentials (the only admin account — not registerable)
# ---------------------------------------------------------------------------
ADMIN_EMAIL = "admin@legalassist.ai"
ADMIN_PASSWORD = "1234"


# ---------------------------------------------------------------------------
# POST /auth/login
# ---------------------------------------------------------------------------

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user or admin with email + password.
    Returns a JWT containing role, name, and user_id.
    """
    # ── Admin fast-path ──────────────────────────────────────────────────
    if payload.email.lower() == ADMIN_EMAIL:
        if payload.password != ADMIN_PASSWORD:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        admin_user = db.query(User).join(Role).filter(
            User.email == ADMIN_EMAIL,
            Role.name == "admin",
            User.deleted_at.is_(None),
        ).first()
        if not admin_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Admin account not found in DB. Run seed_db.py first.",
            )
        token = create_access_token(
            {"sub": str(admin_user.id), "role": "admin", "name": admin_user.name}
        )
        return TokenResponse(
            access_token=token,
            role="admin",
            name=admin_user.name,
            user_id=str(admin_user.id),
        )

    # ── Regular user path ────────────────────────────────────────────────
    user = db.query(User).filter(
        User.email == payload.email.lower(),
        User.deleted_at.is_(None),
    ).first()

    if not user or not user.password_hash or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    role_name = user.role.name if user.role else "user"
    token = create_access_token(
        {"sub": str(user.id), "role": role_name, "name": user.name}
    )
    return TokenResponse(
        access_token=token,
        role=role_name,
        name=user.name,
        user_id=str(user.id),
    )


# ---------------------------------------------------------------------------
# POST /auth/register
# ---------------------------------------------------------------------------

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new regular user account.
    Admin email is reserved and cannot be registered here.
    """
    if payload.email.lower() == ADMIN_EMAIL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is reserved.",
        )

    existing = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    user_role = db.query(Role).filter(Role.name == "user").first()
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User role not found. Run seed_db.py first.",
        )

    new_user = User(
        name=payload.name,
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        role_id=user_role.id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(
        {"sub": str(new_user.id), "role": "user", "name": new_user.name}
    )
    return TokenResponse(
        access_token=token,
        role="user",
        name=new_user.name,
        user_id=str(new_user.id),
    )


# ---------------------------------------------------------------------------
# GET /auth/me
# ---------------------------------------------------------------------------

@router.get("/me", response_model=MeResponse)
def me(current_user: dict = Depends(get_current_user)):
    """
    Return the DB-verified current user.
    Requires a valid Bearer token in the Authorization header.
    """
    return MeResponse(
        user_id=current_user["user_id"],
        name=current_user["name"],
        role=current_user["role"],
        email=current_user.get("email"),
    )