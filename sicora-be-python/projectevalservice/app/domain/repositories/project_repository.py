from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ..entities import Project, ProjectStatus, ProjectType
from ..value_objects import AcademicPeriod


class ProjectRepository(ABC):

    @abstractmethod
    async def create(self, project: Project) -> Project:
        """Create a new project"""
        pass

    @abstractmethod
    async def get_by_id(self, project_id: UUID) -> Optional[Project]:
        """Get project by ID"""
        pass

    @abstractmethod
    async def get_by_group_id(self, group_id: UUID) -> List[Project]:
        """Get projects by group ID"""
        pass

    @abstractmethod
    async def get_by_cohort_id(self, cohort_id: UUID) -> List[Project]:
        """Get projects by cohort ID"""
        pass

    @abstractmethod
    async def get_by_stakeholder_id(self, stakeholder_id: UUID) -> List[Project]:
        """Get projects by stakeholder ID"""
        pass

    @abstractmethod
    async def get_by_status(self, status: ProjectStatus) -> List[Project]:
        """Get projects by status"""
        pass

    @abstractmethod
    async def get_by_academic_period(self, period: AcademicPeriod) -> List[Project]:
        """Get projects by academic period"""
        pass

    @abstractmethod
    async def get_active_projects(self) -> List[Project]:
        """Get all active projects"""
        pass

    @abstractmethod
    async def update(self, project: Project) -> Project:
        """Update existing project"""
        pass

    @abstractmethod
    async def delete(self, project_id: UUID) -> bool:
        """Delete project"""
        pass

    @abstractmethod
    async def search_projects(
        self,
        title: Optional[str] = None,
        project_type: Optional[ProjectType] = None,
        status: Optional[ProjectStatus] = None,
        academic_year: Optional[int] = None,
        trimester: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[List[Project], int]:
        """Search projects with filters and pagination"""
        pass
