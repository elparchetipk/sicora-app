"""Create Evaluation Period use case."""

from ...domain.entities import EvaluationPeriod
from ...domain.repositories import EvaluationPeriodRepositoryInterface, QuestionnaireRepositoryInterface
from ...domain.exceptions import QuestionnaireNotFoundError, EvaluationPeriodOverlapError
from ..dtos.period_dtos import CreateEvaluationPeriodRequest, EvaluationPeriodResponse
from ..interfaces import ScheduleServiceInterface


class CreateEvaluationPeriodUseCase:
    """
    Caso de uso para crear un nuevo período de evaluación.
    
    Responsabilidades:
    - Validar que el cuestionario existe
    - Verificar que no hay solapamiento de fechas
    - Validar que los grupos/materias existen en ScheduleService
    - Crear la entidad EvaluationPeriod con validaciones de dominio
    - Persistir el período en el repositorio
    """
    
    def __init__(
        self,
        evaluation_period_repository: EvaluationPeriodRepositoryInterface,
        questionnaire_repository: QuestionnaireRepositoryInterface,
        schedule_service: ScheduleServiceInterface
    ):
        self._evaluation_period_repository = evaluation_period_repository
        self._questionnaire_repository = questionnaire_repository
        self._schedule_service = schedule_service
    
    async def execute(self, request: CreateEvaluationPeriodRequest) -> EvaluationPeriodResponse:
        """
        Ejecuta el caso de uso de creación de período de evaluación.
        
        Args:
            request: Datos del período a crear
            
        Returns:
            EvaluationPeriodResponse: Período de evaluación creado
            
        Raises:
            QuestionnaireNotFoundError: Si el cuestionario no existe
            EvaluationPeriodOverlapError: Si hay solapamiento de fechas
            InvalidScheduleGroupError: Si los grupos no existen
        """
        # Verificar que el cuestionario existe y está activo
        questionnaire = await self._questionnaire_repository.get_by_id(request.questionnaire_id)
        if not questionnaire or not questionnaire.is_active:
            raise QuestionnaireNotFoundError(f"No se encontró el cuestionario activo con ID: {request.questionnaire_id}")
        
        # Verificar que no hay solapamiento de fechas
        overlapping_periods = await self._evaluation_period_repository.get_overlapping_periods(
            request.start_date, 
            request.end_date
        )
        if overlapping_periods:
            raise EvaluationPeriodOverlapError(
                f"Ya existe un período de evaluación que se solapa con las fechas {request.start_date} - {request.end_date}"
            )
        
        # Validar grupos/materias en ScheduleService
        for group_id in request.target_groups:
            if not await self._schedule_service.group_exists(group_id):
                raise ValueError(f"El grupo con ID {group_id} no existe")
        
        # Crear la entidad con validaciones de dominio
        evaluation_period = EvaluationPeriod.create(
            name=request.name,
            description=request.description,
            start_date=request.start_date,
            end_date=request.end_date,
            questionnaire_id=request.questionnaire_id,
            target_groups=request.target_groups,
            is_anonymous=request.is_anonymous
        )
        
        # Persistir en el repositorio
        created_period = await self._evaluation_period_repository.create(evaluation_period)
        
        return EvaluationPeriodResponse(
            id=created_period.id,
            name=created_period.name,
            description=created_period.description,
            start_date=created_period.start_date,
            end_date=created_period.end_date,
            status=created_period.status.value,
            questionnaire_id=created_period.questionnaire_id,
            target_groups=created_period.target_groups,
            is_anonymous=created_period.is_anonymous,
            created_at=created_period.created_at,
            updated_at=created_period.updated_at
        )
