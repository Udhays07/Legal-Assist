# Backend API System

A role-based FastAPI backend system designed for knowledge management and intelligent user interactions with support for RAG (Retrieval-Augmented Generation) capabilities.

## Project Overview

This backend system provides a comprehensive foundation for building knowledge-based applications with the following core capabilities:
- **Role-based Access Control**: Admin and user roles with hierarchical permissions
- **Resource Management**: Content and document management with categorization
- **AI-Powered Interactions**: RAG-enabled chatbot and semantic search
- **User Authentication**: JWT-based authentication with session management
- **Extensible Architecture**: Modular design for easy feature additions

## Folder Structure

```
backend/
│
├── app/
│   ├── main.py                    # FastAPI application entry point
│   │
│   ├── core/                      # Core application components
│   │   ├── config.py             # Configuration and environment settings
│   │   ├── database.py           # Database connection and session management
│   │   └── security.py           # Authentication, authorization, and security utilities
│   │
│   ├── models/                    # Database models (SQLAlchemy ORM)
│   │   ├── base.py               # Base model classes and mixins
│   │   ├── user.py               # User and authentication models
│   │   └── resource.py           # Resource and content models
│   │
│   ├── schemas/                   # Pydantic schemas for API validation
│   │   ├── user.py               # User-related request/response schemas
│   │   └── resource.py           # Resource-related request/response schemas
│   │
│   ├── api/                       # API route definitions
"""
Backend — Legal Assistant

Concise documentation for the Backend service (FastAPI + SQLAlchemy).
"""

## Quickstart

1. Create and activate a virtual environment inside `Backend`:

```powershell
cd Backend
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Configure environment variables: copy `.env.example` to `.env` and update `DATABASE_URL`.

4. Run migrations and seed initial data:

```powershell
alembic upgrade head
python -m app.models.seed_roles
```

5. Start the development server:

```powershell
uvicorn app.main:app --reload
```

## Project layout (important files)

- `app/main.py` — FastAPI application entrypoint
- `app/core/database.py` — SQLAlchemy engine, session and Base
- `app/models/` — SQLAlchemy models
- `app/schemas/` — Pydantic request/response schemas
- `app/api/` — API route modules and routers
- `alembic/` — Alembic configuration and migrations
- `requirements.txt` — Python dependencies

## Migrations & Seeding

- Use Alembic for schema changes. Autogenerate with:

```powershell
alembic revision --autogenerate -m "message"
```

- Apply migrations with `alembic upgrade head` and then run the seed script for roles.

## Notes

- Default `DATABASE_URL` is read from `.env`.
- Roles (`admin`, `user`) are seeded by `app.models.seed_roles` and are intended to be immutable at the application level.

If you want, I can:
- Add a `.env.example` file
- Create a small script to automate venv creation, install, migrate and seed
- Add common curl examples for the category/document endpoints
