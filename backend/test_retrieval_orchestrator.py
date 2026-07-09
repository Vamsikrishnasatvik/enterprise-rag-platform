from app.db.session import SessionLocal

from app.services.retrieval_orchestrator import (
    retrieve_documents,
)

print("=" * 80)
print("SEMANTIC")
print("=" * 80)

semantic = retrieve_documents(
    question="leave policy",
    tenant_id=1,
    limit=3,
    strategy="semantic",
)

for chunk in semantic:
    print(chunk["chunk_id"], chunk["score"])

print()

print("=" * 80)
print("BM25")
print("=" * 80)

bm25 = retrieve_documents(
    question="leave policy",
    tenant_id=1,
    limit=3,
    strategy="bm25",
)

for chunk in bm25:
    print(chunk["chunk_id"], chunk["score"])

print()

print("=" * 80)
print("HYBRID")
print("=" * 80)

hybrid = retrieve_documents(
    question="leave policy",
    tenant_id=1,
    limit=5,
    strategy="hybrid",
)

for chunk in hybrid:
    print(chunk["chunk_id"], chunk["score"])