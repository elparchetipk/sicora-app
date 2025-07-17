"""Campus model for schedule service."""

from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class CampusModel(Base):
  """SQLAlchemy model for Campus entity."""
  
  __tablename__ = "campuses"
  __table_args__ = {'schema': 'scheduleservice_schema'}
  
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
  name = Column(String(100), nullable=False)
  code = Column(String(20), nullable=False, unique=True, index=True)
  address = Column(Text, nullable=True)
  city = Column(String(50), nullable=True)
  is_active = Column(Boolean, default=True, nullable=False, index=True)
  created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
  updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
  deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)
  
  # Relationships
  venues = relationship("VenueModel", back_populates="campus")
  
  def __repr__(self):
    return f"<CampusModel(id={self.id}, name={self.name}, code={self.code})>"
