"""Venue model for schedule service."""

from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class VenueModel(Base):
  """SQLAlchemy model for Venue entity."""
  
  __tablename__ = "venues"
  __table_args__ = {'schema': 'scheduleservice_schema'}
  
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
  name = Column(String(100), nullable=False)
  code = Column(String(20), nullable=False, unique=True, index=True)
  type = Column(String(50), nullable=False)  # "CLASSROOM", "LAB", "AUDITORIUM", etc.
  capacity = Column(BigInteger, nullable=False)
  campus_id = Column(UUID(as_uuid=True), ForeignKey('scheduleservice_schema.campuses.id'), nullable=False, index=True)
  floor = Column(String(10), nullable=True)
  is_active = Column(Boolean, default=True, nullable=False)
  created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
  updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
  deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)
  
  # Relationships
  campus = relationship("CampusModel", back_populates="venues")
  schedules = relationship("ScheduleModel", back_populates="venue")
  
  def __repr__(self):
    return f"<VenueModel(id={self.id}, name={self.name}, code={self.code}, type={self.type})>"
