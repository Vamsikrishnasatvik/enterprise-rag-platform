from app.services.retrieval_orchestrator import (
    retrieve_documents,
)

print("=" * 80)
print("MULTI QUERY RETRIEVAL")
print("=" * 80)

results = retrieve_documents(
    question="What is the HR Leave Policy?",
    tenant_id=1,
    limit=3,
    strategy="multi_query",
)

for chunk in results:

    print(
        chunk["chunk_id"],
        round(chunk["score"], 4),
    )