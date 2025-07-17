"""Question SQLAlchemy model."""

from sqlalchemy import Column, String, Text, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from ..config.database import Base
from ...domain.value_objects import QuestionType


class QuestionModel(Base):
    """
    Modelo SQLAlchemy para la entidad Question.
    
    Representa las preguntas que se pueden incluir en cuestionarios
    de evaluación de instructores.
    """
    
    __tablename__ = "questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(Text, nullable=False)
    question_type = Column(SQLEnum(QuestionType), nullable=False, default=QuestionType.SCALE_1_5)
    category = Column(String(100), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = {"schema": "evalinservice_schema"}
    
    def __repr__(self):
        return f"<Question(id={self.id}, text='{self.text[:50]}...', type={self.question_type})>"
