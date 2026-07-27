from app.services.retrieval.base import BaseRetriever


class MetadataRetriever(BaseRetriever):
    """
    Placeholder for metadata filtering.

    Future support:
        - department
        - owner
        - status
        - document type
    """

    def retrieve(
        self,
        query: str,
        limit: int,
        **kwargs,
    ):
        return []