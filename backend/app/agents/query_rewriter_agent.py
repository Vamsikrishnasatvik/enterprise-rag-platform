import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.query_rewriter_service import rewrite_query

logger = logging.getLogger(__name__)


class QueryRewriterAgent(BaseAgent):

    def __init__(self):
        super().__init__("QueryRewriterAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        # ---------------------------------------------------------
        # Original Question
        # ---------------------------------------------------------

        question = state["question"]

        memory_context = state.get(
            "memory_context",
            "",
        )
        
        # ---------------------------------------------------------
        # Rewrite Query
        # ---------------------------------------------------------

        rewritten_query = rewrite_query(
            question=question,
            memory_context=memory_context,
        )

        # ---------------------------------------------------------
        # Store Query
        # ---------------------------------------------------------

        if rewritten_query:
            state["retrieval_query"] = rewritten_query
        else:
            state["retrieval_query"] = question

        # Optional (helps debugging)

        state["original_question"] = question

        logger.info(
            "Query Rewrite | original='%s' | rewritten='%s'",
            question,
            state["retrieval_query"],
        )

        # ---------------------------------------------------------
        # Execution Trace
        # ---------------------------------------------------------

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": "QueryRewriterAgent",
                "original": question,
                "rewritten": state["retrieval_query"],
            }
        )

        return state