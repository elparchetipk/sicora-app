"""Redis adapter implementation for caching operations."""

import json
import pickle
from typing import Any, Optional, List, Dict
from datetime import timedelta
import redis.asyncio as redis

from app.application.interfaces.cache_interface import CacheInterface
from app.domain.exceptions.ai_exceptions import CacheError


class RedisAdapter(CacheInterface):
    """Redis cache adapter implementation."""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        decode_responses: bool = False,
        max_connections: int = 10,
        key_prefix: str = "aiservice:"
    ):
        """Initialize Redis adapter."""
        try:
            self.redis_pool = redis.ConnectionPool(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=decode_responses,
                max_connections=max_connections
            )
            self.key_prefix = key_prefix
            
        except Exception as e:
            raise CacheError(f"Failed to initialize Redis: {str(e)}")
    
    async def _get_client(self) -> redis.Redis:
        """Get Redis client from pool."""
        return redis.Redis(connection_pool=self.redis_pool)
    
    def _make_key(self, key: str) -> str:
        """Add prefix to key."""
        return f"{self.key_prefix}{key}"
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache."""
        try:
            client = await self._get_client()
            prefixed_key = self._make_key(key)
            
            value = await client.get(prefixed_key)
            if value is None:
                return None
            
            # Try to deserialize as JSON first, then pickle
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                try:
                    return pickle.loads(value)
                except (pickle.PickleError, TypeError):
                    return value.decode('utf-8') if isinstance(value, bytes) else value
                    
        except Exception as e:
            raise CacheError(f"Failed to get key '{key}' from Redis: {str(e)}")
        finally:
            await client.aclose()
    
    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[timedelta] = None
    ) -> bool:
        """Set value in Redis cache with optional expiration."""
        try:
            client = await self._get_client()
            prefixed_key = self._make_key(key)
            
            # Serialize value
            if isinstance(value, (dict, list, tuple)):
                serialized_value = json.dumps(value)
            elif isinstance(value, str):
                serialized_value = value
            else:
                serialized_value = pickle.dumps(value)
            
            # Set value with optional expiration
            if expire:
                result = await client.setex(
                    prefixed_key,
                    expire,
                    serialized_value
                )
            else:
                result = await client.set(prefixed_key, serialized_value)
            
            return bool(result)
            
        except Exception as e:
            raise CacheError(f"Failed to set key '{key}' in Redis: {str(e)}")
        finally:
            await client.aclose()
    
    async def delete(self, key: str) -> bool:
        """Delete value from Redis cache."""
        try:
            client = await self._get_client()
            prefixed_key = self._make_key(key)
            
            result = await client.delete(prefixed_key)
            return bool(result)
            
        except Exception as e:
            raise CacheError(f"Failed to delete key '{key}' from Redis: {str(e)}")
        finally:
            await client.aclose()
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis cache."""
        try:
            client = await self._get_client()
            prefixed_key = self._make_key(key)
            
            result = await client.exists(prefixed_key)
            return bool(result)
            
        except Exception as e:
            raise CacheError(f"Failed to check existence of key '{key}' in Redis: {str(e)}")
        finally:
            await client.aclose()
    
    async def expire(self, key: str, expire: timedelta) -> bool:
        """Set expiration for existing key in Redis."""
        try:
            client = await self._get_client()
            prefixed_key = self._make_key(key)
            
            result = await client.expire(prefixed_key, expire)
            return bool(result)
            
        except Exception as e:
            raise CacheError(f"Failed to set expiration for key '{key}' in Redis: {str(e)}")
        finally:
            await client.aclose()
    
    async def get_many(self, keys: List[str]) -> List[Optional[Any]]:
        """Get multiple values from Redis cache."""
        try:
            client = await self._get_client()
            prefixed_keys = [self._make_key(key) for key in keys]
            
            values = await client.mget(prefixed_keys)
            
            results = []
            for value in values:
                if value is None:
                    results.append(None)
                    continue
                
                # Try to deserialize
                try:
                    results.append(json.loads(value))
                except (json.JSONDecodeError, TypeError):
                    try:
                        results.append(pickle.loads(value))
                    except (pickle.PickleError, TypeError):
                        results.append(value.decode('utf-8') if isinstance(value, bytes) else value)
            
            return results
            
        except Exception as e:
            raise CacheError(f"Failed to get multiple keys from Redis: {str(e)}")
        finally:
            await client.aclose()
    
    async def set_many(
        self,
        mapping: dict,
        expire: Optional[timedelta] = None
    ) -> bool:
        """Set multiple values in Redis cache."""
        try:
            client = await self._get_client()
            
            # Prepare data for mset
            prefixed_mapping = {}
            for key, value in mapping.items():
                prefixed_key = self._make_key(key)
                
                # Serialize value
                if isinstance(value, (dict, list, tuple)):
                    serialized_value = json.dumps(value)
                elif isinstance(value, str):
                    serialized_value = value
                else:
                    serialized_value = pickle.dumps(value)
                
                prefixed_mapping[prefixed_key] = serialized_value
            
            # Set all values
            result = await client.mset(prefixed_mapping)
            
            # Set expiration if specified
            if expire and result:
                for prefixed_key in prefixed_mapping.keys():
                    await client.expire(prefixed_key, expire)
            
            return bool(result)
            
        except Exception as e:
            raise CacheError(f"Failed to set multiple keys in Redis: {str(e)}")
        finally:
            await client.aclose()
    
    async def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching a pattern."""
        try:
            client = await self._get_client()
            prefixed_pattern = self._make_key(pattern)
            
            keys = await client.keys(prefixed_pattern)
            if keys:
                return await client.delete(*keys)
            return 0
            
        except Exception as e:
            raise CacheError(f"Failed to clear pattern '{pattern}' from Redis: {str(e)}")
        finally:
            await client.aclose()
    
    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment a numeric value in Redis."""
        try:
            client = await self._get_client()
            prefixed_key = self._make_key(key)
            
            result = await client.incrby(prefixed_key, amount)
            return result
            
        except Exception as e:
            raise CacheError(f"Failed to increment key '{key}' in Redis: {str(e)}")
        finally:
            await client.aclose()
    
    async def decrement(self, key: str, amount: int = 1) -> int:
        """Decrement a numeric value in Redis."""
        try:
            client = await self._get_client()
            prefixed_key = self._make_key(key)
            
            result = await client.decrby(prefixed_key, amount)
            return result
            
        except Exception as e:
            raise CacheError(f"Failed to decrement key '{key}' in Redis: {str(e)}")
        finally:
            await client.aclose()
    
    async def get_ttl(self, key: str) -> int:
        """Get time to live for a key in seconds."""
        try:
            client = await self._get_client()
            prefixed_key = self._make_key(key)
            
            ttl = await client.ttl(prefixed_key)
            return ttl
            
        except Exception as e:
            raise CacheError(f"Failed to get TTL for key '{key}' in Redis: {str(e)}")
        finally:
            await client.aclose()
    
    async def health_check(self) -> bool:
        """Check Redis connection health."""
        try:
            client = await self._get_client()
            await client.ping()
            return True
            
        except Exception:
            return False
        finally:
            await client.aclose()
    
    async def get_info(self) -> Dict[str, Any]:
        """Get Redis server information."""
        try:
            client = await self._get_client()
            info = await client.info()
            return info
            
        except Exception as e:
            raise CacheError(f"Failed to get Redis info: {str(e)}")
        finally:
            await client.aclose()
