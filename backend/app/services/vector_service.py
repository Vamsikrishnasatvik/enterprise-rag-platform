import logging

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.core.config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

COLLECTION_NAME = "document_chunks"
VECTOR_SIZE = 384

# =============================================================================
# Qdrant Client
# =============================================================================

client = QdrantClient(
    url=settings.QDRANT_URL,
)

# =============================================================================
# Collection Management
# =============================================================================


def create_collection() -> None:
    """
    Creates the Qdrant collection if it does not already exist.
    """

    collections = client.get_collections()

    existing_collections = {
        collection.name
        for collection in collections.collections
    }

    if COLLECTION_NAME in existing_collections:

        logger.info(
            "Qdrant collection already exists: %s",
            COLLECTION_NAME,
        )

        return

    logger.info(
        "Creating Qdrant collection: %s",
        COLLECTION_NAME,
    )

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE,
        ),
    )


# =============================================================================
# Vector Storage
# =============================================================================


def upsert_chunks(
    chunk_records,
    embeddings,
) -> None:
    """
    Stores document chunk embeddings in Qdrant.
    """

    if not chunk_records:

        logger.info(
            "No chunks to upsert."
        )

        return

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
                    "tenant_id": chunk.tenant_id,
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

    logger.info(
        "Upserted %d vector(s) into '%s'.",
        len(points),
        COLLECTION_NAME,
    )