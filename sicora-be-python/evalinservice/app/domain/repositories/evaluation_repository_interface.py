"""Evaluation repository interface."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from ..entities.evaluation import Evaluation
from ..value_objects.evaluation_status import EvaluationStatus


class EvaluationRepositoryInterface(ABC):
    """
    Interface para el repositorio de evaluaciones.
    Define el contrato para persistencia de evaluaciones de instructores.
    """
    
    @abstractmethod
    async def create(self, evaluation: Evaluation) -> Evaluation:
        """Crea una nueva evaluación."""
        pass
    
    @abstractmethod
    async def get_by_id(self, evaluation_id: UUID) -> Optional[Evaluation]:
        """Obtiene una evaluación por su ID."""
        pass
    
    @abstractmethod
    async def get_all(
        self,
        student_id: Optional[UUID] = None,
        instructor_id: Optional[UUID] = None,
        period_id: Optional[UUID] = None,
        status: Optional[EvaluationStatus] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Evaluation]:
        """Obtiene una lista de evaluaciones con filtros opcionales."""
        pass
    
    @abstractmethod
    async def update(self, evaluation: Evaluation) -> Evaluation:
        """Actualiza una evaluación existente."""
        pass
    
    @abstractmethod
    async def delete(self, evaluation_id: UUID) -> bool:
        """Elimina una evaluación."""
        pass
    
    @abstractmethod
    async def get_by_student_and_instructor(
        self, 
        student_id: UUID, 
        instructor_id: UUID,
        period_id: Optional[UUID] = None
    ) -> Optional[Evaluation]:
        """Obtiene evaluación específica de un estudiante hacia un instructor."""
        pass
    
    @abstractmethod
    async def get_student_evaluations(
        self, 
        student_id: UUID,
        period_id: Optional[UUID] = None
    ) -> List[Evaluation]:
        """Obtiene todas las evaluaciones realizadas por un estudiante."""
        pass
    
    @abstractmethod
    async def get_instructor_evaluations(
        self, 
        instructor_id: UUID,
        period_id: Optional[UUID] = None,
        status: Optional[EvaluationStatus] = None
    ) -> List[Evaluation]:
        """Obtiene todas las evaluaciones recibidas por un instructor."""
        pass
    
    @abstractmethod
    async def get_period_evaluations(
        self, 
        period_id: UUID,
        status: Optional[EvaluationStatus] = None
    ) -> List[Evaluation]:
        """Obtiene todas las evaluaciones de un período específico."""
        pass
    
    @abstractmethod
    async def count_total(
        self,
        student_id: Optional[UUID] = None,
        instructor_id: Optional[UUID] = None,
        period_id: Optional[UUID] = None,
        status: Optional[EvaluationStatus] = None
    ) -> int:
        """Cuenta el total de evaluaciones con filtros opcionales."""
        pass
    
    @abstractmethod
    async def exists_evaluation(
        self, 
        student_id: UUID, 
        instructor_id: UUID, 
        period_id: UUID
    ) -> bool:
        """Verifica si existe una evaluación específica."""
        pass
    
    @abstractmethod
    async def get_evaluation_statistics(
        self,
        instructor_id: Optional[UUID] = None,
        period_id: Optional[UUID] = None
    ) -> Dict:
        """Obtiene estadísticas de evaluaciones."""
        pass
    
    @abstractmethod
    async def get_submitted_evaluations_by_period(self, period_id: UUID) -> List[Evaluation]:
        """Obtiene evaluaciones enviadas de un período específico."""
        pass
    
    @abstractmethod
    async def get_instructor_average_ratings(
        self, 
        instructor_id: UUID,
        period_id: Optional[UUID] = None
    ) -> Dict[UUID, float]:
        """Obtiene promedios de calificación por pregunta para un instructor."""
        pass
