from abc import ABC, abstractmethod

from app.graph.state import GraphState


class BaseAnswerGenerator(ABC):
    """
    Base class for all answer generation strategies.
    """

    @abstractmethod
    def generate(
        self,
        state: GraphState,
    ) -> str:
        pass