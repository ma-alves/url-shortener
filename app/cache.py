import redis
from redis.cache import CacheConfig

from .settings import Settings
import logging

logger = logging.getLogger(__name__)

redis_client = redis.Redis(
    protocol=3,
    cache_config=CacheConfig(),
    decode_responses=True,
    host=Settings().redis_host,
    port=Settings().redis_port,
    db=Settings().redis_db,
)


def get_cached_code(key):
    try:
        data = redis_client.get(key)
        if data:
            logger.info(f"Cache hit for key: {key}")
        else:
            logger.info(f"Cache miss for key: {key}")
        return data
    except redis.RedisError as e:
        logger.error(f"Error accessing Redis: {str(e)}")
        return None


def set_cached_data(key, value):
    redis_client.set(key, value)
    logger.info(f"Data cached for key: {key}")
