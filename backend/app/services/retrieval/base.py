from abc import ABC, abstractmethod
from typing import Any


class BaseRetriever(ABC):
    """
    Abstract base class for retrieval strategies.

    All retrieval implementations must return a list of
    retrieved document chunks.
    """

    @abstractmethod
    def retrieve(
        self,
        query: str,
        limit: int,
        **kwargs: Any,
    ) -> list:
        """
        Retrieves the most relevant document chunks.

        Args:
            query: User retrieval query.
            limit: Maximum number of chunks to return.
            **kwargs: Strategy-specific retrieval options.

        Returns:
            A list of retrieved chunks.
        """
        raise NotImplementedError