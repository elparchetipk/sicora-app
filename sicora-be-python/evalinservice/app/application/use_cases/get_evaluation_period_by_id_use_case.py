"""Get Evaluation Period by ID use case."""

from uuid import UUID

from ...domain.repositories import EvaluationPeriodRepositoryInterface
from ...domain.exceptions import EvaluationPeriodNotFoundError
from ..dtos.period_dtos import EvaluationPeriodResponse


class GetEvaluationPeriodByIdUseCase:
    """
    Caso de uso para obtener un período de evaluación por su ID.
    
    Responsabilidades:
    - Buscar el período por ID en el repositorio
    - Validar que el período existe
    - Convertir entidad a DTO de respuesta
    """
    
    def __init__(self, evaluation_period_repository: EvaluationPeriodRepositoryInterface):
        self._evaluation_period_repository = evaluation_period_repository
    
    async def execute(self, period_id: UUID) -> EvaluationPeriodResponse:
        """
        Ejecuta el caso de uso de obtención de período por ID.
        
        Args:
            period_id: ID del período a buscar
            
        Returns:
            EvaluationPeriodResponse: Período encontrado
            
        Raises:
            EvaluationPeriodNotFoundError: Si el período no existe
        """
        period = await self._evaluation_period_repository.get_by_id(period_id)
        
        if not period:
            raise EvaluationPeriodNotFoundError(f"No se encontró el período de evaluación con ID: {period_id}")
        
        return EvaluationPeriodResponse(
            id=period.id,
            name=period.name,
            description=period.description,
            start_date=period.start_date,
            end_date=period.end_date,
            status=period.status.value,
            questionnaire_id=period.questionnaire_id,
            target_groups=period.target_groups,
            is_anonymous=period.is_anonymous,
            created_at=period.created_at,
            updated_at=period.updated_at
        )
