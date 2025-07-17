"""Get Question by ID use case."""

from uuid import UUID

from ...domain.repositories import QuestionRepositoryInterface
from ...domain.exceptions import QuestionNotFoundError
from ..dtos.question_dtos import QuestionResponse


class GetQuestionByIdUseCase:
    """
    Caso de uso para obtener una pregunta por su ID.
    
    Responsabilidades:
    - Buscar pregunta por ID en el repositorio
    - Validar que la pregunta existe
    - Convertir entidad a DTO de respuesta
    """
    
    def __init__(self, question_repository: QuestionRepositoryInterface):
        self._question_repository = question_repository
    
    async def execute(self, question_id: UUID) -> QuestionResponse:
        """
        Ejecuta el caso de uso de obtención de pregunta por ID.
        
        Args:
            question_id: ID de la pregunta a buscar
            
        Returns:
            QuestionResponse: Pregunta encontrada
            
        Raises:
            QuestionNotFoundError: Si la pregunta no existe
        """
        # Buscar pregunta en el repositorio
        question = await self._question_repository.get_by_id(question_id)
        
        if not question:
            raise QuestionNotFoundError(f"Pregunta con ID {question_id} no encontrada")
        
        # Convertir a DTO de respuesta
        return QuestionResponse(
            id=question.id,
            text=question.text,
            question_type=question.question_type,
            category=question.category,
            is_required=question.is_required,
            order_index=question.order_index,
            is_active=question.is_active,
            options=question.options,
            created_at=question.created_at,
            updated_at=question.updated_at
        )
