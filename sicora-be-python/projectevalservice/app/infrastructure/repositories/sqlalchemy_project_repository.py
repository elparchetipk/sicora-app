from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload

from ...domain.entities import Project, ProjectStatus, ProjectType
from ...domain.repositories import ProjectRepository
from ...domain.value_objects import AcademicPeriod
from ..database.models import ProjectModel


class SQLAlchemyProjectRepository(ProjectRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    def _model_to_entity(self, model: ProjectModel) -> Project:
        """Convert SQLAlchemy model to domain entity"""
        return Project(
            id=model.id,
            title=model.title,
            description=model.description,
            status=model.status,
            project_type=model.project_type,
            cohort_id=model.cohort_id,
            group_id=model.group_id,
            stakeholder_id=model.stakeholder_id,
            trimester=model.trimester,
            academic_year=model.academic_year,
            created_at=model.created_at,
            updated_at=model.updated_at,
            start_date=model.start_date,
            expected_end_date=model.expected_end_date,
            actual_end_date=model.actual_end_date,
            technologies=model.technologies or [],
            repository_url=model.repository_url,
            demo_url=model.demo_url,
            documentation_url=model.documentation_url,
            scope_locked=model.scope_locked,
            scope_lock_reason=model.scope_lock_reason,
            scope_locked_by=model.scope_locked_by,
            scope_locked_at=model.scope_locked_at,
            stakeholder_expectations_documented=model.stakeholder_expectations_documented,
            stakeholder_limitations_communicated=model.stakeholder_limitations_communicated,
        )

    def _entity_to_model(self, entity: Project) -> ProjectModel:
        """Convert domain entity to SQLAlchemy model"""
        return ProjectModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            status=entity.status,
            project_type=entity.project_type,
            cohort_id=entity.cohort_id,
            group_id=entity.group_id,
            stakeholder_id=entity.stakeholder_id,
            trimester=entity.trimester,
            academic_year=entity.academic_year,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            start_date=entity.start_date,
            expected_end_date=entity.expected_end_date,
            actual_end_date=entity.actual_end_date,
            technologies=entity.technologies,
            repository_url=entity.repository_url,
            demo_url=entity.demo_url,
            documentation_url=entity.documentation_url,
            scope_locked=entity.scope_locked,
            scope_lock_reason=entity.scope_lock_reason,
            scope_locked_by=entity.scope_locked_by,
            scope_locked_at=entity.scope_locked_at,
            stakeholder_expectations_documented=entity.stakeholder_expectations_documented,
            stakeholder_limitations_communicated=entity.stakeholder_limitations_communicated,
        )

    async def create(self, project: Project) -> Project:
        """Create a new project"""
        model = self._entity_to_model(project)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)

    async def get_by_id(self, project_id: UUID) -> Optional[Project]:
        """Get project by ID"""
        stmt = select(ProjectModel).where(ProjectModel.id == project_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None

    async def get_by_group_id(self, group_id: UUID) -> List[Project]:
        """Get projects by group ID"""
        stmt = select(ProjectModel).where(ProjectModel.group_id == group_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]

    async def get_by_cohort_id(self, cohort_id: UUID) -> List[Project]:
        """Get projects by cohort ID"""
        stmt = select(ProjectModel).where(ProjectModel.cohort_id == cohort_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]

    async def get_by_stakeholder_id(self, stakeholder_id: UUID) -> List[Project]:
        """Get projects by stakeholder ID"""
        stmt = select(ProjectModel).where(ProjectModel.stakeholder_id == stakeholder_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]

    async def get_by_status(self, status: ProjectStatus) -> List[Project]:
        """Get projects by status"""
        stmt = select(ProjectModel).where(ProjectModel.status == status)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]

    async def get_by_academic_period(self, period: AcademicPeriod) -> List[Project]:
        """Get projects by academic period"""
        stmt = select(ProjectModel).where(
            and_(
                ProjectModel.academic_year == period.academic_year,
                ProjectModel.trimester == period.trimester,
            )
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]

    async def get_active_projects(self) -> List[Project]:
        """Get all active projects"""
        active_statuses = [
            ProjectStatus.IDEA_PROPOSAL,
            ProjectStatus.IDEA_EVALUATION,
            ProjectStatus.IDEA_APPROVED,
            ProjectStatus.IN_DEVELOPMENT,
            ProjectStatus.UNDER_REVIEW,
        ]
        stmt = select(ProjectModel).where(ProjectModel.status.in_(active_statuses))
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]

    async def update(self, project: Project) -> Project:
        """Update existing project"""
        stmt = select(ProjectModel).where(ProjectModel.id == project.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            raise ValueError(f"Project with id {project.id} not found")

        # Update model fields
        model.title = project.title
        model.description = project.description
        model.status = project.status
        model.project_type = project.project_type
        model.stakeholder_id = project.stakeholder_id
        model.technologies = project.technologies
        model.repository_url = project.repository_url
        model.demo_url = project.demo_url
        model.documentation_url = project.documentation_url
        model.scope_locked = project.scope_locked
        model.scope_lock_reason = project.scope_lock_reason
        model.scope_locked_by = project.scope_locked_by
        model.scope_locked_at = project.scope_locked_at
        model.stakeholder_expectations_documented = (
            project.stakeholder_expectations_documented
        )
        model.stakeholder_limitations_communicated = (
            project.stakeholder_limitations_communicated
        )
        model.updated_at = project.updated_at

        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)

    async def delete(self, project_id: UUID) -> bool:
        """Delete project"""
        stmt = select(ProjectModel).where(ProjectModel.id == project_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            await self.session.delete(model)
            await self.session.commit()
            return True
        return False

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

        # Build base query
        stmt = select(ProjectModel)
        conditions = []

        if title:
            conditions.append(ProjectModel.title.ilike(f"%{title}%"))
        if project_type:
            conditions.append(ProjectModel.project_type == project_type)
        if status:
            conditions.append(ProjectModel.status == status)
        if academic_year:
            conditions.append(ProjectModel.academic_year == academic_year)
        if trimester:
            conditions.append(ProjectModel.trimester == trimester)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        # Count total results
        count_stmt = select(func.count()).select_from(stmt.subquery())
        count_result = await self.session.execute(count_stmt)
        total_count = count_result.scalar()

        # Apply pagination
        offset = (page - 1) * page_size
        stmt = stmt.offset(offset).limit(page_size)

        # Execute query
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        projects = [self._model_to_entity(model) for model in models]
        return projects, total_count
