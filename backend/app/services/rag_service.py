from app.services.hybrid_search_service import (
    hybrid_search,
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


def answer_question(
    db,
    tenant_id: int,
    question: str,
    department: str | None = None,
    category: str | None = None,
    source: str | None = None,
    tags: list[str] | None = None,
):
    results = hybrid_search(
        db=db,
        tenant_id=tenant_id,
        query=question,
        department=department,
        category=category,
        source=source,
        tags=tags,
    )

    search_results = [
        item["result"]
        for item in results
    ]

    context = build_context(
        search_results
    )

    answer = generate_answer(
        question,
        context,
    )

    sources = []

    for item in results:
        result = item["result"]

        sources.append(
            {
                "chunk_id": result.payload[
                    "chunk_id"
                ],
                "document_id": result.payload[
                    "document_id"
                ],
                "content": result.payload[
                    "content"
                ],
                "score": item["score"],
            }
        )

    return {
        "answer": answer,
        "sources": sources,
    }


def answer_conversation_question(
    db,
    tenant_id: int,
    conversation_id: int,
    question: str,
    department: str | None = None,
    category: str | None = None,
    source: str | None = None,
    tags: list[str] | None = None,
):
    history = build_chat_history(
        db,
        conversation_id,
    )

    results = hybrid_search(
        db=db,
        tenant_id=tenant_id,
        query=question,
        department=department,
        category=category,
        source=source,
        tags=tags,
    )

    search_results = [
        item["result"]
        for item in results
    ]

    context = build_context(
        search_results
    )

    answer = generate_answer(
        question,
        context,
        history,
    )

    sources = []

    for item in results:
        result = item["result"]

        sources.append(
            {
                "chunk_id": result.payload[
                    "chunk_id"
                ],
                "document_id": result.payload[
                    "document_id"
                ],
                "content": result.payload[
                    "content"
                ],
                "score": item["score"],
            }
        )

    return {
        "answer": answer,
        "sources": sources,
    }