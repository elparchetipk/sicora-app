"""DTOs for Question operations."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ...domain.value_objects.question_type import QuestionType


@dataclass
class CreateQuestionRequest:
    """DTO para crear una nueva pregunta."""
    text: str
    question_type: QuestionType
    category: str
    is_required: bool = True
    order_index: int = 0
    options: Optional[str] = None


@dataclass
class UpdateQuestionRequest:
    """DTO para actualizar una pregunta."""
    text: Optional[str] = None
    category: Optional[str] = None
    is_required: Optional[bool] = None
    order_index: Optional[int] = None
    options: Optional[str] = None


@dataclass
class QuestionResponse:
    """DTO de respuesta para preguntas."""
    id: UUID
    text: str
    question_type: QuestionType
    category: str
    is_required: bool
    order_index: int
    is_active: bool
    options: Optional[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class QuestionListResponse:
    """DTO de respuesta para lista de preguntas."""
    questions: List[QuestionResponse]
    total: int
    limit: int
    offset: int


@dataclass
class BulkQuestionUploadRequest:
    """DTO para carga masiva de preguntas desde CSV."""
    csv_content: str
    validate_only: bool = False


@dataclass
class BulkQuestionUploadResult:
    """DTO de resultado para carga masiva de preguntas."""
    successful_count: int
    failed_count: int
    errors: List[str]
    created_questions: List[QuestionResponse]
