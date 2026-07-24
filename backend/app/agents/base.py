import logging
from abc import ABC, abstractmethod
from time import perf_counter

from app.graph.state import GraphState

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    def __call__(self, state: GraphState) -> GraphState:
        logger.info(f"[{self.name}] START")

        start = perf_counter()

        try:
            updated_state = self.run(state)

            updated_state.setdefault("execution_trace", []).append(self.name)
            updated_state.setdefault("agent_timings", {})[self.name] = (
                perf_counter() - start
            )

            logger.info(
                f"[{self.name}] END ({updated_state['agent_timings'][self.name]:.3f}s)"
            )

            return updated_state

        except Exception as e:
            logger.exception(f"[{self.name}] FAILED")

            state.setdefault("errors", []).append(str(e))
            raise

    @abstractmethod
    def run(self, state: GraphState) -> GraphState:
        """
        Implement agent logic.
        """
        pass