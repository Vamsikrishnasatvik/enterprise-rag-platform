import logging

from app.services.embedding_service import (
    generate_embeddings,
)


logger = logging.getLogger(__name__)


def rerank_chunks(
    query: str,
    chunks: list,
) -> list:
    """
    Phase 3.5.2

    Semantic reranker using embedding similarity.

    Since embeddings are normalized,
    cosine similarity == dot product.
    """

    if not chunks:
        return []

    logger.info(
        "Semantic reranking %d chunks",
        len(chunks),
    )

    query_embedding = generate_embeddings(
        [query]
    )[0]

    chunk_embeddings = generate_embeddings(
        [
            chunk["content"]
            for chunk in chunks
        ]
    )

    scored_chunks = []

    for chunk, embedding in zip(
        chunks,
        chunk_embeddings,
    ):

        similarity = sum(
            q * c
            for q, c in zip(
                query_embedding,
                embedding,
            )
        )

        chunk["rerank_score"] = round(
            similarity,
            4,
        )

        scored_chunks.append(chunk)

    reranked = sorted(
        scored_chunks,
        key=lambda x: x["rerank_score"],
        reverse=True,
    )

    logger.info(
        "Semantic reranking completed"
    )

    return reranked