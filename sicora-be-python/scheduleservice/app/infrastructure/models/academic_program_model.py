"""Academic Program model for schedule service."""

from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Column, String, Boolean, DateTime, Text, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class AcademicProgramModel(Base):
  """SQLAlchemy model for Academic Program entity."""
  
  __tablename__ = "academic_programs"
  __table_args__ = {'schema': 'scheduleservice_schema'}
  
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
  name = Column(String(200), nullable=False)
  code = Column(String(20), nullable=False, unique=True, index=True)
  type = Column(String(50), nullable=False)
  duration = Column(BigInteger, nullable=False)  # Duration in quarters
  is_active = Column(Boolean, default=True, nullable=False, index=True)
  description = Column(Text, nullable=True)
  created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
  updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
  deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)
  
  # Relationships
  academic_groups = relationship("AcademicGroupModel", back_populates="academic_program")
  
  def __repr__(self):
    return f"<AcademicProgramModel(id={self.id}, name={self.name}, code={self.code})>"