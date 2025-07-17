from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.evaluation_criterion import (
    EvaluationCriterion,
    CriterionApproval,
    CriterionChangeHistory,
    CriterionCategory,
    CriterionStatus,
)


class EvaluationCriterionRepository(ABC):
    """Repository interface for evaluation criteria."""

    @abstractmethod
    async def create(self, criterion: EvaluationCriterion) -> EvaluationCriterion:
        """Create a new evaluation criterion."""
        pass

    @abstractmethod
    async def get_by_id(self, criterion_id: UUID) -> Optional[EvaluationCriterion]:
        """Get criterion by ID."""
        pass

    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[EvaluationCriterion]:
        """Get criterion by code (e.g., AR-001)."""
        pass

    @abstractmethod
    async def get_active_criteria(
        self, category: Optional[CriterionCategory] = None
    ) -> List[EvaluationCriterion]:
        """Get all active criteria, optionally filtered by category."""
        pass

    @abstractmethod
    async def get_by_status(self, status: CriterionStatus) -> List[EvaluationCriterion]:
        """Get criteria by status."""
        pass

    @abstractmethod
    async def update(self, criterion: EvaluationCriterion) -> EvaluationCriterion:
        """Update an existing criterion."""
        pass

    @abstractmethod
    async def get_pending_approval(self) -> List[EvaluationCriterion]:
        """Get criteria pending approval."""
        pass

    @abstractmethod
    async def get_versions(self, code: str) -> List[EvaluationCriterion]:
        """Get all versions of a criterion by code."""
        pass


class CriterionApprovalRepository(ABC):
    """Repository interface for criterion approvals."""

    @abstractmethod
    async def create(self, approval: CriterionApproval) -> CriterionApproval:
        """Create a new approval record."""
        pass

    @abstractmethod
    async def get_by_criterion_id(self, criterion_id: UUID) -> List[CriterionApproval]:
        """Get all approvals for a criterion."""
        pass

    @abstractmethod
    async def get_approval_count(
        self, criterion_id: UUID, approved: bool = True
    ) -> int:
        """Count approvals/rejections for a criterion."""
        pass

    @abstractmethod
    async def has_member_voted(self, criterion_id: UUID, member_id: UUID) -> bool:
        """Check if a pedagogical member has already voted."""
        pass


class CriterionChangeHistoryRepository(ABC):
    """Repository interface for criterion change history."""

    @abstractmethod
    async def create(self, history: CriterionChangeHistory) -> CriterionChangeHistory:
        """Create a new history record."""
        pass

    @abstractmethod
    async def get_by_criterion_id(
        self, criterion_id: UUID
    ) -> List[CriterionChangeHistory]:
        """Get change history for a criterion."""
        pass

    @abstractmethod
    async def get_recent_changes(self, days: int = 30) -> List[CriterionChangeHistory]:
        """Get recent changes within specified days."""
        pass
