"""Get Questions use case."""

from typing import Optional

from ...domain.repositories import QuestionRepositoryInterface
from ...domain.value_objects import QuestionType
from ..dtos.question_dtos import QuestionResponse, QuestionListResponse


class GetQuestionsUseCase:
    """
    Caso de uso para obtener preguntas con filtros opcionales.
    
    Responsabilidades:
    - Aplicar filtros de búsqueda
    - Obtener preguntas del repositorio con paginación
    - Convertir entidades a DTOs de respuesta
    - Calcular metadatos de paginación
    """
    
    def __init__(self, question_repository: QuestionRepositoryInterface):
        self._question_repository = question_repository
    
    async def execute(
        self,
        category: Optional[str] = None,
        question_type: Optional[QuestionType] = None,
        is_active: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> QuestionListResponse:
        """
        Ejecuta el caso de uso de obtención de preguntas.
        
        Args:
            category: Filtro por categoría (opcional)
            question_type: Filtro por tipo de pregunta (opcional)
            is_active: Filtro por estado activo (opcional)
            limit: Límite de resultados
            offset: Offset para paginación
            
        Returns:
            QuestionListResponse: Lista de preguntas con metadatos
        """
        # Obtener preguntas del repositorio
        questions = await self._question_repository.get_all(
            category=category,
            question_type=question_type,
            is_active=is_active,
            limit=limit,
            offset=offset
        )
        
        # Obtener total para paginación
        total = await self._question_repository.count_total(
            category=category,
            question_type=question_type,
            is_active=is_active
        )
        
        # Convertir entidades a DTOs
        question_responses = [
            QuestionResponse(
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
            for question in questions
        ]
        
        return QuestionListResponse(
            questions=question_responses,
            total=total,
            limit=limit,
            offset=offset
        )
