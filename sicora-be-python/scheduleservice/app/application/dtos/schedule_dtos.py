"""Data Transfer Objects for Schedule operations."""

from dataclasses import dataclass
from datetime import date, time
from typing import Optional, List
from uuid import UUID


# Schedule DTOs
@dataclass(frozen=True)
class CreateScheduleDTO:
    """DTO for creating a schedule."""
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    instructor_id: UUID
    group_id: UUID
    venue_id: UUID
    subject: str
    notes: Optional[str] = None


@dataclass(frozen=True)
class UpdateScheduleDTO:
    """DTO for updating a schedule."""
    schedule_id: UUID
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    instructor_id: Optional[UUID] = None
    group_id: Optional[UUID] = None
    venue_id: Optional[UUID] = None
    subject: Optional[str] = None
    notes: Optional[str] = None


@dataclass(frozen=True)
class ScheduleResponseDTO:
    """DTO for schedule response."""
    id: UUID
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    instructor_id: UUID
    group_id: UUID
    venue_id: UUID
    subject: str
    status: str
    notes: Optional[str]
    created_at: date
    updated_at: date


@dataclass(frozen=True)
class ScheduleFilterDTO:
    """DTO for filtering schedules."""
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    instructor_id: Optional[UUID] = None
    group_id: Optional[UUID] = None
    venue_id: Optional[UUID] = None
    status: Optional[str] = None


# Academic Program DTOs
@dataclass(frozen=True)
class CreateAcademicProgramDTO:
    """DTO for creating an academic program."""
    name: str
    code: str
    program_type: str
    duration_months: int
    description: Optional[str] = None


@dataclass(frozen=True)
class UpdateAcademicProgramDTO:
    """DTO for updating an academic program."""
    program_id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    duration_months: Optional[int] = None


@dataclass(frozen=True)
class AcademicProgramResponseDTO:
    """DTO for academic program response."""
    id: UUID
    name: str
    code: str
    program_type: str
    duration_months: int
    description: Optional[str]
    is_active: bool
    created_at: date
    updated_at: date


# Academic Group DTOs
@dataclass(frozen=True)
class CreateAcademicGroupDTO:
    """DTO for creating an academic group."""
    group_number: str
    program_id: UUID
    start_date: date
    end_date: date
    max_students: int


@dataclass(frozen=True)
class UpdateAcademicGroupDTO:
    """DTO for updating an academic group."""
    group_id: UUID
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    max_students: Optional[int] = None


@dataclass(frozen=True)
class AcademicGroupResponseDTO:
    """DTO for academic group response."""
    id: UUID
    group_number: str
    program_id: UUID
    start_date: date
    end_date: date
    max_students: int
    current_students: int
    is_active: bool
    created_at: date
    updated_at: date


# Venue DTOs
@dataclass(frozen=True)
class CreateVenueDTO:
    """DTO for creating a venue."""
    name: str
    code: str
    capacity: int
    venue_type: str
    building: str
    floor: str
    campus_id: UUID
    description: Optional[str] = None
    equipment: Optional[str] = None


@dataclass(frozen=True)
class UpdateVenueDTO:
    """DTO for updating a venue."""
    venue_id: UUID
    name: Optional[str] = None
    capacity: Optional[int] = None
    description: Optional[str] = None
    equipment: Optional[str] = None


@dataclass(frozen=True)
class VenueResponseDTO:
    """DTO for venue response."""
    id: UUID
    name: str
    code: str
    capacity: int
    venue_type: str
    building: str
    floor: str
    campus_id: UUID
    description: Optional[str]
    equipment: Optional[str]
    is_active: bool
    created_at: date
    updated_at: date


# Bulk Upload DTOs
@dataclass(frozen=True)
class BulkScheduleUploadDTO:
    """DTO for bulk schedule upload."""
    schedules: List[CreateScheduleDTO]


@dataclass(frozen=True)
class BulkUploadResultDTO:
    """DTO for bulk upload result."""
    total_processed: int
    successful: int
    failed: int
    errors: List[str]
