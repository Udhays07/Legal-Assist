"""
Database seeding script for initial setup.

Seeds:
  - Roles: 'admin' and 'user'
  - Admin account: admin@legalassist.ai / 1234 (bcrypt hashed)
  - Default categories: Criminal Law, Civil Rights, Family Law, Corporate Law

Run this AFTER running 'alembic upgrade head'.
Usage:
    cd Backend
    venv\\Scripts\\python seed_db.py
"""

import sys
import os

# Ensure the Backend directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.admin import Category, Role, User
from app.core.security import hash_password

ADMIN_EMAIL = "admin@legalassist.ai"
ADMIN_PASSWORD = "1234"
ADMIN_NAME = "Administrator"

CATEGORIES = [
    ("Criminal Law", "Matters related to Criminal Law"),
    ("Civil Rights", "Matters related to Civil Rights"),
    ("Family Law", "Matters related to Family Law"),
    ("Corporate Law", "Matters related to Corporate Law"),
    ("Property Law", "Matters related to Property Law"),
    ("Constitutional Law", "Matters related to Constitutional Law"),
]


def seed():
    db = SessionLocal()
    try:
        # ── Roles ─────────────────────────────────────────────────────────
        for role_name in ("admin", "user"):
            if not db.query(Role).filter(Role.name == role_name).first():
                db.add(Role(name=role_name))
        db.flush()
        print("[OK] Roles seeded.")

        # -- Admin account -------------------------------------------------
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        existing_admin = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if not existing_admin:
            admin_user = User(
                name=ADMIN_NAME,
                email=ADMIN_EMAIL,
                password_hash=hash_password(ADMIN_PASSWORD),
                role_id=admin_role.id,
            )
            db.add(admin_user)
            print(f"[OK] Admin account created: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
        else:
            print(f"[--] Admin account already exists: {ADMIN_EMAIL}")

        # -- Categories ----------------------------------------------------
        for title, description in CATEGORIES:
            if not db.query(Category).filter(Category.title == title).first():
                db.add(Category(title=title, description=description))
        print("[OK] Categories seeded.")

        db.commit()
        print("\n[DONE] Database seeding complete.")

    except Exception as e:
        print(f"[ERROR] Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
