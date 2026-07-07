from app.services.embedding_service import (
    generate_embeddings,
)

from app.services.vector_service import (
    client,
)

COLLECTION_NAME = "document_chunks"


def search_chunks(
    query: str,
    limit: int = 3,
    metadata_filters: dict | None = None,
):
    """
    Search relevant document chunks.

    metadata_filters is currently unused and will
    be implemented in a future milestone.
    """

    vector = generate_embeddings(
        [query]
    )[0]

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=limit,
        with_payload=True,
    ).points

    return results