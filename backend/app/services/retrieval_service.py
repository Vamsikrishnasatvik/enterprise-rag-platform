from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
)

from app.services.embedding_service import (
    generate_embeddings,
)

from app.services.vector_service import (
    client,
    ensure_collection,
)

COLLECTION_NAME = "document_chunks"


def search_chunks(
    query: str,
    tenant_id: int | None = None,
    limit: int = 3,
    metadata_filters: dict | None = None,
):
    """
    Semantic search using Qdrant.

    Supports:
    - tenant filtering
    - metadata filtering

    Returns normalized chunk dictionaries.
    """
    ensure_collection()

    vector = generate_embeddings([query])[0]

    conditions = []

    # ------------------------------------
    # Tenant Filter
    # ------------------------------------

    if tenant_id is not None:

        conditions.append(
            FieldCondition(
                key="tenant_id",
                match=MatchValue(
                    value=tenant_id,
                ),
            )
        )

    # ------------------------------------
    # Metadata Filters
    # ------------------------------------

    if metadata_filters:

        for key, value in metadata_filters.items():

            conditions.append(
                FieldCondition(
                    key=key,
                    match=MatchValue(
                        value=value,
                    ),
                )
            )

    query_filter = (
        Filter(must=conditions)
        if conditions
        else None
    )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        query_filter=query_filter,
        limit=limit,
        with_payload=True,
    ).points

    normalized = []

    for result in results:

        normalized.append(
            {
                "chunk_id": result.payload["chunk_id"],
                "document_id": result.payload["document_id"],
                "content": result.payload["content"],
                "score": result.score,
                "page_number": result.payload.get(
                    "page_number"
                ),
                "section": result.payload.get(
                    "section"
                ),
            }
        )

    return normalized