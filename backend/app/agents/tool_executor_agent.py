import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.tools import tool_executor

logger = logging.getLogger(__name__)


class ToolExecutorAgent(BaseAgent):
    """
    Executes the tools selected by the Planner/Supervisor.

    Multiple tools may be executed sequentially. The outputs are stored
    in the graph state for downstream agents.
    """

    def __init__(self):
        super().__init__("ToolExecutorAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        execution_plan = state.get("execution_plan") or []

        if not isinstance(execution_plan, list):
            execution_plan = []

        tool_outputs = []

        # ---------------------------------------------------------
        # Execute Tools
        # ---------------------------------------------------------

        for step in execution_plan:

            if not isinstance(step, dict):
                continue

            tool_name = step.get(
                "tool",
                "rag",
            )

            tool_inputs = step.get(
                "inputs",
            ) or {}

            result = tool_executor.execute(
                tool_name=tool_name,
                state=state,
                **tool_inputs,
            )

            if not result.success:
                raise RuntimeError(
                    f"Tool '{tool_name}' failed: {result.error}"
                )

            tool_outputs.append(result)

        state.update(
            {
                "tool_outputs": tool_outputs,
                "tool_output": (
                    tool_outputs[0]
                    if tool_outputs
                    else None
                ),
            }
        )

        tool_names = [
            output.tool_name
            for output in tool_outputs
        ]

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": self.name,
                "status": "success",
                "tools": tool_names,
                "count": len(tool_outputs),
            }
        )

        logger.info(
            "Executed %d tool(s): %s",
            len(tool_outputs),
            ", ".join(tool_names),
        )

        return state