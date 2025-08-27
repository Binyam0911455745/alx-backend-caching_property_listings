import logging
from django.core.cache import cache
from .models import Property

# Set up logging
logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Fetches all properties from the cache or the database.
    """
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all())
        cache.set('all_properties', properties, 3600)  # Cache for 1 hour
    return properties

def get_redis_cache_metrics():
    """
    Retrieves and logs Redis cache hit/miss metrics.
    """
    try:
        # Get the Redis client from the cache backend
        redis_client = cache.get_client()

        # Get metrics from Redis INFO command
        info = redis_client.info()
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)

        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = keyspace_hits / total_requests if total_requests > 0 else 0

        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'hit_ratio': round(hit_ratio, 2)
        }
        
        # Log the metrics
        logger.info(f"Redis Cache Metrics: Hits={metrics['keyspace_hits']}, Misses={metrics['keyspace_misses']}, Hit Ratio={metrics['hit_ratio']}")

        return metrics

    except Exception as e:
        logger.error(f"Failed to get Redis metrics: {e}")
        return {}