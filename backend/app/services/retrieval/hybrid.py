import logging
from typing import Any

from app.services.retrieval.base import BaseRetriever
from app.services.retrieval.fusion import reciprocal_rank_fusion
from app.services.retrieval.keyword import KeywordRetriever
from app.services.retrieval.metadata import MetadataRetriever
from app.services.retrieval.semantic import SemanticRetriever

logger = logging.getLogger(__name__)

# =============================================================================
# Hybrid Retriever
# =============================================================================


class HybridRetriever(BaseRetriever):
    """
    Enterprise retrieval orchestrator.

    Supported strategies:

        • semantic
        • keyword
        • hybrid

    Hybrid retrieval combines semantic and keyword retrieval
    using Reciprocal Rank Fusion (RRF).
    """

    def __init__(self) -> None:
        self.semantic = SemanticRetriever()
        self.keyword = KeywordRetriever()
        self.metadata = MetadataRetriever()

    def retrieve(
        self,
        query: str,
        limit: int,
        strategy: str = "semantic",
        **kwargs: Any,
    ) -> list:
        """
        Retrieves relevant document chunks using the selected
        retrieval strategy.
        """

        strategy = strategy.lower()

        logger.info(
            "HybridRetriever | strategy=%s | limit=%d",
            strategy,
            limit,
        )

        # ---------------------------------------------------------
        # Semantic Retrieval
        # ---------------------------------------------------------

        if strategy == "semantic":

            results = self.semantic.retrieve(
                query=query,
                limit=limit,
                strategy="semantic",
                **kwargs,
            )

        # ---------------------------------------------------------
        # Keyword Retrieval
        # ---------------------------------------------------------

        elif strategy == "keyword":

            results = self.keyword.retrieve(
                query=query,
                limit=limit,
                **kwargs,
            )

        # ---------------------------------------------------------
        # Hybrid Retrieval (Semantic + Keyword + RRF)
        # ---------------------------------------------------------

        elif strategy == "hybrid":

            semantic_results = self.semantic.retrieve(
                query=query,
                limit=limit * 2,
                strategy="semantic",
                **kwargs,
            )

            keyword_results = self.keyword.retrieve(
                query=query,
                limit=limit * 2,
                **kwargs,
            )

            results = reciprocal_rank_fusion(
                [
                    semantic_results,
                    keyword_results,
                ]
            )[:limit]

        else:

            raise ValueError(
                f"Unknown retrieval strategy: {strategy}"
            )

        logger.info(
            "HybridRetriever | retrieved=%d chunks",
            len(results),
        )

        return results