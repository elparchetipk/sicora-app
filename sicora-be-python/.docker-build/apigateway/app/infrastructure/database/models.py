"""
Modelos SQLAlchemy para APIGateway
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, JSON
from sqlalchemy.sql import func
from .database import Base


class RequestLogModel(Base):
    """Modelo para logging de requests."""

    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), nullable=True, index=True)
    service_name = Column(String(100), nullable=False, index=True)
    endpoint = Column(String(500), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Float, nullable=False)
    request_size_bytes = Column(Integer, default=0)
    response_size_bytes = Column(Integer, default=0)
    ip_address = Column(String(45), nullable=False)
    user_agent = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False, index=True)
    status = Column(String(20), nullable=False)
    error_message = Column(Text, nullable=True)


class ServiceHealthModel(Base):
    """Modelo para health status de servicios."""

    __tablename__ = "service_health"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(100), nullable=False, unique=True, index=True)
    is_healthy = Column(Boolean, default=True, nullable=False)
    last_check = Column(DateTime, default=func.now(), nullable=False)
    response_time_ms = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    service_metadata = Column(JSON, nullable=True)
