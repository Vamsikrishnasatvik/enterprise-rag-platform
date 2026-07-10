from app.services.retrieval_orchestrator import (
    retrieve_documents,
)

from app.services.context_compression_service import (
    compress_context,
)

results = retrieve_documents(
    question="Explain the HR Leave Policy",
    tenant_id=1,
    strategy="multi_query",
    limit=10,
)

print("=" * 80)
print("BEFORE")
print(len(results))

compressed = compress_context(results)

print("AFTER")
print(len(compressed))
print("=" * 80)

for chunk in compressed:

    print(
        chunk["chunk_id"],
        round(
            chunk["score"],
            4,
        ),
    )