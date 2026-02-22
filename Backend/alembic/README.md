# Alembic (Migrations) — Legal Assistant

This directory contains Alembic migration configuration for the Backend.

## Purpose
- Track and apply database schema changes for the project using Alembic.
- Autogenerate migration scripts from SQLAlchemy models where possible.

## Important notes for this repository
- The project reads the database URL from `DATABASE_URL` in the Backend `.env` file. The Alembic `env.py` is configured to load `.env` and will override the placeholder `sqlalchemy.url` in `alembic.ini`.
- `env.py` also imports the application's SQLAlchemy `Base` (from `app.core.database`) so autogeneration of migrations is enabled.

## Prerequisites
- Virtual environment activated (recommended):

```powershell
cd Backend
.\.venv\Scripts\activate
```

- Install dependencies:

```powershell
pip install -r requirements.txt
```

## Common commands
- Create an autogenerate migration (run from `Backend`):

```powershell
alembic revision --autogenerate -m "initial schema"
```

- Apply all pending migrations:

```powershell
alembic upgrade head
```

- Generate a blank migration to edit by hand:

```powershell
alembic revision -m "manual changes" --autogenerate
```

- Show current revision:

```powershell
alembic current
```

- Stamp the DB with the current head without running migrations (useful for initial setup when DB already matches models):

```powershell
alembic stamp head
```

## Seeding initial data
After applying migrations, seed the initial `roles` rows (`admin`, `user`):

```powershell
# run from Backend directory
python app/models/seed_roles.py
```

(Or run the script via your preferred runner.)

## Troubleshooting
- If Alembic cannot find the DB driver, ensure `DATABASE_URL` is valid and the appropriate DB driver is installed (we use `psycopg2-binary` for PostgreSQL).
- If autogenerate doesn't detect model metadata, confirm `app.core.database.Base` imports correctly and `target_metadata` in `alembic/env.py` is set.

## More info
- Alembic docs: https://alembic.sqlalchemy.org/
- SQLAlchemy migration patterns: follow best practices for managing schema changes in a team environment.
