"""Create Evaluation use case."""

from uuid import UUID

from ...domain.entities import Evaluation
from ...domain.repositories import (
    EvaluationRepositoryInterface, 
    EvaluationPeriodRepositoryInterface,
    QuestionnaireRepositoryInterface
)
from ...domain.exceptions import (
    EvaluationPeriodNotFoundError, 
    EvaluationPeriodNotActiveError,
    EvaluationAlreadyExistsError,
    InvalidQuestionResponseError
)
from ..dtos.evaluation_dtos import CreateEvaluationRequest, EvaluationResponse
from ..interfaces import UserServiceInterface


class CreateEvaluationUseCase:
    """
    Caso de uso para crear una nueva evaluación.
    
    Responsabilidades:
    - Validar que el período de evaluación existe y está activo
    - Verificar que el usuario puede evaluar (no ha evaluado ya)
    - Validar respuestas contra el cuestionario
    - Crear la entidad Evaluation con validaciones de dominio
    - Persistir la evaluación en el repositorio
    """
    
    def __init__(
        self,
        evaluation_repository: EvaluationRepositoryInterface,
        evaluation_period_repository: EvaluationPeriodRepositoryInterface,
        questionnaire_repository: QuestionnaireRepositoryInterface,
        user_service: UserServiceInterface
    ):
        self._evaluation_repository = evaluation_repository
        self._evaluation_period_repository = evaluation_period_repository
        self._questionnaire_repository = questionnaire_repository
        self._user_service = user_service
    
    async def execute(self, request: CreateEvaluationRequest) -> EvaluationResponse:
        """
        Ejecuta el caso de uso de creación de evaluación.
        
        Args:
            request: Datos de la evaluación a crear
            
        Returns:
            EvaluationResponse: Evaluación creada
            
        Raises:
            EvaluationPeriodNotFoundError: Si el período no existe
            EvaluationPeriodNotActiveError: Si el período no está activo
            EvaluationAlreadyExistsError: Si el usuario ya evaluó
            InvalidQuestionResponseError: Si las respuestas son inválidas
        """
        # Verificar que el período existe y está activo
        period = await self._evaluation_period_repository.get_by_id(request.evaluation_period_id)
        if not period:
            raise EvaluationPeriodNotFoundError(f"No se encontró el período con ID: {request.evaluation_period_id}")
        
        if not period.is_active():
            raise EvaluationPeriodNotActiveError(f"El período de evaluación no está activo")
        
        # Verificar que el usuario no ha evaluado ya
        existing_evaluation = await self._evaluation_repository.get_by_period_and_student(
            request.evaluation_period_id, 
            request.student_id
        )
        if existing_evaluation:
            raise EvaluationAlreadyExistsError(
                f"El estudiante ya realizó una evaluación para este período"
            )
        
        # Obtener el cuestionario para validar respuestas
        questionnaire = await self._questionnaire_repository.get_by_id(period.questionnaire_id)
        
        # Validar que las respuestas correspondan a las preguntas del cuestionario
        question_ids = set(questionnaire.question_ids)
        response_question_ids = set(response.question_id for response in request.responses)
        
        if question_ids != response_question_ids:
            missing_questions = question_ids - response_question_ids
            extra_questions = response_question_ids - question_ids
            error_msg = []
            if missing_questions:
                error_msg.append(f"Faltan respuestas para preguntas: {missing_questions}")
            if extra_questions:
                error_msg.append(f"Respuestas para preguntas no válidas: {extra_questions}")
            raise InvalidQuestionResponseError("; ".join(error_msg))
        
        # Verificar que el usuario existe y puede evaluar
        user = await self._user_service.get_user_by_id(request.student_id)
        if not user or user.role != "student":
            raise ValueError(f"El usuario no es un estudiante válido")
        
        # Crear la entidad con validaciones de dominio
        evaluation = Evaluation.create(
            student_id=request.student_id,
            instructor_id=request.instructor_id,
            evaluation_period_id=request.evaluation_period_id,
            responses=request.responses,
            comments=request.comments
        )
        
        # Persistir en el repositorio
        created_evaluation = await self._evaluation_repository.create(evaluation)
        
        return EvaluationResponse(
            id=created_evaluation.id,
            student_id=created_evaluation.student_id,
            instructor_id=created_evaluation.instructor_id,
            evaluation_period_id=created_evaluation.evaluation_period_id,
            status=created_evaluation.status.value,
            responses=created_evaluation.responses,
            comments=created_evaluation.comments,
            submitted_at=created_evaluation.submitted_at,
            created_at=created_evaluation.created_at,
            updated_at=created_evaluation.updated_at
        )
