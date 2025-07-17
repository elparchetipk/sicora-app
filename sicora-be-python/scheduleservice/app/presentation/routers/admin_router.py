"""Admin router for managing academic entities."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from pydantic import ValidationError

from ..schemas.schedule_schemas import (
    AcademicProgramCreateRequest,
    AcademicProgramUpdateRequest,
    AcademicProgramResponse,
    AcademicGroupCreateRequest,
    AcademicGroupUpdateRequest,
    AcademicGroupResponse,
    VenueCreateRequest,
    VenueUpdateRequest,
    VenueResponse,
    BulkUploadResultResponse,
    MessageResponse,
)
from ...application.use_cases.academic_entity_use_cases import (
    CreateAcademicProgramUseCase,
    ListAcademicProgramsUseCase,
    CreateAcademicGroupUseCase,
    ListAcademicGroupsUseCase,
    CreateVenueUseCase,
    ListVenuesUseCase,
)
from ...application.use_cases.schedule_use_cases import BulkUploadSchedulesUseCase
from ...application.dtos.schedule_dtos import (
    CreateAcademicProgramDTO,
    UpdateAcademicProgramDTO,
    CreateAcademicGroupDTO,
    UpdateAcademicGroupDTO,
    CreateVenueDTO,
    UpdateVenueDTO,
    BulkScheduleUploadDTO,
    CreateScheduleDTO,
)
from ...domain.exceptions.schedule_exceptions import (
    AcademicProgramNotFoundError,
    AcademicGroupNotFoundError,
    VenueNotFoundError,
    DuplicateEntityError,
    InvalidScheduleDataError,
)
from ...dependencies import (
    get_create_academic_program_use_case,
    get_list_academic_programs_use_case,
    get_create_academic_group_use_case,
    get_list_academic_groups_use_case,
    get_create_venue_use_case,
    get_list_venues_use_case,
    get_bulk_upload_schedules_use_case,
)

router = APIRouter(prefix="/admin", tags=["Admin"])


# Academic Programs Endpoints
@router.get("/programs", response_model=List[AcademicProgramResponse])
async def list_academic_programs(
    active_only: bool = True,
    use_case: ListAcademicProgramsUseCase = Depends(get_list_academic_programs_use_case),
):
    """List academic programs."""
    try:
        programs = await use_case.execute(active_only)
        return [
            AcademicProgramResponse(
                id=program.id,
                name=program.name,
                code=program.code,
                program_type=program.program_type,
                duration_months=program.duration_months,
                description=program.description,
                is_active=program.is_active,
                created_at=program.created_at,
                updated_at=program.updated_at,
            )
            for program in programs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving academic programs: {str(e)}"
        )


@router.post("/programs", response_model=AcademicProgramResponse, status_code=status.HTTP_201_CREATED)
async def create_academic_program(
    program_data: AcademicProgramCreateRequest,
    use_case: CreateAcademicProgramUseCase = Depends(get_create_academic_program_use_case),
):
    """Create a new academic program."""
    try:
        # Convert to DTO
        create_dto = CreateAcademicProgramDTO(
            name=program_data.name,
            code=program_data.code,
            program_type=program_data.program_type,
            duration_months=program_data.duration_months,
            description=program_data.description,
        )
        
        # Create program
        program = await use_case.execute(create_dto)
        
        return AcademicProgramResponse(
            id=program.id,
            name=program.name,
            code=program.code,
            program_type=program.program_type,
            duration_months=program.duration_months,
            description=program.description,
            is_active=program.is_active,
            created_at=program.created_at,
            updated_at=program.updated_at,
        )
    except DuplicateEntityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating academic program: {str(e)}"
        )


# Academic Groups Endpoints
@router.get("/groups", response_model=List[AcademicGroupResponse])
async def list_academic_groups(
    program_id: Optional[UUID] = None,
    active_only: bool = True,
    use_case: ListAcademicGroupsUseCase = Depends(get_list_academic_groups_use_case),
):
    """List academic groups."""
    try:
        groups = await use_case.execute(program_id, active_only)
        return [
            AcademicGroupResponse(
                id=group.id,
                group_number=group.group_number,
                program_id=group.program_id,
                start_date=group.start_date,
                end_date=group.end_date,
                max_students=group.max_students,
                current_students=group.current_students,
                is_active=group.is_active,
                created_at=group.created_at,
                updated_at=group.updated_at,
            )
            for group in groups
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving academic groups: {str(e)}"
        )


@router.post("/groups", response_model=AcademicGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_academic_group(
    group_data: AcademicGroupCreateRequest,
    use_case: CreateAcademicGroupUseCase = Depends(get_create_academic_group_use_case),
):
    """Create a new academic group."""
    try:
        # Convert to DTO
        create_dto = CreateAcademicGroupDTO(
            group_number=group_data.group_number,
            program_id=group_data.program_id,
            start_date=group_data.start_date,
            end_date=group_data.end_date,
            max_students=group_data.max_students,
        )
        
        # Create group
        group = await use_case.execute(create_dto)
        
        return AcademicGroupResponse(
            id=group.id,
            group_number=group.group_number,
            program_id=group.program_id,
            start_date=group.start_date,
            end_date=group.end_date,
            max_students=group.max_students,
            current_students=group.current_students,
            is_active=group.is_active,
            created_at=group.created_at,
            updated_at=group.updated_at,
        )
    except AcademicProgramNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DuplicateEntityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating academic group: {str(e)}"
        )


# Venues Endpoints
@router.get("/venues", response_model=List[VenueResponse])
async def list_venues(
    campus_id: Optional[UUID] = None,
    active_only: bool = True,
    use_case: ListVenuesUseCase = Depends(get_list_venues_use_case),
):
    """List venues."""
    try:
        venues = await use_case.execute(campus_id, active_only)
        return [
            VenueResponse(
                id=venue.id,
                name=venue.name,
                code=venue.code,
                capacity=venue.capacity,
                venue_type=venue.venue_type,
                building=venue.building,
                floor=venue.floor,
                campus_id=venue.campus_id,
                description=venue.description,
                equipment=venue.equipment,
                is_active=venue.is_active,
                created_at=venue.created_at,
                updated_at=venue.updated_at,
            )
            for venue in venues
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving venues: {str(e)}"
        )


@router.post("/venues", response_model=VenueResponse, status_code=status.HTTP_201_CREATED)
async def create_venue(
    venue_data: VenueCreateRequest,
    use_case: CreateVenueUseCase = Depends(get_create_venue_use_case),
):
    """Create a new venue."""
    try:
        # Convert to DTO
        create_dto = CreateVenueDTO(
            name=venue_data.name,
            code=venue_data.code,
            capacity=venue_data.capacity,
            venue_type=venue_data.venue_type,
            building=venue_data.building,
            floor=venue_data.floor,
            campus_id=venue_data.campus_id,
            description=venue_data.description,
            equipment=venue_data.equipment,
        )
        
        # Create venue
        venue = await use_case.execute(create_dto)
        
        return VenueResponse(
            id=venue.id,
            name=venue.name,
            code=venue.code,
            capacity=venue.capacity,
            venue_type=venue.venue_type,
            building=venue.building,
            floor=venue.floor,
            campus_id=venue.campus_id,
            description=venue.description,
            equipment=venue.equipment,
            is_active=venue.is_active,
            created_at=venue.created_at,
            updated_at=venue.updated_at,
        )
    except DuplicateEntityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating venue: {str(e)}"
        )


# Bulk Upload Endpoint
@router.post("/schedules/upload", response_model=BulkUploadResultResponse)
async def bulk_upload_schedules(
    file: UploadFile = File(...),
    use_case: BulkUploadSchedulesUseCase = Depends(get_bulk_upload_schedules_use_case),
):
    """Bulk upload schedules from CSV file."""
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only CSV files are allowed"
            )
        
        # Read CSV content
        content = await file.read()
        csv_content = content.decode('utf-8')
        
        # Parse CSV and create DTOs (simplified for demo)
        # In real implementation, you would parse CSV properly
        schedules_data = []  # This would be parsed from CSV
        
        bulk_dto = BulkScheduleUploadDTO(schedules=schedules_data)
        
        # Process bulk upload
        result = await use_case.execute(bulk_dto)
        
        return BulkUploadResultResponse(
            total_processed=result.total_processed,
            successful=result.successful,
            failed=result.failed,
            errors=result.errors,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing bulk upload: {str(e)}"
        )
