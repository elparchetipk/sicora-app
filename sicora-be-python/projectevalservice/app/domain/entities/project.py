from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from enum import Enum


class ProjectStatus(Enum):
    IDEA_PROPOSAL = "idea_proposal"
    IDEA_EVALUATION = "idea_evaluation"
    IDEA_APPROVED = "idea_approved"
    IDEA_REJECTED = "idea_rejected"
    IN_DEVELOPMENT = "in_development"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProjectType(Enum):
    WEB_APPLICATION = "web_application"
    MOBILE_APPLICATION = "mobile_application"
    DESKTOP_APPLICATION = "desktop_application"
    API_SERVICE = "api_service"
    DATA_ANALYTICS = "data_analytics"
    OTHER = "other"


@dataclass
class Project:
    id: UUID
    title: str
    description: str
    status: ProjectStatus
    project_type: ProjectType
    cohort_id: UUID
    group_id: UUID
    stakeholder_id: Optional[UUID]
    trimester: int
    academic_year: int
    created_at: datetime
    updated_at: datetime
    start_date: datetime
    expected_end_date: datetime
    actual_end_date: Optional[datetime]

    # Technical details
    technologies: List[str]
    repository_url: Optional[str]
    demo_url: Optional[str]
    documentation_url: Optional[str]

    # Academic control
    scope_locked: bool = False
    scope_lock_reason: Optional[str] = None
    scope_locked_by: Optional[UUID] = None
    scope_locked_at: Optional[datetime] = None

    # Stakeholder management
    stakeholder_expectations_documented: bool = False
    stakeholder_limitations_communicated: bool = False

    def lock_scope(self, instructor_id: UUID, reason: str) -> None:
        """Lock project scope to prevent unauthorized changes"""
        self.scope_locked = True
        self.scope_lock_reason = reason
        self.scope_locked_by = instructor_id
        self.scope_locked_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def unlock_scope(self, instructor_id: UUID) -> None:
        """Unlock project scope for authorized changes"""
        self.scope_locked = False
        self.scope_lock_reason = None
        self.scope_locked_by = instructor_id
        self.scope_locked_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update_status(self, new_status: ProjectStatus) -> None:
        """Update project status"""
        self.status = new_status
        self.updated_at = datetime.utcnow()

    def complete_project(self) -> None:
        """Mark project as completed"""
        self.status = ProjectStatus.COMPLETED
        self.actual_end_date = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def is_scope_change_allowed(self) -> bool:
        """Check if scope changes are allowed"""
        return not self.scope_locked

    def is_in_active_development(self) -> bool:
        """Check if project is in active development phase"""
        return self.status in [ProjectStatus.IN_DEVELOPMENT, ProjectStatus.UNDER_REVIEW]
