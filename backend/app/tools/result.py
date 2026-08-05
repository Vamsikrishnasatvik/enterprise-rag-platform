from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolResult:
    """
    Standard output returned by every tool.

    This allows the Supervisor and ToolExecutor
    to treat all tools identically.
    """

    tool_name: str

    success: bool

    data: Any = None

    sources: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    latency: float = 0.0

    error: str | None = None