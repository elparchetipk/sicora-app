"""Domain exceptions for schedule management."""


class ScheduleException(Exception):
    """Base exception for schedule domain."""
    pass


class ScheduleNotFoundError(ScheduleException):
    """Raised when schedule is not found."""
    
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"Schedule not found: {field}={value}")


class ScheduleConflictError(ScheduleException):
    """Raised when there's a scheduling conflict."""
    
    def __init__(self, message: str):
        super().__init__(f"Schedule conflict: {message}")


class AcademicProgramNotFoundError(ScheduleException):
    """Raised when academic program is not found."""
    
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"Academic program not found: {field}={value}")


class AcademicGroupNotFoundError(ScheduleException):
    """Raised when academic group is not found."""
    
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"Academic group not found: {field}={value}")


class VenueNotFoundError(ScheduleException):
    """Raised when venue is not found."""
    
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"Venue not found: {field}={value}")


class InvalidScheduleDataError(ScheduleException):
    """Raised when schedule data is invalid."""
    
    def __init__(self, message: str):
        super().__init__(f"Invalid schedule data: {message}")


class InstructorNotAvailableError(ScheduleException):
    """Raised when instructor is not available for scheduling."""
    
    def __init__(self, instructor_id: str, time_slot: str):
        super().__init__(f"Instructor {instructor_id} not available at {time_slot}")


class VenueNotAvailableError(ScheduleException):
    """Raised when venue is not available for scheduling."""
    
    def __init__(self, venue_id: str, time_slot: str):
        super().__init__(f"Venue {venue_id} not available at {time_slot}")


class DuplicateEntityError(ScheduleException):
    """Raised when trying to create duplicate entity."""
    
    def __init__(self, entity_type: str, field: str, value: str):
        super().__init__(f"Duplicate {entity_type}: {field}={value}")


class InvalidDateRangeError(ScheduleException):
    """Raised when date range is invalid."""
    
    def __init__(self, start_date: str, end_date: str):
        super().__init__(f"Invalid date range: {start_date} to {end_date}")


class InvalidTimeSlotError(ScheduleException):
    """Raised when time slot is invalid."""
    
    def __init__(self, message: str):
        super().__init__(f"Invalid time slot: {message}")


class GroupCapacityExceededError(ScheduleException):
    """Raised when trying to exceed group capacity."""
    
    def __init__(self, group_id: str, current: int, max_capacity: int):
        super().__init__(f"Group {group_id} capacity exceeded: {current}/{max_capacity}")


class InactiveEntityError(ScheduleException):
    """Raised when trying to use an inactive entity."""
    
    def __init__(self, entity_type: str, entity_id: str):
        super().__init__(f"Cannot use inactive {entity_type}: {entity_id}")
