import logging
import time
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseAgent(ABC):

    def __init__(self, name: str):
        self.name = name

    def __call__(self, state):

        logger.info("[%s] START", self.name)

        start = time.perf_counter()

        try:

            state = self.run(state)

            elapsed = round(time.perf_counter() - start, 3)

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

            elapsed = round(time.perf_counter() - start, 3)

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
                }
            )

            logger.exception("[%s] FAILED", self.name)
            raise

    @abstractmethod
    def run(self, state):
        pass