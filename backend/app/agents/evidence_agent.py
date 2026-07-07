import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.evidence_service import (
    prepare_evidence,
)

from app.services.context_service import (
    build_context,
)

logger = logging.getLogger(__name__)


class EvidenceAgent(BaseAgent):
    """
    Phase 3.6.1

    Selects the final evidence passed
    to the AnswerAgent.
    """

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("EvidenceAgent started")

        state.setdefault("execution_trace", [])
        state.setdefault("reranked_chunks", [])
        state.setdefault("evidence_chunks", [])

        evidence = prepare_evidence(
            state["reranked_chunks"]
        )

        state["evidence_chunks"] = evidence

        # Final context used by the LLM
        state["context"] = build_context(
            evidence
        )

        state["execution_trace"].append(
            {
                "agent": "EvidenceAgent",
                "status": "completed",
                "evidence_chunks": len(evidence),
            }
        )

        logger.info(
            "EvidenceAgent completed - %d evidence chunks",
            len(evidence),
        )

        return state