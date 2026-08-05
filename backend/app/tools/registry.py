from typing import Dict

from app.tools.base import BaseTool


class ToolRegistry:
    """
    Central registry for all enterprise tools.

    Responsible for:
        - registering tools
        - retrieving tools
        - listing available tools
    """

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(
        self,
        tool: BaseTool,
    ) -> None:
        """
        Register a tool instance.
        """

        name = tool.name.lower()

        if name in self._tools:
            raise ValueError(
                f"Tool '{name}' is already registered."
            )

        self._tools[name] = tool

    def get(
        self,
        name: str,
    ) -> BaseTool:
        """
        Retrieve a registered tool.
        """

        try:
            return self._tools[name.lower()]
        except KeyError:
            raise ValueError(
                f"Unknown tool '{name}'."
            )

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether a tool exists.
        """

        return name.lower() in self._tools

    def list_tools(self) -> list[str]:
        """
        Return all registered tool names.
        """

        return sorted(self._tools.keys())