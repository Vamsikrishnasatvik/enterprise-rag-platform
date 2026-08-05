from app.agents.retriever_agent import RetrieverAgent
from app.graph.state import GraphState
from app.tools.base import BaseTool
from app.tools.result import ToolResult


class RAGTool(BaseTool):
    """
    Enterprise RAG Tool.
    Wraps the existing RetrieverAgent.
    """

    name = "rag"

    description = (
        "Retrieve enterprise knowledge from indexed documents."
    )

    def __init__(self):
        self.retriever = RetrieverAgent()

    def execute(
        self,
        state: GraphState,
        **kwargs,
    ) -> ToolResult:

        updated_state = self.retriever.run(state)

        return ToolResult(
            tool_name=self.name,
            success=True,
            data={
                "retrieval_context": updated_state.get(
                    "retrieval_context"
                ),
                "retrieved_chunks": updated_state.get(
                    "retrieved_chunks"
                ),
                "retrieval_score": updated_state.get(
                    "retrieval_score"
                ),
            },
            sources=updated_state.get(
                "retrieved_chunks",
                [],
            ),
        )