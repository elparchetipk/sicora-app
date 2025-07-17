"""Evaluation SQLAlchemy model."""

from sqlalchemy import Column, Text, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.sql import func
import uuid

from ..config.database import Base
from ...domain.value_objects import EvaluationStatus


class EvaluationModel(Base):
    """
    Modelo SQLAlchemy para la entidad Evaluation.
    
    Representa una evaluación completa realizada por un estudiante
    hacia un instructor en un período específico.
    """
    
    __tablename__ = "evaluations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), nullable=False)
    instructor_id = Column(UUID(as_uuid=True), nullable=False)
    evaluation_period_id = Column(UUID(as_uuid=True), ForeignKey("evalinservice_schema.evaluation_periods.id"), nullable=False)
    status = Column(SQLEnum(EvaluationStatus), nullable=False, default=EvaluationStatus.SUBMITTED)
    responses = Column(JSON, nullable=False)  # Array de objetos {question_id, score}
    comments = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = {"schema": "evalinservice_schema"}
    
    def __repr__(self):
        return f"<Evaluation(id={self.id}, student={self.student_id}, instructor={self.instructor_id})>"
