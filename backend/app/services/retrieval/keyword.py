from app.services.retrieval.base import BaseRetriever


class KeywordRetriever(BaseRetriever):
    """
    Placeholder for BM25 keyword search.

    Phase 6.1.2 will implement this.
    """

    def retrieve(
        self,
        query: str,
        limit: int,
        **kwargs,
    ):
        return []