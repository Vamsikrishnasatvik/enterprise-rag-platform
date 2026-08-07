import logging

from redis import Redis
from rq import Queue

from app.core.config import settings

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

DEFAULT_QUEUE_NAME = "default"

# =============================================================================
# Redis Connection
# =============================================================================

logger.info(
    "Initializing Redis connection for background queue."
)

redis_conn = Redis.from_url(
    settings.REDIS_URL,
)

# =============================================================================
# Background Queue
# =============================================================================

queue = Queue(
    DEFAULT_QUEUE_NAME,
    connection=redis_conn,
)

logger.info(
    "Background queue initialized: %s",
    DEFAULT_QUEUE_NAME,
)