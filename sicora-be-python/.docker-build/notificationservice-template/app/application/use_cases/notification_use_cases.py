"""
Casos de uso para las operaciones de notificaciones.

Implementa la lógica de negocio para crear, obtener y actualizar notificaciones,
utilizando la interfaz del repositorio definida en la capa de dominio.
"""

from typing import Optional, Tuple, List

from app.domain.entities.notification import Notification, InvalidNotificationDataError
from app.domain.repositories.notification_repository import NotificationRepository
from app.domain.value_objects.notification_type import NotificationType
from app.application.dtos.notification_dtos import (
    CreateNotificationDTO,
    NotificationDTO,
    NotificationListDTO,
    NotificationFilterDTO,
    MarkAsReadDTO
)


class NotificationUseCases:
    """
    Casos de uso para las operaciones de notificaciones.
    
    Implementa la lógica de negocio para crear, obtener y actualizar notificaciones,
    utilizando el repositorio de notificaciones.
    """
    
    def __init__(self, notification_repository: NotificationRepository):
        """
        Inicializa los casos de uso con el repositorio de notificaciones.
        
        Args:
            notification_repository: Implementación del repositorio de notificaciones
        """
        self.notification_repository = notification_repository
    
    async def create_notification(self, dto: CreateNotificationDTO) -> NotificationDTO:
        """
        Crea una nueva notificación.
        
        Args:
            dto: DTO con los datos de la notificación a crear
            
        Returns:
            DTO con los datos de la notificación creada
            
        Raises:
            InvalidNotificationDataError: Si los datos de la notificación son inválidos
        """
        try:
            # Crear entidad de dominio
            notification = Notification(
                user_id=dto.user_id,
                title=dto.title,
                message=dto.message,
                notification_type=dto.type
            )
            
            # Guardar en el repositorio
            created_notification = await self.notification_repository.create(notification)
            
            # Convertir a DTO
            return NotificationDTO(
                id=created_notification.id,
                user_id=created_notification.user_id,
                title=created_notification.title,
                message=created_notification.message,
                type=created_notification.notification_type.value,
                read_status=created_notification.read_status,
                created_at=created_notification.created_at
            )
        except InvalidNotificationDataError as e:
            # Propagar excepciones de dominio
            raise e
    
    async def get_notifications_by_user(self, filter_dto: NotificationFilterDTO) -> NotificationListDTO:
        """
        Obtiene las notificaciones de un usuario con paginación y filtros.
        
        Args:
            filter_dto: DTO con los filtros a aplicar
            
        Returns:
            DTO con la lista paginada de notificaciones
        """
        # Obtener notificaciones del repositorio
        notifications, total = await self.notification_repository.get_by_user_id(
            user_id=filter_dto.user_id,
            page=filter_dto.page,
            per_page=filter_dto.per_page,
            read_status=filter_dto.read_status,
            notification_type=filter_dto.type
        )
        
        # Convertir a DTOs
        notification_dtos = [
            NotificationDTO(
                id=notification.id,
                user_id=notification.user_id,
                title=notification.title,
                message=notification.message,
                type=notification.notification_type.value,
                read_status=notification.read_status,
                created_at=notification.created_at
            )
            for notification in notifications
        ]
        
        # Crear DTO de lista
        return NotificationListDTO(
            notifications=notification_dtos,
            total=total,
            page=filter_dto.page,
            per_page=filter_dto.per_page
        )
    
    async def mark_notification_as_read(self, dto: MarkAsReadDTO) -> NotificationDTO:
        """
        Marca una notificación como leída.
        
        Args:
            dto: DTO con el ID de la notificación a marcar como leída
            
        Returns:
            DTO con los datos de la notificación actualizada
            
        Raises:
            ValueError: Si la notificación no existe
        """
        # Obtener notificación del repositorio
        notification = await self.notification_repository.get_by_id(dto.notification_id)
        
        if not notification:
            raise ValueError(f"Notificación con ID {dto.notification_id} no encontrada")
        
        # Marcar como leída
        notification.mark_as_read()
        
        # Actualizar en el repositorio
        updated_notification = await self.notification_repository.update(notification)
        
        # Convertir a DTO
        return NotificationDTO(
            id=updated_notification.id,
            user_id=updated_notification.user_id,
            title=updated_notification.title,
            message=updated_notification.message,
            type=updated_notification.notification_type.value,
            read_status=updated_notification.read_status,
            created_at=updated_notification.created_at
        )