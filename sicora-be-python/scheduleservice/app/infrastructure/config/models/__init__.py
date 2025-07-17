"""SQLAlchemy models for ScheduleService."""

from sqlalchemy import Column, String, Integer, DateTime, Date, Time, Boolean, Text, ForeignKey, UUID
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class AcademicProgramModel(Base):
    """Academic Program SQLAlchemy model."""
    
    __tablename__ = "academic_programs"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    code = Column(String(20), nullable=False, unique=True, index=True)
    program_type = Column(String(50), nullable=False)
    duration_months = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    groups = relationship("AcademicGroupModel", back_populates="program")


class AcademicGroupModel(Base):
    """Academic Group SQLAlchemy model."""
    
    __tablename__ = "academic_groups"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_number = Column(String(50), nullable=False, unique=True, index=True)
    program_id = Column(PostgresUUID(as_uuid=True), ForeignKey("academic_programs.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    max_students = Column(Integer, nullable=False)
    current_students = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    program = relationship("AcademicProgramModel", back_populates="groups")
    schedules = relationship("ScheduleModel", back_populates="group")


class VenueModel(Base):
    """Venue SQLAlchemy model."""
    
    __tablename__ = "venues"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    code = Column(String(20), nullable=False, unique=True, index=True)
    capacity = Column(Integer, nullable=False)
    venue_type = Column(String(50), nullable=False)
    building = Column(String(100), nullable=False)
    floor = Column(String(20), nullable=False)
    campus_id = Column(PostgresUUID(as_uuid=True), nullable=False)  # External reference
    description = Column(Text, nullable=True)
    equipment = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    schedules = relationship("ScheduleModel", back_populates="venue")


class ScheduleModel(Base):
    """Schedule SQLAlchemy model."""
    
    __tablename__ = "schedules"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    instructor_id = Column(PostgresUUID(as_uuid=True), nullable=False, index=True)  # External reference
    group_id = Column(PostgresUUID(as_uuid=True), ForeignKey("academic_groups.id"), nullable=False)
    venue_id = Column(PostgresUUID(as_uuid=True), ForeignKey("venues.id"), nullable=False)
    subject = Column(String(200), nullable=False)
    status = Column(String(20), nullable=False, default="ACTIVE")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    group = relationship("AcademicGroupModel", back_populates="schedules")
    venue = relationship("VenueModel", back_populates="schedules")
    
    # Indexes for performance
    __table_args__ = (
        # Composite indexes for common queries
        {"extend_existing": True}
    )
