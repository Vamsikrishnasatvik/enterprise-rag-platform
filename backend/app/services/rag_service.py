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

from app.graph.graph_builder import graph


def answer_question(
    question: str,
):
    initial_state = {
        "question": question,
        "tenant_id": 0,
        "user_id": 0,
        "conversation_id": None,
        "rewritten_query": None,
        "intent": None,
        "entities": [],
        "metadata_filters": {},
        "execution_plan": {},
        "retrieved_chunks": [],
        "context": None,
        "confidence_score": 0.0,
        "needs_retry": False,
        "answer": None,
        "citations": [],
        "execution_trace": [],
    }

    final_state = graph.invoke(initial_state)
    print(final_state["execution_trace"])

    return {
        "answer": final_state["answer"],
        "sources": final_state["retrieved_chunks"],
    }


def answer_conversation_question(
    db,
    conversation_id: int,
    question: str,
):
    history = build_chat_history(
        db,
        conversation_id,
    )

    results = search_chunks(
        question
    )

    context = build_context(
        results
    )

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