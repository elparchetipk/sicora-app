"""Attendance domain entity."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from ..value_objects import AttendanceStatus


class AttendanceRecord:
    """Domain entity representing an attendance record."""
    
    def __init__(
        self,
        student_id: UUID,
        schedule_id: UUID,
        instructor_id: UUID,
        date: datetime,
        block_identifier: str,
        venue_id: UUID,
        status: AttendanceStatus = AttendanceStatus.ABSENT,
        qr_code_used: Optional[str] = None,
        notes: Optional[str] = None,
        recorded_at: Optional[datetime] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.student_id = student_id
        self.schedule_id = schedule_id
        self.instructor_id = instructor_id
        self.date = date
        self.block_identifier = block_identifier
        self.venue_id = venue_id
        self.status = status
        self.qr_code_used = qr_code_used
        self.notes = notes
        self.recorded_at = recorded_at or datetime.utcnow()
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def mark_present(self, qr_code: str, notes: Optional[str] = None) -> None:
        """Mark student as present with QR code verification."""
        self.status = AttendanceStatus.PRESENT
        self.qr_code_used = qr_code
        self.notes = notes
        self.recorded_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def mark_absent(self, notes: Optional[str] = None) -> None:
        """Mark student as absent."""
        self.status = AttendanceStatus.ABSENT
        self.notes = notes
        self.updated_at = datetime.utcnow()
    
    def mark_justified(self, notes: Optional[str] = None) -> None:
        """Mark absence as justified (usually after justification approval)."""
        self.status = AttendanceStatus.JUSTIFIED
        self.notes = notes
        self.updated_at = datetime.utcnow()
    
    def can_update_on_same_day(self, current_date: datetime) -> bool:
        """Check if attendance can be updated (same day only)."""
        return self.date.date() == current_date.date()
    
    def is_present(self) -> bool:
        """Check if student is marked as present."""
        return self.status == AttendanceStatus.PRESENT
    
    def is_absent(self) -> bool:
        """Check if student is marked as absent."""
        return self.status == AttendanceStatus.ABSENT
    
    def is_justified(self) -> bool:
        """Check if absence is justified."""
        return self.status == AttendanceStatus.JUSTIFIED
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, AttendanceRecord):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __repr__(self) -> str:
        return (
            f"AttendanceRecord(id={self.id}, student_id={self.student_id}, "
            f"date={self.date}, status={self.status.value})"
        )
