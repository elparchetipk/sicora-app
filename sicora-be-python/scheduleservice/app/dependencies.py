"""Dependencies for ScheduleService presentation layer."""

from fastapi import Depends
from sqlalchemy.orm import Session

from ..infrastructure.config.database import get_database
from ..infrastructure.repositories import (
    ScheduleRepositorySQLAlchemy,
    AcademicProgramRepositorySQLAlchemy,
    AcademicGroupRepositorySQLAlchemy,
    VenueRepositorySQLAlchemy,
)
from ..application.use_cases.schedule_use_cases import (
    CreateScheduleUseCase,
    GetScheduleUseCase,
    ListSchedulesUseCase,
    UpdateScheduleUseCase,
    DeleteScheduleUseCase,
    BulkUploadSchedulesUseCase,
)
from ..application.use_cases.academic_entity_use_cases import (
    CreateAcademicProgramUseCase,
    ListAcademicProgramsUseCase,
    CreateAcademicGroupUseCase,
    ListAcademicGroupsUseCase,
    CreateVenueUseCase,
    ListVenuesUseCase,
)


# Repository Dependencies
def get_schedule_repository(db: Session = Depends(get_database)) -> ScheduleRepositorySQLAlchemy:
    """Get schedule repository instance."""
    return ScheduleRepositorySQLAlchemy(db)


def get_academic_program_repository(db: Session = Depends(get_database)) -> AcademicProgramRepositorySQLAlchemy:
    """Get academic program repository instance."""
    return AcademicProgramRepositorySQLAlchemy(db)


def get_academic_group_repository(db: Session = Depends(get_database)) -> AcademicGroupRepositorySQLAlchemy:
    """Get academic group repository instance."""
    return AcademicGroupRepositorySQLAlchemy(db)


def get_venue_repository(db: Session = Depends(get_database)) -> VenueRepositorySQLAlchemy:
    """Get venue repository instance."""
    return VenueRepositorySQLAlchemy(db)


# Schedule Use Case Dependencies
def get_create_schedule_use_case(
    schedule_repo: ScheduleRepositorySQLAlchemy = Depends(get_schedule_repository),
    group_repo: AcademicGroupRepositorySQLAlchemy = Depends(get_academic_group_repository),
    venue_repo: VenueRepositorySQLAlchemy = Depends(get_venue_repository),
) -> CreateScheduleUseCase:
    """Get create schedule use case instance."""
    return CreateScheduleUseCase(schedule_repo, group_repo, venue_repo)


def get_get_schedule_use_case(
    schedule_repo: ScheduleRepositorySQLAlchemy = Depends(get_schedule_repository),
) -> GetScheduleUseCase:
    """Get schedule use case instance."""
    return GetScheduleUseCase(schedule_repo)


def get_list_schedules_use_case(
    schedule_repo: ScheduleRepositorySQLAlchemy = Depends(get_schedule_repository),
) -> ListSchedulesUseCase:
    """Get list schedules use case instance."""
    return ListSchedulesUseCase(schedule_repo)


def get_update_schedule_use_case(
    schedule_repo: ScheduleRepositorySQLAlchemy = Depends(get_schedule_repository),
    group_repo: AcademicGroupRepositorySQLAlchemy = Depends(get_academic_group_repository),
    venue_repo: VenueRepositorySQLAlchemy = Depends(get_venue_repository),
) -> UpdateScheduleUseCase:
    """Get update schedule use case instance."""
    return UpdateScheduleUseCase(schedule_repo, group_repo, venue_repo)


def get_delete_schedule_use_case(
    schedule_repo: ScheduleRepositorySQLAlchemy = Depends(get_schedule_repository),
) -> DeleteScheduleUseCase:
    """Get delete schedule use case instance."""
    return DeleteScheduleUseCase(schedule_repo)


def get_bulk_upload_schedules_use_case(
    schedule_repo: ScheduleRepositorySQLAlchemy = Depends(get_schedule_repository),
    group_repo: AcademicGroupRepositorySQLAlchemy = Depends(get_academic_group_repository),
    venue_repo: VenueRepositorySQLAlchemy = Depends(get_venue_repository),
) -> BulkUploadSchedulesUseCase:
    """Get bulk upload schedules use case instance."""
    return BulkUploadSchedulesUseCase(schedule_repo, group_repo, venue_repo)


# Academic Entity Use Case Dependencies
def get_create_academic_program_use_case(
    program_repo: AcademicProgramRepositorySQLAlchemy = Depends(get_academic_program_repository),
) -> CreateAcademicProgramUseCase:
    """Get create academic program use case instance."""
    return CreateAcademicProgramUseCase(program_repo)


def get_list_academic_programs_use_case(
    program_repo: AcademicProgramRepositorySQLAlchemy = Depends(get_academic_program_repository),
) -> ListAcademicProgramsUseCase:
    """Get list academic programs use case instance."""
    return ListAcademicProgramsUseCase(program_repo)


def get_create_academic_group_use_case(
    group_repo: AcademicGroupRepositorySQLAlchemy = Depends(get_academic_group_repository),
    program_repo: AcademicProgramRepositorySQLAlchemy = Depends(get_academic_program_repository),
) -> CreateAcademicGroupUseCase:
    """Get create academic group use case instance."""
    return CreateAcademicGroupUseCase(group_repo, program_repo)


def get_list_academic_groups_use_case(
    group_repo: AcademicGroupRepositorySQLAlchemy = Depends(get_academic_group_repository),
) -> ListAcademicGroupsUseCase:
    """Get list academic groups use case instance."""
    return ListAcademicGroupsUseCase(group_repo)


def get_create_venue_use_case(
    venue_repo: VenueRepositorySQLAlchemy = Depends(get_venue_repository),
) -> CreateVenueUseCase:
    """Get create venue use case instance."""
    return CreateVenueUseCase(venue_repo)


def get_list_venues_use_case(
    venue_repo: VenueRepositorySQLAlchemy = Depends(get_venue_repository),
) -> ListVenuesUseCase:
    """Get list venues use case instance."""
    return ListVenuesUseCase(venue_repo)
