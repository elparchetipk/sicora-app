from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from enum import Enum


class ProjectStatus(str, Enum):
    """Estado de un proyecto formativo."""

    IDEA_PROPOSAL = "idea_proposal"
    IDEA_APPROVED = "idea_approved"
    IN_DEVELOPMENT = "in_development"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class EvaluationStatus(str, Enum):
    """Estado de una evaluación."""

    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"


class TrimesterType(str, Enum):
    """Tipos de trimestre según programa."""

    ADSO_T2 = "adso_t2"  # Ideas de proyecto
    ADSO_T3 = "adso_t3"  # Desarrollo inicial
    ADSO_T4 = "adso_t4"  # Desarrollo intermedio
    ADSO_T5 = "adso_t5"  # Desarrollo avanzado
    ADSO_T6 = "adso_t6"  # Refinamiento
    ADSO_T7 = "adso_t7"  # Proyecto final
    PSW_T2 = "psw_t2"  # Ideas de proyecto
    PSW_T3 = "psw_t3"  # Desarrollo
    PSW_T4 = "psw_t4"  # Proyecto final


@dataclass(frozen=True)
class ProjectIdea:
    """Entidad para ideas de proyecto propuestas."""

    id: UUID
    group_id: UUID
    title: str
    description: str
    proposed_technologies: List[str]
    stakeholder_info: Optional[str]
    business_value: str
    technical_complexity: int  # 1-5 scale
    estimated_duration_weeks: int
    submitted_by: UUID
    submitted_at: datetime
    status: ProjectStatus
    approval_comments: Optional[str] = None
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None

    def is_approved(self) -> bool:
        """Verifica si la idea está aprobada."""
        return self.status == ProjectStatus.IDEA_APPROVED

    def can_start_development(self) -> bool:
        """Verifica si puede iniciar desarrollo."""
        return self.is_approved() and self.approved_at is not None


@dataclass(frozen=True)
class StudentGroup:
    """Entidad para grupos de estudiantes."""

    id: UUID
    name: str
    program_type: str  # ADSO, PSW
    current_trimester: TrimesterType
    members: List[UUID]  # Student IDs
    leader_id: UUID
    instructor_id: UUID
    stakeholder_id: Optional[UUID]
    created_at: datetime
    is_active: bool = True

    def has_optimal_size(self) -> bool:
        """Verifica si tiene tamaño óptimo (número impar 3-5)."""
        return len(self.members) in [3, 5] and len(self.members) % 2 == 1

    def is_complete(self) -> bool:
        """Verifica si el grupo está completo."""
        return len(self.members) >= 3 and self.leader_id in self.members


@dataclass(frozen=True)
class EvaluationSession:
    """Entidad para sesiones de evaluación."""

    id: UUID
    project_idea_id: UUID
    group_id: UUID
    trimester: TrimesterType
    session_number: int  # 1, 2, etc. dentro del trimestre
    scheduled_date: datetime
    duration_minutes: int
    location: str
    jury_members: List[UUID]  # Instructor IDs (2 or more)
    status: EvaluationStatus
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    def is_scheduled_today(self) -> bool:
        """Verifica si está programada para hoy."""
        return self.scheduled_date.date() == datetime.utcnow().date()

    def has_minimum_jury(self) -> bool:
        """Verifica si tiene el mínimo de jurados (2)."""
        return len(self.jury_members) >= 2

    def can_start(self) -> bool:
        """Verifica si puede iniciar."""
        return (
            self.status == EvaluationStatus.SCHEDULED
            and self.has_minimum_jury()
            and datetime.utcnow() >= self.scheduled_date
        )


@dataclass(frozen=True)
class EvaluationResult:
    """Resultado de evaluación de un criterio."""

    id: UUID
    evaluation_session_id: UUID
    criterion_id: UUID
    evaluator_id: UUID
    score: Optional[int]  # Points awarded
    is_compliant: bool
    comments: str
    voice_note_ids: List[UUID]  # Associated voice notes
    created_at: datetime

    def has_voice_feedback(self) -> bool:
        """Verifica si tiene retroalimentación por voz."""
        return len(self.voice_note_ids) > 0


@dataclass(frozen=True)
class EvaluationSummary:
    """Resumen consolidado de una sesión de evaluación."""

    id: UUID
    evaluation_session_id: UUID
    total_criteria_evaluated: int
    total_criteria_passed: int
    overall_percentage: float
    average_score: float
    key_strengths: List[str]
    improvement_areas: List[str]
    next_steps_recommendations: List[str]
    generated_by: UUID
    generated_at: datetime

    @property
    def pass_rate(self) -> float:
        """Calcula el porcentaje de criterios aprobados."""
        if self.total_criteria_evaluated == 0:
            return 0.0
        return (self.total_criteria_passed / self.total_criteria_evaluated) * 100
