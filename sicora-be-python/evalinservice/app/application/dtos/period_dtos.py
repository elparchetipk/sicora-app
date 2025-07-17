"""DTOs for Evaluation Period operations."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ...domain.value_objects.period_status import PeriodStatus


@dataclass
class CreateEvaluationPeriodRequest:
    """DTO para crear un nuevo período de evaluación."""
    name: str
    start_date: datetime
    end_date: datetime
    description: Optional[str] = None
    questionnaire_id: Optional[UUID] = None


@dataclass
class UpdateEvaluationPeriodRequest:
    """DTO para actualizar un período de evaluación."""
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    questionnaire_id: Optional[UUID] = None


@dataclass
class EvaluationPeriodResponse:
    """DTO de respuesta para períodos de evaluación."""
    id: UUID
    name: str
    description: Optional[str]
    start_date: datetime
    end_date: datetime
    status: PeriodStatus
    questionnaire_id: Optional[UUID]
    questionnaire_name: Optional[str]  # Nombre del cuestionario para mostrar
    is_active: bool
    remaining_days: int
    duration_days: int
    created_at: datetime
    updated_at: datetime


@dataclass
class EvaluationPeriodListResponse:
    """DTO de respuesta para lista de períodos de evaluación."""
    periods: List[EvaluationPeriodResponse]
    total: int
    limit: int
    offset: int


@dataclass
class ActivatePeriodRequest:
    """DTO para activar un período."""
    force: bool = False  # Forzar activación aunque se superponga con otros


@dataclass
class PeriodStatusResponse:
    """DTO de respuesta para estado de período."""
    id: UUID
    name: str
    status: PeriodStatus
    is_active: bool
    is_current: bool
    is_upcoming: bool
    is_expired: bool
    remaining_days: int
