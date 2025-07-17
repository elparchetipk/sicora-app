"""Domain exceptions for schedule management."""

from .schedule_exceptions import (
    ScheduleException,
    ScheduleNotFoundError,
    ScheduleConflictError,
    AcademicProgramNotFoundError,
    AcademicGroupNotFoundError,
    VenueNotFoundError,
    InvalidScheduleDataError,
    InstructorNotAvailableError,
    VenueNotAvailableError,
    DuplicateEntityError,
    InvalidDateRangeError,
    InvalidTimeSlotError,
    GroupCapacityExceededError,
    InactiveEntityError,
)

__all__ = [
    "ScheduleException",
    "ScheduleNotFoundError",
    "ScheduleConflictError",
    "AcademicProgramNotFoundError",
    "AcademicGroupNotFoundError",
    "VenueNotFoundError",
    "InvalidScheduleDataError",
    "InstructorNotAvailableError",
    "VenueNotAvailableError",
    "DuplicateEntityError",
    "InvalidDateRangeError",
    "InvalidTimeSlotError",
    "GroupCapacityExceededError",
    "InactiveEntityError",
]
