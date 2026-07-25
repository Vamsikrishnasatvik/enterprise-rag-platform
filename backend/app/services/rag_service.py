import logging

from sqlalchemy.orm import Session

from app.graph.workflow import graph
from app.services.message_service import create_message

logger = logging.getLogger(__name__)


def answer_question(
    db: Session,
    conversation_id: int,
    question: str,
):
    """
    Production Agentic RAG pipeline powered by LangGraph.
    """

    state = {

        # ---------------------------------------------------------------------
        # Runtime
        # ---------------------------------------------------------------------

        "db": db,
        "conversation_id": conversation_id,

        # ---------------------------------------------------------------------
        # User Input
        # ---------------------------------------------------------------------

        "question": question,

        # ---------------------------------------------------------------------
        # Memory
        # ---------------------------------------------------------------------

        "conversation_summary": "",
        "recent_messages": [],
        "memory_context": "",

        # ---------------------------------------------------------------------
        # Planner
        # ---------------------------------------------------------------------

        "execution_plan": {},
        "query_type": "",
        "planning_reason": "",

        # ---------------------------------------------------------------------
        # Supervisor
        # ---------------------------------------------------------------------

        "next_node": "",
        "routing_reason": "",
        "needs_retrieval": False,
        "needs_verification": False,

        # ---------------------------------------------------------------------
        # Retrieval
        # ---------------------------------------------------------------------

        "retrieval_query": "",
        "retrieval_limit": 3,
        "retrieval_strategy": "semantic",
        "retrieved_chunks": [],
        "retrieval_context": "",
        "retrieved_document_count": 0,
        "retrieval_score": 0.0,

        # ---------------------------------------------------------------------
        # Answer
        # ---------------------------------------------------------------------

        "answer": "",
        "citations": [],

        # ---------------------------------------------------------------------
        # Reflection
        # ---------------------------------------------------------------------

        "reflection": {},
        "confidence_score": 0.0,
        "needs_retry": False,

        # ---------------------------------------------------------------------
        # Verification
        # ---------------------------------------------------------------------

        "verification": {},
        "verification_passed": False,
        "verification_reason": "",

        # ---------------------------------------------------------------------
        # Retry
        # ---------------------------------------------------------------------

        "retry_required": False,
        "retry_reason": "",
        "retry_count": 0,
        "max_retries": 2,

        # ---------------------------------------------------------------------
        # Monitoring
        # ---------------------------------------------------------------------

        "execution_trace": [],
        "agent_timings": {},
        "errors": [],

        # ---------------------------------------------------------------------
        # Tool Calling (Future)
        # ---------------------------------------------------------------------

        "selected_tool": "",
        "tool_result": {},
        "tool_reason": "",
    }

    # -------------------------------------------------------------------------
    # Execute Workflow
    # -------------------------------------------------------------------------

    result = graph.invoke(state)

    # -------------------------------------------------------------------------
    # Workflow Summary
    # -------------------------------------------------------------------------

    logger.info("=" * 80)
    logger.info("Workflow Complete")
    logger.info("Query Type      : %s", result.get("query_type"))
    logger.info("Route           : %s", result.get("next_node"))
    logger.info("Retries         : %d", result.get("retry_count", 0))
    logger.info("Documents       : %d", result.get("retrieved_document_count", 0))
    logger.info("Top Score       : %.4f", result.get("retrieval_score", 0.0))
    logger.info("Confidence      : %.2f", result.get("confidence_score", 0.0))
    logger.info("Answer Length   : %d", len(result.get("answer", "")))
    logger.info("=" * 80)

    # -------------------------------------------------------------------------
    # Persist Messages
    # -------------------------------------------------------------------------

    create_message(
        db=db,
        conversation_id=conversation_id,
        tenant_id=1,
        role="user",
        content=question,
    )

    create_message(
        db=db,
        conversation_id=conversation_id,
        tenant_id=1,
        role="assistant",
        content=result["answer"],
    )

    # -------------------------------------------------------------------------
    # Sources
    # -------------------------------------------------------------------------

    sources = []

    for chunk in result.get("retrieved_chunks", []):

        sources.append(
            {
                "chunk_id": chunk.payload["chunk_id"],
                "document_id": chunk.payload["document_id"],
                "content": chunk.payload["content"],
                "score": chunk.score,
            }
        )

    # -------------------------------------------------------------------------
    # API Response
    # -------------------------------------------------------------------------

    return {
        "answer": result["answer"],
        "sources": sources,
        "citations": result.get("citations", []),
        "reflection": result.get("reflection", {}),
        "verification": result.get("verification", {}),
        "confidence": result.get("confidence_score", 0.0),
        "query_type": result.get("query_type"),
        "retrieval_score": result.get("retrieval_score", 0.0),
        "retrieved_documents": result.get("retrieved_document_count", 0),
        "retry_count": result.get("retry_count", 0),
        "execution_trace": result.get("execution_trace", []),
        "agent_timings": result.get("agent_timings", {}),
        "errors": result.get("errors", []),
    }