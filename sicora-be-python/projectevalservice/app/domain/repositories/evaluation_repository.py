from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ..entities import Evaluation, EvaluationStatus, EvaluationType


class EvaluationRepository(ABC):

    @abstractmethod
    async def create(self, evaluation: Evaluation) -> Evaluation:
        """Create a new evaluation"""
        pass

    @abstractmethod
    async def get_by_id(self, evaluation_id: UUID) -> Optional[Evaluation]:
        """Get evaluation by ID"""
        pass

    @abstractmethod
    async def get_by_project_id(self, project_id: UUID) -> List[Evaluation]:
        """Get evaluations by project ID"""
        pass

    @abstractmethod
    async def get_by_evaluator_id(self, evaluator_id: UUID) -> List[Evaluation]:
        """Get evaluations by evaluator ID"""
        pass

    @abstractmethod
    async def get_by_status(self, status: EvaluationStatus) -> List[Evaluation]:
        """Get evaluations by status"""
        pass

    @abstractmethod
    async def get_by_type(self, evaluation_type: EvaluationType) -> List[Evaluation]:
        """Get evaluations by type"""
        pass

    @abstractmethod
    async def get_scheduled_evaluations(
        self, evaluator_id: Optional[UUID] = None
    ) -> List[Evaluation]:
        """Get scheduled evaluations, optionally filtered by evaluator"""
        pass

    @abstractmethod
    async def get_evaluations_by_period(
        self, academic_year: int, trimester: int
    ) -> List[Evaluation]:
        """Get evaluations by academic period"""
        pass

    @abstractmethod
    async def update(self, evaluation: Evaluation) -> Evaluation:
        """Update existing evaluation"""
        pass

    @abstractmethod
    async def delete(self, evaluation_id: UUID) -> bool:
        """Delete evaluation"""
        pass

    @abstractmethod
    async def get_project_evaluation_history(
        self, project_id: UUID
    ) -> List[Evaluation]:
        """Get complete evaluation history for a project"""
        pass
