"""Generate Instructor Report use case."""

from uuid import UUID
from typing import Dict, Any
from collections import defaultdict

from ...domain.repositories import (
    EvaluationRepositoryInterface,
    EvaluationPeriodRepositoryInterface,
    QuestionRepositoryInterface
)
from ...domain.exceptions import EvaluationPeriodNotFoundError
from ..dtos.report_dtos import InstructorReportResponse, QuestionStatsResponse
from ..interfaces import UserServiceInterface


class GenerateInstructorReportUseCase:
    """
    Caso de uso para generar reporte de evaluación de un instructor.
    
    Responsabilidades:
    - Validar que el período existe
    - Obtener todas las evaluaciones del instructor en el período
    - Calcular estadísticas por pregunta
    - Generar reporte consolidado con métricas
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
    
    async def execute(
        self, 
        instructor_id: UUID, 
        evaluation_period_id: UUID
    ) -> InstructorReportResponse:
        """
        Ejecuta el caso de uso de generación de reporte de instructor.
        
        Args:
            instructor_id: ID del instructor
            evaluation_period_id: ID del período de evaluación
            
        Returns:
            InstructorReportResponse: Reporte del instructor
            
        Raises:
            EvaluationPeriodNotFoundError: Si el período no existe
        """
        # Verificar que el período existe
        period = await self._evaluation_period_repository.get_by_id(evaluation_period_id)
        if not period:
            raise EvaluationPeriodNotFoundError(f"No se encontró el período con ID: {evaluation_period_id}")
        
        # Obtener información del instructor
        instructor = await self._user_service.get_user_by_id(instructor_id)
        
        # Obtener todas las evaluaciones del instructor en el período
        evaluations = await self._evaluation_repository.get_by_instructor_and_period(
            instructor_id, 
            evaluation_period_id
        )
        
        if not evaluations:
            return InstructorReportResponse(
                instructor_id=instructor_id,
                instructor_name=f"{instructor.first_name} {instructor.last_name}" if instructor else "Unknown",
                evaluation_period_id=evaluation_period_id,
                period_name=period.name,
                total_evaluations=0,
                question_stats=[],
                overall_average=0.0,
                comments=[]
            )
        
        # Agrupar respuestas por pregunta
        question_responses = defaultdict(list)
        all_comments = []
        
        for evaluation in evaluations:
            for response in evaluation.responses:
                question_responses[response.question_id].append(response.score)
            
            if evaluation.comments:
                all_comments.append(evaluation.comments)
        
        # Calcular estadísticas por pregunta
        question_stats = []
        total_scores = []
        
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
            
            total_scores.extend(scores)
        
        # Calcular promedio general
        overall_average = sum(total_scores) / len(total_scores) if total_scores else 0.0
        
        return InstructorReportResponse(
            instructor_id=instructor_id,
            instructor_name=f"{instructor.first_name} {instructor.last_name}" if instructor else "Unknown",
            evaluation_period_id=evaluation_period_id,
            period_name=period.name,
            total_evaluations=len(evaluations),
            question_stats=question_stats,
            overall_average=round(overall_average, 2),
            comments=all_comments
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
