"""Update Evaluation Period use case."""

from uuid import UUID

from ...domain.repositories import EvaluationPeriodRepositoryInterface
from ...domain.exceptions import EvaluationPeriodNotFoundError, EvaluationPeriodInvalidStateError
from ..dtos.period_dtos import UpdateEvaluationPeriodRequest, EvaluationPeriodResponse


class UpdateEvaluationPeriodUseCase:
    """
    Caso de uso para actualizar un período de evaluación existente.
    
    Responsabilidades:
    - Validar que el período existe
    - Verificar que el período no esté cerrado
    - Aplicar actualizaciones con validaciones de dominio
    - Persistir cambios en el repositorio
    """
    
    def __init__(self, evaluation_period_repository: EvaluationPeriodRepositoryInterface):
        self._evaluation_period_repository = evaluation_period_repository
    
    async def execute(
        self, 
        period_id: UUID, 
        request: UpdateEvaluationPeriodRequest
    ) -> EvaluationPeriodResponse:
        """
        Ejecuta el caso de uso de actualización de período de evaluación.
        
        Args:
            period_id: ID del período a actualizar
            request: Datos a actualizar
            
        Returns:
            EvaluationPeriodResponse: Período actualizado
            
        Raises:
            EvaluationPeriodNotFoundError: Si el período no existe
            EvaluationPeriodInvalidStateError: Si el período no se puede modificar
        """
        # Obtener el período existente
        period = await self._evaluation_period_repository.get_by_id(period_id)
        if not period:
            raise EvaluationPeriodNotFoundError(f"No se encontró el período de evaluación con ID: {period_id}")
        
        # Verificar que se puede modificar
        if not period.can_be_modified():
            raise EvaluationPeriodInvalidStateError(
                f"No se puede modificar el período de evaluación en estado: {period.status.value}"
            )
        
        # Aplicar actualizaciones
        if request.name:
            period.update_name(request.name)
        
        if request.description is not None:
            period.update_description(request.description)
        
        if request.start_date:
            period.update_start_date(request.start_date)
        
        if request.end_date:
            period.update_end_date(request.end_date)
        
        if request.target_groups is not None:
            period.update_target_groups(request.target_groups)
        
        # Persistir cambios
        updated_period = await self._evaluation_period_repository.update(period)
        
        return EvaluationPeriodResponse(
            id=updated_period.id,
            name=updated_period.name,
            description=updated_period.description,
            start_date=updated_period.start_date,
            end_date=updated_period.end_date,
            status=updated_period.status.value,
            questionnaire_id=updated_period.questionnaire_id,
            target_groups=updated_period.target_groups,
            is_anonymous=updated_period.is_anonymous,
            created_at=updated_period.created_at,
            updated_at=updated_period.updated_at
        )
