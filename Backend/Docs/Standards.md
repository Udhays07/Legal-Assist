# Python FastAPI Coding Standards

## Table of Contents
1. [General Python Standards](#general-python-standards)
2. [FastAPI Specific Standards](#fastapi-specific-standards)
3. [Code Organization](#code-organization)
4. [Naming Conventions](#naming-conventions)
5. [Type Hints](#type-hints)
6. [Documentation](#documentation)
7. [Error Handling](#error-handling)
8. [Security](#security)
9. [Testing](#testing)
10. [Performance](#performance)

---

## General Python Standards

### PEP 8 Compliance
Follow [PEP 8](https://pep8.org/) style guide for Python code.

**Line Length**
- Maximum line length: 88 characters (Black formatter default)
- For docstrings and comments: 72 characters

**Indentation**
- Use 4 spaces per indentation level
- Never mix tabs and spaces

**Imports**
```python
# Standard library imports
import os
import sys
from typing import List, Optional

# Third-party imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Local application imports
from app.models import User
from app.services import user_service
```

**Import Organization**
1. Standard library imports
2. Related third-party imports
3. Local application/library specific imports
4. Each group separated by a blank line

### Code Formatting
Use **Black** as the code formatter with default settings.

```bash
black .
```

Use **isort** for import sorting:
```bash
isort . --profile black
```

---

## FastAPI Specific Standards

### Application Structure
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance
│   ├── config.py            # Configuration settings
│   ├── dependencies.py      # Shared dependencies
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── users.py
│   │   │   │   ├── items.py
│   │   │   └── router.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   ├── crud/
│   │   ├── __init__.py
│   │   └── user.py
│   └── db/
│       ├── __init__.py
│       ├── base.py
│       └── session.py
├── tests/
├── requirements.txt
└── .env
```

### Router Definition
```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all users with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    return await user_service.get_users(skip=skip, limit=limit)
```

### Dependency Injection
```python
# dependencies.py
from typing import Generator
from sqlalchemy.orm import Session
from app.db.session import SessionLocal


def get_db() -> Generator:
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Validation logic here
    return user
```

---

## Code Organization

### Separation of Concerns

**Models** (Database Models)
```python
# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
```

**Schemas** (Pydantic Models)
```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True
```

**Services** (Business Logic)
```python
# app/services/user_service.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    @staticmethod
    async def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user."""
        # Business logic here
        pass
    
    @staticmethod
    async def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email address."""
        return db.query(User).filter(User.email == email).first()


user_service = UserService()
```

---

## Naming Conventions

### Variables and Functions
- Use `snake_case` for variables, functions, and methods
- Use descriptive names that convey purpose

```python
# Good
user_email = "user@example.com"
total_amount = calculate_total()

# Bad
ue = "user@example.com"
x = calc()
```

### Classes
- Use `PascalCase` for class names
- Use meaningful, noun-based names

```python
# Good
class UserService:
    pass

class EmailValidator:
    pass

# Bad
class userservice:
    pass

class Validate:
    pass
```

### Constants
- Use `UPPER_SNAKE_CASE` for constants
- Define constants at module level

```python
# config.py
DATABASE_URL = "postgresql://user:pass@localhost/db"
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30
```

### Private Methods and Attributes
- Use single leading underscore for internal use

```python
class UserService:
    def _validate_email(self, email: str) -> bool:
        """Internal validation method."""
        pass
    
    def create_user(self, email: str) -> User:
        """Public method."""
        if not self._validate_email(email):
            raise ValueError("Invalid email")
```

---

## Type Hints

### Always Use Type Hints
Type hints improve code readability and enable better IDE support.

```python
from typing import List, Optional, Dict, Any, Union
from datetime import datetime


def get_user(user_id: int) -> Optional[User]:
    """Retrieve user by ID."""
    pass


async def create_users(users: List[UserCreate]) -> List[User]:
    """Create multiple users."""
    pass


def process_data(data: Dict[str, Any]) -> Dict[str, Union[str, int]]:
    """Process data dictionary."""
    pass
```

### Pydantic Models for Request/Response
```python
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    username: str
    age: Optional[int] = None
    
    @validator("age")
    def validate_age(cls, v):
        if v is not None and (v < 0 or v > 150):
            raise ValueError("Age must be between 0 and 150")
        return v


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True
```

---

## Documentation

### Docstrings
Use Google-style docstrings for all public modules, classes, and functions.

```python
def create_user(email: str, password: str, db: Session) -> User:
    """
    Create a new user in the database.
    
    Args:
        email: User's email address
        password: User's plain text password (will be hashed)
        db: Database session
    
    Returns:
        Created user object
    
    Raises:
        ValueError: If email is already registered
        DatabaseError: If database operation fails
    
    Example:
        >>> user = create_user("test@example.com", "password123", db)
        >>> print(user.email)
        test@example.com
    """
    # Implementation
    pass
```

### API Documentation
Use FastAPI's built-in documentation features:

```python
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user account with the provided details.",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid request data"},
        409: {"description": "Email already registered"},
    },
)
async def create_user(user: UserCreate):
    """
    Create a new user with all the information:
    
    - **email**: Valid email address
    - **password**: Minimum 8 characters
    - **username**: Unique username
    """
    pass
```

---

## Error Handling

### Custom Exceptions
```python
# app/exceptions.py
from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )


class EmailAlreadyExistsException(HTTPException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email {email} is already registered"
        )
```

### Exception Handlers
```python
# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


app = FastAPI()


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Log the error
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
```

### Proper Error Raising
```python
from fastapi import HTTPException, status


async def get_user(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user
```

---

## Security

### Password Hashing
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)
```

### Environment Variables
```python
# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
```

### Input Validation
```python
from pydantic import BaseModel, validator, Field
import re


class UserCreate(BaseModel):
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator("email")
    def validate_email(cls, v):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError("Invalid email format")
        return v.lower()
    
    @validator("password")
    def validate_password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v
```

### CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],  # Don't use ["*"] in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

---

## Testing

### Test Structure
```
tests/
├── __init__.py
├── conftest.py           # Pytest fixtures
├── test_api/
│   ├── __init__.py
│   ├── test_users.py
│   └── test_items.py
└── test_services/
    ├── __init__.py
    └── test_user_service.py
```

### Testing Standards
```python
# tests/test_api/test_users.py
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestUserEndpoints:
    """Test suite for user endpoints."""
    
    def test_create_user_success(self):
        """Test successful user creation."""
        response = client.post(
            "/api/v1/users/",
            json={
                "email": "test@example.com",
                "password": "Password123",
                "username": "testuser"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "password" not in data
    
    def test_create_user_duplicate_email(self):
        """Test user creation with duplicate email fails."""
        # First user
        client.post("/api/v1/users/", json={...})
        
        # Duplicate attempt
        response = client.post("/api/v1/users/", json={...})
        assert response.status_code == 409
    
    @pytest.mark.parametrize("invalid_email", [
        "notanemail",
        "@example.com",
        "test@",
        "",
    ])
    def test_create_user_invalid_email(self, invalid_email):
        """Test user creation with invalid emails."""
        response = client.post(
            "/api/v1/users/",
            json={"email": invalid_email, "password": "Password123"}
        )
        assert response.status_code == 422
```

### Fixtures
```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.main import app
from app.dependencies import get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with database override."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

---

## Performance

### Database Queries
```python
# Use select_in_loading for relationships
from sqlalchemy.orm import selectinload

users = db.query(User).options(
    selectinload(User.posts)
).all()

# Use pagination
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()
```

### Async Operations
```python
from asyncio import gather


async def get_user_data(user_id: int):
    """Fetch user data from multiple sources concurrently."""
    user_task = fetch_user(user_id)
    posts_task = fetch_user_posts(user_id)
    comments_task = fetch_user_comments(user_id)
    
    user, posts, comments = await gather(user_task, posts_task, comments_task)
    
    return {
        "user": user,
        "posts": posts,
        "comments": comments
    }
```

### Caching
```python
from functools import lru_cache
from typing import List


@lru_cache(maxsize=128)
def get_settings():
    """Cache settings to avoid repeated file reads."""
    return Settings()


# Use Redis for distributed caching
from redis import Redis
import json

redis_client = Redis(host='localhost', port=6379, db=0)


async def get_user_cached(user_id: int) -> Optional[User]:
    """Get user with Redis caching."""
    cache_key = f"user:{user_id}"
    
    # Try cache first
    cached = redis_client.get(cache_key)
    if cached:
        return User(**json.loads(cached))
    
    # Fetch from database
    user = await fetch_user_from_db(user_id)
    if user:
        redis_client.setex(
            cache_key,
            3600,  # 1 hour TTL
            json.dumps(user.dict())
        )
    
    return user
```

---

## Additional Best Practices

### Logging
```python
import logging
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@router.post("/users/")
async def create_user(user: UserCreate):
    logger.info(f"Creating user with email: {user.email}")
    try:
        result = await user_service.create_user(user)
        logger.info(f"User created successfully: {result.id}")
        return result
    except Exception as e:
        logger.error(f"Failed to create user: {str(e)}", exc_info=True)
        raise
```

### Background Tasks
```python
from fastapi import BackgroundTasks


def send_welcome_email(email: str):
    """Send welcome email to new user."""
    # Email sending logic
    pass


@router.post("/users/")
async def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks
):
    created_user = await user_service.create_user(user)
    background_tasks.add_task(send_welcome_email, created_user.email)
    return created_user
```

### API Versioning
```python
# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import users, items

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])

# app/main.py
from app.api.v1.router import api_router as api_v1_router

app.include_router(api_v1_router, prefix="/api/v1")
```

---

## Tools and Linters

### Required Development Tools
```bash
# Install development dependencies
pip install black isort flake8 mypy pylint pytest pytest-cov
```

### Pre-commit Configuration
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ["--max-line-length=88", "--extend-ignore=E203"]
```

### Makefile Commands
```makefile
.PHONY: format lint test

format:
	black .
	isort . --profile black

lint:
	flake8 app tests
	mypy app
	pylint app

test:
	pytest tests/ -v --cov=app --cov-report=html
```

---

## Conclusion

Following these coding standards ensures:
- Consistent, readable code across the project
- Easier onboarding for new developers
- Reduced bugs through type checking and validation
- Better security practices
- Improved maintainability and scalability

Review and update these standards regularly as the project evolves.