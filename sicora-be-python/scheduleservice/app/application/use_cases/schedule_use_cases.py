"""Schedule management use cases."""

from datetime import date
from typing import List, Optional
from uuid import UUID

from ..dtos.schedule_dtos import (
    CreateScheduleDTO,
    UpdateScheduleDTO,
    ScheduleResponseDTO,
    ScheduleFilterDTO,
    BulkScheduleUploadDTO,
    BulkUploadResultDTO,
)
from ...domain.repositories.schedule_repository_interface import ScheduleRepositoryInterface
from ...domain.repositories.academic_group_repository_interface import AcademicGroupRepositoryInterface
from ...domain.repositories.venue_repository_interface import VenueRepositoryInterface
from ...domain.entities.schedule_entity import Schedule
from ...domain.value_objects.time_slot import TimeSlot
from ...domain.value_objects.schedule_status import ScheduleStatus
from ...domain.exceptions.schedule_exceptions import (
    ScheduleNotFoundError,
    ScheduleConflictError,
    AcademicGroupNotFoundError,
    VenueNotFoundError,
    InstructorNotAvailableError,
    VenueNotAvailableError,
    InvalidScheduleDataError,
)


class CreateScheduleUseCase:
    """Use case for creating a new schedule."""
    
    def __init__(
        self,
        schedule_repository: ScheduleRepositoryInterface,
        group_repository: AcademicGroupRepositoryInterface,
        venue_repository: VenueRepositoryInterface,
    ):
        self._schedule_repository = schedule_repository
        self._group_repository = group_repository
        self._venue_repository = venue_repository
    
    async def execute(self, create_data: CreateScheduleDTO) -> ScheduleResponseDTO:
        """Create a new schedule."""
        # Validate group exists and is active
        group = await self._group_repository.get_by_id(create_data.group_id)
        if not group or not group.is_active:
            raise AcademicGroupNotFoundError("id", str(create_data.group_id))
        
        # Validate venue exists and is active
        venue = await self._venue_repository.get_by_id(create_data.venue_id)
        if not venue or not venue.is_active:
            raise VenueNotFoundError("id", str(create_data.venue_id))
        
        # Create time slot
        time_slot = TimeSlot(create_data.start_time, create_data.end_time)
        
        # Check for instructor conflicts
        instructor_has_conflict = await self._schedule_repository.check_instructor_conflict(
            create_data.instructor_id,
            create_data.start_date,
            create_data.end_date
        )
        if instructor_has_conflict:
            raise InstructorNotAvailableError(
                str(create_data.instructor_id),
                f"{create_data.start_date} - {create_data.end_date}"
            )
        
        # Check for venue conflicts
        venue_has_conflict = await self._schedule_repository.check_venue_conflict(
            create_data.venue_id,
            create_data.start_date,
            create_data.end_date
        )
        if venue_has_conflict:
            raise VenueNotAvailableError(
                str(create_data.venue_id),
                f"{create_data.start_date} - {create_data.end_date}"
            )
        
        # Create schedule entity
        schedule = Schedule(
            start_date=create_data.start_date,
            end_date=create_data.end_date,
            time_slot=time_slot,
            instructor_id=create_data.instructor_id,
            group_id=create_data.group_id,
            venue_id=create_data.venue_id,
            subject=create_data.subject,
            notes=create_data.notes,
        )
        
        # Save schedule
        created_schedule = await self._schedule_repository.create(schedule)
        
        # Return response DTO
        return ScheduleResponseDTO(
            id=created_schedule.id,
            start_date=created_schedule.start_date,
            end_date=created_schedule.end_date,
            start_time=created_schedule.time_slot.start_time,
            end_time=created_schedule.time_slot.end_time,
            instructor_id=created_schedule.instructor_id,
            group_id=created_schedule.group_id,
            venue_id=created_schedule.venue_id,
            subject=created_schedule.subject,
            status=created_schedule.status.value,
            notes=created_schedule.notes,
            created_at=created_schedule.created_at.date(),
            updated_at=created_schedule.updated_at.date(),
        )


