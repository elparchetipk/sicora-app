"""Update Question use case."""

from uuid import UUID

from ...domain.repositories import QuestionRepositoryInterface
from ...domain.exceptions import QuestionNotFoundError, QuestionAlreadyExistsError
from ..dtos.question_dtos import UpdateQuestionRequest, QuestionResponse


class UpdateQuestionUseCase:
    """
    Caso de uso para actualizar una pregunta existente.
    
    Responsabilidades:
    - Validar que la pregunta existe
    - Verificar que no se duplique el texto si se cambia
    - Aplicar actualizaciones usando métodos de dominio
    - Persistir cambios en el repositorio
    - Retornar la respuesta actualizada
    """
    
    def __init__(self, question_repository: QuestionRepositoryInterface):
        self._question_repository = question_repository
    
    async def execute(self, question_id: UUID, request: UpdateQuestionRequest) -> QuestionResponse:
        """
        Ejecuta el caso de uso de actualización de pregunta.
        
        Args:
            question_id: ID de la pregunta a actualizar
            request: Datos de actualización
            
        Returns:
            QuestionResponse: Pregunta actualizada
            
        Raises:
            QuestionNotFoundError: Si la pregunta no existe
            QuestionAlreadyExistsError: Si el nuevo texto ya existe
            InvalidQuestionTextError: Si el texto es inválido
        """
        # Buscar pregunta existente
        question = await self._question_repository.get_by_id(question_id)
        
        if not question:
            raise QuestionNotFoundError(f"Pregunta con ID {question_id} no encontrada")
        
        # Verificar duplicado de texto si se está cambiando
        if request.text and request.text != question.text:
            if await self._question_repository.exists_by_text(request.text, exclude_id=question_id):
                raise QuestionAlreadyExistsError(f"Ya existe una pregunta con el texto: {request.text}")
        
        # Aplicar actualizaciones usando métodos de dominio
        if request.text:
            question.update_text(request.text)
        
        if request.category:
            question.update_category(request.category)
        
        if request.options is not None:
            question.set_options(request.options)
        
        if request.order_index is not None:
            question.set_order(request.order_index)
        
        if request.is_required is not None:
            if request.is_required != question.is_required:
                question.toggle_required()
        
        # Persistir cambios
        updated_question = await self._question_repository.update(question)
        
        # Convertir a DTO de respuesta
        return QuestionResponse(
            id=updated_question.id,
            text=updated_question.text,
            question_type=updated_question.question_type,
            category=updated_question.category,
            is_required=updated_question.is_required,
            order_index=updated_question.order_index,
            is_active=updated_question.is_active,
            options=updated_question.options,
            created_at=updated_question.created_at,
            updated_at=updated_question.updated_at
        )
