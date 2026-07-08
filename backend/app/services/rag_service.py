from app.graph.graph_builder import graph

from app.db.session import SessionLocal

from app.services.conversation_service import (
    create_conversation,
)

from app.services.message_service import (
    save_user_message,
    save_assistant_message,
    build_chat_history,
)

from app.services.retrieval_service import (
    search_chunks,
)

from app.services.context_service import (
    build_context,
)

from app.services.llm_service import (
    generate_answer,
)


def answer_question(
    question: str,
    conversation_id: int | None = None,
):
    db = SessionLocal()

    try:

        # Temporary values until authentication is integrated
        tenant_id = 1
        user_id = 1

        # Create a new conversation if needed
        if conversation_id is None:

            conversation = create_conversation(
                db=db,
                tenant_id=tenant_id,
                title=question[:50],
            )

            conversation_id = conversation.id

        # Save the user's message
        save_user_message(
            db=db,
            conversation_id=conversation_id,
            content=question,
            tenant_id=tenant_id,
        )

        initial_state = {
            # Request
            "question": question,
            "tenant_id": tenant_id,
            "user_id": user_id,
            "conversation_id": conversation_id,

            # Query Understanding
            "rewritten_query": None,
            "intent": None,
            "entities": [],

            # Planning
            "metadata_filters": {},

            "execution_plan": {
                "search_strategy": "semantic",
                "retrieval_count": 3,
                "use_metadata_filters": False,
                "use_memory": True,
                "requires_reranking": False,
                "requires_verification": False,
                "multi_document": False,
            },

            # Retrieval
            "search_limit": 3,
            "use_metadata_filters": False,
            "retrieval_strategy": "semantic",

            "retrieved_chunks": [],
            "reranked_chunks": [],
            "evidence_chunks": [],
            "context": None,

            # Conversation Memory
            "chat_history": [],

            # Verification
            "confidence_score": 0.0,
            "needs_retry": False,
            "verification_reason": None,
            "retrieval_attempts": 0,
            "max_retrieval_attempts": 2,

            # Final Response
            "answer": None,
            "citations": [],

            # Monitoring
            "execution_trace": [],
        }

        print("=" * 80)
        print("INITIAL STATE")
        print(initial_state)
        print("=" * 80)

        final_state = graph.invoke(initial_state)

        print("=" * 80)
        print("EXECUTION TRACE")
        print(final_state["execution_trace"])
        print("=" * 80)

        # Save assistant response
        save_assistant_message(
            db=db,
            conversation_id=conversation_id,
            content=final_state["answer"],
            tenant_id=tenant_id,
        )

        return {
            "conversation_id": conversation_id,
            "answer": final_state["answer"],
            "sources": final_state["evidence_chunks"],
            "execution_trace": final_state["execution_trace"],
        }

    finally:
        db.close()


def answer_conversation_question(
    db,
    conversation_id: int,
    question: str,
):
    """
    Legacy helper.

    Can be removed once all conversation handling
    goes through the LangGraph workflow.
    """

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