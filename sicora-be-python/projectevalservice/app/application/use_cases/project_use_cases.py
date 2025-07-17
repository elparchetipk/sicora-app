from typing import List, Optional
from uuid import UUID
from datetime import datetime

from ...domain.entities import Project, ProjectStatus, ProjectType
from ...domain.repositories import ProjectRepository
from ...domain.value_objects import AcademicPeriod


class CreateProjectUseCase:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def execute(
        self,
        title: str,
        description: str,
        project_type: ProjectType,
        cohort_id: UUID,
        group_id: UUID,
        trimester: int,
        academic_year: int,
        technologies: List[str],
        stakeholder_id: Optional[UUID] = None,
        expected_duration_weeks: int = 16,
    ) -> Project:
        """Create a new project"""

        # Calculate dates
        start_date = datetime.utcnow()
        expected_end_date = datetime.utcnow().replace(
            month=start_date.month + (expected_duration_weeks // 4)
        )

        project = Project(
            id=UUID(),
            title=title,
            description=description,
            status=ProjectStatus.IDEA_PROPOSAL,
            project_type=project_type,
            cohort_id=cohort_id,
            group_id=group_id,
            stakeholder_id=stakeholder_id,
            trimester=trimester,
            academic_year=academic_year,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            start_date=start_date,
            expected_end_date=expected_end_date,
            actual_end_date=None,
            technologies=technologies,
            repository_url=None,
            demo_url=None,
            documentation_url=None,
            scope_locked=False,
            scope_lock_reason=None,
            scope_locked_by=None,
            scope_locked_at=None,
            stakeholder_expectations_documented=False,
            stakeholder_limitations_communicated=False,
        )

        return await self.project_repository.create(project)


class GetProjectUseCase:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def execute(self, project_id: UUID) -> Optional[Project]:
        """Get project by ID"""
        return await self.project_repository.get_by_id(project_id)


class UpdateProjectStatusUseCase:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def execute(
        self, project_id: UUID, new_status: ProjectStatus, instructor_id: UUID
    ) -> Optional[Project]:
        """Update project status (only instructors can do this)"""

        project = await self.project_repository.get_by_id(project_id)
        if not project:
            return None

        project.update_status(new_status)

        return await self.project_repository.update(project)


class LockProjectScopeUseCase:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def execute(
        self, project_id: UUID, instructor_id: UUID, reason: str
    ) -> Optional[Project]:
        """Lock project scope to prevent unauthorized changes"""

        project = await self.project_repository.get_by_id(project_id)
        if not project:
            return None

        project.lock_scope(instructor_id, reason)

        return await self.project_repository.update(project)


class GetProjectsByGroupUseCase:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def execute(self, group_id: UUID) -> List[Project]:
        """Get all projects for a group"""
        return await self.project_repository.get_by_group_id(group_id)


class GetProjectsByCohortUseCase:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def execute(self, cohort_id: UUID) -> List[Project]:
        """Get all projects for a cohort"""
        return await self.project_repository.get_by_cohort_id(cohort_id)


class GetProjectsByPeriodUseCase:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def execute(self, academic_year: int, trimester: int) -> List[Project]:
        """Get projects by academic period"""
        period = AcademicPeriod(academic_year, trimester)
        return await self.project_repository.get_by_academic_period(period)


class SearchProjectsUseCase:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def execute(
        self,
        title: Optional[str] = None,
        project_type: Optional[ProjectType] = None,
        status: Optional[ProjectStatus] = None,
        academic_year: Optional[int] = None,
        trimester: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[List[Project], int]:
        """Search projects with filters"""
        return await self.project_repository.search_projects(
            title=title,
            project_type=project_type,
            status=status,
            academic_year=academic_year,
            trimester=trimester,
            page=page,
            page_size=page_size,
        )
