import logging
from typing import Any

from app.services.retrieval.base import BaseRetriever

logger = logging.getLogger(__name__)

# =============================================================================
# Metadata Retriever
# =============================================================================


class MetadataRetriever(BaseRetriever):
    """
    Placeholder retriever for metadata-based filtering.

    Planned support includes filtering by:

        • Department
        • Owner
        • Document Status
        • Document Type
        • Tags
        • Created Date
        • Custom Metadata

    This retriever currently returns an empty result set and
    serves as an extension point for future enterprise features.
    """

    def retrieve(
        self,
        query: str,
        limit: int,
        **kwargs: Any,
    ) -> list:
        """
        Retrieves document chunks using metadata filters.

        Returns:
            An empty list until metadata filtering is implemented.
        """

        logger.info(
            "MetadataRetriever not implemented. Returning empty result set."
        )

        return []