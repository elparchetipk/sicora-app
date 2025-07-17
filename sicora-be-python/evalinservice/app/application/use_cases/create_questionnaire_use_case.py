"""Create Questionnaire use case."""

from ...domain.entities import Questionnaire
from ...domain.repositories import QuestionnaireRepositoryInterface
from ...domain.exceptions import QuestionnaireAlreadyExistsError
from ..dtos.questionnaire_dtos import CreateQuestionnaireRequest, QuestionnaireResponse


class CreateQuestionnaireUseCase:
    """
    Caso de uso para crear un nuevo cuestionario.
    
    Responsabilidades:
    - Validar que no exista un cuestionario con el mismo nombre
    - Crear la entidad Questionnaire con validaciones de dominio
    - Persistir el cuestionario en el repositorio
    - Retornar la respuesta formateada
    """
    
    def __init__(self, questionnaire_repository: QuestionnaireRepositoryInterface):
        self._questionnaire_repository = questionnaire_repository
    
    async def execute(self, request: CreateQuestionnaireRequest) -> QuestionnaireResponse:
        """
        Ejecuta el caso de uso de creación de cuestionario.
        
        Args:
            request: Datos del cuestionario a crear
            
        Returns:
            QuestionnaireResponse: Cuestionario creado
            
        Raises:
            QuestionnaireAlreadyExistsError: Si ya existe un cuestionario con el mismo nombre
            InvalidQuestionnaireNameError: Si el nombre es inválido
        """
        # Verificar si ya existe un cuestionario con el mismo nombre
        if await self._questionnaire_repository.exists_by_name(request.name):
            raise QuestionnaireAlreadyExistsError(f"Ya existe un cuestionario con el nombre: {request.name}")
        
        # Crear la entidad con validaciones de dominio
        questionnaire = Questionnaire.create(
            name=request.name,
            description=request.description
        )
        
        # Persistir en el repositorio
        created_questionnaire = await self._questionnaire_repository.create(questionnaire)
        
        # Convertir a DTO de respuesta
        return QuestionnaireResponse(
            id=created_questionnaire.id,
            name=created_questionnaire.name,
            description=created_questionnaire.description,
            is_active=created_questionnaire.is_active,
            question_count=created_questionnaire.get_question_count(),
            created_at=created_questionnaire.created_at,
            updated_at=created_questionnaire.updated_at,
            question_ids=created_questionnaire.question_ids
        )
