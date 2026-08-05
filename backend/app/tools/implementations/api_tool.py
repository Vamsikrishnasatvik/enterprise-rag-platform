from app.graph.state import GraphState
from app.tools.base import BaseTool
from app.tools.result import ToolResult


class APITool(BaseTool):

    name = "api"

    description = "Call enterprise APIs."

    def execute(
        self,
        state: GraphState,
        **kwargs,
    ) -> ToolResult:

        return ToolResult(
            tool_name=self.name,
            success=False,
            error="APITool is not implemented yet.",
        )