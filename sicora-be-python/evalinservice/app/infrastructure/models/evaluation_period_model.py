"""Evaluation Period SQLAlchemy model."""

from sqlalchemy import Column, String, Text, DateTime, Boolean, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
import uuid

from ..config.database import Base
from ...domain.value_objects import PeriodStatus


class EvaluationPeriodModel(Base):
    """
    Modelo SQLAlchemy para la entidad EvaluationPeriod.
    
    Representa períodos de tiempo durante los cuales se pueden
    realizar evaluaciones de instructores.
    """
    
    __tablename__ = "evaluation_periods"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(SQLEnum(PeriodStatus), nullable=False, default=PeriodStatus.SCHEDULED)
    questionnaire_id = Column(UUID(as_uuid=True), ForeignKey("evalinservice_schema.questionnaires.id"), nullable=False)
    target_groups = Column(ARRAY(UUID(as_uuid=True)), nullable=False, default=[])
    is_anonymous = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = {"schema": "evalinservice_schema"}
    
    def __repr__(self):
        return f"<EvaluationPeriod(id={self.id}, name='{self.name}', status={self.status})>"
