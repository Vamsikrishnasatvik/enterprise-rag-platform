import logging
from dataclasses import dataclass

from sqlalchemy import or_

from app.db.session import SessionLocal
from app.models.document_chunk import DocumentChunk

logger = logging.getLogger(__name__)


@dataclass
class KeywordResult:
    """
    Lightweight retrieval result compatible with the
    existing RAG pipeline.
    """

    payload: dict
    score: float


class KeywordRetriever:
    """
    PostgreSQL keyword retrieval.

    Phase 6.1.2

    Current implementation:
        ILIKE search

    Future:
        PostgreSQL Full Text Search
        BM25
        Elasticsearch
    """

    def retrieve(
        self,
        query: str,
        limit: int,
        **kwargs,
    ):

        db = SessionLocal()

        try:

            terms = [
                term.strip()
                for term in query.split()
                if term.strip()
            ]

            if not terms:
                return []

            filters = [
                DocumentChunk.content.ilike(f"%{term}%")
                for term in terms
            ]

            chunks = (
                db.query(DocumentChunk)
                .filter(or_(*filters))
                .limit(limit)
                .all()
            )

            results = []

            for chunk in chunks:

                results.append(
                    KeywordResult(
                        payload={
                            "chunk_id": chunk.id,
                            "document_id": chunk.document_id,
                            "content": chunk.content,
                            "metadata": chunk.chunk_metadata or {},
                        },
                        score=1.0,   # temporary fixed score
                    )
                )

            logger.info(
                "KeywordRetriever | query='%s' | retrieved=%d",
                query,
                len(results),
            )

            return results

        finally:
            db.close()