"""
Notification Entity - Entidad Principal del Dominio

Representa una notificación en el sistema con sus atributos y comportamientos.
"""

from datetime import datetime
from typing import Optional
import time

from ..value_objects.notification_type import NotificationType


class NotificationError(Exception):
    """Excepción base para errores relacionados con notificaciones."""
    pass


class InvalidNotificationDataError(NotificationError):
    """Excepción para datos inválidos en una notificación."""
    pass


class Notification:
    """
    Entidad que representa una notificación en el sistema.

    Attributes:
        id: Identificador único de la notificación
        user_id: ID del usuario destinatario
        title: Título de la notificación
        message: Contenido de la notificación
        notification_type: Tipo de notificación (email, push, in_app)
        read_status: Indica si la notificación ha sido leída
        created_at: Fecha y hora de creación
    """

    def __init__(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: NotificationType,
        id: Optional[int] = None,
        read_status: bool = False,
        created_at: Optional[datetime] = None
    ):
        """
        Inicializa una nueva notificación con validaciones.

        Args:
            user_id: ID del usuario destinatario
            title: Título de la notificación
            message: Contenido de la notificación
            notification_type: Tipo de notificación
            id: Identificador único (opcional)
            read_status: Estado de lectura (por defecto False)
            created_at: Fecha de creación (por defecto ahora)

        Raises:
            InvalidNotificationDataError: Si algún dato no cumple las validaciones
        """
        # Validaciones
        if not title or title.strip() == "":
            raise InvalidNotificationDataError("El título no puede estar vacío")

        if not message or message.strip() == "":
            raise InvalidNotificationDataError("El mensaje no puede estar vacío")

        if not isinstance(user_id, int) or user_id <= 0:
            raise InvalidNotificationDataError("El ID de usuario debe ser un entero positivo")

        if created_at and created_at > datetime.now():
            raise InvalidNotificationDataError("La fecha de creación no puede estar en el futuro")

        # Asignación de atributos
        self.id = id
        self.user_id = user_id
        self.title = title
        self.message = message
        self.notification_type = notification_type
        self.read_status = read_status
        self.created_at = created_at or datetime.now()

    def mark_as_read(self) -> None:
        """Marca la notificación como leída."""
        self.read_status = True

    def is_read(self) -> bool:
        """
        Verifica si la notificación ha sido leída.

        Returns:
            bool: True si ha sido leída, False en caso contrario
        """
        return self.read_status

    def is_expired(self, expiration_days: int = 30) -> bool:
        """
        Verifica si la notificación ha expirado según un período definido.

        Args:
            expiration_days: Días después de los cuales se considera expirada

        Returns:
            bool: True si ha expirado, False en caso contrario
        """
        if not self.created_at:
            return False

        expiration_date = self.created_at.timestamp() + (expiration_days * 24 * 60 * 60)
        return time.time() > expiration_date
