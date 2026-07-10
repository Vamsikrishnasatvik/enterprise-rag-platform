from app.services.context_compression_service import (
    compress_context,
)


def test_context_compression():

    chunks = [
        {
            "chunk_id": 1,
            "content": "A" * 200,
            "score": 0.95,
        },
        {
            "chunk_id": 2,
            "content": "B" * 200,
            "score": 0.90,
        },
        {
            "chunk_id": 3,
            "content": "A" * 200,   # duplicate
            "score": 0.85,
        },
        {
            "chunk_id": 4,
            "content": "short",
            "score": 0.99,
        },
    ]

    compressed = compress_context(
        chunks,
        max_chunks=6,
        min_length=100,
    )

    # Duplicate removed
    assert len(compressed) == 2

    # Highest scored chunk remains first
    assert compressed[0]["chunk_id"] == 1

    # No short chunks
    assert all(
        len(chunk["content"]) >= 100
        for chunk in compressed
    )