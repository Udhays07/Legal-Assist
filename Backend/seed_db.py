from app.core.database import SessionLocal
from app.models.admin import User, Category, Role
import uuid

def seed():
    db = SessionLocal()
    try:
        role_name = "user"
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name)
            db.add(role)
            db.flush()
            
        mock_user_id = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
        user = db.query(User).filter(User.id == mock_user_id).first()
        if not user:
            user = User(id=mock_user_id, name="Mock User", role_id=role.id)
            db.add(user)
            db.commit()
            print("Mock user created.")
            
        categories = ["Criminal Law", "Civil Rights", "Family Law", "Corporate Law"]
        for cat_str in categories:
            cat = db.query(Category).filter(Category.title == cat_str).first()
            if not cat:
                c = Category(title=cat_str, description=f"Matters related to {cat_str}")
                db.add(c)
        db.commit()
        print("Categories created.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    seed()
