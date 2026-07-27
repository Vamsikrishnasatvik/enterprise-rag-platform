from app.services.retrieval.base import BaseRetriever
from app.services.retrieval_service import search_chunks


class SemanticRetriever(BaseRetriever):
    """
    Semantic vector search using Qdrant.
    """

    def retrieve(
        self,
        query: str,
        limit: int,
        strategy: str = "semantic",
        **kwargs,
    ):
        return search_chunks(
            query=query,
            limit=limit,
            strategy=strategy,
        )