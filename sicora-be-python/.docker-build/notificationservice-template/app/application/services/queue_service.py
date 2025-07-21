"""
Servicio de cola asíncrona para NotificationService
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import aioredis

logger = logging.getLogger(__name__)

class QueueService:
    """Servicio de cola para notificaciones asíncronas."""

    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis: Optional[aioredis.Redis] = None
        self.queue_name = "notification_queue"
        self.dead_letter_queue = "notification_dlq"

    async def init_redis(self):
        """Inicializar conexión Redis."""
        self.redis = await aioredis.from_url(self.redis_url)

    async def enqueue_notification(
        self,
        notification_data: Dict[str, Any]
    ) -> bool:
        """Encolar notificación para procesamiento asíncrono."""
        try:
            if not self.redis:
                await self.init_redis()

            # Agregar timestamp
            notification_data['queued_at'] = datetime.utcnow().isoformat()
            notification_data['retry_count'] = 0

            await self.redis.lpush(
                self.queue_name,
                json.dumps(notification_data)
            )

            logger.info(f"Notificación encolada: {notification_data.get('type', 'unknown')}")
            return True

        except Exception as e:
            logger.error(f"Error encolando notificación: {str(e)}")
            return False

    async def process_queue(self):
        """Procesamiento continuo de la cola."""
        if not self.redis:
            await self.init_redis()

        logger.info("Iniciando procesamiento de cola de notificaciones")

        while True:
            try:
                # Obtener notificación de la cola
                result = await self.redis.brpop(self.queue_name, timeout=5)

                if result:
                    queue_name, notification_json = result
                    notification_data = json.loads(notification_json)

                    # Procesar notificación
                    success = await self._process_notification(notification_data)

                    if not success:
                        # Mover a dead letter queue si falla
                        await self._handle_failed_notification(notification_data)

            except Exception as e:
                logger.error(f"Error procesando cola: {str(e)}")
                await asyncio.sleep(1)

    async def _process_notification(self, data: Dict[str, Any]) -> bool:
        """Procesar una notificación individual."""
        # Aquí iría la lógica de procesamiento real
        logger.info(f"Procesando notificación: {data}")
        return True

    async def _handle_failed_notification(self, data: Dict[str, Any]):
        """Manejar notificación fallida."""
        data['failed_at'] = datetime.utcnow().isoformat()
        await self.redis.lpush(
            self.dead_letter_queue,
            json.dumps(data)
        )
        logger.warning(f"Notificación movida a DLQ: {data}")
