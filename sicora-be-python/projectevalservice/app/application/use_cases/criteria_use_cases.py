from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ...domain.entities import (
    EvaluationCriterion,
    CriterionStatus,
    CriterionCategory,
    CriterionApproval,
    ApprovalStatus,
    CriterionChangeHistory,
)
from ...domain.repositories import CriterionRepository


class CreateCriterionUseCase:
    def __init__(self, criterion_repository: CriterionRepository):
        self.criterion_repository = criterion_repository

    async def execute(
        self,
        code: str,
        title: str,
        description: str,
        category: CriterionCategory,
        is_required: bool,
        points: int,
        created_by: UUID,
        effective_date: Optional[datetime] = None,
        expiration_date: Optional[datetime] = None,
    ) -> EvaluationCriterion:
        """Create a new evaluation criterion in draft status"""

        criterion = EvaluationCriterion(
            id=UUID(),
            code=code,
            title=title,
            description=description,
            category=category,
            status=CriterionStatus.DRAFT,
            is_required=is_required,
            points=points,
            version=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            created_by=created_by,
            approved_by=[],
            rejection_reason=None,
            effective_date=effective_date,
            expiration_date=expiration_date,
        )

        # Create change history
        change_history = CriterionChangeHistory(
            id=UUID(),
            criterion_id=criterion.id,
            changed_by=created_by,
            change_type="CREATE",
            old_version=None,
            new_version=criterion.__dict__,
            change_reason="Initial creation",
            created_at=datetime.utcnow(),
        )

        return await self.criterion_repository.create(criterion, change_history)


class SubmitCriterionForApprovalUseCase:
    def __init__(self, criterion_repository: CriterionRepository):
        self.criterion_repository = criterion_repository

    async def execute(
        self, criterion_id: UUID, submitted_by: UUID
    ) -> Optional[EvaluationCriterion]:
        """Submit a criterion for approval"""

        criterion = await self.criterion_repository.get_by_id(criterion_id)
        if not criterion:
            return None

        if criterion.status != CriterionStatus.DRAFT:
            raise ValueError("Only criteria in draft status can be submitted for approval")

        # Update status to pending approval
        updated_criterion = EvaluationCriterion(
            **{
                **criterion.__dict__,
                "status": CriterionStatus.PENDING_APPROVAL,
                "updated_at": datetime.utcnow(),
            }
        )

        # Create change history
        change_history = CriterionChangeHistory(
            id=UUID(),
            criterion_id=criterion.id,
            changed_by=submitted_by,
            change_type="UPDATE",
            old_version=criterion.__dict__,
            new_version=updated_criterion.__dict__,
            change_reason="Submitted for approval",
            created_at=datetime.utcnow(),
        )

        return await self.criterion_repository.update(updated_criterion, change_history)


class ApproveCriterionUseCase:
    def __init__(self, criterion_repository: CriterionRepository):
        self.criterion_repository = criterion_repository

    async def execute(
        self,
        criterion_id: UUID,
        approver_id: UUID,
        comments: Optional[str] = None,
    ) -> Optional[EvaluationCriterion]:
        """Approve a criterion"""

        criterion = await self.criterion_repository.get_by_id(criterion_id)
        if not criterion:
            return None

        if criterion.status != CriterionStatus.PENDING_APPROVAL:
            raise ValueError("Only criteria in pending approval status can be approved")

        # Create approval record
        approval = CriterionApproval(
            id=UUID(),
            criterion_id=criterion.id,
            pedagogical_member_id=approver_id,
            approval_status=ApprovalStatus.APPROVED,
            comments=comments,
            created_at=datetime.utcnow(),
        )

        # Add approver to the list
        approved_by = list(criterion.approved_by) if criterion.approved_by else []
        if approver_id not in approved_by:
            approved_by.append(approver_id)

        # Check if we have enough approvals
        is_fully_approved = len(approved_by) >= 3 or (
            not criterion.requires_unanimous_approval() and len(approved_by) >= 2
        )

        # Update criterion status if fully approved
        updated_criterion = EvaluationCriterion(
            **{
                **criterion.__dict__,
                "approved_by": approved_by,
                "status": CriterionStatus.ACTIVE if is_fully_approved else criterion.status,
                "updated_at": datetime.utcnow(),
            }
        )

        # Create change history
        change_history = CriterionChangeHistory(
            id=UUID(),
            criterion_id=criterion.id,
            changed_by=approver_id,
            change_type="APPROVE",
            old_version=criterion.__dict__,
            new_version=updated_criterion.__dict__,
            change_reason=f"Approved by {approver_id}" + (f": {comments}" if comments else ""),
            created_at=datetime.utcnow(),
        )

        return await self.criterion_repository.approve(
            updated_criterion, approval, change_history
        )


