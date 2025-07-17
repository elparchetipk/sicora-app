"""Academic Group model for schedule service."""

from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class AcademicGroupModel(Base):
  """SQLAlchemy model for Academic Group entity."""
  
  __tablename__ = "academic_groups"
  __table_args__ = {'schema': 'scheduleservice_schema'}
  
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
  number = Column(String(20), nullable=False, unique=True, index=True)
  academic_program_id = Column(UUID(as_uuid=True), ForeignKey('scheduleservice_schema.academic_programs.id'), nullable=False, index=True)
  quarter = Column(BigInteger, nullable=False)
  year = Column(BigInteger, nullable=False)
  shift = Column(String(20), nullable=False)  # "MORNING", "AFTERNOON", "EVENING"
  is_active = Column(Boolean, default=True, nullable=False)
  created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
  updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
  deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)
  
  # Relationships
  academic_program = relationship("AcademicProgramModel", back_populates="academic_groups")
  schedules = relationship("ScheduleModel", back_populates="academic_group")
  
  def __repr__(self):
    return f"<AcademicGroupModel(id={self.id}, number={self.number}, quarter={self.quarter}, year={self.year})>"