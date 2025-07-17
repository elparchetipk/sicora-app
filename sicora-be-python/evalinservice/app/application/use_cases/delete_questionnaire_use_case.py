"""Delete Questionnaire use case."""

from uuid import UUID

from ...domain.repositories import QuestionnaireRepositoryInterface, EvaluationPeriodRepositoryInterface
from ...domain.exceptions import QuestionnaireNotFoundError, QuestionnaireInUseError


class DeleteQuestionnaireUseCase:
    """
    Caso de uso para eliminar un cuestionario.
    
    Responsabilidades:
    - Validar que el cuestionario existe
    - Verificar que no esté siendo usado en períodos de evaluación
    - Eliminar del repositorio
    """
    
    def __init__(
        self, 
        questionnaire_repository: QuestionnaireRepositoryInterface,
        evaluation_period_repository: EvaluationPeriodRepositoryInterface
    ):
        self._questionnaire_repository = questionnaire_repository
        self._evaluation_period_repository = evaluation_period_repository
    
    async def execute(self, questionnaire_id: UUID) -> bool:
        """
        Ejecuta el caso de uso de eliminación de cuestionario.
        
        Args:
            questionnaire_id: ID del cuestionario a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            QuestionnaireNotFoundError: Si el cuestionario no existe
            QuestionnaireInUseError: Si el cuestionario está siendo usado
        """
        # Verificar que el cuestionario existe
        questionnaire = await self._questionnaire_repository.get_by_id(questionnaire_id)
        if not questionnaire:
            raise QuestionnaireNotFoundError(f"No se encontró el cuestionario con ID: {questionnaire_id}")
        
        # Verificar que no esté siendo usado en períodos de evaluación
        periods_using_questionnaire = await self._evaluation_period_repository.get_by_questionnaire_id(questionnaire_id)
        if periods_using_questionnaire:
            raise QuestionnaireInUseError(
                f"No se puede eliminar el cuestionario porque está siendo usado en {len(periods_using_questionnaire)} período(s) de evaluación"
            )
        
        # Eliminar el cuestionario
        return await self._questionnaire_repository.delete(questionnaire_id)
