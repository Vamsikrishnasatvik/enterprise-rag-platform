from app.services.retrieval_orchestrator import (
    retrieve_documents,
)


def test_semantic_retrieval():

    results = retrieve_documents(
        question="What is the HR Leave Policy?",
        tenant_id=1,
        strategy="semantic",
        limit=5,
    )

    assert isinstance(results, list)
    assert len(results) > 0

    first = results[0]

    assert "chunk_id" in first
    assert "content" in first
    assert "score" in first


def test_hybrid_retrieval():

    results = retrieve_documents(
        question="What is the HR Leave Policy?",
        tenant_id=1,
        strategy="hybrid",
        limit=5,
    )

    assert isinstance(results, list)
    assert len(results) > 0


def test_multi_query_retrieval():

    results = retrieve_documents(
        question="Explain the HR Leave Policy",
        tenant_id=1,
        strategy="multi_query",
        limit=5,
    )

    assert isinstance(results, list)
    assert len(results) > 0