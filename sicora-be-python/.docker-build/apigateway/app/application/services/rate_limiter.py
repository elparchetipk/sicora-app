"""
Servicio de rate limiting para APIGateway
"""

import aioredis
import time
from typing import Optional
import os

class RateLimiter:
    """Servicio de rate limiting usando Redis."""

    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis: Optional[aioredis.Redis] = None

    async def init_redis(self):
        """Inicializar conexión Redis."""
        self.redis = await aioredis.from_url(self.redis_url)

    async def is_allowed(
        self,
        key: str,
        limit: int = 100,
        window: int = 3600
    ) -> bool:
        """
        Verificar si la request está permitida.

        Args:
            key: Clave única (user_id, ip, etc.)
            limit: Número máximo de requests
            window: Ventana de tiempo en segundos
        """
        if not self.redis:
            await self.init_redis()

        current_time = int(time.time())
        window_start = current_time - window

        # Limpiar requests antiguas
        await self.redis.zremrangebyscore(key, 0, window_start)

        # Contar requests actuales
        current_requests = await self.redis.zcard(key)

        if current_requests >= limit:
            return False

        # Agregar request actual
        await self.redis.zadd(key, {str(current_time): current_time})
        await self.redis.expire(key, window)

        return True

    async def get_remaining(
        self,
        key: str,
        limit: int = 100
    ) -> int:
        """Obtener número de requests restantes."""
        if not self.redis:
            return limit

        current_requests = await self.redis.zcard(key)
        return max(0, limit - current_requests)
