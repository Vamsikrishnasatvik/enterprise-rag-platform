from app.graph.state import GraphState
from app.tools.base import BaseTool
from app.tools.result import ToolResult


class PythonTool(BaseTool):

    name = "python"

    description = "Execute Python code."

    def execute(
        self,
        state: GraphState,
        **kwargs,
    ) -> ToolResult:

        return ToolResult(
            tool_name=self.name,
            success=False,
            error="PythonTool is not implemented yet.",
        )