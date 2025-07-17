"""Close Evaluation Period use case."""

from uuid import UUID

from ...domain.repositories import EvaluationPeriodRepositoryInterface
from ...domain.exceptions import EvaluationPeriodNotFoundError, EvaluationPeriodInvalidStateError
from ..dtos.period_dtos import EvaluationPeriodResponse
from ..interfaces import NotificationServiceInterface


class CloseEvaluationPeriodUseCase:
    """
    Caso de uso para cerrar un período de evaluación.
    
    Responsabilidades:
    - Validar que el período existe
    - Verificar que el período se puede cerrar
    - Cambiar estado a cerrado
    - Enviar notificaciones a administradores
    - Persistir cambios en el repositorio
    """
    
    def __init__(
        self,
        evaluation_period_repository: EvaluationPeriodRepositoryInterface,
        notification_service: NotificationServiceInterface
    ):
        self._evaluation_period_repository = evaluation_period_repository
        self._notification_service = notification_service
    
    async def execute(self, period_id: UUID) -> EvaluationPeriodResponse:
        """
        Ejecuta el caso de uso de cierre de período de evaluación.
        
        Args:
            period_id: ID del período a cerrar
            
        Returns:
            EvaluationPeriodResponse: Período cerrado
            
        Raises:
            EvaluationPeriodNotFoundError: Si el período no existe
            EvaluationPeriodInvalidStateError: Si el período no se puede cerrar
        """
        # Obtener el período existente
        period = await self._evaluation_period_repository.get_by_id(period_id)
        if not period:
            raise EvaluationPeriodNotFoundError(f"No se encontró el período de evaluación con ID: {period_id}")
        
        # Cerrar el período
        period.close()
        
        # Persistir cambios
        updated_period = await self._evaluation_period_repository.update(period)
        
        # Enviar notificación
        await self._notification_service.send_period_closed_notification(period_id, updated_period.name)
        
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
