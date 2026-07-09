from app.db.session import SessionLocal
from app.services.ingestion_service import process_document

db = SessionLocal()

process_document(
    db=db,
    document_id=11,
)

db.close()