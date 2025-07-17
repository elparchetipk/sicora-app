from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from enum import Enum


class CriterionStatus(str, Enum):
    """Estado de un criterio de evaluación."""

    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    ACTIVE = "active"
    INACTIVE = "inactive"


class CriterionCategory(str, Enum):
    """Categorías de criterios de evaluación."""

    ARCHITECTURE = "architecture"
    DATA_MANAGEMENT = "data_management"
    UI_UX = "ui_ux"
    FUNCTIONALITY = "functionality"
    SECURITY = "security"
    TESTING = "testing"
    VCS = "vcs"
    CI_CD = "ci_cd"
    DEPLOYMENT = "deployment"
    METHODOLOGY = "methodology"
    VOICE_NOTES = "voice_notes"
    DATABASE_VCS = "database_vcs"


class ApprovalStatus(str, Enum):
    """Estado de aprobación de criterios."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(frozen=True)
class EvaluationCriterion:
    """Entidad de dominio para criterios de evaluación."""

    id: UUID
    code: str  # AR-001, BD-001, etc.
    title: str
    description: str
    category: CriterionCategory
    status: CriterionStatus
    is_required: bool
    points: int
    version: int
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    approved_by: Optional[List[UUID]] = None
    rejection_reason: Optional[str] = None
    effective_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None

    def is_active(self) -> bool:
        """Verifica si el criterio está activo."""
        return (
            self.status == CriterionStatus.ACTIVE
            and (
                self.effective_date is None or self.effective_date <= datetime.utcnow()
            )
            and (
                self.expiration_date is None or self.expiration_date > datetime.utcnow()
            )
        )

    def can_be_modified(self) -> bool:
        """Verifica si el criterio puede ser modificado."""
        return self.status in [CriterionStatus.DRAFT, CriterionStatus.PENDING_APPROVAL]

    def requires_unanimous_approval(self) -> bool:
        """Verifica si requiere aprobación unánime (nuevo criterio)."""
        return self.version == 1


@dataclass(frozen=True)
class CriterionApproval:
    """Entidad para gestionar aprobaciones de criterios."""

    id: UUID
    criterion_id: UUID
    pedagogical_member_id: UUID
    approval_status: ApprovalStatus
    comments: Optional[str]
    created_at: datetime


@dataclass(frozen=True)
class CriterionChangeHistory:
    """Historial de cambios de criterios."""

    id: UUID
    criterion_id: UUID
    changed_by: UUID
    change_type: str  # CREATE, UPDATE, DEACTIVATE
    old_version: Optional[dict]
    new_version: dict
    change_reason: str
    created_at: datetime
