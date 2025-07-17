"""Notification Service adapter."""

from uuid import UUID
from typing import Dict, Any
import httpx

from ...application.interfaces import NotificationServiceInterface


class NotificationServiceAdapter(NotificationServiceInterface):
    """
    Adaptador para servicio de notificaciones.
    
    Responsabilidades:
    - Implementar interfaz de NotificationService
    - Enviar notificaciones a usuarios del sistema
    - Manejar diferentes tipos de notificaciones
    """
    
    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient()
    
    async def send_period_start_notification(
        self, 
        period_id: UUID, 
        period_name: str,
        target_users: list
    ) -> bool:
        """
        Enviar notificación de inicio de período de evaluación.
        
        Args:
            period_id: ID del período
            period_name: Nombre del período
            target_users: Lista de usuarios objetivo
            
        Returns:
            bool: True si se envió correctamente
        """
        try:
            payload = {
                "type": "period_start",
                "title": "Nuevo período de evaluación disponible",
                "message": f"Ha comenzado el período de evaluación: {period_name}",
                "metadata": {
                    "period_id": str(period_id),
                    "period_name": period_name
                },
                "target_users": [str(user_id) for user_id in target_users]
            }
            
            response = await self._client.post(
                f"{self._base_url}/api/v1/notifications",
                json=payload
            )
            
            return response.status_code == 201
            
        except httpx.RequestError as e:
            print(f"Error al enviar notificación: {e}")
            return False
    
    async def send_period_end_notification(
        self, 
        period_id: UUID, 
        period_name: str,
        target_users: list
    ) -> bool:
        """
        Enviar notificación de fin de período de evaluación.
        
        Args:
            period_id: ID del período
            period_name: Nombre del período
            target_users: Lista de usuarios objetivo
            
        Returns:
            bool: True si se envió correctamente
        """
        try:
            payload = {
                "type": "period_end",
                "title": "Período de evaluación próximo a finalizar",
                "message": f"El período de evaluación '{period_name}' finalizará pronto. Completa tus evaluaciones pendientes.",
                "metadata": {
                    "period_id": str(period_id),
                    "period_name": period_name
                },
                "target_users": [str(user_id) for user_id in target_users]
            }
            
            response = await self._client.post(
                f"{self._base_url}/api/v1/notifications",
                json=payload
            )
            
            return response.status_code == 201
            
        except httpx.RequestError as e:
            print(f"Error al enviar notificación: {e}")
            return False
    
    async def send_period_closed_notification(
        self, 
        period_id: UUID, 
        period_name: str
    ) -> bool:
        """
        Enviar notificación de cierre de período a administradores.
        
        Args:
            period_id: ID del período
            period_name: Nombre del período
            
        Returns:
            bool: True si se envió correctamente
        """
        try:
            payload = {
                "type": "period_closed",
                "title": "Período de evaluación cerrado",
                "message": f"El período de evaluación '{period_name}' ha sido cerrado y está listo para generar reportes.",
                "metadata": {
                    "period_id": str(period_id),
                    "period_name": period_name
                },
                "target_roles": ["admin", "coordinator"]
            }
            
            response = await self._client.post(
                f"{self._base_url}/api/v1/notifications",
                json=payload
            )
            
            return response.status_code == 201
            
        except httpx.RequestError as e:
            print(f"Error al enviar notificación: {e}")
            return False
    
    async def send_evaluation_submitted_notification(
        self, 
        evaluation_id: UUID,
        student_id: UUID,
        instructor_id: UUID
    ) -> bool:
        """
        Enviar notificación de evaluación enviada.
        
        Args:
            evaluation_id: ID de la evaluación
            student_id: ID del estudiante
            instructor_id: ID del instructor
            
        Returns:
            bool: True si se envió correctamente
        """
        try:
            payload = {
                "type": "evaluation_submitted",
                "title": "Evaluación recibida",
                "message": "Se ha recibido una nueva evaluación.",
                "metadata": {
                    "evaluation_id": str(evaluation_id),
                    "student_id": str(student_id),
                    "instructor_id": str(instructor_id)
                },
                "target_roles": ["admin", "coordinator"]
            }
            
            response = await self._client.post(
                f"{self._base_url}/api/v1/notifications",
                json=payload
            )
            
            return response.status_code == 201
            
        except httpx.RequestError as e:
            print(f"Error al enviar notificación: {e}")
            return False
    
    async def close(self):
        """Cerrar el cliente HTTP."""
        await self._client.aclose()
