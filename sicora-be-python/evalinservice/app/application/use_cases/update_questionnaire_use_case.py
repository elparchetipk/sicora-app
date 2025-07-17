"""Update Questionnaire use case."""

from uuid import UUID

from ...domain.repositories import QuestionnaireRepositoryInterface
from ...domain.exceptions import QuestionnaireNotFoundError, QuestionnaireAlreadyExistsError
from ..dtos.questionnaire_dtos import UpdateQuestionnaireRequest, QuestionnaireResponse


class UpdateQuestionnaireUseCase:
    """
    Caso de uso para actualizar un cuestionario existente.
    
    Responsabilidades:
    - Validar que el cuestionario existe
    - Verificar que el nuevo nombre no esté en uso por otro cuestionario
    - Aplicar actualizaciones con validaciones de dominio
    - Persistir cambios en el repositorio
    """
    
    def __init__(self, questionnaire_repository: QuestionnaireRepositoryInterface):
        self._questionnaire_repository = questionnaire_repository
    
    async def execute(
        self, 
        questionnaire_id: UUID, 
        request: UpdateQuestionnaireRequest
    ) -> QuestionnaireResponse:
        """
        Ejecuta el caso de uso de actualización de cuestionario.
        
        Args:
            questionnaire_id: ID del cuestionario a actualizar
            request: Datos a actualizar
            
        Returns:
            QuestionnaireResponse: Cuestionario actualizado
            
        Raises:
            QuestionnaireNotFoundError: Si el cuestionario no existe
            QuestionnaireAlreadyExistsError: Si el nuevo nombre ya está en uso
        """
        # Obtener el cuestionario existente
        questionnaire = await self._questionnaire_repository.get_by_id(questionnaire_id)
        if not questionnaire:
            raise QuestionnaireNotFoundError(f"No se encontró el cuestionario con ID: {questionnaire_id}")
        
        # Verificar nombre duplicado si se está cambiando
        if request.name and request.name != questionnaire.name:
            if await self._questionnaire_repository.exists_by_name(request.name):
                raise QuestionnaireAlreadyExistsError(f"Ya existe un cuestionario con el nombre: {request.name}")
        
        # Aplicar actualizaciones
        if request.name:
            questionnaire.update_name(request.name)
        
        if request.description is not None:
            questionnaire.update_description(request.description)
        
        if request.is_active is not None:
            if request.is_active:
                questionnaire.activate()
            else:
                questionnaire.deactivate()
        
        # Persistir cambios
        updated_questionnaire = await self._questionnaire_repository.update(questionnaire)
        
        return QuestionnaireResponse(
            id=updated_questionnaire.id,
            name=updated_questionnaire.name,
            description=updated_questionnaire.description,
            is_active=updated_questionnaire.is_active,
            question_count=updated_questionnaire.get_question_count(),
            created_at=updated_questionnaire.created_at,
            updated_at=updated_questionnaire.updated_at,
            question_ids=updated_questionnaire.question_ids
        )
