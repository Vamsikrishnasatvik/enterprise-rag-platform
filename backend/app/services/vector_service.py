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
    """
    Store document chunks in Qdrant.

    Rich metadata is flattened into the payload
    for efficient filtering while preserving the
    original metadata object.
    """

    points = []

    for chunk, vector in zip(
        chunk_records,
        embeddings,
    ):

        metadata = (
            chunk.chunk_metadata
            or {}
        )

        payload = {
            "tenant_id": chunk.tenant_id,
            "chunk_id": chunk.id,
            "document_id": chunk.document_id,
            "content": chunk.content,

            # Rich metadata fields
            "department": metadata.get(
                "department",
                "",
            ),
            "document_type": metadata.get(
                "document_type",
                "",
            ),
            "version": metadata.get(
                "version",
                "",
            ),
            "effective_date": metadata.get(
                "effective_date",
                "",
            ),
            "owner": metadata.get(
                "owner",
                "",
            ),
            "classification": metadata.get(
                "classification",
                "",
            ),
            "tags": metadata.get(
                "tags",
                [],
            ),

            # Keep original metadata
            "metadata": metadata,
        }

        points.append(
            PointStruct(
                id=chunk.id,
                vector=vector,
                payload=payload,
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )