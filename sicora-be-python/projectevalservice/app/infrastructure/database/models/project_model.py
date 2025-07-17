from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Boolean,
    Integer,
    Float,
    JSON,
    Enum as SQLEnum,
)
from sqlalchemy.sql import func
import uuid
import enum

from .connection import Base
from ...domain.entities.project_enums import ProjectStatus, ProjectType


class ProjectModel(Base):
    __tablename__ = "projects"
    __table_args__ = {'schema': 'projectevalservice_schema'}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(
        SQLEnum(ProjectStatus), nullable=False, default=ProjectStatus.IDEA_PROPOSAL
    )
    project_type = Column(SQLEnum(ProjectType), nullable=False)

    # References to other services
    cohort_id = Column(String(36), nullable=False)
    group_id = Column(String(36), nullable=False)
    stakeholder_id = Column(String(36), nullable=True)

    # Academic information
    trimester = Column(Integer, nullable=False)
    academic_year = Column(Integer, nullable=False)

    # Dates
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    start_date = Column(DateTime(timezone=True), nullable=False)
    expected_end_date = Column(DateTime(timezone=True), nullable=False)
    actual_end_date = Column(DateTime(timezone=True), nullable=True)

    # Technical details - usando JSON para SQLite compatibility
    technologies = Column(JSON, nullable=False, default=[])
    repository_url = Column(String(500), nullable=True)
    demo_url = Column(String(500), nullable=True)
    documentation_url = Column(String(500), nullable=True)

    # Academic control
    scope_locked = Column(Boolean, default=False)
    scope_lock_reason = Column(Text, nullable=True)
    scope_locked_by = Column(String(36), nullable=True)
    scope_locked_at = Column(DateTime(timezone=True), nullable=True)

    # Stakeholder management
    stakeholder_expectations_documented = Column(Boolean, default=False)
    stakeholder_limitations_communicated = Column(Boolean, default=False)

    __table_args__ = {"schema": "projectevalservice_schema"}
