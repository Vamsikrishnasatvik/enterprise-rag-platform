import logging
from typing import Any

from app.services.retrieval.base import BaseRetriever
from app.services.retrieval_service import search_chunks

logger = logging.getLogger(__name__)

# =============================================================================
# Semantic Retriever
# =============================================================================


class SemanticRetriever(BaseRetriever):
    """
    Semantic vector retriever backed by Qdrant.

    This retriever delegates semantic search to the shared
    retrieval service.
    """

    def retrieve(
        self,
        query: str,
        limit: int,
        strategy: str = "semantic",
        **kwargs: Any,
    ) -> list:
        """
        Retrieves the most semantically relevant document chunks.

        Args:
            query: User retrieval query.
            limit: Maximum number of chunks to retrieve.
            strategy: Retrieval strategy (defaults to semantic).
            **kwargs: Reserved for future retrieval options.

        Returns:
            A list of retrieved chunks.
        """

        logger.info(
            "Semantic retrieval | limit=%d",
            limit,
        )

        return search_chunks(
            query=query,
            limit=limit,
            strategy=strategy,
        )