from app.services.vector_service import client

print("=" * 80)

print(client.get_collections())

print("=" * 80)

info = client.get_collection("document_chunks")

print(info)

print("=" * 80)

points, _ = client.scroll(
    collection_name="document_chunks",
    limit=5,
    with_payload=True,
)

print(f"Returned {len(points)} points")

print("=" * 80)