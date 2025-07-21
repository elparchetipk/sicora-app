"""
Modelos ORM para la base de datos.

Este módulo define los modelos SQLAlchemy que mapean las entidades del dominio
a tablas de la base de datos.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum

from app.domain.value_objects.notification_type import NotificationType
from .database import Base


class NotificationModel(Base):
    """
    Modelo ORM para la tabla de notificaciones.
    
    Mapea la entidad Notification del dominio a una tabla en la base de datos.
    """
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    type = Column(String, nullable=False)
    read_status = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, title='{self.title}', type='{self.type}')>"