from app.services.multi_query_service import (
    generate_multi_queries,
)


def test_multi_query_generation():

    queries = generate_multi_queries(
        "What is the HR Leave Policy?"
    )

    assert isinstance(
        queries,
        list,
    )

    assert len(queries) >= 4

    assert all(
        isinstance(query, str)
        for query in queries
    )

    assert all(
        len(query.strip()) > 0
        for query in queries
    )

    # Original query should normally appear
    assert any(
        "leave" in query.lower()
        for query in queries
    )