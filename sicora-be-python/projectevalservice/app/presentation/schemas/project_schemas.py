from pydantic import BaseModel, Field, UUID4
from typing import Optional, List
from datetime import datetime
from enum import Enum

from ...domain.entities import ProjectStatus, ProjectType


class ProjectStatusSchema(str, Enum):
    IDEA_PROPOSAL = "idea_proposal"
    IDEA_EVALUATION = "idea_evaluation"
    IDEA_APPROVED = "idea_approved"
    IDEA_REJECTED = "idea_rejected"
    IN_DEVELOPMENT = "in_development"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProjectTypeSchema(str, Enum):
    WEB_APPLICATION = "web_application"
    MOBILE_APPLICATION = "mobile_application"
    DESKTOP_APPLICATION = "desktop_application"
    API_SERVICE = "api_service"
    DATA_ANALYTICS = "data_analytics"
    OTHER = "other"


class ProjectCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Project title")
    description: str = Field(..., min_length=1, description="Project description")
    project_type: ProjectTypeSchema = Field(..., description="Type of project")
    cohort_id: UUID4 = Field(..., description="Cohort ID")
    group_id: UUID4 = Field(..., description="Group ID")
    stakeholder_id: Optional[UUID4] = Field(None, description="Stakeholder ID")
    trimester: int = Field(..., ge=1, le=7, description="Academic trimester")
    academic_year: int = Field(..., ge=2020, description="Academic year")
    technologies: List[str] = Field(default=[], description="Technologies used")
    expected_duration_weeks: int = Field(
        default=16, ge=1, le=52, description="Expected duration in weeks"
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "Sistema de Gestión de Inventarios",
                "description": "Sistema web para gestión de inventarios de pequeñas empresas",
                "project_type": "web_application",
                "cohort_id": "123e4567-e89b-12d3-a456-426614174000",
                "group_id": "123e4567-e89b-12d3-a456-426614174001",
                "stakeholder_id": "123e4567-e89b-12d3-a456-426614174002",
                "trimester": 3,
                "academic_year": 2025,
                "technologies": ["Python", "FastAPI", "React", "PostgreSQL"],
                "expected_duration_weeks": 16,
            }
        }


class ProjectUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    project_type: Optional[ProjectTypeSchema] = None
    stakeholder_id: Optional[UUID4] = None
    technologies: Optional[List[str]] = None
    repository_url: Optional[str] = Field(None, max_length=500)
    demo_url: Optional[str] = Field(None, max_length=500)
    documentation_url: Optional[str] = Field(None, max_length=500)

    class Config:
        schema_extra = {
            "example": {
                "title": "Sistema de Gestión de Inventarios - Actualizado",
                "repository_url": "https://github.com/sena/inventory-system",
                "demo_url": "https://demo.inventory-system.com",
            }
        }


class ProjectStatusUpdateSchema(BaseModel):
    status: ProjectStatusSchema = Field(..., description="New project status")
    reason: Optional[str] = Field(None, description="Reason for status change")

    class Config:
        schema_extra = {
            "example": {
                "status": "idea_approved",
                "reason": "Project meets all requirements and is ready for development",
            }
        }


class ProjectScopeLockSchema(BaseModel):
    reason: str = Field(..., min_length=1, description="Reason for locking scope")

    class Config:
        schema_extra = {
            "example": {
                "reason": "Project scope locked due to stakeholder exceeding change requests limit"
            }
        }


class ProjectResponseSchema(BaseModel):
    id: UUID4
    title: str
    description: str
    status: ProjectStatusSchema
    project_type: ProjectTypeSchema
    cohort_id: UUID4
    group_id: UUID4
    stakeholder_id: Optional[UUID4]
    trimester: int
    academic_year: int
    created_at: datetime
    updated_at: datetime
    start_date: datetime
    expected_end_date: datetime
    actual_end_date: Optional[datetime]
    technologies: List[str]
    repository_url: Optional[str]
    demo_url: Optional[str]
    documentation_url: Optional[str]
    scope_locked: bool
    scope_lock_reason: Optional[str]
    scope_locked_by: Optional[UUID4]
    scope_locked_at: Optional[datetime]
    stakeholder_expectations_documented: bool
    stakeholder_limitations_communicated: bool

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Sistema de Gestión de Inventarios",
                "description": "Sistema web para gestión de inventarios de pequeñas empresas",
                "status": "in_development",
                "project_type": "web_application",
                "cohort_id": "123e4567-e89b-12d3-a456-426614174001",
                "group_id": "123e4567-e89b-12d3-a456-426614174002",
                "stakeholder_id": "123e4567-e89b-12d3-a456-426614174003",
                "trimester": 3,
                "academic_year": 2025,
                "created_at": "2025-06-17T10:00:00Z",
                "updated_at": "2025-06-17T10:00:00Z",
                "start_date": "2025-06-17T10:00:00Z",
                "expected_end_date": "2025-10-17T10:00:00Z",
                "actual_end_date": None,
                "technologies": ["Python", "FastAPI", "React", "PostgreSQL"],
                "repository_url": "https://github.com/sena/inventory-system",
                "demo_url": None,
                "documentation_url": None,
                "scope_locked": False,
                "scope_lock_reason": None,
                "scope_locked_by": None,
                "scope_locked_at": None,
                "stakeholder_expectations_documented": True,
                "stakeholder_limitations_communicated": True,
            }
        }


class ProjectSearchSchema(BaseModel):
    title: Optional[str] = Field(None, description="Search by title")
    project_type: Optional[ProjectTypeSchema] = Field(
        None, description="Filter by project type"
    )
    status: Optional[ProjectStatusSchema] = Field(None, description="Filter by status")
    academic_year: Optional[int] = Field(
        None, ge=2020, description="Filter by academic year"
    )
    trimester: Optional[int] = Field(
        None, ge=1, le=7, description="Filter by trimester"
    )
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Number of items per page")

    class Config:
        schema_extra = {
            "example": {
                "title": "inventory",
                "project_type": "web_application",
                "status": "in_development",
                "academic_year": 2025,
                "trimester": 3,
                "page": 1,
                "page_size": 20,
            }
        }


class ProjectListResponseSchema(BaseModel):
    projects: List[ProjectResponseSchema]
    total_count: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        schema_extra = {
            "example": {
                "projects": [],
                "total_count": 50,
                "page": 1,
                "page_size": 20,
                "total_pages": 3,
            }
        }
