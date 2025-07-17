"""Get Evaluations use case."""

from typing import List, Optional
from uuid import UUID

from ...domain.repositories import EvaluationRepositoryInterface
from ...domain.value_objects import EvaluationStatus
from ..dtos.evaluation_dtos import EvaluationResponse


class GetEvaluationsUseCase:
    """
    Caso de uso para obtener evaluaciones con filtros opcionales.
    
    Responsabilidades:
    - Obtener evaluaciones desde el repositorio
    - Aplicar filtros por período, instructor, estudiante o estado
    - Convertir entidades a DTOs de respuesta
    """
    
    def __init__(self, evaluation_repository: EvaluationRepositoryInterface):
        self._evaluation_repository = evaluation_repository
    
    async def execute(
        self,
        evaluation_period_id: Optional[UUID] = None,
        instructor_id: Optional[UUID] = None,
        student_id: Optional[UUID] = None,
        status: Optional[EvaluationStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[EvaluationResponse]:
        """
        Ejecuta el caso de uso de obtención de evaluaciones.
        
        Args:
            evaluation_period_id: Filtro por período de evaluación (opcional)
            instructor_id: Filtro por instructor (opcional)
            student_id: Filtro por estudiante (opcional)
            status: Filtro por estado de evaluación (opcional)
            skip: Número de registros a omitir
            limit: Límite de registros a retornar
            
        Returns:
            List[EvaluationResponse]: Lista de evaluaciones
        """
        evaluations = await self._evaluation_repository.get_all(
            evaluation_period_id=evaluation_period_id,
            instructor_id=instructor_id,
            student_id=student_id,
            status=status,
            skip=skip,
            limit=limit
        )
        
        return [
            EvaluationResponse(
                id=evaluation.id,
                student_id=evaluation.student_id,
                instructor_id=evaluation.instructor_id,
                evaluation_period_id=evaluation.evaluation_period_id,
                status=evaluation.status.value,
                responses=evaluation.responses,
                comments=evaluation.comments,
                submitted_at=evaluation.submitted_at,
                created_at=evaluation.created_at,
                updated_at=evaluation.updated_at
            )
            for evaluation in evaluations
        ]
