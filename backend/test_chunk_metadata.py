from app.db.session import SessionLocal
from app.models.document_chunk import DocumentChunk

db = SessionLocal()

chunks = (
    db.query(DocumentChunk)
    .filter(DocumentChunk.document_id == 24)
    .limit(3)
    .all()
)

for chunk in chunks:
    print("=" * 80)
    print(chunk.chunk_metadata)

db.close()