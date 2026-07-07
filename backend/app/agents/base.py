from abc import ABC, abstractmethod

from app.graph.state import GraphState


class BaseAgent(ABC):
    """
    Base interface for all agents.
    """

    @abstractmethod
    def run(self, state: GraphState) -> GraphState:
        """
        Process the graph state and return the updated state.
        """
        pass