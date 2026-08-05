from app.graph.state import GraphState
from app.tools.base import BaseTool
from app.tools.result import ToolResult


class SQLTool(BaseTool):

    name = "sql"

    description = "Execute SQL queries against enterprise databases."

    def execute(
        self,
        state: GraphState,
        **kwargs,
    ) -> ToolResult:

        return ToolResult(
            tool_name=self.name,
            success=False,
            error="SQLTool is not implemented yet.",
        )