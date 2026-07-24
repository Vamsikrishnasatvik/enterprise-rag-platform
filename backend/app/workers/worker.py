from redis import Redis
from rq import Worker, Queue

from app.core.config import settings

redis_conn = Redis.from_url(
    settings.REDIS_URL,
)

worker = Worker(
    [Queue("default", connection=redis_conn)]
)

worker.work()