class RejectCriterionUseCase:
    def __init__(self, criterion_repository: CriterionRepository):
        self.criterion_repository = criterion_repository

    async def execute(
        self,
        criterion_id: UUID,
        rejector_id: UUID,
        rejection_reason: str,
    ) -> Optional[EvaluationCriterion]:
        """Reject a criterion"""

        criterion = await self.criterion_repository.get_by_id(criterion_id)
        if not criterion:
            return None

        if criterion.status != CriterionStatus.PENDING_APPROVAL:
            raise ValueError("Only criteria in pending approval status can be rejected")

        # Create rejection record
        rejection = CriterionApproval(
            id=UUID(),
            criterion_id=criterion.id,
            pedagogical_member_id=rejector_id,
            approval_status=ApprovalStatus.REJECTED,
            comments=rejection_reason,
            created_at=datetime.utcnow(),
        )

        # Update criterion status
        updated_criterion = EvaluationCriterion(
            **{
                **criterion.__dict__,
                "status": CriterionStatus.DRAFT,
                "rejection_reason": rejection_reason,
                "updated_at": datetime.utcnow(),
            }
        )

        # Create change history
        change_history = CriterionChangeHistory(
            id=UUID(),
            criterion_id=criterion.id,
            changed_by=rejector_id,
            change_type="REJECT",
            old_version=criterion.__dict__,
            new_version=updated_criterion.__dict__,
            change_reason=f"Rejected: {rejection_reason}",
            created_at=datetime.utcnow(),
        )

        return await self.criterion_repository.reject(
            updated_criterion, rejection, change_history
        )


class GetCriterionUseCase:
    def __init__(self, criterion_repository: CriterionRepository):
        self.criterion_repository = criterion_repository

    async def execute(self, criterion_id: UUID) -> Optional[EvaluationCriterion]:
        """Get criterion by ID"""
        return await self.criterion_repository.get_by_id(criterion_id)


class GetCriteriaUseCase:
    def __init__(self, criterion_repository: CriterionRepository):
        self.criterion_repository = criterion_repository

    async def execute(
        self,
        status: Optional[CriterionStatus] = None,
        category: Optional[CriterionCategory] = None,
        is_required: Optional[bool] = None,
        active_only: bool = False,
    ) -> List[EvaluationCriterion]:
        """Get criteria with optional filters"""
        return await self.criterion_repository.get_criteria(
            status=status,
            category=category,
            is_required=is_required,
            active_only=active_only,
        )


class GetCriterionHistoryUseCase:
    def __init__(self, criterion_repository: CriterionRepository):
        self.criterion_repository = criterion_repository

    async def execute(self, criterion_id: UUID) -> List[CriterionChangeHistory]:
        """Get change history for a criterion"""
        return await self.criterion_repository.get_history(criterion_id)


class DeactivateCriterionUseCase:
    def __init__(self, criterion_repository: CriterionRepository):
        self.criterion_repository = criterion_repository

    async def execute(
        self, criterion_id: UUID, deactivated_by: UUID, reason: str
    ) -> Optional[EvaluationCriterion]:
        """Deactivate a criterion"""

        criterion = await self.criterion_repository.get_by_id(criterion_id)
        if not criterion:
            return None

        if criterion.status != CriterionStatus.ACTIVE:
            raise ValueError("Only active criteria can be deactivated")

        # Update criterion status
        updated_criterion = EvaluationCriterion(
            **{
                **criterion.__dict__,
                "status": CriterionStatus.INACTIVE,
                "updated_at": datetime.utcnow(),
            }
        )

        # Create change history
        change_history = CriterionChangeHistory(
            id=UUID(),
            criterion_id=criterion.id,
            changed_by=deactivated_by,
            change_type="DEACTIVATE",
            old_version=criterion.__dict__,
            new_version=updated_criterion.__dict__,
            change_reason=f"Deactivated: {reason}",
            created_at=datetime.utcnow(),
        )

        return await self.criterion_repository.update(updated_criterion, change_history)