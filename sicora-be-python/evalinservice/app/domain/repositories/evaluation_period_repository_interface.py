"""Evaluation Period repository interface."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ..entities.evaluation_period import EvaluationPeriod
from ..value_objects.period_status import PeriodStatus


class EvaluationPeriodRepositoryInterface(ABC):
    """
    Interface para el repositorio de períodos de evaluación.
    Define el contrato para persistencia de períodos de evaluación.
    """
    
    @abstractmethod
    async def create(self, period: EvaluationPeriod) -> EvaluationPeriod:
        """Crea un nuevo período de evaluación."""
        pass
    
    @abstractmethod
    async def get_by_id(self, period_id: UUID) -> Optional[EvaluationPeriod]:
        """Obtiene un período por su ID."""
        pass
    
    @abstractmethod
    async def get_all(
        self,
        status: Optional[PeriodStatus] = None,
        is_active: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[EvaluationPeriod]:
        """Obtiene una lista de períodos con filtros opcionales."""
        pass
    
    @abstractmethod
    async def update(self, period: EvaluationPeriod) -> EvaluationPeriod:
        """Actualiza un período existente."""
        pass
    
    @abstractmethod
    async def delete(self, period_id: UUID) -> bool:
        """Elimina un período."""
        pass
    
    @abstractmethod
    async def get_active_periods(self) -> List[EvaluationPeriod]:
        """Obtiene todos los períodos activos."""
        pass
    
    @abstractmethod
    async def get_current_periods(self) -> List[EvaluationPeriod]:
        """Obtiene períodos que están actualmente en vigor (por fechas)."""
        pass
    
    @abstractmethod
    async def get_upcoming_periods(self) -> List[EvaluationPeriod]:
        """Obtiene períodos programados para el futuro."""
        pass
    
    @abstractmethod
    async def get_expired_periods(self) -> List[EvaluationPeriod]:
        """Obtiene períodos que han expirado."""
        pass
    
    @abstractmethod
    async def get_overlapping_periods(
        self, 
        start_date: datetime, 
        end_date: datetime,
        exclude_id: Optional[UUID] = None
    ) -> List[EvaluationPeriod]:
        """Obtiene períodos que se superponen con el rango de fechas dado."""
        pass
    
    @abstractmethod
    async def count_total(
        self,
        status: Optional[PeriodStatus] = None,
        is_active: Optional[bool] = None
    ) -> int:
        """Cuenta el total de períodos con filtros opcionales."""
        pass
    
    @abstractmethod
    async def exists_by_name(self, name: str, exclude_id: Optional[UUID] = None) -> bool:
        """Verifica si existe un período con el nombre especificado."""
        pass
    
    @abstractmethod
    async def get_periods_by_questionnaire(self, questionnaire_id: UUID) -> List[EvaluationPeriod]:
        """Obtiene períodos asociados a un cuestionario específico."""
        pass
