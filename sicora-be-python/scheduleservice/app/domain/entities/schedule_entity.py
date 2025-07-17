"""Schedule entity."""

from datetime import datetime, date, time
from typing import Optional
from uuid import UUID, uuid4

from ..value_objects.schedule_status import ScheduleStatus
from ..value_objects.time_slot import TimeSlot


class Schedule:
    """Schedule domain entity representing a class schedule."""
    
    def __init__(
        self,
        start_date: date,
        end_date: date,
        time_slot: TimeSlot,
        instructor_id: UUID,
        group_id: UUID,
        venue_id: UUID,
        subject: str,
        id: Optional[UUID] = None,
        status: ScheduleStatus = ScheduleStatus.ACTIVE,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """Initialize Schedule entity."""
        if start_date > end_date:
            raise ValueError("Start date must be before or equal to end date")
        if len(subject.strip()) < 2:
            raise ValueError("Subject must have at least 2 characters")
        
        self.id = id or uuid4()
        self.start_date = start_date
        self.end_date = end_date
        self.time_slot = time_slot
        self.instructor_id = instructor_id
        self.group_id = group_id
        self.venue_id = venue_id
        self.subject = subject.strip()
        self.status = status
        self.notes = notes.strip() if notes else None
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def update_subject(self, subject: str) -> None:
        """Update schedule subject."""
        if len(subject.strip()) < 2:
            raise ValueError("Subject must have at least 2 characters")
        self.subject = subject.strip()
        self.updated_at = datetime.now()
    
    def update_dates(self, start_date: date, end_date: date) -> None:
        """Update schedule dates."""
        if start_date > end_date:
            raise ValueError("Start date must be before or equal to end date")
        self.start_date = start_date
        self.end_date = end_date
        self.updated_at = datetime.now()
    
    def update_time_slot(self, time_slot: TimeSlot) -> None:
        """Update schedule time slot."""
        self.time_slot = time_slot
        self.updated_at = datetime.now()
    
    def update_venue(self, venue_id: UUID) -> None:
        """Update schedule venue."""
        self.venue_id = venue_id
        self.updated_at = datetime.now()
    
    def update_instructor(self, instructor_id: UUID) -> None:
        """Update schedule instructor."""
        self.instructor_id = instructor_id
        self.updated_at = datetime.now()
    
    def update_notes(self, notes: str) -> None:
        """Update schedule notes."""
        self.notes = notes.strip() if notes else None
        self.updated_at = datetime.now()
    
    def cancel(self) -> None:
        """Cancel the schedule."""
        self.status = ScheduleStatus.CANCELLED
        self.updated_at = datetime.now()
    
    def reschedule(self) -> None:
        """Mark schedule as rescheduled."""
        self.status = ScheduleStatus.RESCHEDULED
        self.updated_at = datetime.now()
    
    def complete(self) -> None:
        """Mark schedule as completed."""
        self.status = ScheduleStatus.COMPLETED
        self.updated_at = datetime.now()
    
    def activate(self) -> None:
        """Activate the schedule."""
        self.status = ScheduleStatus.ACTIVE
        self.updated_at = datetime.now()
    
    def __str__(self) -> str:
        return f"{self.subject} - {self.start_date} to {self.end_date}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Schedule):
            return False
        return self.id == other.id
