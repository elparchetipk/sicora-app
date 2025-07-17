"""Academic Group entity."""

from datetime import datetime, date
from typing import Optional
from uuid import UUID, uuid4


class AcademicGroup:
    """Academic Group domain entity representing a cohort of students."""
    
    def __init__(
        self,
        group_number: str,
        program_id: UUID,
        start_date: date,
        end_date: date,
        max_students: int,
        id: Optional[UUID] = None,
        current_students: int = 0,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """Initialize Academic Group entity."""
        if len(group_number.strip()) < 1:
            raise ValueError("Group number must not be empty")
        if start_date > end_date:
            raise ValueError("Start date must be before or equal to end date")
        if max_students < 1:
            raise ValueError("Max students must be at least 1")
        if current_students < 0:
            raise ValueError("Current students cannot be negative")
        if current_students > max_students:
            raise ValueError("Current students cannot exceed max students")
        
        self.id = id or uuid4()
        self.group_number = group_number.strip().upper()
        self.program_id = program_id
        self.start_date = start_date
        self.end_date = end_date
        self.max_students = max_students
        self.current_students = current_students
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def update_dates(self, start_date: date, end_date: date) -> None:
        """Update group dates."""
        if start_date > end_date:
            raise ValueError("Start date must be before or equal to end date")
        self.start_date = start_date
        self.end_date = end_date
        self.updated_at = datetime.now()
    
    def update_max_students(self, max_students: int) -> None:
        """Update maximum number of students."""
        if max_students < 1:
            raise ValueError("Max students must be at least 1")
        if self.current_students > max_students:
            raise ValueError("Max students cannot be less than current students")
        self.max_students = max_students
        self.updated_at = datetime.now()
    
    def add_student(self) -> None:
        """Add a student to the group."""
        if self.current_students >= self.max_students:
            raise ValueError("Group is already at maximum capacity")
        self.current_students += 1
        self.updated_at = datetime.now()
    
    def remove_student(self) -> None:
        """Remove a student from the group."""
        if self.current_students <= 0:
            raise ValueError("No students to remove")
        self.current_students -= 1
        self.updated_at = datetime.now()
    
    def activate(self) -> None:
        """Activate the group."""
        self.is_active = True
        self.updated_at = datetime.now()
    
    def deactivate(self) -> None:
        """Deactivate the group."""
        self.is_active = False
        self.updated_at = datetime.now()
    
    @property
    def is_full(self) -> bool:
        """Check if the group is at maximum capacity."""
        return self.current_students >= self.max_students
    
    @property
    def available_slots(self) -> int:
        """Get number of available slots."""
        return self.max_students - self.current_students
    
    def __str__(self) -> str:
        return f"Group {self.group_number} ({self.current_students}/{self.max_students})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, AcademicGroup):
            return False
        return self.id == other.id
