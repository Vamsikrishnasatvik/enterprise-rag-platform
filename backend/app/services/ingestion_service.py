from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.services.document_parser import (
    parse_document,
)
from app.services.chunking_service import (
    chunk_document,
)
from app.services.document_chunk_service import (
    create_document_chunks,
)
from app.services.embedding_service import (
    generate_embeddings,
)
from app.services.vector_service import (
    create_collection,
    upsert_chunks,
)


def process_document(
    db: Session,
    document_id: int,
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id
        )
        .first()
    )

    if not document:
        raise ValueError(
            "Document not found"
        )

    # Prevent accidental re-indexing
    if document.status == "INDEXED":
        return document

    try:
        document.status = "PROCESSING"
        db.commit()
        db.refresh(document)

        # Remove old chunks if this document
        # is being reprocessed
        (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id
                == document.id
            )
            .delete()
        )

        db.commit()

        parsed = parse_document(
            document.storage_path,
            document.file_type,
        )

        chunks = chunk_document(
            parsed
        )

        chunk_records = (
            create_document_chunks(
                db=db,
                document_id=document.id,
                chunks=chunks,
            )
        )

        embeddings = (
            generate_embeddings(
                chunks
            )
        )

        create_collection()

        upsert_chunks(
            chunk_records,
            embeddings,
        )

        document.status = "INDEXED"
        db.commit()
        db.refresh(document)

        return document

    except Exception:
        db.rollback()

        document.status = "FAILED"
        db.commit()
        db.refresh(document)

        raise