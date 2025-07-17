"""Get Evaluation by ID use case."""

from uuid import UUID

from ...domain.repositories import EvaluationRepositoryInterface
from ...domain.exceptions import EvaluationNotFoundError
from ..dtos.evaluation_dtos import EvaluationResponse


class GetEvaluationByIdUseCase:
    """
    Caso de uso para obtener una evaluación por su ID.
    
    Responsabilidades:
    - Buscar la evaluación por ID en el repositorio
    - Validar que la evaluación existe
    - Convertir entidad a DTO de respuesta
    """
    
    def __init__(self, evaluation_repository: EvaluationRepositoryInterface):
        self._evaluation_repository = evaluation_repository
    
    async def execute(self, evaluation_id: UUID) -> EvaluationResponse:
        """
        Ejecuta el caso de uso de obtención de evaluación por ID.
        
        Args:
            evaluation_id: ID de la evaluación a buscar
            
        Returns:
            EvaluationResponse: Evaluación encontrada
            
        Raises:
            EvaluationNotFoundError: Si la evaluación no existe
        """
        evaluation = await self._evaluation_repository.get_by_id(evaluation_id)
        
        if not evaluation:
            raise EvaluationNotFoundError(f"No se encontró la evaluación con ID: {evaluation_id}")
        
        return EvaluationResponse(
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
