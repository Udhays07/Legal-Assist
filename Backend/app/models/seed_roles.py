"""
Database seeding script for initial roles.

This script ensures that the 'admin' and 'user' roles exist in the roles table.
It should be run after the initial migration and before application startup.
"""

from app.core.database import SessionLocal
from app.models.admin import Role

# List of roles to seed
INITIAL_ROLES = [
    {"name": "admin"},
    {"name": "user"}
]

def seed_roles():
    """
    Seed the roles table with initial roles if they do not exist.
    """
    session = SessionLocal()
    try:
        for role_data in INITIAL_ROLES:
            exists = session.query(Role).filter_by(name=role_data["name"]).first()
            if not exists:
                session.add(Role(**role_data))
        session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    seed_roles()
    print("Roles seeded successfully.")
