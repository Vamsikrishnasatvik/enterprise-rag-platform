import logging
from dataclasses import dataclass
from typing import Any

from sqlalchemy import or_

from app.db.session import SessionLocal
from app.models.document_chunk import DocumentChunk
from app.services.retrieval.base import BaseRetriever

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

DEFAULT_KEYWORD_SCORE = 1.0

# =============================================================================
# Retrieval Result
# =============================================================================


@dataclass
class KeywordResult:
    """
    Lightweight retrieval result compatible with the
    existing RAG pipeline.
    """

    payload: dict
    score: float


# =============================================================================
# Keyword Retriever
# =============================================================================


class KeywordRetriever(BaseRetriever):
    """
    PostgreSQL keyword retriever.

    Current implementation:
        • ILIKE search

    Future improvements:
        • PostgreSQL Full Text Search
        • BM25
        • Elasticsearch
    """

    def retrieve(
        self,
        query: str,
        limit: int,
        **kwargs: Any,
    ) -> list[KeywordResult]:
        """
        Retrieves document chunks using keyword matching.
        """

        terms = [
            term.strip()
            for term in query.split()
            if term.strip()
        ]

        if not terms:

            logger.info(
                "Keyword retrieval skipped (empty query)."
            )

            return []

        db = SessionLocal()

        try:

            filters = [
                DocumentChunk.content.ilike(
                    f"%{term}%"
                )
                for term in terms
            ]

            chunks = (
                db.query(DocumentChunk)
                .filter(
                    or_(*filters),
                )
                .limit(limit)
                .all()
            )

            results = [
                KeywordResult(
                    payload={
                        "chunk_id": chunk.id,
                        "document_id": chunk.document_id,
                        "content": chunk.content,
                        "metadata": (
                            chunk.chunk_metadata
                            or {}
                        ),
                    },
                    score=DEFAULT_KEYWORD_SCORE,
                )
                for chunk in chunks
            ]

            logger.info(
                (
                    "KeywordRetriever | "
                    "terms=%d | "
                    "retrieved=%d"
                ),
                len(terms),
                len(results),
            )

            return results

        finally:
            db.close()