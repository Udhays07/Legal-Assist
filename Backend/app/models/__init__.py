# Ensure models are imported so SQLAlchemy metadata is populated for Alembic autogenerate
from . import admin  # noqa: F401
from . import chat  # noqa: F401
