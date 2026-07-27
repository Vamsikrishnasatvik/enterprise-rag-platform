import logging

from app.services.retrieval.keyword import KeywordRetriever
from app.services.retrieval.metadata import MetadataRetriever
from app.services.retrieval.semantic import SemanticRetriever

logger = logging.getLogger(__name__)


class HybridRetriever:
    """
    Enterprise retrieval orchestrator.

    Phase 6.1.1
        - Semantic retrieval only

    Phase 6.1.2
        - Semantic + BM25

    Phase 6.1.3
        - Metadata search

    Phase 6.1.4
        - Reciprocal Rank Fusion
    """

    def __init__(self):
        self.semantic = SemanticRetriever()
        self.keyword = KeywordRetriever()
        self.metadata = MetadataRetriever()

    def retrieve(
        self,
        query: str,
        limit: int,
        strategy: str = "semantic",
        **kwargs,
    ):
        """
        Retrieve relevant document chunks.

        Phase 6.1.1 uses semantic search only.

        Future versions will combine:
            - Semantic Search
            - Keyword Search (BM25)
            - Metadata Search
            - Reciprocal Rank Fusion (RRF)
        """

        logger.info(
            "HybridRetriever | strategy=%s | limit=%d | query='%s'",
            strategy,
            limit,
            query,
        )

        results = self.semantic.retrieve(
            query=query,
            limit=limit,
            strategy=strategy,
        )

        logger.info(
            "HybridRetriever | retrieved=%d chunks",
            len(results),
        )

        return results