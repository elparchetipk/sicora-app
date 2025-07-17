"""DTOs for Reports and Statistics."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID


@dataclass
class QuestionStatistics:
    """Estadísticas de una pregunta específica."""
    question_id: UUID
    question_text: str
    question_type: str
    total_responses: int
    average_rating: Optional[float]
    response_distribution: Dict[str, int]  # Distribución de respuestas


@dataclass
class QuestionStatsResponse:
    """Respuesta de estadísticas de pregunta."""
    question_id: UUID
    question_text: str
    average_score: float
    response_count: int
    distribution: Dict[str, int]


@dataclass
class InstructorReportResponse:
    """Respuesta del reporte de instructor."""
    instructor_id: UUID
    period_id: UUID
    total_evaluations: int
    average_rating: float
    response_rate: float
    question_averages: Dict[str, float]
    strengths: List[str]
    improvement_areas: List[str]
    generated_at: datetime


@dataclass
class InstructorSummaryResponse:
    """Resumen de instructor para reporte de período."""
    instructor_id: UUID
    instructor_name: str
    average_rating: float
    total_evaluations: int
    response_rate: float


@dataclass
class PeriodReportResponse:
    """Respuesta del reporte de período."""
    period_id: UUID
    total_instructors: int
    total_evaluations: int
    completion_rate: float
    average_rating: float
    instructor_rankings: List[InstructorSummaryResponse]
    question_analysis: Dict[str, float]
    department_summary: Dict[str, Dict[str, float]]
    generated_at: datetime


@dataclass
class InstructorEvaluationReport:
    """Reporte de evaluación para un instructor."""
    instructor_id: UUID
    instructor_name: str
    period_id: Optional[UUID]
    period_name: Optional[str]
    total_evaluations: int
    overall_average: float
    question_statistics: List[QuestionStatistics]
    qualitative_comments: List[str]  # Comentarios anonimizados
    created_at: datetime


@dataclass
class ProgramEvaluationReport:
    """Reporte de evaluación para un programa académico."""
    program_id: UUID
    program_name: str
    period_id: Optional[UUID]
    period_name: Optional[str]
    total_instructors: int
    total_evaluations: int
    average_rating: float
    instructor_summaries: List[Dict]  # Resumen por instructor
    created_at: datetime


@dataclass
class FichaEvaluationReport:
    """Reporte de evaluación para una ficha específica."""
    ficha_id: UUID
    ficha_name: str
    period_id: Optional[UUID]
    period_name: Optional[str]
    total_students: int
    total_evaluations_completed: int
    participation_rate: float
    instructor_summaries: List[Dict]  # Resumen por instructor
    created_at: datetime


@dataclass
class ParticipationStatus:
    """Estado de participación de un estudiante."""
    student_id: UUID
    student_name: str
    student_email: str
    total_instructors_to_evaluate: int
    completed_evaluations: int
    pending_evaluations: int
    participation_percentage: float
    last_evaluation_date: Optional[datetime]


@dataclass
class ParticipationReport:
    """Reporte de participación de estudiantes."""
    ficha_id: UUID
    ficha_name: str
    period_id: UUID
    period_name: str
    total_students: int
    students_participated: int
    students_completed_all: int
    overall_participation_rate: float
    student_details: List[ParticipationStatus]
    created_at: datetime


@dataclass
class QualitativeCommentsResponse:
    """Respuesta con comentarios cualitativos anonimizados."""
    instructor_id: UUID
    instructor_name: str
    period_id: Optional[UUID]
    period_name: Optional[str]
    total_comments: int
    comments: List[Dict]  # Comentarios con metadatos (fecha, categoría, etc.)
    created_at: datetime


@dataclass
class EvaluationStatistics:
    """Estadísticas generales de evaluaciones."""
    total_evaluations: int
    evaluations_by_status: Dict[str, int]
    evaluations_by_period: Dict[str, int]
    average_completion_time_minutes: Optional[float]
    most_active_periods: List[Dict]
    top_rated_instructors: List[Dict]
    participation_trends: List[Dict]


@dataclass
class ExportReportRequest:
    """Request para exportar reportes a CSV."""
    instructor_id: Optional[UUID] = None
    program_id: Optional[UUID] = None
    ficha_id: Optional[UUID] = None
    period_id: Optional[UUID] = None
    format: str = "csv"  # csv, excel, pdf
    include_comments: bool = False
    anonymize_data: bool = True


@dataclass 
class ExportReportResponse:
    """Response para exportación de reportes."""
    file_url: str
    file_name: str
    file_size_bytes: int
    export_date: datetime
    record_count: int
    format: str
