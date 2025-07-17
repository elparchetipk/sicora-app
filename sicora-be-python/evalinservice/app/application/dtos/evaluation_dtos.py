"""DTOs for Evaluation operations."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from ...domain.value_objects.evaluation_status import EvaluationStatus
from .period_dtos import EvaluationPeriodResponse


@dataclass
class EvaluationResponseRequest:
    """DTO para una respuesta individual a una pregunta."""
    question_id: UUID
    response_value: str
    comment: Optional[str] = None


@dataclass
class CreateEvaluationRequest:
    """DTO para crear una nueva evaluación."""
    instructor_id: UUID
    period_id: UUID
    questionnaire_id: UUID


@dataclass
class SubmitEvaluationRequest:
    """DTO para enviar una evaluación."""
    responses: List[EvaluationResponseRequest]
    general_comment: Optional[str] = None


@dataclass
class EvaluationResponseData:
    """DTO para respuesta individual en evaluación."""
    question_id: UUID
    response_value: str
    comment: Optional[str]


@dataclass
class EvaluationResponse:
    """DTO de respuesta para evaluaciones."""
    id: UUID
    student_id: UUID
    instructor_id: UUID
    instructor_name: str  # Nombre del instructor para mostrar
    period_id: UUID
    period_name: str  # Nombre del período para mostrar
    questionnaire_id: UUID
    questionnaire_name: str  # Nombre del cuestionario para mostrar
    status: EvaluationStatus
    responses: List[EvaluationResponseData]
    general_comment: Optional[str]
    completion_percentage: float
    submitted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


@dataclass
class EvaluationListResponse:
    """DTO de respuesta para lista de evaluaciones."""
    evaluations: List[EvaluationResponse]
    total: int
    limit: int
    offset: int


@dataclass
class InstructorToEvaluateResponse:
    """DTO para instructor que puede ser evaluado."""
    instructor_id: UUID
    instructor_name: str
    instructor_email: str
    photo_url: Optional[str]
    has_been_evaluated: bool
    evaluation_id: Optional[UUID]  # Si ya fue evaluado
    can_evaluate: bool  # Si puede ser evaluado en el período actual


@dataclass
class InstructorsToEvaluateResponse:
    """DTO de respuesta para instructores que pueden ser evaluados."""
    instructors: List[InstructorToEvaluateResponse]
    period_id: UUID
    period_name: str
    period_end_date: datetime


@dataclass
class QuestionnaireForEvaluationResponse:
    """DTO para cuestionario con preguntas para evaluación."""
    questionnaire_id: UUID
    questionnaire_name: str
    instructor_id: UUID
    instructor_name: str
    period_id: UUID
    period_name: str
    questions: List[dict]  # Preguntas con detalles completos


@dataclass
class MyEvaluationsResponse:
    """DTO para las evaluaciones del usuario actual."""
    completed_evaluations: List[EvaluationResponse]
    pending_instructors: List[InstructorToEvaluateResponse]
    current_period: Optional[EvaluationPeriodResponse]
    total_completed: int
    total_pending: int
