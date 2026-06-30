from redis import Redis
from rq import Queue

from app.core.config import settings
from app.workers.ingestion_worker import (
    process_ingestion_job,
)


def get_redis_connection():
    return Redis.from_url(
        settings.REDIS_URL
    )


def get_ingestion_queue():
    redis_conn = get_redis_connection()

    return Queue(
        "ingestion",
        connection=redis_conn,
    )


def enqueue_ingestion_job(
    job_id: int,
):
    queue = get_ingestion_queue()

    return queue.enqueue(
        process_ingestion_job,
        job_id,
        job_timeout="30m",
    )