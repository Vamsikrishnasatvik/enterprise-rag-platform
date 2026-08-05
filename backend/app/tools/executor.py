import logging
import time

from app.graph.state import GraphState
from app.tools.registry import ToolRegistry
from app.tools.result import ToolResult

logger = logging.getLogger(__name__)


class ToolExecutor:
    """
    Executes registered tools.
    """

    def __init__(
        self,
        registry: ToolRegistry,
    ):
        self.registry = registry

    def execute(
        self,
        tool_name: str,
        state: GraphState,
        **kwargs,
    ) -> ToolResult:

        start_time = time.perf_counter()

        try:
            tool = self.registry.get(tool_name)

            result = tool.execute(
                state=state,
                **kwargs,
            )

            result.latency = (
                time.perf_counter() - start_time
            )

            logger.info(
                "Tool '%s' executed successfully in %.3fs",
                tool_name,
                result.latency,
            )

            return result

        except Exception as exc:

            latency = (
                time.perf_counter() - start_time
            )

            logger.exception(
                "Tool '%s' execution failed.",
                tool_name,
            )

            return ToolResult(
                tool_name=tool_name,
                success=False,
                latency=latency,
                error=str(exc),
            )