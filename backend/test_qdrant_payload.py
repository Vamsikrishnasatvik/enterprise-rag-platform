from app.services.vector_service import client

results = client.scroll(
    collection_name="document_chunks",
    limit=1,
    with_payload=True,
)

point = results[0][0]

print("=" * 80)
print(point.payload)
print("=" * 80)