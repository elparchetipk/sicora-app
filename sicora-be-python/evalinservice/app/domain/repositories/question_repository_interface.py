"""Question repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.question import Question
from ..value_objects.question_type import QuestionType


class QuestionRepositoryInterface(ABC):
    """
    Interface para el repositorio de preguntas.
    Define el contrato para persistencia de preguntas de evaluación.
    """
    
    @abstractmethod
    async def create(self, question: Question) -> Question:
        """Crea una nueva pregunta."""
        pass
    
    @abstractmethod
    async def get_by_id(self, question_id: UUID) -> Optional[Question]:
        """Obtiene una pregunta por su ID."""
        pass
    
    @abstractmethod
    async def get_all(
        self, 
        category: Optional[str] = None,
        question_type: Optional[QuestionType] = None,
        is_active: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Question]:
        """Obtiene una lista de preguntas con filtros opcionales."""
        pass
    
    @abstractmethod
    async def update(self, question: Question) -> Question:
        """Actualiza una pregunta existente."""
        pass
    
    @abstractmethod
    async def delete(self, question_id: UUID) -> bool:
        """Elimina una pregunta."""
        pass
    
    @abstractmethod
    async def get_by_category(self, category: str) -> List[Question]:
        """Obtiene preguntas por categoría."""
        pass
    
    @abstractmethod
    async def get_by_type(self, question_type: QuestionType) -> List[Question]:
        """Obtiene preguntas por tipo."""
        pass
    
    @abstractmethod
    async def get_active_questions(self) -> List[Question]:
        """Obtiene todas las preguntas activas."""
        pass
    
    @abstractmethod
    async def count_total(
        self,
        category: Optional[str] = None,
        question_type: Optional[QuestionType] = None,
        is_active: Optional[bool] = None
    ) -> int:
        """Cuenta el total de preguntas con filtros opcionales."""
        pass
    
    @abstractmethod
    async def exists_by_text(self, text: str, exclude_id: Optional[UUID] = None) -> bool:
        """Verifica si existe una pregunta con el texto especificado."""
        pass
    
    @abstractmethod
    async def get_max_order_index(self, category: str) -> int:
        """Obtiene el mayor índice de orden en una categoría."""
        pass
    
    @abstractmethod
    async def bulk_create(self, questions: List[Question]) -> List[Question]:
        """Crea múltiples preguntas en una transacción."""
        pass
