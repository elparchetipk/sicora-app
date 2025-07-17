"""DTOs for Questionnaire operations."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID


@dataclass
class CreateQuestionnaireRequest:
    """DTO para crear un nuevo cuestionario."""
    name: str
    description: Optional[str] = None


@dataclass
class UpdateQuestionnaireRequest:
    """DTO para actualizar un cuestionario."""
    name: Optional[str] = None
    description: Optional[str] = None


@dataclass
class QuestionnaireResponse:
    """DTO de respuesta para cuestionarios."""
    id: UUID
    name: str
    description: Optional[str]
    is_active: bool
    question_count: int
    created_at: datetime
    updated_at: datetime
    question_ids: List[UUID]


@dataclass
class QuestionnaireListResponse:
    """DTO de respuesta para lista de cuestionarios."""
    questionnaires: List[QuestionnaireResponse]
    total: int
    limit: int
    offset: int


@dataclass
class AddQuestionToQuestionnaireRequest:
    """DTO para agregar pregunta a cuestionario."""
    question_id: UUID


@dataclass
class ReorderQuestionsRequest:
    """DTO para reordenar preguntas en cuestionario."""
    question_ids: List[UUID]


@dataclass
class QuestionnaireWithQuestionsResponse:
    """DTO de respuesta para cuestionario con preguntas detalladas."""
    id: UUID
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    questions: List[dict]  # Incluye detalles completos de las preguntas
