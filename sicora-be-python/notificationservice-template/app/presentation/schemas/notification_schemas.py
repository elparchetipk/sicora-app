"""
Schemas de Pydantic para las operaciones de notificaciones.

Estos schemas definen la estructura de los datos que se reciben y envían
a través de los endpoints de notificaciones.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator

from app.domain.value_objects.notification_type import NotificationType


class CreateNotificationRequest(BaseModel):
    """Schema para la creación de una notificación."""
    user_id: int = Field(..., gt=0, description="ID del usuario destinatario")
    title: str = Field(..., min_length=1, description="Título de la notificación")
    message: str = Field(..., min_length=1, description="Contenido de la notificación")
    type: str = Field(..., description="Tipo de notificación: email, push, in_app")
    
    @validator('type')
    def validate_notification_type(cls, v):
        """Valida que el tipo de notificación sea válido."""
        try:
            return NotificationType.from_string(v).value
        except ValueError as e:
            raise ValueError(str(e))
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "title": "Nueva actualización",
                "message": "Se ha lanzado una nueva versión de la aplicación",
                "type": "in_app"
            }
        }


class NotificationResponse(BaseModel):
    """Schema para la respuesta de una notificación."""
    id: int = Field(..., description="ID único de la notificación")
    user_id: int = Field(..., description="ID del usuario destinatario")
    title: str = Field(..., description="Título de la notificación")
    message: str = Field(..., description="Contenido de la notificación")
    type: str = Field(..., description="Tipo de notificación")
    read_status: bool = Field(..., description="Estado de lectura")
    created_at: datetime = Field(..., description="Fecha de creación")
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "title": "Nueva actualización",
                "message": "Se ha lanzado una nueva versión de la aplicación",
                "type": "in_app",
                "read_status": False,
                "created_at": "2023-06-20T10:30:00"
            }
        }


class NotificationListResponse(BaseModel):
    """Schema para la respuesta de una lista paginada de notificaciones."""
    notifications: List[NotificationResponse] = Field(..., description="Lista de notificaciones")
    total: int = Field(..., description="Número total de notificaciones")
    page: int = Field(..., description="Página actual")
    per_page: int = Field(..., description="Notificaciones por página")
    
    class Config:
        schema_extra = {
            "example": {
                "notifications": [
                    {
                        "id": 1,
                        "user_id": 1,
                        "title": "Nueva actualización",
                        "message": "Se ha lanzado una nueva versión de la aplicación",
                        "type": "in_app",
                        "read_status": False,
                        "created_at": "2023-06-20T10:30:00"
                    }
                ],
                "total": 1,
                "page": 1,
                "per_page": 10
            }
        }


class MarkAsReadRequest(BaseModel):
    """Schema para marcar una notificación como leída."""
    notification_id: int = Field(..., gt=0, description="ID de la notificación a marcar como leída")
    
    class Config:
        schema_extra = {
            "example": {
                "notification_id": 1
            }
        }


class ErrorResponse(BaseModel):
    """Schema para respuestas de error."""
    detail: str = Field(..., description="Descripción del error")
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "Notificación no encontrada"
            }
        }