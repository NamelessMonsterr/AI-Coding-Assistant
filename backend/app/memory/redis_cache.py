"""
Redis caching layer for performance optimization
"""
import redis
import json
import hashlib
from typing import Any, Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class RedisCache:
    """Redis-based caching for LLM responses and session data"""
    
    def __init__(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                password=settings.redis_password,
                decode_responses=True,
                socket_connect_timeout=5
            )
            self.redis_client.ping()
            logger.info("✅ Redis cache initialized successfully")
            self.enabled = True
        except Exception as e:
            logger.warning(f"Redis connection failed: {str(e)}. Caching disabled.")
            self.enabled = False
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate unique cache key"""
        key_data = f"{args}{kwargs}"
        key_hash = hashlib.md5(key_data.encode()).hexdigest()
        return f"{prefix}:{key_hash}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.enabled:
            return None
        try:
            value = self.redis_client.get(key)
            if value:
                logger.debug(f"Cache HIT: {key}")
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache with TTL (default: 1 hour)"""
        if not self.enabled:
            return
        try:
            self.redis_client.setex(key, ttl, json.dumps(value, default=str))
            logger.debug(f"Cache SET: {key}")
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}")
    
    def delete(self, key: str):
        """Delete key from cache"""
        if not self.enabled:
            return
        try:
            self.redis_client.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}")
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        if not self.enabled:
            return {"enabled": False}
        try:
            info = self.redis_client.info('stats')
            hits = info.get('keyspace_hits', 0)
            misses = info.get('keyspace_misses', 0)
            total = hits + misses
            hit_rate = round((hits / total * 100), 2) if total > 0 else 0.0
            return {
                "enabled": True,
                "keyspace_hits": hits,
                "keyspace_misses": misses,
                "hit_rate": hit_rate
            }
        except Exception as e:
            return {"enabled": True, "error": str(e)}


# Global cache instance
cache = RedisCache()
