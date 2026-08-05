import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.tools import tool_executor

logger = logging.getLogger(__name__)


class ToolExecutorAgent(BaseAgent):

    def __init__(self):
        super().__init__("ToolExecutorAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        execution_plan = state.get(
            "execution_plan",
            [],
        )

        tool_outputs = []

        # ---------------------------------------------------------
        # Execute Tools
        # ---------------------------------------------------------

        for step in execution_plan:

            result = tool_executor.execute(
                tool_name=step.get(
                    "tool",
                    "rag",
                ),
                state=state,
                **step.get(
                    "inputs",
                    {},
                ),
            )

            if not result.success:
                raise RuntimeError(result.error)

            tool_outputs.append(result)

        # ---------------------------------------------------------
        # Store Results
        # ---------------------------------------------------------

        state["tool_outputs"] = tool_outputs

        if tool_outputs:
            state["tool_output"] = tool_outputs[0]

        # ---------------------------------------------------------
        # Execution Trace
        # ---------------------------------------------------------

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": "ToolExecutorAgent",
                "tools": [
                    output.tool_name
                    for output in tool_outputs
                ],
                "count": len(tool_outputs),
            }
        )

        logger.info(
            "Executed %d tool(s): %s",
            len(tool_outputs),
            ", ".join(
                output.tool_name
                for output in tool_outputs
            ),
        )

        return state