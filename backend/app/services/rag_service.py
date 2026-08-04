import logging

from sqlalchemy.orm import Session

from app.graph.workflow import graph
from app.services.message_service import create_message

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

DEFAULT_TOP_K = 3
DEFAULT_MAX_RETRIES = 2

VALID_RETRIEVAL_STRATEGIES = {
    "semantic",
    "keyword",
    "hybrid",
}


# =============================================================================
# State Builder
# =============================================================================

def build_initial_state(
    db: Session,
    conversation_id: int,
    question: str,
    retrieval_strategy: str = "hybrid",
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
        "retrieval_limit": DEFAULT_TOP_K,
        "retrieval_strategy": retrieval_strategy,
        "retrieved_chunks": [],
        "retrieval_context": "",
        "retrieved_document_count": 0,
        "retrieval_score": 0.0,
        "reranker_score": 0.0,

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
        "max_retries": DEFAULT_MAX_RETRIES,

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

        payload = chunk.payload

        sources.append(
            {
                "chunk_id": payload.get("chunk_id"),
                "document_id": payload.get("document_id"),
                "content": payload.get("content", ""),
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
    retrieval_strategy: str = "hybrid",
):
    """
    Execute the complete Agentic RAG workflow.
    """

    # -------------------------------------------------------------------------
    # Validate Retrieval Strategy
    # -------------------------------------------------------------------------

    if retrieval_strategy not in VALID_RETRIEVAL_STRATEGIES:

        logger.warning(
            "Unknown retrieval strategy '%s'. Falling back to 'hybrid'.",
            retrieval_strategy,
        )

        retrieval_strategy = "hybrid"

    state = build_initial_state(
        db=db,
        conversation_id=conversation_id,
        question=question,
        retrieval_strategy=retrieval_strategy,
    )

    logger.info(
        "Starting Agentic RAG Workflow | conversation=%s | strategy=%s | top_k=%d | max_retries=%d",
        conversation_id,
        retrieval_strategy,
        state["retrieval_limit"],
        state["max_retries"],
    )

    # -------------------------------------------------------------------------
    # Execute Workflow
    # -------------------------------------------------------------------------

    try:

        result = graph.invoke(
            state,
            config={
                "recursion_limit": 100,
            },
        )

    except Exception:

        logger.exception(
            "Agentic RAG workflow execution failed."
        )

        raise

    log_workflow_summary(result)

    # -------------------------------------------------------------------------
    # Persist Conversation
    # -------------------------------------------------------------------------

    try:

        persist_messages(
            db=db,
            conversation_id=conversation_id,
            question=question,
            answer=result["answer"],
        )

    except Exception:

        logger.exception(
            "Failed to persist conversation messages."
        )

    return build_response(result)