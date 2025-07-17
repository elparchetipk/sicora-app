"""Interface for Notification Service."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from uuid import UUID


class NotificationServiceInterface(ABC):
    """
    Interface para servicio de notificaciones.
    Define el contrato para envío de notificaciones y recordatorios.
    """
    
    @abstractmethod
    async def send_period_notification(
        self, 
        recipients: List[UUID],
        period_name: str,
        period_end_date: str,
        template_data: Dict
    ) -> Dict:
        """Envía notificación de nuevo período de evaluación."""
        pass
    
    @abstractmethod
    async def send_reminder_notification(
        self,
        recipients: List[UUID],
        ficha_id: str,
        custom_message: Optional[str] = None
    ) -> Dict:
        """Envía recordatorio de evaluaciones pendientes."""
        pass
    
    @abstractmethod
    async def send_evaluation_completed_notification(
        self,
        instructor_id: UUID,
        student_name: str,
        evaluation_details: Dict
    ) -> Dict:
        """Envía notificación de evaluación completada al instructor."""
        pass
    
    @abstractmethod
    async def send_bulk_notification(
        self,
        recipients: List[UUID],
        message: str,
        notification_type: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Envía notificación masiva a múltiples destinatarios."""
        pass
    
    @abstractmethod
    async def get_notification_status(self, notification_id: str) -> Optional[Dict]:
        """Obtiene el estado de una notificación enviada."""
        pass
    
    @abstractmethod
    async def validate_recipients(self, recipient_ids: List[UUID]) -> List[UUID]:
        """Valida y filtra destinatarios válidos para notificaciones."""
        pass