class GetScheduleUseCase:
    """Use case for retrieving schedules."""
    
    def __init__(self, schedule_repository: ScheduleRepositoryInterface):
        self._schedule_repository = schedule_repository
    
    async def execute(self, schedule_id: UUID) -> ScheduleResponseDTO:
        """Get schedule by ID."""
        schedule = await self._schedule_repository.get_by_id(schedule_id)
        if not schedule:
            raise ScheduleNotFoundError("id", str(schedule_id))
        
        return ScheduleResponseDTO(
            id=schedule.id,
            start_date=schedule.start_date,
            end_date=schedule.end_date,
            start_time=schedule.time_slot.start_time,
            end_time=schedule.time_slot.end_time,
            instructor_id=schedule.instructor_id,
            group_id=schedule.group_id,
            venue_id=schedule.venue_id,
            subject=schedule.subject,
            status=schedule.status.value,
            notes=schedule.notes,
            created_at=schedule.created_at.date(),
            updated_at=schedule.updated_at.date(),
        )


class ListSchedulesUseCase:
    """Use case for listing schedules with filters."""
    
    def __init__(self, schedule_repository: ScheduleRepositoryInterface):
        self._schedule_repository = schedule_repository
    
    async def execute(self, filters: Optional[ScheduleFilterDTO] = None) -> List[ScheduleResponseDTO]:
        """List schedules with optional filters."""
        if filters:
            if filters.date_from and filters.date_to:
                schedules = await self._schedule_repository.get_by_date_range(
                    filters.date_from, filters.date_to
                )
            elif filters.instructor_id:
                schedules = await self._schedule_repository.get_by_instructor(filters.instructor_id)
            elif filters.group_id:
                schedules = await self._schedule_repository.get_by_group(filters.group_id)
            elif filters.venue_id:
                schedules = await self._schedule_repository.get_by_venue(filters.venue_id)
            else:
                schedules = await self._schedule_repository.get_active_schedules()
        else:
            schedules = await self._schedule_repository.get_active_schedules()
        
        return [
            ScheduleResponseDTO(
                id=schedule.id,
                start_date=schedule.start_date,
                end_date=schedule.end_date,
                start_time=schedule.time_slot.start_time,
                end_time=schedule.time_slot.end_time,
                instructor_id=schedule.instructor_id,
                group_id=schedule.group_id,
                venue_id=schedule.venue_id,
                subject=schedule.subject,
                status=schedule.status.value,
                notes=schedule.notes,
                created_at=schedule.created_at.date(),
                updated_at=schedule.updated_at.date(),
            )
            for schedule in schedules
        ]


