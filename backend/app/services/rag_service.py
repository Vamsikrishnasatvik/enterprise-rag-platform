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
):
    results = search_chunks(
        question
    )

    context = build_context(
        results
    )

    answer = generate_answer(
        question,
        context,
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