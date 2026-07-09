from app.services.retrieval_service import (
    search_chunks,
)

from app.services.bm25_service import (
    bm25_search,
)

from app.services.fusion_service import (
    reciprocal_rank_fusion,
)


def retrieve_documents(
    *,
    question: str,
    tenant_id: int,
    limit: int,
    strategy: str = "semantic",
    metadata_filters: dict | None = None,
):
    """
    Central retrieval orchestrator.

    Supports:
    - semantic
    - bm25
    - hybrid (Semantic + BM25 + RRF)
    """

    if strategy == "semantic":

        return search_chunks(
            query=question,
            tenant_id=tenant_id,
            limit=limit,
            metadata_filters=metadata_filters,
        )

    if strategy == "bm25":

        return bm25_search(
            query=question,
            tenant_id=tenant_id,
            limit=limit,
            metadata_filters=metadata_filters,
        )

    if strategy == "hybrid":

        semantic_results = search_chunks(
            query=question,
            tenant_id=tenant_id,
            limit=limit,
            metadata_filters=metadata_filters,
        )

        lexical_results = bm25_search(
            query=question,
            tenant_id=tenant_id,
            limit=limit,
            metadata_filters=metadata_filters,
        )

        return reciprocal_rank_fusion(
            [
                semantic_results,
                lexical_results,
            ]
        )

    raise ValueError(
        f"Unknown retrieval strategy: {strategy}"
    )