from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from ..schemas import (
    ProjectCreateSchema,
    ProjectUpdateSchema,
    ProjectStatusUpdateSchema,
    ProjectScopeLockSchema,
    ProjectResponseSchema,
    ProjectSearchSchema,
    ProjectListResponseSchema,
)
from ...application.use_cases import (
    CreateProjectUseCase,
    GetProjectUseCase,
    UpdateProjectStatusUseCase,
    LockProjectScopeUseCase,
    GetProjectsByGroupUseCase,
    GetProjectsByCohortUseCase,
    GetProjectsByPeriodUseCase,
    SearchProjectsUseCase,
)
from ...infrastructure.database import get_async_db
from ...infrastructure.repositories import SQLAlchemyProjectRepository
from sqlalchemy.ext.asyncio import AsyncSession
import math

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


# Dependency to get project repository
async def get_project_repository(
    db: AsyncSession = Depends(get_async_db),
) -> SQLAlchemyProjectRepository:
    return SQLAlchemyProjectRepository(db)


@router.post(
    "/", response_model=ProjectResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_project(
    project_data: ProjectCreateSchema,
    project_repo: SQLAlchemyProjectRepository = Depends(get_project_repository),
):
    """Create a new project"""
    try:
        use_case = CreateProjectUseCase(project_repo)
        project = await use_case.execute(
            title=project_data.title,
            description=project_data.description,
            project_type=project_data.project_type,
            cohort_id=project_data.cohort_id,
            group_id=project_data.group_id,
            trimester=project_data.trimester,
            academic_year=project_data.academic_year,
            technologies=project_data.technologies,
            stakeholder_id=project_data.stakeholder_id,
            expected_duration_weeks=project_data.expected_duration_weeks,
        )
        return ProjectResponseSchema.from_orm(project)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating project: {str(e)}",
        )


@router.get("/{project_id}", response_model=ProjectResponseSchema)
async def get_project(
    project_id: UUID,
    project_repo: SQLAlchemyProjectRepository = Depends(get_project_repository),
):
    """Get project by ID"""
    use_case = GetProjectUseCase(project_repo)
    project = await use_case.execute(project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    return ProjectResponseSchema.from_orm(project)


@router.put("/{project_id}/status", response_model=ProjectResponseSchema)
async def update_project_status(
    project_id: UUID,
    status_data: ProjectStatusUpdateSchema,
    instructor_id: UUID,  # This should come from authentication
    project_repo: SQLAlchemyProjectRepository = Depends(get_project_repository),
):
    """Update project status (instructor only)"""
    use_case = UpdateProjectStatusUseCase(project_repo)
    project = await use_case.execute(project_id, status_data.status, instructor_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    return ProjectResponseSchema.from_orm(project)


@router.post("/{project_id}/lock-scope", response_model=ProjectResponseSchema)
async def lock_project_scope(
    project_id: UUID,
    lock_data: ProjectScopeLockSchema,
    instructor_id: UUID,  # This should come from authentication
    project_repo: SQLAlchemyProjectRepository = Depends(get_project_repository),
):
    """Lock project scope (instructor only)"""
    use_case = LockProjectScopeUseCase(project_repo)
    project = await use_case.execute(project_id, instructor_id, lock_data.reason)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    return ProjectResponseSchema.from_orm(project)


@router.get("/group/{group_id}", response_model=List[ProjectResponseSchema])
async def get_projects_by_group(
    group_id: UUID,
    project_repo: SQLAlchemyProjectRepository = Depends(get_project_repository),
):
    """Get all projects for a group"""
    use_case = GetProjectsByGroupUseCase(project_repo)
    projects = await use_case.execute(group_id)

    return [ProjectResponseSchema.from_orm(project) for project in projects]


@router.get("/cohort/{cohort_id}", response_model=List[ProjectResponseSchema])
async def get_projects_by_cohort(
    cohort_id: UUID,
    project_repo: SQLAlchemyProjectRepository = Depends(get_project_repository),
):
    """Get all projects for a cohort"""
    use_case = GetProjectsByCohortUseCase(project_repo)
    projects = await use_case.execute(cohort_id)

    return [ProjectResponseSchema.from_orm(project) for project in projects]


@router.get(
    "/period/{academic_year}/{trimester}", response_model=List[ProjectResponseSchema]
)
async def get_projects_by_period(
    academic_year: int,
    trimester: int,
    project_repo: SQLAlchemyProjectRepository = Depends(get_project_repository),
):
    """Get projects by academic period"""
    use_case = GetProjectsByPeriodUseCase(project_repo)
    projects = await use_case.execute(academic_year, trimester)

    return [ProjectResponseSchema.from_orm(project) for project in projects]


@router.get("/", response_model=ProjectListResponseSchema)
async def search_projects(
    search_params: ProjectSearchSchema = Depends(),
    project_repo: SQLAlchemyProjectRepository = Depends(get_project_repository),
):
    """Search projects with filters"""
    use_case = SearchProjectsUseCase(project_repo)
    projects, total_count = await use_case.execute(
        title=search_params.title,
        project_type=search_params.project_type,
        status=search_params.status,
        academic_year=search_params.academic_year,
        trimester=search_params.trimester,
        page=search_params.page,
        page_size=search_params.page_size,
    )

    total_pages = (
        math.ceil(total_count / search_params.page_size) if total_count > 0 else 1
    )

    return ProjectListResponseSchema(
        projects=[ProjectResponseSchema.from_orm(project) for project in projects],
        total_count=total_count,
        page=search_params.page,
        page_size=search_params.page_size,
        total_pages=total_pages,
    )
