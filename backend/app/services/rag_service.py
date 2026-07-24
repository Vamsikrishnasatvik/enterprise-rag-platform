from sqlalchemy.orm import Session

from app.graph.workflow import graph

from app.services.message_service import (
    create_message,
)


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
        "conversation_history": [],
        "memory_context": "",

        # ---------------------------------------------------------------------
        # Retrieval
        # ---------------------------------------------------------------------
        "retrieval_query": "",
        "retrieval_limit": 3,
        "retrieval_strategy": "semantic",
        "retrieved_chunks": [],
        "compressed_context": "",

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
    }

    result = graph.invoke(state)

    # -------------------------------------------------------------------------
    # Persist Conversation
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
    # Build Sources
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

    return {
        "answer": result["answer"],
        "sources": sources,
    }