import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.db.session import SessionLocal

from app.services.evidence_service import (
    prepare_evidence,
)

from app.services.document_service import (
    get_document_name,
)

logger = logging.getLogger(__name__)


class EvidenceAgent(BaseAgent):
    """
    Phase 3.6.2

    Selects the best evidence and enriches it
    with document metadata.
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

        db = SessionLocal()

        try:

            enriched = []

            for chunk in evidence:

                enriched.append(
                    {
                        "chunk_id": chunk["chunk_id"],
                        "document_id": chunk["document_id"],
                        "document_name": get_document_name(
                            db,
                            chunk["document_id"],
                        ),
                        "page_number": chunk.get(
                            "page_number"
                        ),
                        "section": chunk.get(
                            "section"
                        ),
                        "content": chunk["content"],
                        "score": chunk["score"],
                    }
                )

        finally:
            db.close()

        state["evidence_chunks"] = enriched

        print("=" * 80)
        print("ENRICHED EVIDENCE")
        print(enriched)
        print("=" * 80)

        state["execution_trace"].append(
            {
                "agent": "EvidenceAgent",
                "status": "completed",
                "evidence_chunks": len(enriched),
            }
        )

        logger.info(
            "EvidenceAgent completed - %d evidence chunks",
            len(enriched),
        )

        return state