class UpdateScheduleUseCase:
    """Use case for updating an existing schedule."""
    
    def __init__(
        self,
        schedule_repository: ScheduleRepositoryInterface,
        group_repository: AcademicGroupRepositoryInterface,
        venue_repository: VenueRepositoryInterface,
    ):
        self._schedule_repository = schedule_repository
        self._group_repository = group_repository
        self._venue_repository = venue_repository
    
    async def execute(self, update_data: UpdateScheduleDTO) -> ScheduleResponseDTO:
        """Update an existing schedule."""
        # Get existing schedule
        schedule = await self._schedule_repository.get_by_id(update_data.schedule_id)
        if not schedule:
            raise ScheduleNotFoundError("id", str(update_data.schedule_id))
        
        # Update fields if provided
        if update_data.start_date and update_data.end_date:
            schedule.update_dates(update_data.start_date, update_data.end_date)
        
        if update_data.start_time and update_data.end_time:
            time_slot = TimeSlot(update_data.start_time, update_data.end_time)
            schedule.update_time_slot(time_slot)
        
        if update_data.instructor_id:
            # Check for conflicts
            instructor_has_conflict = await self._schedule_repository.check_instructor_conflict(
                update_data.instructor_id,
                schedule.start_date,
                schedule.end_date,
                exclude_schedule_id=schedule.id
            )
            if instructor_has_conflict:
                raise InstructorNotAvailableError(
                    str(update_data.instructor_id),
                    f"{schedule.start_date} - {schedule.end_date}"
                )
            schedule.update_instructor(update_data.instructor_id)
        
        if update_data.venue_id:
            # Check venue exists and is active
            venue = await self._venue_repository.get_by_id(update_data.venue_id)
            if not venue or not venue.is_active:
                raise VenueNotFoundError("id", str(update_data.venue_id))
            
            # Check for conflicts
            venue_has_conflict = await self._schedule_repository.check_venue_conflict(
                update_data.venue_id,
                schedule.start_date,
                schedule.end_date,
                exclude_schedule_id=schedule.id
            )
            if venue_has_conflict:
                raise VenueNotAvailableError(
                    str(update_data.venue_id),
                    f"{schedule.start_date} - {schedule.end_date}"
                )
            schedule.update_venue(update_data.venue_id)
        
        if update_data.group_id:
            # Check group exists and is active
            group = await self._group_repository.get_by_id(update_data.group_id)
            if not group or not group.is_active:
                raise AcademicGroupNotFoundError("id", str(update_data.group_id))
            schedule.group_id = update_data.group_id
        
        if update_data.subject:
            schedule.update_subject(update_data.subject)
        
        if update_data.notes is not None:
            schedule.update_notes(update_data.notes)
        
        # Save updated schedule
        updated_schedule = await self._schedule_repository.update(schedule)
        
        return ScheduleResponseDTO(
            id=updated_schedule.id,
            start_date=updated_schedule.start_date,
            end_date=updated_schedule.end_date,
            start_time=updated_schedule.time_slot.start_time,
            end_time=updated_schedule.time_slot.end_time,
            instructor_id=updated_schedule.instructor_id,
            group_id=updated_schedule.group_id,
            venue_id=updated_schedule.venue_id,
            subject=updated_schedule.subject,
            status=updated_schedule.status.value,
            notes=updated_schedule.notes,
            created_at=updated_schedule.created_at.date(),
            updated_at=updated_schedule.updated_at.date(),
        )


class DeleteScheduleUseCase:
    """Use case for deleting a schedule."""
    
    def __init__(self, schedule_repository: ScheduleRepositoryInterface):
        self._schedule_repository = schedule_repository
    
    async def execute(self, schedule_id: UUID) -> None:
        """Delete a schedule."""
        schedule = await self._schedule_repository.get_by_id(schedule_id)
        if not schedule:
            raise ScheduleNotFoundError("id", str(schedule_id))
        
        await self._schedule_repository.delete(schedule_id)


class BulkUploadSchedulesUseCase:
    """Use case for bulk uploading schedules."""
    
    def __init__(
        self,
        schedule_repository: ScheduleRepositoryInterface,
        group_repository: AcademicGroupRepositoryInterface,
        venue_repository: VenueRepositoryInterface,
    ):
        self._schedule_repository = schedule_repository
        self._group_repository = group_repository
        self._venue_repository = venue_repository
    
    async def execute(self, bulk_data: BulkScheduleUploadDTO) -> BulkUploadResultDTO:
        """Upload multiple schedules from CSV data."""
        successful = 0
        failed = 0
        errors = []
        
        for i, schedule_data in enumerate(bulk_data.schedules):
            try:
                # Validate and create schedule using CreateScheduleUseCase logic
                create_use_case = CreateScheduleUseCase(
                    self._schedule_repository,
                    self._group_repository,
                    self._venue_repository
                )
                await create_use_case.execute(schedule_data)
                successful += 1
            except Exception as e:
                failed += 1
                errors.append(f"Row {i + 1}: {str(e)}")
        
        return BulkUploadResultDTO(
            total_processed=len(bulk_data.schedules),
            successful=successful,
            failed=failed,
            errors=errors
        )
