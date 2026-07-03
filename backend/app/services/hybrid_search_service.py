from app.services.retrieval_service import (
    search_chunks,
)
from app.services.keyword_search_service import (
    keyword_search,
)
from app.services.query_expansion_service import (
    expand_query,
)

# from app.services.reranker_service import (
#     rerank,
# )


def get_dynamic_limit(
    query: str,
) -> int:
    query = query.lower()

    if any(
        word in query
        for word in [
            "all",
            "list",
            "every",
            "countries",
            "compare",
        ]
    ):
        return 10

    return 5


def is_analytics_query(
    query: str,
):
    query = query.lower()

    keywords = [
        "salary",
        "employee",
        "department",
        "location",
        "count",
        "average",
        "highest",
        "lowest",
        "maximum",
        "minimum",
        "list",
        "all",
        "top",
    ]

    return any(
        word in query
        for word in keywords
    )


def reciprocal_rank_fusion(
    vector_results,
    keyword_results,
    k: int = 60,
):
    scores = {}

    #
    # Vector Results
    #
    for rank, result in enumerate(
        vector_results,
        start=1,
    ):
        chunk_id = result.payload[
            "chunk_id"
        ]

        if chunk_id not in scores:
            scores[chunk_id] = {
                "score": 0,
                "result": result,
            }

        scores[chunk_id]["score"] += (
            1 / (k + rank)
        )

    #
    # Keyword Results
    #
    for rank, item in enumerate(
        keyword_results,
        start=1,
    ):
        chunk = item["chunk"]

        chunk_id = chunk.id

        if chunk_id not in scores:
            payload = {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "content": chunk.content,
                "department": None,
                "category": None,
                "source": None,
                "tags": [],
                "metadata": {},
            }

            class KeywordResult:
                def __init__(self, payload):
                    self.payload = payload

            scores[chunk_id] = {
                "score": 0,
                "result": KeywordResult(
                    payload
                ),
            }

        scores[chunk_id]["score"] += (
            1 / (k + rank)
        )

    return sorted(
        scores.values(),
        key=lambda x: x["score"],
        reverse=True,
    )


def deduplicate_results(
    results,
):
    seen = set()
    unique_results = []

    for item in results:
        payload = item[
            "result"
        ].payload

        key = (
            payload.get(
                "document_id"
            ),
            payload.get(
                "chunk_id"
            ),
        )

        if key in seen:
            continue

        seen.add(key)

        unique_results.append(
            item
        )

    return unique_results


def boost_structured_results(
    query: str,
    results,
):
    if not is_analytics_query(
        query
    ):
        return results

    for item in results:
        payload = item[
            "result"
        ].payload

        document_id = payload.get(
            "document_id"
        )

        #
        # HR CSV document
        #
        if document_id == 22:
            item["score"] += 1

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True,
    )


def hybrid_search(
    db,
    tenant_id: int,
    query: str,
    limit: int | None = None,
    department: str | None = None,
    category: str | None = None,
    source: str | None = None,
    tags: list[str] | None = None,
):
    expanded_query = expand_query(
        query
    )

    if limit is None:
        limit = get_dynamic_limit(
            expanded_query
        )

    retrieval_limit = max(
        limit * 4,
        20,
    )

    print("=" * 80)
    print(
        "EXPANDED QUERY:",
        expanded_query,
    )
    print(
        "RETRIEVAL LIMIT:",
        retrieval_limit,
    )
    print("=" * 80)

    #
    # Vector Search
    #
    vector_results = search_chunks(
        query=expanded_query,
        tenant_id=tenant_id,
        limit=retrieval_limit,
        department=department,
        category=category,
        source=source,
        tags=tags,
    )

    #
    # Clean query for keyword search
    #
    keyword_query = expanded_query.lower()

    for phrase in [
        "list all",
        "show all",
        "what are",
        "which are",
        "give me",
    ]:
        keyword_query = keyword_query.replace(
            phrase,
            ""
        )

    keyword_query = keyword_query.strip()

    #
    # Keyword Search
    #
    keyword_results = keyword_search(
        db=db,
        tenant_id=tenant_id,
        query=keyword_query,
        limit=retrieval_limit,
    )

    print(
        "KEYWORD QUERY:",
        keyword_query,
    )

    print(
        "VECTOR RESULTS:",
        len(vector_results),
    )

    print(
        "KEYWORD RESULTS:",
        len(keyword_results),
    )

    fused_results = (
        reciprocal_rank_fusion(
            vector_results,
            keyword_results,
        )
    )

    fused_results = (
        deduplicate_results(
            fused_results
        )
    )

    fused_results = (
        boost_structured_results(
            expanded_query,
            fused_results,
        )
    )

    print("=" * 80)
    print("FINAL RESULTS")

    for item in fused_results[:20]:
        payload = item[
            "result"
        ].payload

        print(
            payload.get(
                "document_id"
            ),
            item["score"],
        )

    print("=" * 80)

    # Phase 3
    # fused_results = rerank(
    #     expanded_query,
    #     fused_results,
    # )

    return fused_results[
        :limit
    ]