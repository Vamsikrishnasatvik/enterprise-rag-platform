from app.graph.workflow import graph

from app.services.retrieval_service import (
    search_chunks,
)
from app.services.context_service import (
    build_context,
)
from app.services.llm_service import (
    generate_answer,
)
from app.services.message_service import (
    build_chat_history,
)


def answer_question(question: str):
    """
    Agentic RAG pipeline powered by LangGraph.
    """

    state = {
        "question": question,

        # Retrieval
        "retrieved_chunks": [],
        "compressed_context": "",

        # Generation
        "answer": "",
        "citations": [],

        # Planning
        "execution_plan": {},
        "query_type": "",

        # Routing
        "next_node": "",
        "routing_reason": "",
        "needs_retrieval": False,
        "needs_verification": False,

        # Reflection
        "reflection": {},
        "confidence_score": 0.0,
        "needs_retry": False,

        # Monitoring
        "execution_trace": [],
        "agent_timings": {},
        "errors": [],

        # Verification
        "verification": {},
        "verification_passed": False,
        "verification_reason": "",

        # Retry
        "retry_required": False,
        "retry_reason": "",
        "retry_count": 0,
        "max_retries": 2,

        # Retrieval
        "retrieval_limit": 3,
        "retrieval_strategy": "semantic",

        "retry_count": 0,
    }

    result = graph.invoke(state)

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

        "execution_plan": result.get("execution_plan"),
        "query_type": result.get("query_type"),
        "planning_reason": result.get("planning_reason"),

        "confidence_score": result.get("confidence_score"),
        "reflection": result.get("reflection"),

        "execution_trace": result.get("execution_trace", []),
        "agent_timings": result.get("agent_timings", {}),

        "verification": result.get("verification"),
        "verification_passed": result.get("verification_passed"),
        "verification_reason": result.get("verification_reason"),
    }


def answer_conversation_question(
    db,
    conversation_id: int,
    question: str,
):
    """
    Legacy conversation pipeline.
    (Will migrate to LangGraph in a later phase.)
    """

    history = build_chat_history(
        db,
        conversation_id,
    )

    results = search_chunks(question)

    context = build_context(results)

    answer = generate_answer(
        question,
        context,
        history,
    )

    sources = []

    for result in results:
        sources.append(
            {
                "chunk_id": result.payload["chunk_id"],
                "document_id": result.payload["document_id"],
                "content": result.payload["content"],
                "score": result.score,
            }
        )

    return {
        "answer": answer,
        "sources": sources,
    }