from app.tools.executor import ToolExecutor
from app.tools.implementations.api_tool import APITool
from app.tools.implementations.python_tool import PythonTool
from app.tools.implementations.rag_tool import RAGTool
from app.tools.implementations.sql_tool import SQLTool
from app.tools.registry import ToolRegistry

tool_registry = ToolRegistry()

tool_registry.register(RAGTool())
tool_registry.register(SQLTool())
tool_registry.register(APITool())
tool_registry.register(PythonTool())

tool_executor = ToolExecutor(
    registry=tool_registry,
)