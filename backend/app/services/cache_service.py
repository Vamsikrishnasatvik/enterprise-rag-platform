import json
import redis

redis_client = redis.Redis(
    host="enterprise_redis",
    port=6379,
    decode_responses=True,
)


def get_cache(key: str):
    value = redis_client.get(key)

    if value:
        return json.loads(value)

    return None


def set_cache(
    key: str,
    value,
    ttl: int = 3600,
):
    redis_client.setex(
        key,
        ttl,
        json.dumps(value),
    )


def delete_cache(key: str):
    redis_client.delete(key)