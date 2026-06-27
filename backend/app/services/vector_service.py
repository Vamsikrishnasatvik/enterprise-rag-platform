from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

from app.core.config import settings

COLLECTION_NAME = "document_chunks"
VECTOR_SIZE = 384

client = QdrantClient(
    url=settings.QDRANT_URL,
)


def create_collection():
    collections = client.get_collections()

    names = [
        c.name
        for c in collections.collections
    ]

    if COLLECTION_NAME in names:
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE,
        ),
    )


def upsert_chunks(
    chunk_records,
    embeddings,
):
    points = []

    for chunk, vector in zip(
        chunk_records,
        embeddings,
    ):
        points.append(
            PointStruct(
                id=chunk.id,
                vector=vector,
                payload={
                    "chunk_id": chunk.id,
                    "document_id": chunk.document_id,
                    "content": chunk.content,
                    "metadata": (
                        chunk.chunk_metadata
                        or {}
                    ),
                },
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )