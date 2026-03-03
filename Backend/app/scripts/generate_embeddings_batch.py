"""
Batch script to generate embeddings for existing documents.

This script is useful for:
1. Initial population of embeddings when the feature is first deployed
2. Regenerating embeddings after model changes
3. Fixing missing embeddings for documents

Usage:
    python -m app.scripts.generate_embeddings_batch

Options:
    --force: Regenerate embeddings even if they already exist
    --limit: Process only N documents (for testing)
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.admin import Document, DocumentEmbedding
from app.services.embedding_service import create_or_update_embedding
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_embeddings_for_all_documents(
    force: bool = False,
    limit: int = None
):
    """
    Generate embeddings for all documents in the database.
    
    Args:
        force: If True, regenerate embeddings even if they already exist
        limit: If set, process only this many documents
    """
    db: Session = SessionLocal()
    
    try:
        # Query all non-deleted documents
        query = db.query(Document).filter(Document.deleted_at == None)
        
        if limit:
            query = query.limit(limit)
        
        documents = query.all()
        total_docs = len(documents)
        
        logger.info(f"Found {total_docs} documents to process")
        
        if total_docs == 0:
            logger.info("No documents found. Exiting.")
            return
        
        success_count = 0
        skip_count = 0
        error_count = 0
        
        for idx, doc in enumerate(documents, 1):
            try:
                # Check if embedding already exists
                existing_embedding = db.query(DocumentEmbedding).filter(
                    DocumentEmbedding.document_id == doc.id
                ).first()
                
                if existing_embedding and not force:
                    logger.info(f"[{idx}/{total_docs}] Skipping document {doc.id} - embedding already exists")
                    skip_count += 1
                    continue
                
                # Generate or update embedding
                logger.info(f"[{idx}/{total_docs}] Processing document {doc.id}: {doc.title[:50]}...")
                create_or_update_embedding(db, doc.id, doc.content)
                success_count += 1
                
            except Exception as e:
                logger.error(f"[{idx}/{total_docs}] Failed to process document {doc.id}: {str(e)}")
                error_count += 1
                continue
        
        logger.info("=" * 60)
        logger.info("Batch processing complete!")
        logger.info(f"Total documents: {total_docs}")
        logger.info(f"Successfully processed: {success_count}")
        logger.info(f"Skipped (already exist): {skip_count}")
        logger.info(f"Errors: {error_count}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Fatal error during batch processing: {str(e)}")
        raise
    finally:
        db.close()


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate embeddings for existing documents"
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Regenerate embeddings even if they already exist'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Process only N documents (for testing)'
    )
    
    args = parser.parse_args()
    
    logger.info("Starting batch embedding generation...")
    logger.info(f"Force regenerate: {args.force}")
    logger.info(f"Limit: {args.limit if args.limit else 'None (process all)'}")
    
    generate_embeddings_for_all_documents(
        force=args.force,
        limit=args.limit
    )


if __name__ == "__main__":
    main()