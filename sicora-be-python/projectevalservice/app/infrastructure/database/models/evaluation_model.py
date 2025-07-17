from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Integer,
    Float,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from .connection import Base
from ...domain.entities import EvaluationStatus, EvaluationType


class EvaluationModel(Base):
    __tablename__ = "evaluations"
    __table_args__ = {'schema': 'projectevalservice_schema'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projectevalservice_schema.projects.id"), nullable=False)

    # Evaluation details
    evaluation_type = Column(SQLEnum(EvaluationType), nullable=False)
    status = Column(
        SQLEnum(EvaluationStatus), nullable=False, default=EvaluationStatus.SCHEDULED
    )
    trimester = Column(Integer, nullable=False)
    academic_year = Column(Integer, nullable=False)

    # Scheduling
    scheduled_date = Column(DateTime(timezone=True), nullable=False)
    actual_date = Column(DateTime(timezone=True), nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    location = Column(String(255), nullable=False)

    # Scores
    technical_score = Column(Float, nullable=True)
    presentation_score = Column(Float, nullable=True)
    documentation_score = Column(Float, nullable=True)
    innovation_score = Column(Float, nullable=True)
    collaboration_score = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)

    # Feedback
    general_comments = Column(Text, nullable=True)
    technical_feedback = Column(Text, nullable=True)
    presentation_feedback = Column(Text, nullable=True)
    improvement_suggestions = Column(Text, nullable=True)
    voice_notes_url = Column(String(500), nullable=True)
    voice_notes_transcript = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    created_by = Column(UUID(as_uuid=True), nullable=False)
    evaluated_by = Column(UUID(as_uuid=True), nullable=True)

    # Relationships
    # project = relationship("ProjectModel", back_populates="evaluations")

    __table_args__ = {"schema": "projectevalservice_schema"}
