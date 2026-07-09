from app.db.session import SessionLocal
from app.models.document_chunk import DocumentChunk

db = SessionLocal()

chunk = (
    db.query(DocumentChunk)
    .first()
)

print("=" * 80)
print(chunk.chunk_metadata)
print("=" * 80)

db.close()