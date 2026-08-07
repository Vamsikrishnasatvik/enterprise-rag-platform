import logging
import time
from abc import ABC, abstractmethod

from app.graph.state import GraphState

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Base class for all workflow agents.

    Provides a standardized execution lifecycle including:

    - start/end logging
    - execution timing
    - execution trace recording
    - centralized error handling

    Concrete agents only implement `run()`.
    """

    def __init__(
        self,
        name: str,
    ):
        self.name = name

    def __call__(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("[%s] START", self.name)

        start = time.perf_counter()

        try:

            state = self.run(state)

            elapsed = round(
                time.perf_counter() - start,
                3,
            )

            state.setdefault(
                "agent_timings",
                {},
            )[self.name] = elapsed

            state.setdefault(
                "execution_trace",
                [],
            ).append(
                {
                    "agent": self.name,
                    "status": "success",
                    "duration": elapsed,
                }
            )

            logger.info(
                "[%s] END (%.3fs)",
                self.name,
                elapsed,
            )

            return state

        except Exception as exc:

            elapsed = round(
                time.perf_counter() - start,
                3,
            )

            state.setdefault(
                "errors",
                [],
            ).append(
                {
                    "agent": self.name,
                    "error": str(exc),
                }
            )

            state.setdefault(
                "execution_trace",
                [],
            ).append(
                {
                    "agent": self.name,
                    "status": "failed",
                    "duration": elapsed,
                    "error": str(exc),
                }
            )

            logger.exception(
                "[%s] FAILED (%.3fs)",
                self.name,
                elapsed,
            )

            raise

    @abstractmethod
    def run(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Execute the agent-specific business logic.

        Implementations should update and return the shared GraphState.
        """
        raise NotImplementedError