from app.services.vector_service import client

points, _ = client.scroll(
    collection_name="document_chunks",
    limit=3000,
    with_payload=True,
)

found = False

for point in points:
    if point.payload["document_id"] == 24:
        found = True
        print("=" * 80)
        print(point.payload)
        print("=" * 80)
        break

if not found:
    print("Document 24 not found.")