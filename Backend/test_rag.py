from app.core.database import SessionLocal
from app.services.rag_service import RAGService
import uuid

def main():
    db = SessionLocal()
    try:
        rag = RAGService(db)
        res = rag.query(
            user_query='What is corporate law?',
            user_id=uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
        )
        print(res)
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == '__main__':
    main()
