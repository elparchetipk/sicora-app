"""
Proveedor de SMS para NotificationService
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class SMSProvider:
    """Proveedor de notificaciones por SMS (Mock para desarrollo)."""

    def __init__(self):
        self.api_key = os.getenv("SMS_API_KEY", "")
        self.enabled = os.getenv("SMS_ENABLED", "false").lower() == "true"

    async def send_notification(
        self,
        to_phone: str,
        message: str
    ) -> bool:
        """Enviar notificación por SMS."""
        try:
            if not self.enabled:
                logger.info(f"SMS Mock: Enviando a {to_phone}: {message}")
                return True

            # Aquí iría la integración real con Twilio, AWS SNS, etc.
            # Por ahora es un mock para desarrollo

            logger.info(f"SMS enviado exitosamente a {to_phone}")
            return True

        except Exception as e:
            logger.error(f"Error enviando SMS a {to_phone}: {str(e)}")
            return False
