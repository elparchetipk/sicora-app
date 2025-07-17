"""Questionnaire SQLAlchemy model."""

from sqlalchemy import Column, String, Text, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..config.database import Base


class QuestionnaireModel(Base):
    """
    Modelo SQLAlchemy para la entidad Questionnaire.
    
    Representa cuestionarios que agrupan preguntas para evaluaciones
    de instructores.
    """
    
    __tablename__ = "questionnaires"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    question_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=False, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = {"schema": "evalinservice_schema"}
    
    def __repr__(self):
        return f"<Questionnaire(id={self.id}, name='{self.name}', questions={len(self.question_ids or [])})>"
