"""
Implementación concreta del repositorio de notificaciones.

Este módulo implementa la interfaz NotificationRepository definida en la capa de dominio
utilizando SQLAlchemy para acceder a la base de datos.
"""

from typing import List, Optional, Tuple
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.notification import Notification
from app.domain.repositories.notification_repository import NotificationRepository
from app.domain.value_objects.notification_type import NotificationType
from app.infrastructure.database.models import NotificationModel


class SQLAlchemyNotificationRepository(NotificationRepository):
    """
    Implementación del repositorio de notificaciones utilizando SQLAlchemy.
    """
    
    def __init__(self, session: AsyncSession):
        """
        Inicializa el repositorio con una sesión de base de datos.
        
        Args:
            session: Sesión de SQLAlchemy para acceder a la base de datos
        """
        self.session = session
    
    async def create(self, notification: Notification) -> Notification:
        """
        Crea una nueva notificación en la base de datos.
        
        Args:
            notification: Entidad de notificación a crear
            
        Returns:
            Notificación creada con ID asignado
        """
        # Crear modelo ORM
        notification_model = NotificationModel(
            user_id=notification.user_id,
            title=notification.title,
            message=notification.message,
            type=notification.notification_type.value,
            read_status=notification.read_status,
            created_at=notification.created_at
        )
        
        # Guardar en la base de datos
        self.session.add(notification_model)
        await self.session.flush()
        await self.session.commit()
        
        # Actualizar entidad con ID asignado
        notification.id = notification_model.id
        
        return notification
    
    async def get_by_id(self, notification_id: int) -> Optional[Notification]:
        """
        Obtiene una notificación por su ID.
        
        Args:
            notification_id: ID de la notificación
            
        Returns:
            Notificación encontrada o None si no existe
        """
        # Consultar la base de datos
        query = select(NotificationModel).where(NotificationModel.id == notification_id)
        result = await self.session.execute(query)
        notification_model = result.scalar_one_or_none()
        
        # Si no existe, retornar None
        if not notification_model:
            return None
        
        # Convertir modelo a entidad
        return self._model_to_entity(notification_model)
    
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
        # Construir consulta base
        query = select(NotificationModel).where(NotificationModel.user_id == user_id)
        count_query = select(func.count()).select_from(NotificationModel).where(NotificationModel.user_id == user_id)
        
        # Aplicar filtros adicionales
        if read_status is not None:
            query = query.where(NotificationModel.read_status == read_status)
            count_query = count_query.where(NotificationModel.read_status == read_status)
        
        if notification_type is not None:
            query = query.where(NotificationModel.type == notification_type.value)
            count_query = count_query.where(NotificationModel.type == notification_type.value)
        
        # Aplicar ordenamiento y paginación
        query = query.order_by(NotificationModel.created_at.desc())
        query = query.offset((page - 1) * per_page).limit(per_page)
        
        # Ejecutar consultas
        result = await self.session.execute(query)
        count_result = await self.session.execute(count_query)
        
        # Obtener resultados
        notification_models = result.scalars().all()
        total = count_result.scalar_one()
        
        # Convertir modelos a entidades
        notifications = [self._model_to_entity(model) for model in notification_models]
        
        return notifications, total
    
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
        # Verificar que la notificación existe
        if notification.id is None:
            raise ValueError("No se puede actualizar una notificación sin ID")
        
        # Construir consulta de actualización
        query = (
            update(NotificationModel)
            .where(NotificationModel.id == notification.id)
            .values(
                title=notification.title,
                message=notification.message,
                type=notification.notification_type.value,
                read_status=notification.read_status
            )
            .execution_options(synchronize_session="fetch")
        )
        
        # Ejecutar consulta
        result = await self.session.execute(query)
        await self.session.commit()
        
        # Verificar que se actualizó correctamente
        if result.rowcount == 0:
            raise ValueError(f"Notificación con ID {notification.id} no encontrada")
        
        return notification
    
    async def delete(self, notification_id: int) -> bool:
        """
        Elimina una notificación por su ID.
        
        Args:
            notification_id: ID de la notificación
            
        Returns:
            True si se eliminó correctamente, False si no existía
        """
        # Construir consulta de eliminación
        query = (
            delete(NotificationModel)
            .where(NotificationModel.id == notification_id)
            .execution_options(synchronize_session="fetch")
        )
        
        # Ejecutar consulta
        result = await self.session.execute(query)
        await self.session.commit()
        
        # Verificar si se eliminó correctamente
        return result.rowcount > 0
    
    def _model_to_entity(self, model: NotificationModel) -> Notification:
        """
        Convierte un modelo ORM a una entidad de dominio.
        
        Args:
            model: Modelo ORM de notificación
            
        Returns:
            Entidad de notificación
        """
        return Notification(
            user_id=model.user_id,
            title=model.title,
            message=model.message,
            notification_type=NotificationType.from_string(model.type),
            id=model.id,
            read_status=model.read_status,
            created_at=model.created_at
        )