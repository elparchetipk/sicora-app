"""Remove Question from Questionnaire use case."""

from uuid import UUID

from ...domain.repositories import QuestionnaireRepositoryInterface, QuestionRepositoryInterface
from ...domain.exceptions import QuestionnaireNotFoundError, QuestionNotFoundError, QuestionNotInQuestionnaireError
from ..dtos.questionnaire_dtos import QuestionnaireResponse


class RemoveQuestionFromQuestionnaireUseCase:
    """
    Caso de uso para remover una pregunta de un cuestionario.
    
    Responsabilidades:
    - Validar que el cuestionario y la pregunta existen
    - Verificar que la pregunta esté en el cuestionario
    - Remover la pregunta del cuestionario
    - Persistir cambios en el repositorio
    """
    
    def __init__(
        self,
        questionnaire_repository: QuestionnaireRepositoryInterface,
        question_repository: QuestionRepositoryInterface
    ):
        self._questionnaire_repository = questionnaire_repository
        self._question_repository = question_repository
    
    async def execute(
        self, 
        questionnaire_id: UUID, 
        question_id: UUID
    ) -> QuestionnaireResponse:
        """
        Ejecuta el caso de uso de remoción de pregunta del cuestionario.
        
        Args:
            questionnaire_id: ID del cuestionario
            question_id: ID de la pregunta a remover
            
        Returns:
            QuestionnaireResponse: Cuestionario actualizado
            
        Raises:
            QuestionnaireNotFoundError: Si el cuestionario no existe
            QuestionNotFoundError: Si la pregunta no existe
            QuestionNotInQuestionnaireError: Si la pregunta no está en el cuestionario
        """
        # Verificar que el cuestionario existe
        questionnaire = await self._questionnaire_repository.get_by_id(questionnaire_id)
        if not questionnaire:
            raise QuestionnaireNotFoundError(f"No se encontró el cuestionario con ID: {questionnaire_id}")
        
        # Verificar que la pregunta existe
        question = await self._question_repository.get_by_id(question_id)
        if not question:
            raise QuestionNotFoundError(f"No se encontró la pregunta con ID: {question_id}")
        
        # Remover la pregunta del cuestionario
        questionnaire.remove_question(question_id)
        
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
