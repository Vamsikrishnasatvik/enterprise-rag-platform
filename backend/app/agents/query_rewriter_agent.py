import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.query_rewriter_service import rewrite_query

logger = logging.getLogger(__name__)


class QueryRewriterAgent(BaseAgent):
    """
    Rewrites the user's question into a retrieval-optimized query.

    The actual rewriting, validation, and hallucination detection are
    handled by the query_rewriter_service. This agent simply orchestrates
    the process and stores the resulting retrieval query.
    """

    def __init__(self):
        super().__init__("QueryRewriterAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        question = state.get(
            "question",
            "",
        ).strip()

        if not question:
            state.update(
                {
                    "original_question": "",
                    "retrieval_query": "",
                }
            )
            return state

        memory_context = state.get(
            "memory_context",
            "",
        )

        rewritten_query = (
            rewrite_query(
                question=question,
                memory_context=memory_context,
            )
            or ""
        ).strip()

        state.update(
            {
                "original_question": question,
                "retrieval_query": (
                    rewritten_query
                    if rewritten_query
                    else question
                ),
            }
        )

        logger.info(
            "Query Rewrite | original='%s' | rewritten='%s'",
            question,
            state["retrieval_query"],
        )

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": self.name,
                "original": question,
                "rewritten": state["retrieval_query"],
            }
        )

        return state