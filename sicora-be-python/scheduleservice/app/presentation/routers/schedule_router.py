"""Schedule router for public and authenticated endpoints."""

from datetime import date
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File
from pydantic import ValidationError

from ..schemas.schedule_schemas import (
    ScheduleCreateRequest,
    ScheduleUpdateRequest,
    ScheduleResponse,
    ScheduleFilterRequest,
    BulkUploadResultResponse,
    MessageResponse,
    ErrorResponse,
)
from ...application.use_cases.schedule_use_cases import (
    CreateScheduleUseCase,
    GetScheduleUseCase,
    ListSchedulesUseCase,
    UpdateScheduleUseCase,
    DeleteScheduleUseCase,
    BulkUploadSchedulesUseCase,
)
from ...application.dtos.schedule_dtos import (
    CreateScheduleDTO,
    UpdateScheduleDTO,
    ScheduleFilterDTO,
    BulkScheduleUploadDTO,
)
from ...domain.exceptions.schedule_exceptions import (
    ScheduleNotFoundError,
    ScheduleConflictError,
    AcademicGroupNotFoundError,
    VenueNotFoundError,
    InstructorNotAvailableError,
    VenueNotAvailableError,
    InvalidScheduleDataError,
)
from ...dependencies import (
    get_create_schedule_use_case,
    get_get_schedule_use_case,
    get_list_schedules_use_case,
    get_update_schedule_use_case,
    get_delete_schedule_use_case,
    get_bulk_upload_schedules_use_case,
)

router = APIRouter(prefix="/schedule", tags=["Schedule"])


@router.get("/", response_model=List[ScheduleResponse])
async def list_schedules(
    date_from: Optional[date] = Query(None, description="Filter from date"),
    date_to: Optional[date] = Query(None, description="Filter to date"),
    instructor_id: Optional[UUID] = Query(None, description="Filter by instructor"),
    group_id: Optional[UUID] = Query(None, description="Filter by group"),
    venue_id: Optional[UUID] = Query(None, description="Filter by venue"),
    status: Optional[str] = Query(None, description="Filter by status"),
    use_case: ListSchedulesUseCase = Depends(get_list_schedules_use_case),
):
    """
    Get schedules with optional filtering.
    
    - **date_from**: Filter schedules from this date
    - **date_to**: Filter schedules to this date
    - **instructor_id**: Filter by specific instructor
    - **group_id**: Filter by specific academic group
    - **venue_id**: Filter by specific venue
    - **status**: Filter by schedule status
    """
    try:
        # Create filter DTO
        filters = None
        if any([date_from, date_to, instructor_id, group_id, venue_id, status]):
            filters = ScheduleFilterDTO(
                date_from=date_from,
                date_to=date_to,
                instructor_id=instructor_id,
                group_id=group_id,
                venue_id=venue_id,
                status=status,
            )
        
        # Get schedules
        schedules = await use_case.execute(filters)
        
        # Convert to response format
        return [
            ScheduleResponse(
                id=schedule.id,
                start_date=schedule.start_date,
                end_date=schedule.end_date,
                start_time=schedule.start_time,
                end_time=schedule.end_time,
                instructor_id=schedule.instructor_id,
                group_id=schedule.group_id,
                venue_id=schedule.venue_id,
                subject=schedule.subject,
                status=schedule.status,
                notes=schedule.notes,
                created_at=schedule.created_at,
                updated_at=schedule.updated_at,
            )
            for schedule in schedules
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving schedules: {str(e)}"
        )


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(
    schedule_id: UUID,
    use_case: GetScheduleUseCase = Depends(get_get_schedule_use_case),
):
    """Get a specific schedule by ID."""
    try:
        schedule = await use_case.execute(schedule_id)
        return ScheduleResponse(
            id=schedule.id,
            start_date=schedule.start_date,
            end_date=schedule.end_date,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            instructor_id=schedule.instructor_id,
            group_id=schedule.group_id,
            venue_id=schedule.venue_id,
            subject=schedule.subject,
            status=schedule.status,
            notes=schedule.notes,
            created_at=schedule.created_at,
            updated_at=schedule.updated_at,
        )
    except ScheduleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving schedule: {str(e)}"
        )


@router.post("/", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule_data: ScheduleCreateRequest,
    use_case: CreateScheduleUseCase = Depends(get_create_schedule_use_case),
):
    """Create a new schedule."""
    try:
        # Convert to DTO
        create_dto = CreateScheduleDTO(
            start_date=schedule_data.start_date,
            end_date=schedule_data.end_date,
            start_time=schedule_data.start_time,
            end_time=schedule_data.end_time,
            instructor_id=schedule_data.instructor_id,
            group_id=schedule_data.group_id,
            venue_id=schedule_data.venue_id,
            subject=schedule_data.subject,
            notes=schedule_data.notes,
        )
        
        # Create schedule
        schedule = await use_case.execute(create_dto)
        
        return ScheduleResponse(
            id=schedule.id,
            start_date=schedule.start_date,
            end_date=schedule.end_date,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            instructor_id=schedule.instructor_id,
            group_id=schedule.group_id,
            venue_id=schedule.venue_id,
            subject=schedule.subject,
            status=schedule.status,
            notes=schedule.notes,
            created_at=schedule.created_at,
            updated_at=schedule.updated_at,
        )
    except (AcademicGroupNotFoundError, VenueNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except (InstructorNotAvailableError, VenueNotAvailableError) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except InvalidScheduleDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating schedule: {str(e)}"
        )


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: UUID,
    schedule_data: ScheduleUpdateRequest,
    use_case: UpdateScheduleUseCase = Depends(get_update_schedule_use_case),
):
    """Update an existing schedule."""
    try:
        # Convert to DTO
        update_dto = UpdateScheduleDTO(
            schedule_id=schedule_id,
            start_date=schedule_data.start_date,
            end_date=schedule_data.end_date,
            start_time=schedule_data.start_time,
            end_time=schedule_data.end_time,
            instructor_id=schedule_data.instructor_id,
            group_id=schedule_data.group_id,
            venue_id=schedule_data.venue_id,
            subject=schedule_data.subject,
            notes=schedule_data.notes,
        )
        
        # Update schedule
        schedule = await use_case.execute(update_dto)
        
        return ScheduleResponse(
            id=schedule.id,
            start_date=schedule.start_date,
            end_date=schedule.end_date,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            instructor_id=schedule.instructor_id,
            group_id=schedule.group_id,
            venue_id=schedule.venue_id,
            subject=schedule.subject,
            status=schedule.status,
            notes=schedule.notes,
            created_at=schedule.created_at,
            updated_at=schedule.updated_at,
        )
    except ScheduleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except (AcademicGroupNotFoundError, VenueNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except (InstructorNotAvailableError, VenueNotAvailableError) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating schedule: {str(e)}"
        )


@router.delete("/{schedule_id}", response_model=MessageResponse)
async def delete_schedule(
    schedule_id: UUID,
    use_case: DeleteScheduleUseCase = Depends(get_delete_schedule_use_case),
):
    """Delete a schedule."""
    try:
        await use_case.execute(schedule_id)
        return MessageResponse(message="Schedule deleted successfully")
    except ScheduleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting schedule: {str(e)}"
        )
