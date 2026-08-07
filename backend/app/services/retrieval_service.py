import logging
from collections import OrderedDict
from dataclasses import dataclass

from sqlalchemy import or_

from app.db.session import SessionLocal
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embeddings
from app.services.reranker_service import rerank_results
from app.services.vector_service import client

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

COLLECTION_NAME = "document_chunks"

DEFAULT_KEYWORD_SCORE = 0.50
HYBRID_MULTIPLIER = 2
MIN_KEYWORD_LENGTH = 3

# =============================================================================
# Search Result
# =============================================================================


@dataclass
class SearchResult:
    """
    Standard search result returned by every retrieval strategy.
    """

    score: float
    payload: dict


# =============================================================================
# Semantic Search
# =============================================================================


def semantic_search(
    query: str,
    limit: int,
) -> list[SearchResult]:
    """
    Performs vector similarity search using Qdrant.
    """

    logger.info(
        "Semantic search | query='%s' | limit=%d",
        query,
        limit,
    )

    vector = generate_embeddings([query])[0]

    points = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=limit,
        with_payload=True,
    ).points

    results = []

    for point in points:

        payload = dict(point.payload)

        payload["semantic_score"] = float(point.score)

        results.append(
            SearchResult(
                score=float(point.score),
                payload=payload,
            )
        )

    logger.info(
        "Semantic search returned %d chunk(s).",
        len(results),
    )

    return results


# =============================================================================
# Keyword Search
# =============================================================================


def keyword_search(
    query: str,
    limit: int,
) -> list[SearchResult]:
    """
    Performs PostgreSQL keyword search using ILIKE.
    """

    logger.info(
        "Keyword search | query='%s' | limit=%d",
        query,
        limit,
    )

    db = SessionLocal()

    try:

        words = [
            word.strip()
            for word in query.split()
            if len(word.strip()) >= MIN_KEYWORD_LENGTH
        ]

        if not words:
            return []

        filters = [
            DocumentChunk.content.ilike(f"%{word}%")
            for word in words
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
                SearchResult(
                    score=DEFAULT_KEYWORD_SCORE,
                    payload={
                        "chunk_id": chunk.id,
                        "document_id": chunk.document_id,
                        "content": chunk.content,
                        "keyword_score": DEFAULT_KEYWORD_SCORE,
                    },
                )
            )

        logger.info(
            "Keyword search returned %d chunk(s).",
            len(results),
        )

        return results

    except Exception:

        logger.exception(
            "Keyword search failed."
        )

        return []

    finally:
        db.close()


# =============================================================================
# Merge Results
# =============================================================================


def merge_results(
    semantic_results: list[SearchResult],
    keyword_results: list[SearchResult],
) -> list[SearchResult]:
    """
    Merges semantic and keyword search results while preserving
    semantic and keyword metadata.
    """

    merged = OrderedDict()

    for chunk in semantic_results + keyword_results:

        chunk_id = chunk.payload["chunk_id"]

        if chunk_id not in merged:
            merged[chunk_id] = chunk
            continue

        existing = merged[chunk_id]

        existing.payload.update(
            {
                key: value
                for key, value in chunk.payload.items()
                if key in (
                    "semantic_score",
                    "keyword_score",
                )
            }
        )

        existing.score = max(
            existing.score,
            chunk.score,
        )

    merged_results = sorted(
        merged.values(),
        key=lambda result: result.score,
        reverse=True,
    )

    logger.info(
        "Merged retrieval results | semantic=%d | keyword=%d | merged=%d",
        len(semantic_results),
        len(keyword_results),
        len(merged_results),
    )

    return merged_results


# =============================================================================
# Public Search API
# =============================================================================


def search_chunks(
    query: str,
    limit: int = 3,
    strategy: str = "semantic",
) -> list[SearchResult]:
    """
    Unified retrieval entry point.

    Supported strategies:
        - semantic
        - keyword
        - hybrid
    """

    query = query.strip()

    if not query:
        logger.warning(
            "Empty retrieval query received."
        )
        return []

    strategy = strategy.lower()

    logger.info(
        "Search | strategy=%s | limit=%d | query='%s'",
        strategy,
        limit,
        query,
    )

    # -------------------------------------------------------------------------
    # Semantic Search
    # -------------------------------------------------------------------------

    if strategy == "semantic":

        return semantic_search(
            query=query,
            limit=limit,
        )

    # -------------------------------------------------------------------------
    # Keyword Search
    # -------------------------------------------------------------------------

    elif strategy == "keyword":

        return keyword_search(
            query=query,
            limit=limit,
        )

    # -------------------------------------------------------------------------
    # Hybrid Search
    # -------------------------------------------------------------------------

    elif strategy == "hybrid":

        semantic_results = semantic_search(
            query=query,
            limit=limit * HYBRID_MULTIPLIER,
        )

        keyword_results = keyword_search(
            query=query,
            limit=limit * HYBRID_MULTIPLIER,
        )

        merged = merge_results(
            semantic_results,
            keyword_results,
        )

        logger.info(
            "Running reranker on %d merged chunk(s).",
            len(merged),
        )

        reranked = rerank_results(
            query=query,
            chunks=merged,
        )

        logger.info(
            "Hybrid search returned %d chunk(s).",
            min(limit, len(reranked)),
        )

        return reranked[:limit]

    raise ValueError(
        f"Unknown retrieval strategy: {strategy}"
    )