"""
DTOs para las operaciones relacionadas con notificaciones.

Estos DTOs definen la estructura de los datos que se intercambian entre
la capa de presentación y la capa de aplicación.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator

from app.domain.value_objects.notification_type import NotificationType


class CreateNotificationDTO(BaseModel):
    """DTO para la creación de una notificación."""
    user_id: int = Field(..., gt=0, description="ID del usuario destinatario")
    title: str = Field(..., min_length=1, description="Título de la notificación")
    message: str = Field(..., min_length=1, description="Contenido de la notificación")
    type: str = Field(..., description="Tipo de notificación: email, push, in_app")
    
    @validator('type')
    def validate_notification_type(cls, v):
        """Valida que el tipo de notificación sea válido."""
        try:
            return NotificationType.from_string(v)
        except ValueError as e:
            raise ValueError(str(e))


class NotificationDTO(BaseModel):
    """DTO para representar una notificación."""
    id: int = Field(..., description="ID único de la notificación")
    user_id: int = Field(..., description="ID del usuario destinatario")
    title: str = Field(..., description="Título de la notificación")
    message: str = Field(..., description="Contenido de la notificación")
    type: str = Field(..., description="Tipo de notificación")
    read_status: bool = Field(..., description="Estado de lectura")
    created_at: datetime = Field(..., description="Fecha de creación")


class NotificationListDTO(BaseModel):
    """DTO para representar una lista paginada de notificaciones."""
    notifications: List[NotificationDTO] = Field(..., description="Lista de notificaciones")
    total: int = Field(..., description="Número total de notificaciones")
    page: int = Field(..., description="Página actual")
    per_page: int = Field(..., description="Notificaciones por página")


class MarkAsReadDTO(BaseModel):
    """DTO para marcar una notificación como leída."""
    notification_id: int = Field(..., gt=0, description="ID de la notificación a marcar como leída")


class NotificationFilterDTO(BaseModel):
    """DTO para filtrar notificaciones."""
    user_id: int = Field(..., gt=0, description="ID del usuario")
    page: int = Field(1, ge=1, description="Número de página")
    per_page: int = Field(10, ge=1, le=100, description="Elementos por página")
    read_status: Optional[bool] = Field(None, description="Filtrar por estado de lectura")
    type: Optional[str] = Field(None, description="Filtrar por tipo de notificación")
    
    @validator('type')
    def validate_notification_type(cls, v):
        """Valida que el tipo de notificación sea válido si se proporciona."""
        if v is not None:
            try:
                return NotificationType.from_string(v)
            except ValueError as e:
                raise ValueError(str(e))
        return v