import logging

from redis import Redis
from rq import Queue

from app.core.config import settings
from app.workers.ingestion_worker import (
    process_ingestion_job,
)

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

INGESTION_QUEUE_NAME = "ingestion"
JOB_TIMEOUT = "30m"

# =============================================================================
# Redis
# =============================================================================


def get_redis_connection() -> Redis:
    """
    Returns a Redis connection used by background queues.
    """

    return Redis.from_url(
        settings.REDIS_URL,
    )


# =============================================================================
# Queue
# =============================================================================


def get_ingestion_queue() -> Queue:
    """
    Returns the ingestion job queue.
    """

    return Queue(
        INGESTION_QUEUE_NAME,
        connection=get_redis_connection(),
    )


# =============================================================================
# Job Scheduling
# =============================================================================


def enqueue_ingestion_job(
    job_id: int,
):
    """
    Enqueues a document ingestion job for background processing.
    """

    logger.info(
        "Enqueuing ingestion job %d.",
        job_id,
    )

    queue = get_ingestion_queue()

    return queue.enqueue(
        process_ingestion_job,
        job_id,
        job_timeout=JOB_TIMEOUT,
    )