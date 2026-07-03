from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
    MatchAny,
)

from app.services.embedding_service import (
    generate_embeddings,
)

from app.services.vector_service import (
    client,
)

COLLECTION_NAME = "document_chunks"


def build_filter(
    tenant_id: int,
    department: str | None = None,
    category: str | None = None,
    source: str | None = None,
    tags: list[str] | None = None,
):
    conditions = []

    # ==========================
    # Tenant Isolation
    # ==========================
    conditions.append(
        FieldCondition(
            key="tenant_id",
            match=MatchValue(
                value=tenant_id,
            ),
        )
    )

    if department:
        conditions.append(
            FieldCondition(
                key="department",
                match=MatchValue(
                    value=department,
                ),
            )
        )

    if category:
        conditions.append(
            FieldCondition(
                key="category",
                match=MatchValue(
                    value=category,
                ),
            )
        )

    if source:
        conditions.append(
            FieldCondition(
                key="source",
                match=MatchValue(
                    value=source,
                ),
            )
        )

    if tags:
        conditions.append(
            FieldCondition(
                key="tags",
                match=MatchAny(
                    any=tags,
                ),
            )
        )

    return Filter(
        must=conditions,
    )


def search_chunks(
    query: str,
    tenant_id: int,
    limit: int = 3,
    department: str | None = None,
    category: str | None = None,
    source: str | None = None,
    tags: list[str] | None = None,
):
    vector = generate_embeddings(
        [query]
    )[0]

    query_filter = build_filter(
        tenant_id=tenant_id,
        department=department,
        category=category,
        source=source,
        tags=tags,
    )

    print("=" * 80)
    print("QUERY:", query)
    print("TENANT:", tenant_id)
    print("DEPARTMENT:", department)
    print("CATEGORY:", category)
    print("SOURCE:", source)
    print("TAGS:", tags)
    print("QUERY FILTER:", query_filter)
    print("=" * 80)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        query_filter=query_filter,
        limit=limit,
        with_payload=True,
    ).points

    print("RESULT COUNT:", len(results))

    for result in results:
        print(result.payload)

    return results