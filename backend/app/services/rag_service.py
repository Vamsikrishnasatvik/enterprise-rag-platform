import logging

from sqlalchemy.orm import Session

from app.graph.workflow import graph
from app.services.message_service import create_message

logger = logging.getLogger(__name__)


# =============================================================================
# State Builder
# =============================================================================

def build_initial_state(
    db: Session,
    conversation_id: int,
    question: str,
) -> dict:
    """
    Build the initial GraphState for the workflow.
    """

    return {

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


# =============================================================================
# Persistence
# =============================================================================

def persist_messages(
    db: Session,
    conversation_id: int,
    question: str,
    answer: str,
):
    """
    Persist the user and assistant messages.
    """

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
        content=answer,
    )


# =============================================================================
# Source Builder
# =============================================================================

def build_sources(result: dict) -> list[dict]:
    """
    Convert retrieved chunks into API response format.
    """

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

    return sources


# =============================================================================
# Workflow Logging
# =============================================================================

def log_workflow_summary(result: dict):
    """
    Log the overall workflow execution summary.
    """

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


# =============================================================================
# Response Builder
# =============================================================================

def build_response(result: dict) -> dict:
    """
    Build the API response.
    """

    return {
        "answer": result["answer"],
        "sources": build_sources(result),
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


# =============================================================================
# Public API
# =============================================================================

def answer_question(
    db: Session,
    conversation_id: int,
    question: str,
):
    """
    Execute the complete Agentic RAG workflow.
    """

    state = build_initial_state(
        db=db,
        conversation_id=conversation_id,
        question=question,
    )

    logger.info(
        "Starting Agentic RAG Workflow | conversation=%s | max_retries=%d",
        conversation_id,
        state["max_retries"],
    )

    result = graph.invoke(
        state,
        config={
            "recursion_limit": 100,
        },
    )

    log_workflow_summary(result)

    persist_messages(
        db=db,
        conversation_id=conversation_id,
        question=question,
        answer=result["answer"],
    )

    return build_response(result)