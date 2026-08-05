from abc import ABC, abstractmethod

from app.graph.state import GraphState
from app.tools.result import ToolResult


class BaseTool(ABC):
    """
    Base class for every enterprise tool.

    Every tool must implement execute() and return
    a ToolResult.
    """

    name: str = ""
    description: str = ""

    @abstractmethod
    def execute(
        self,
        state: GraphState,
        **kwargs,
    ) -> ToolResult:
        """
        Execute the tool.

        Parameters
        ----------
        state:
            Current graph state.

        kwargs:
            Tool-specific arguments.

        Returns
        -------
        ToolResult
        """
        raise NotImplementedError