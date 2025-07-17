"""Questionnaire repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.questionnaire import Questionnaire


class QuestionnaireRepositoryInterface(ABC):
    """
    Interface para el repositorio de cuestionarios.
    Define el contrato para persistencia de cuestionarios de evaluación.
    """
    
    @abstractmethod
    async def create(self, questionnaire: Questionnaire) -> Questionnaire:
        """Crea un nuevo cuestionario."""
        pass
    
    @abstractmethod
    async def get_by_id(self, questionnaire_id: UUID) -> Optional[Questionnaire]:
        """Obtiene un cuestionario por su ID."""
        pass
    
    @abstractmethod
    async def get_all(
        self,
        is_active: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Questionnaire]:
        """Obtiene una lista de cuestionarios con filtros opcionales."""
        pass
    
    @abstractmethod
    async def update(self, questionnaire: Questionnaire) -> Questionnaire:
        """Actualiza un cuestionario existente."""
        pass
    
    @abstractmethod
    async def delete(self, questionnaire_id: UUID) -> bool:
        """Elimina un cuestionario."""
        pass
    
    @abstractmethod
    async def get_active_questionnaires(self) -> List[Questionnaire]:
        """Obtiene todos los cuestionarios activos."""
        pass
    
    @abstractmethod
    async def count_total(self, is_active: Optional[bool] = None) -> int:
        """Cuenta el total de cuestionarios con filtros opcionales."""
        pass
    
    @abstractmethod
    async def exists_by_name(self, name: str, exclude_id: Optional[UUID] = None) -> bool:
        """Verifica si existe un cuestionario con el nombre especificado."""
        pass
    
    @abstractmethod
    async def get_questionnaires_with_question(self, question_id: UUID) -> List[Questionnaire]:
        """Obtiene cuestionarios que contienen una pregunta específica."""
        pass
    
    @abstractmethod
    async def get_questionnaire_questions(self, questionnaire_id: UUID) -> List[UUID]:
        """Obtiene los IDs de las preguntas de un cuestionario en orden."""
        pass
