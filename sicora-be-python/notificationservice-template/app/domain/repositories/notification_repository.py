"""
Interfaz del repositorio de notificaciones.

Define los métodos que debe implementar cualquier repositorio de notificaciones,
siguiendo el principio de inversión de dependencias.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from ..entities.notification import Notification
from ..value_objects.notification_type import NotificationType


class NotificationRepository(ABC):
    """
    Interfaz para el repositorio de notificaciones.
    
    Define los métodos que debe implementar cualquier repositorio concreto
    que maneje notificaciones.
    """
    
    @abstractmethod
    async def create(self, notification: Notification) -> Notification:
        """
        Crea una nueva notificación en el repositorio.
        
        Args:
            notification: Notificación a crear
            
        Returns:
            Notificación creada con ID asignado
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, notification_id: int) -> Optional[Notification]:
        """
        Obtiene una notificación por su ID.
        
        Args:
            notification_id: ID de la notificación
            
        Returns:
            Notificación encontrada o None si no existe
        """
        pass
    
    @abstractmethod
    async def get_by_user_id(
        self, 
        user_id: int, 
        page: int = 1, 
        per_page: int = 10,
        read_status: Optional[bool] = None,
        notification_type: Optional[NotificationType] = None
    ) -> Tuple[List[Notification], int]:
        """
        Obtiene las notificaciones de un usuario con paginación y filtros.
        
        Args:
            user_id: ID del usuario
            page: Número de página (comienza en 1)
            per_page: Elementos por página
            read_status: Filtrar por estado de lectura (opcional)
            notification_type: Filtrar por tipo de notificación (opcional)
            
        Returns:
            Tupla con la lista de notificaciones y el total de notificaciones
        """
        pass
    
    @abstractmethod
    async def update(self, notification: Notification) -> Notification:
        """
        Actualiza una notificación existente.
        
        Args:
            notification: Notificación con los datos actualizados
            
        Returns:
            Notificación actualizada
            
        Raises:
            ValueError: Si la notificación no existe
        """
        pass
    
    @abstractmethod
    async def delete(self, notification_id: int) -> bool:
        """
        Elimina una notificación por su ID.
        
        Args:
            notification_id: ID de la notificación
            
        Returns:
            True si se eliminó correctamente, False si no existía
        """
        pass