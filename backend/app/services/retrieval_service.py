from app.services.embedding_service import generate_embeddings
from app.services.vector_service import client

COLLECTION_NAME = "document_chunks"


def search_chunks(
    query: str,
    limit: int = 3,
    strategy: str = "semantic",
):
    """
    Search the vector database.

    Current supported strategies:

    - semantic
    - hybrid (future-ready)
    - keyword (future-ready)

    Hybrid/keyword currently fall back to semantic search,
    but the architecture is ready for future expansion.
    """

    # ---------------------------------------------------------
    # Semantic Search
    # ---------------------------------------------------------

    vector = generate_embeddings([query])[0]

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=limit,
        with_payload=True,
    ).points

    # ---------------------------------------------------------
    # Future Extensions
    # ---------------------------------------------------------
    #
    # if strategy == "hybrid":
    #     vector_results = semantic_search(...)
    #     keyword_results = bm25_search(...)
    #     return merge(vector_results, keyword_results)
    #
    # if strategy == "keyword":
    #     return bm25_search(...)
    #
    # if strategy == "metadata":
    #     return metadata_search(...)
    #
    # if strategy == "rerank":
    #     return rerank(results)
    #
    # ---------------------------------------------------------

    return results