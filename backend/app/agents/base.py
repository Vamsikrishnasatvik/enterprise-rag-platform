from abc import ABC, abstractmethod
from time import perf_counter

from app.graph.state import GraphState


class BaseAgent(ABC):
    """
    Base class for all agents in the Agentic RAG workflow.
    """

    def __init__(self, name: str):
        self.name = name

    def __call__(self, state: GraphState) -> GraphState:
        start = perf_counter()

        try:
            state.setdefault("execution_trace", []).append(
                f"{self.name} started"
            )

            updated_state = self.run(state)

            duration = perf_counter() - start

            updated_state.setdefault("agent_timings", {})[
                self.name
            ] = round(duration, 4)

            updated_state.setdefault("execution_trace", []).append(
                f"{self.name} completed"
            )

            return updated_state

        except Exception as e:
            state.setdefault("errors", []).append(str(e))
            raise

    @abstractmethod
    def run(self, state: GraphState) -> GraphState:
        """
        Implement agent logic.
        """
        pass