from app.services.self_query_service import (
    generate_self_query,
)


def test_self_query_generation():

    result = generate_self_query(
        "Show HR Leave Policies from 2024"
    )

    assert isinstance(
        result,
        dict,
    )

    assert "query" in result

    assert "metadata_filters" in result

    assert isinstance(
        result["query"],
        str,
    )

    assert isinstance(
        result["metadata_filters"],
        dict,
    )

    assert len(
        result["query"]
    ) > 0