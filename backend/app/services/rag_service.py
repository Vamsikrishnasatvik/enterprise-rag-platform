import logging

from sqlalchemy.orm import Session

from app.graph.state import GraphState
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
# Graph State Builder
# =============================================================================


def build_initial_state(
    db: Session,
    conversation_id: int,
    question: str,
    retrieval_strategy: str = "hybrid",
) -> GraphState:
    """
    Builds the initial GraphState for the Agentic RAG workflow.
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
        # Conversation Memory
        # ---------------------------------------------------------------------
        "conversation_summary": "",
        "recent_messages": [],
        "conversation_history": [],
        "memory_context": "",

        # ---------------------------------------------------------------------
        # Planning
        # ---------------------------------------------------------------------
        "query_type": "",
        "planning_reason": "",
        "execution_plan": [],

        # ---------------------------------------------------------------------
        # Query Rewriting
        # ---------------------------------------------------------------------
        "original_question": question,
        "retrieval_query": "",

        # ---------------------------------------------------------------------
        # Retrieval
        # ---------------------------------------------------------------------
        "retrieval_strategy": retrieval_strategy,
        "retrieval_limit": DEFAULT_TOP_K,
        "retrieved_chunks": [],
        "retrieval_context": "",
        "retrieved_document_count": 0,
        "retrieval_score": 0.0,
        "reranker_score": 0.0,

        # ---------------------------------------------------------------------
        # Tool Execution
        # ---------------------------------------------------------------------
        "tool_outputs": [],

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
    }


# =============================================================================
# Conversation Persistence
# =============================================================================


def persist_messages(
    db: Session,
    conversation_id: int,
    question: str,
    answer: str,
) -> None:
    """
    Persists the user question and generated assistant answer.
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


def build_sources(
    result: GraphState,
) -> list[dict]:
    """
    Converts retrieved chunks into API response sources.
    """

    sources = []

    for chunk in result.get(
        "retrieved_chunks",
        [],
    ):
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


def log_workflow_summary(
    result: GraphState,
) -> None:
    """
    Logs a concise summary of workflow execution.
    """

    reflection = result.get(
        "reflection",
        {},
    )

    verification = result.get(
        "verification",
        {},
    )

    logger.info("=" * 80)
    logger.info("Workflow Complete")
    logger.info(
        "Query Type              : %s",
        result.get("query_type"),
    )
    logger.info(
        "Execution Steps         : %d",
        len(result.get("execution_plan", [])),
    )
    logger.info(
        "Retrieved Documents     : %d",
        result.get(
            "retrieved_document_count",
            0,
        ),
    )
    logger.info(
        "Retrieval Score         : %.4f",
        result.get(
            "retrieval_score",
            0.0,
        ),
    )
    logger.info(
        "Reflection Confidence   : %.2f",
        reflection.get(
            "confidence",
            0.0,
        ),
    )
    logger.info(
        "Verification Confidence : %.2f",
        verification.get(
            "confidence",
            0.0,
        ),
    )
    logger.info(
        "Retries                 : %d",
        result.get(
            "retry_count",
            0,
        ),
    )
    logger.info(
        "Answer Length           : %d",
        len(result.get("answer", "")),
    )
    logger.info("=" * 80)


# =============================================================================
# API Response Builder
# =============================================================================


def build_response(
    result: GraphState,
) -> dict:
    """
    Builds the API response returned to the client.
    """

    return {
        "answer": result.get("answer", ""),
        "sources": build_sources(result),
        "citations": result.get("citations", []),
        "reflection": result.get("reflection", {}),
        "verification": result.get("verification", {}),
        "confidence": result.get(
            "reflection",
            {},
        ).get(
            "confidence",
            0.0,
        ),
        "query_type": result.get("query_type"),
        "retrieval_score": result.get(
            "retrieval_score",
            0.0,
        ),
        "retrieved_document_count": result.get(
            "retrieved_document_count",
            0,
        ),
        "retry_count": result.get(
            "retry_count",
            0,
        ),
        "execution_trace": result.get(
            "execution_trace",
            [],
        ),
        "agent_timings": result.get(
            "agent_timings",
            {},
        ),
        "errors": result.get(
            "errors",
            [],
        ),
    }


# =============================================================================
# Public API
# =============================================================================


def answer_question(
    db: Session,
    conversation_id: int,
    question: str,
    retrieval_strategy: str = "hybrid",
) -> dict:
    """
    Executes the complete Agentic RAG workflow.
    """

    retrieval_strategy = retrieval_strategy.lower()

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
        (
            "Starting Agentic RAG Workflow | "
            "conversation=%s | "
            "strategy=%s | "
            "top_k=%d | "
            "max_retries=%d"
        ),
        conversation_id,
        retrieval_strategy,
        state["retrieval_limit"],
        state["max_retries"],
    )

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