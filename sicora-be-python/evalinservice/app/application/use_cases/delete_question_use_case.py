"""Delete Question use case."""

from uuid import UUID

from ...domain.repositories import QuestionRepositoryInterface, QuestionnaireRepositoryInterface
from ...domain.exceptions import QuestionNotFoundError, QuestionInUseError


class DeleteQuestionUseCase:
    """
    Caso de uso para eliminar una pregunta.
    
    Responsabilidades:
    - Validar que la pregunta existe
    - Verificar que la pregunta no esté en uso en cuestionarios
    - Eliminar la pregunta del repositorio
    """
    
    def __init__(
        self, 
        question_repository: QuestionRepositoryInterface,
        questionnaire_repository: QuestionnaireRepositoryInterface
    ):
        self._question_repository = question_repository
        self._questionnaire_repository = questionnaire_repository
    
    async def execute(self, question_id: UUID) -> bool:
        """
        Ejecuta el caso de uso de eliminación de pregunta.
        
        Args:
            question_id: ID de la pregunta a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente
            
        Raises:
            QuestionNotFoundError: Si la pregunta no existe
            QuestionInUseError: Si la pregunta está siendo usada en cuestionarios
        """
        # Verificar que la pregunta existe
        question = await self._question_repository.get_by_id(question_id)
        
        if not question:
            raise QuestionNotFoundError(f"Pregunta con ID {question_id} no encontrada")
        
        # Verificar que no esté en uso
        questionnaires_using_question = await self._questionnaire_repository.get_questionnaires_with_question(question_id)
        
        if questionnaires_using_question:
            questionnaire_names = [q.name for q in questionnaires_using_question]
            raise QuestionInUseError(
                f"La pregunta está siendo usada en los cuestionarios: {', '.join(questionnaire_names)}"
            )
        
        # Eliminar la pregunta
        return await self._question_repository.delete(question_id)
