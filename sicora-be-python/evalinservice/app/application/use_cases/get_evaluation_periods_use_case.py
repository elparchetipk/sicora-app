"""Get Evaluation Periods use case."""

from typing import List, Optional
from datetime import datetime

from ...domain.repositories import EvaluationPeriodRepositoryInterface
from ...domain.value_objects import PeriodStatus
from ..dtos.period_dtos import EvaluationPeriodResponse


class GetEvaluationPeriodsUseCase:
    """
    Caso de uso para obtener períodos de evaluación con filtros opcionales.
    
    Responsabilidades:
    - Obtener períodos desde el repositorio
    - Aplicar filtros de estado y fechas si se especifican
    - Convertir entidades a DTOs de respuesta
    """
    
    def __init__(self, evaluation_period_repository: EvaluationPeriodRepositoryInterface):
        self._evaluation_period_repository = evaluation_period_repository
    
    async def execute(
        self,
        status: Optional[PeriodStatus] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[EvaluationPeriodResponse]:
        """
        Ejecuta el caso de uso de obtención de períodos de evaluación.
        
        Args:
            status: Filtro por estado del período (opcional)
            start_date: Filtro por fecha de inicio (opcional)
            end_date: Filtro por fecha de fin (opcional)
            skip: Número de registros a omitir
            limit: Límite de registros a retornar
            
        Returns:
            List[EvaluationPeriodResponse]: Lista de períodos de evaluación
        """
        periods = await self._evaluation_period_repository.get_all(
            status=status,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit
        )
        
        return [
            EvaluationPeriodResponse(
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
            for period in periods
        ]
