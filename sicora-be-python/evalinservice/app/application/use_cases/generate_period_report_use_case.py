"""Generate Period Report use case."""

from uuid import UUID
from typing import Dict, List
from collections import defaultdict

from ...domain.repositories import (
    EvaluationRepositoryInterface,
    EvaluationPeriodRepositoryInterface,
    QuestionRepositoryInterface
)
from ...domain.exceptions import EvaluationPeriodNotFoundError
from ..dtos.report_dtos import PeriodReportResponse, InstructorSummaryResponse, QuestionStatsResponse
from ..interfaces import UserServiceInterface


class GeneratePeriodReportUseCase:
    """
    Caso de uso para generar reporte consolidado de un período de evaluación.
    
    Responsabilidades:
    - Validar que el período existe
    - Obtener todas las evaluaciones del período
    - Calcular estadísticas generales y por instructor
    - Generar reporte consolidado con métricas globales
    """
    
    def __init__(
        self,
        evaluation_repository: EvaluationRepositoryInterface,
        evaluation_period_repository: EvaluationPeriodRepositoryInterface,
        question_repository: QuestionRepositoryInterface,
        user_service: UserServiceInterface
    ):
        self._evaluation_repository = evaluation_repository
        self._evaluation_period_repository = evaluation_period_repository
        self._question_repository = question_repository
        self._user_service = user_service
    
    async def execute(self, evaluation_period_id: UUID) -> PeriodReportResponse:
        """
        Ejecuta el caso de uso de generación de reporte del período.
        
        Args:
            evaluation_period_id: ID del período de evaluación
            
        Returns:
            PeriodReportResponse: Reporte del período
            
        Raises:
            EvaluationPeriodNotFoundError: Si el período no existe
        """
        # Verificar que el período existe
        period = await self._evaluation_period_repository.get_by_id(evaluation_period_id)
        if not period:
            raise EvaluationPeriodNotFoundError(f"No se encontró el período con ID: {evaluation_period_id}")
        
        # Obtener todas las evaluaciones del período
        evaluations = await self._evaluation_repository.get_by_period(evaluation_period_id)
        
        if not evaluations:
            return PeriodReportResponse(
                evaluation_period_id=evaluation_period_id,
                period_name=period.name,
                start_date=period.start_date,
                end_date=period.end_date,
                total_evaluations=0,
                participation_rate=0.0,
                overall_average=0.0,
                instructor_summaries=[],
                question_stats=[]
            )
        
        # Agrupar evaluaciones por instructor
        instructor_evaluations = defaultdict(list)
        question_responses = defaultdict(list)
        all_scores = []
        
        for evaluation in evaluations:
            instructor_evaluations[evaluation.instructor_id].append(evaluation)
            
            for response in evaluation.responses:
                question_responses[response.question_id].append(response.score)
                all_scores.append(response.score)
        
        # Generar resúmenes por instructor
        instructor_summaries = []
        for instructor_id, instructor_evals in instructor_evaluations.items():
            instructor = await self._user_service.get_user_by_id(instructor_id)
            
            # Calcular promedio del instructor
            instructor_scores = []
            for eval in instructor_evals:
                for response in eval.responses:
                    instructor_scores.append(response.score)
            
            avg_score = sum(instructor_scores) / len(instructor_scores) if instructor_scores else 0.0
            
            instructor_summaries.append(InstructorSummaryResponse(
                instructor_id=instructor_id,
                instructor_name=f"{instructor.first_name} {instructor.last_name}" if instructor else "Unknown",
                evaluation_count=len(instructor_evals),
                average_score=round(avg_score, 2)
            ))
        
        # Calcular estadísticas por pregunta
        question_stats = []
        for question_id, scores in question_responses.items():
            question = await self._question_repository.get_by_id(question_id)
            
            avg_score = sum(scores) / len(scores)
            min_score = min(scores)
            max_score = max(scores)
            
            question_stats.append(QuestionStatsResponse(
                question_id=question_id,
                question_text=question.text if question else "Unknown",
                response_count=len(scores),
                average_score=round(avg_score, 2),
                min_score=min_score,
                max_score=max_score,
                score_distribution=self._calculate_score_distribution(scores)
            ))
        
        # Calcular métricas generales
        overall_average = sum(all_scores) / len(all_scores) if all_scores else 0.0
        
        # Calcular tasa de participación (requiere información de estudiantes elegibles)
        # Por ahora usamos un cálculo simple basado en los grupos objetivo
        total_eligible_students = len(period.target_groups) * 30  # Estimación
        participation_rate = (len(evaluations) / total_eligible_students) * 100 if total_eligible_students > 0 else 0.0
        
        return PeriodReportResponse(
            evaluation_period_id=evaluation_period_id,
            period_name=period.name,
            start_date=period.start_date,
            end_date=period.end_date,
            total_evaluations=len(evaluations),
            participation_rate=round(participation_rate, 2),
            overall_average=round(overall_average, 2),
            instructor_summaries=sorted(instructor_summaries, key=lambda x: x.average_score, reverse=True),
            question_stats=question_stats
        )
    
    def _calculate_score_distribution(self, scores: list) -> Dict[str, int]:
        """Calcula la distribución de puntuaciones."""
        distribution = defaultdict(int)
        
        for score in scores:
            if score <= 2:
                distribution["muy_bajo"] += 1
            elif score <= 3:
                distribution["bajo"] += 1
            elif score <= 4:
                distribution["medio"] += 1
            elif score <= 4.5:
                distribution["alto"] += 1
            else:
                distribution["muy_alto"] += 1
        
        return dict(distribution)
