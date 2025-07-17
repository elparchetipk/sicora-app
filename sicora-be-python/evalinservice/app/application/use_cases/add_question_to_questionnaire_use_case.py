"""Add Question to Questionnaire use case."""

from uuid import UUID

from ...domain.repositories import QuestionnaireRepositoryInterface, QuestionRepositoryInterface
from ...domain.exceptions import (
    QuestionnaireNotFoundError, 
    QuestionNotFoundError, 
    DuplicateQuestionError
)
from ..dtos.questionnaire_dtos import AddQuestionToQuestionnaireRequest, QuestionnaireResponse


class AddQuestionToQuestionnaireUseCase:
    """
    Caso de uso para agregar una pregunta a un cuestionario.
    
    Responsabilidades:
    - Validar que el cuestionario existe
    - Validar que la pregunta existe
    - Verificar que la pregunta no esté ya en el cuestionario
    - Agregar la pregunta usando métodos de dominio
    - Persistir cambios y retornar respuesta actualizada
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
        request: AddQuestionToQuestionnaireRequest
    ) -> QuestionnaireResponse:
        """
        Ejecuta el caso de uso de agregar pregunta a cuestionario.
        
        Args:
            questionnaire_id: ID del cuestionario
            request: Datos de la pregunta a agregar
            
        Returns:
            QuestionnaireResponse: Cuestionario actualizado
            
        Raises:
            QuestionnaireNotFoundError: Si el cuestionario no existe
            QuestionNotFoundError: Si la pregunta no existe
            DuplicateQuestionError: Si la pregunta ya está en el cuestionario
        """
        # Buscar cuestionario
        questionnaire = await self._questionnaire_repository.get_by_id(questionnaire_id)
        if not questionnaire:
            raise QuestionnaireNotFoundError(f"Cuestionario con ID {questionnaire_id} no encontrado")
        
        # Verificar que la pregunta existe
        question = await self._question_repository.get_by_id(request.question_id)
        if not question:
            raise QuestionNotFoundError(f"Pregunta con ID {request.question_id} no encontrada")
        
        # Agregar pregunta usando método de dominio (incluye validación de duplicados)
        questionnaire.add_question(request.question_id)
        
        # Persistir cambios
        updated_questionnaire = await self._questionnaire_repository.update(questionnaire)
        
        # Convertir a DTO de respuesta
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
