"""Create Question use case."""

from typing import Optional
from uuid import UUID

from ...domain.entities import Question
from ...domain.repositories import QuestionRepositoryInterface
from ...domain.exceptions import QuestionAlreadyExistsError
from ..dtos.question_dtos import CreateQuestionRequest, QuestionResponse


class CreateQuestionUseCase:
    """
    Caso de uso para crear una nueva pregunta de evaluación.
    
    Responsabilidades:
    - Validar que no exista una pregunta con el mismo texto
    - Crear la entidad Question con validaciones de dominio
    - Persistir la pregunta en el repositorio
    - Retornar la respuesta formateada
    """
    
    def __init__(self, question_repository: QuestionRepositoryInterface):
        self._question_repository = question_repository
    
    async def execute(self, request: CreateQuestionRequest) -> QuestionResponse:
        """
        Ejecuta el caso de uso de creación de pregunta.
        
        Args:
            request: Datos de la pregunta a crear
            
        Returns:
            QuestionResponse: Pregunta creada
            
        Raises:
            QuestionAlreadyExistsError: Si ya existe una pregunta con el mismo texto
            InvalidQuestionTextError: Si el texto es inválido
            InvalidQuestionTypeError: Si el tipo es inválido
        """
        # Verificar si ya existe una pregunta con el mismo texto
        if await self._question_repository.exists_by_text(request.text):
            raise QuestionAlreadyExistsError(f"Ya existe una pregunta con el texto: {request.text}")
        
        # Si no se especifica order_index, obtener el siguiente disponible
        if request.order_index == 0:
            max_order = await self._question_repository.get_max_order_index(request.category)
            request.order_index = max_order + 1
        
        # Crear la entidad con validaciones de dominio
        question = Question.create(
            text=request.text,
            question_type=request.question_type,
            category=request.category,
            is_required=request.is_required,
            order_index=request.order_index,
            options=request.options
        )
        
        # Persistir en el repositorio
        created_question = await self._question_repository.create(question)
        
        # Convertir a DTO de respuesta
        return QuestionResponse(
            id=created_question.id,
            text=created_question.text,
            question_type=created_question.question_type,
            category=created_question.category,
            is_required=created_question.is_required,
            order_index=created_question.order_index,
            is_active=created_question.is_active,
            options=created_question.options,
            created_at=created_question.created_at,
            updated_at=created_question.updated_at
        )
