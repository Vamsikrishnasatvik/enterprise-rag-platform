from collections import OrderedDict
from dataclasses import dataclass

from sqlalchemy import or_

from app.db.session import SessionLocal
from app.models.document_chunk import DocumentChunk

from app.services.embedding_service import generate_embeddings
from app.services.vector_service import client
from app.services.reranker_service import rerank_results

COLLECTION_NAME = "document_chunks"


# ==========================================================
# Search Result Wrapper
# ==========================================================

@dataclass
class SearchResult:
    score: float
    payload: dict


# ==========================================================
# Semantic Search
# ==========================================================

def semantic_search(
    query: str,
    limit: int,
):

    vector = generate_embeddings([query])[0]

    return client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=limit,
        with_payload=True,
    ).points


# ==========================================================
# Keyword Search
# ==========================================================

def keyword_search(
    query: str,
    limit: int,
):
    """
    PostgreSQL keyword search using ILIKE.
    """

    db = SessionLocal()

    try:

        words = [
            word.strip()
            for word in query.split()
            if len(word.strip()) > 2
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
                    score=0.50,
                    payload={
                        "chunk_id": chunk.id,
                        "document_id": chunk.document_id,
                        "content": chunk.content,
                    },
                )
            )

        return results

    except Exception:

        return []

    finally:
        db.close()


# ==========================================================
# Merge Results
# ==========================================================

def merge_results(
    semantic_results,
    keyword_results,
):

    merged = OrderedDict()

    for chunk in semantic_results + keyword_results:

        chunk_id = chunk.payload["chunk_id"]

        if chunk_id not in merged:
            merged[chunk_id] = chunk
            continue

        if chunk.score > merged[chunk_id].score:
            merged[chunk_id] = chunk

    return sorted(
        merged.values(),
        key=lambda c: c.score,
        reverse=True,
    )


# ==========================================================
# Public Search API
# ==========================================================

def search_chunks(
    query: str,
    limit: int = 3,
    strategy: str = "semantic",
):

    query = query.strip()

    if not query:
        return []

    strategy = strategy.lower()

    # ---------------------------------------------------------
    # Semantic Search
    # ---------------------------------------------------------

    if strategy == "semantic":

        return semantic_search(
            query=query,
            limit=limit,
        )

    # ---------------------------------------------------------
    # Keyword Search
    # ---------------------------------------------------------

    if strategy == "keyword":

        return keyword_search(
            query=query,
            limit=limit,
        )

    # ---------------------------------------------------------
    # Hybrid Search
    # ---------------------------------------------------------

    if strategy == "hybrid":

        semantic_results = semantic_search(
            query=query,
            limit=limit * 2,
        )

        keyword_results = keyword_search(
            query=query,
            limit=limit * 2,
        )

        merged = merge_results(
            semantic_results,
            keyword_results,
        )

        reranked = rerank_results(
            query=query,
            chunks=merged,
        )

        return reranked[:limit]

    raise ValueError(
        f"Unknown retrieval strategy: {strategy}"
    )