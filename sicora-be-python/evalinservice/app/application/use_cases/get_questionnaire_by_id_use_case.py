"""Get Questionnaire by ID use case."""

from uuid import UUID

from ...domain.repositories import QuestionnaireRepositoryInterface
from ...domain.exceptions import QuestionnaireNotFoundError
from ..dtos.questionnaire_dtos import QuestionnaireResponse


class GetQuestionnaireByIdUseCase:
    """
    Caso de uso para obtener un cuestionario por su ID.
    
    Responsabilidades:
    - Buscar el cuestionario por ID en el repositorio
    - Validar que el cuestionario existe
    - Convertir entidad a DTO de respuesta
    """
    
    def __init__(self, questionnaire_repository: QuestionnaireRepositoryInterface):
        self._questionnaire_repository = questionnaire_repository
    
    async def execute(self, questionnaire_id: UUID) -> QuestionnaireResponse:
        """
        Ejecuta el caso de uso de obtención de cuestionario por ID.
        
        Args:
            questionnaire_id: ID del cuestionario a buscar
            
        Returns:
            QuestionnaireResponse: Cuestionario encontrado
            
        Raises:
            QuestionnaireNotFoundError: Si el cuestionario no existe
        """
        questionnaire = await self._questionnaire_repository.get_by_id(questionnaire_id)
        
        if not questionnaire:
            raise QuestionnaireNotFoundError(f"No se encontró el cuestionario con ID: {questionnaire_id}")
        
        return QuestionnaireResponse(
            id=questionnaire.id,
            name=questionnaire.name,
            description=questionnaire.description,
            is_active=questionnaire.is_active,
            question_count=questionnaire.get_question_count(),
            created_at=questionnaire.created_at,
            updated_at=questionnaire.updated_at,
            question_ids=questionnaire.question_ids
        )
