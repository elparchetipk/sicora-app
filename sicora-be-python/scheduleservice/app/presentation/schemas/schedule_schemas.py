"""Pydantic schemas for Schedule operations."""

from datetime import date, time
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field


# Schedule Schemas
class ScheduleCreateRequest(BaseModel):
    """Schema for creating a schedule."""
    start_date: date = Field(..., description="Schedule start date")
    end_date: date = Field(..., description="Schedule end date")
    start_time: time = Field(..., description="Class start time")
    end_time: time = Field(..., description="Class end time")
    instructor_id: UUID = Field(..., description="Instructor ID")
    group_id: UUID = Field(..., description="Academic group ID")
    venue_id: UUID = Field(..., description="Venue ID")
    subject: str = Field(..., min_length=2, max_length=200, description="Subject name")
    notes: Optional[str] = Field(None, max_length=500, description="Additional notes")


class ScheduleUpdateRequest(BaseModel):
    """Schema for updating a schedule."""
    start_date: Optional[date] = Field(None, description="Schedule start date")
    end_date: Optional[date] = Field(None, description="Schedule end date")
    start_time: Optional[time] = Field(None, description="Class start time")
    end_time: Optional[time] = Field(None, description="Class end time")
    instructor_id: Optional[UUID] = Field(None, description="Instructor ID")
    group_id: Optional[UUID] = Field(None, description="Academic group ID")
    venue_id: Optional[UUID] = Field(None, description="Venue ID")
    subject: Optional[str] = Field(None, min_length=2, max_length=200, description="Subject name")
    notes: Optional[str] = Field(None, max_length=500, description="Additional notes")


class ScheduleResponse(BaseModel):
    """Schema for schedule response."""
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

    class Config:
        from_attributes = True


class ScheduleFilterRequest(BaseModel):
    """Schema for filtering schedules."""
    date_from: Optional[date] = Field(None, description="Filter from date")
    date_to: Optional[date] = Field(None, description="Filter to date")
    instructor_id: Optional[UUID] = Field(None, description="Filter by instructor")
    group_id: Optional[UUID] = Field(None, description="Filter by group")
    venue_id: Optional[UUID] = Field(None, description="Filter by venue")
    status: Optional[str] = Field(None, description="Filter by status")


# Academic Program Schemas
class AcademicProgramCreateRequest(BaseModel):
    """Schema for creating an academic program."""
    name: str = Field(..., min_length=2, max_length=200, description="Program name")
    code: str = Field(..., min_length=2, max_length=20, description="Program code")
    program_type: str = Field(..., description="Program type (TECNICO, TECNOLOGO, etc.)")
    duration_months: int = Field(..., ge=1, description="Duration in months")
    description: Optional[str] = Field(None, max_length=1000, description="Program description")


class AcademicProgramUpdateRequest(BaseModel):
    """Schema for updating an academic program."""
    name: Optional[str] = Field(None, min_length=2, max_length=200, description="Program name")
    description: Optional[str] = Field(None, max_length=1000, description="Program description")
    duration_months: Optional[int] = Field(None, ge=1, description="Duration in months")


class AcademicProgramResponse(BaseModel):
    """Schema for academic program response."""
    id: UUID
    name: str
    code: str
    program_type: str
    duration_months: int
    description: Optional[str]
    is_active: bool
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True


# Academic Group Schemas
class AcademicGroupCreateRequest(BaseModel):
    """Schema for creating an academic group."""
    group_number: str = Field(..., min_length=1, max_length=50, description="Group number")
    program_id: UUID = Field(..., description="Academic program ID")
    start_date: date = Field(..., description="Group start date")
    end_date: date = Field(..., description="Group end date")
    max_students: int = Field(..., ge=1, description="Maximum number of students")


class AcademicGroupUpdateRequest(BaseModel):
    """Schema for updating an academic group."""
    start_date: Optional[date] = Field(None, description="Group start date")
    end_date: Optional[date] = Field(None, description="Group end date")
    max_students: Optional[int] = Field(None, ge=1, description="Maximum number of students")


class AcademicGroupResponse(BaseModel):
    """Schema for academic group response."""
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

    class Config:
        from_attributes = True


# Venue Schemas
class VenueCreateRequest(BaseModel):
    """Schema for creating a venue."""
    name: str = Field(..., min_length=2, max_length=200, description="Venue name")
    code: str = Field(..., min_length=1, max_length=20, description="Venue code")
    capacity: int = Field(..., ge=1, description="Venue capacity")
    venue_type: str = Field(..., min_length=2, max_length=50, description="Venue type")
    building: str = Field(..., min_length=1, max_length=100, description="Building name")
    floor: str = Field(..., min_length=1, max_length=20, description="Floor")
    campus_id: UUID = Field(..., description="Campus ID")
    description: Optional[str] = Field(None, max_length=1000, description="Venue description")
    equipment: Optional[str] = Field(None, max_length=1000, description="Available equipment")


class VenueUpdateRequest(BaseModel):
    """Schema for updating a venue."""
    name: Optional[str] = Field(None, min_length=2, max_length=200, description="Venue name")
    capacity: Optional[int] = Field(None, ge=1, description="Venue capacity")
    description: Optional[str] = Field(None, max_length=1000, description="Venue description")
    equipment: Optional[str] = Field(None, max_length=1000, description="Available equipment")


class VenueResponse(BaseModel):
    """Schema for venue response."""
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

    class Config:
        from_attributes = True


# Bulk Upload Schemas
class BulkUploadResultResponse(BaseModel):
    """Schema for bulk upload result."""
    total_processed: int
    successful: int
    failed: int
    errors: List[str]

    class Config:
        from_attributes = True


# Common Response Schemas
class MessageResponse(BaseModel):
    """Schema for simple message responses."""
    message: str


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: str
    detail: Optional[str] = None
