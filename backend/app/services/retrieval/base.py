from abc import ABC, abstractmethod


class BaseRetriever(ABC):
    """
    Base interface for all retrieval strategies.
    """

    @abstractmethod
    def retrieve(
        self,
        query: str,
        limit: int,
        **kwargs,
    ):
        """
        Retrieve relevant chunks.
        """
        pass