"""Schedule model for schedule service."""

from datetime import datetime, timezone, date
from uuid import uuid4
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class ScheduleModel(Base):
  """SQLAlchemy model for Schedule entity."""
  
  __tablename__ = "schedules"
  __table_args__ = {'schema': 'scheduleservice_schema'}
  
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
  academic_group_id = Column(UUID(as_uuid=True), ForeignKey('scheduleservice_schema.academic_groups.id'), nullable=False, index=True)
  instructor_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # Reference to userservice
  venue_id = Column(UUID(as_uuid=True), ForeignKey('scheduleservice_schema.venues.id'), nullable=False, index=True)
  subject = Column(String(200), nullable=False)
  day_of_week = Column(BigInteger, nullable=False, index=True)  # 0=Monday, 6=Sunday
  start_time = Column(DateTime(timezone=True), nullable=False, index=True)
  end_time = Column(DateTime(timezone=True), nullable=False)
  block_identifier = Column(String(10), nullable=False)  # "1A", "2B", etc.
  start_date = Column(Date, nullable=False, index=True)
  end_date = Column(Date, nullable=False, index=True)
  status = Column(String(20), default="ACTIVE", nullable=True, index=True)  # "ACTIVE", "CANCELLED", "COMPLETED"
  is_active = Column(Boolean, default=True, nullable=False, index=True)
  created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
  updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
  deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)
  
  # Relationships
  academic_group = relationship("AcademicGroupModel", back_populates="schedules")
  venue = relationship("VenueModel", back_populates="schedules")
  
  def __repr__(self):
    return f"<ScheduleModel(id={self.id}, subject={self.subject}, day_of_week={self.day_of_week})>"
