"""
Database configuration and session management for the Legal Assistant backend.

This module sets up the SQLAlchemy engine, session factory, and declarative base for ORM models.
It also provides a dependency function for FastAPI routes to access a database session.

Usage:
    - Import Base in your models to define ORM classes.
    - Use get_db as a dependency in FastAPI endpoints to get a session.
    - The database connection URL is loaded from the .env file.
"""

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Naming convention for constraints so Alembic produces deterministic names
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine for PostgreSQL connection
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a MetaData object with naming convention and declarative Base
metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)

def get_db():
    """
    FastAPI dependency that provides a SQLAlchemy database session.

    Yields:
        db (Session): SQLAlchemy session object.

    Ensures the session is closed after the request is handled.
    Usage example:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
