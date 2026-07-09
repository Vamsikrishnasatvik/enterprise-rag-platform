from app.services.retrieval_service import (
    search_chunks,
)

print("=" * 80)
print("METADATA FILTER TEST")
print("=" * 80)

results = search_chunks(
    query="leave policy",
    tenant_id=1,
    metadata_filters={
        "department": "HR",
    },
    limit=3,
)

print(f"Results: {len(results)}")

for chunk in results:
    print(
        chunk["document_id"],
        round(chunk["score"], 4),
    )