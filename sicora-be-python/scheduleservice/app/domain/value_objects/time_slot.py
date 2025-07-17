"""Time slot value object."""

from datetime import time
from typing import Any


class TimeSlot:
    """Time slot value object representing start and end times."""
    
    def __init__(self, start_time: time, end_time: time):
        """Initialize time slot with validation."""
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")
        
        self._start_time = start_time
        self._end_time = end_time
    
    @property
    def start_time(self) -> time:
        """Get start time."""
        return self._start_time
    
    @property
    def end_time(self) -> time:
        """Get end time."""
        return self._end_time
    
    @property
    def duration_minutes(self) -> int:
        """Calculate duration in minutes."""
        start_seconds = self._start_time.hour * 3600 + self._start_time.minute * 60
        end_seconds = self._end_time.hour * 3600 + self._end_time.minute * 60
        return (end_seconds - start_seconds) // 60
    
    def overlaps_with(self, other: 'TimeSlot') -> bool:
        """Check if this time slot overlaps with another."""
        return not (self._end_time <= other._start_time or self._start_time >= other._end_time)
    
    def __str__(self) -> str:
        return f"{self._start_time.strftime('%H:%M')} - {self._end_time.strftime('%H:%M')}"
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TimeSlot):
            return False
        return self._start_time == other._start_time and self._end_time == other._end_time
    
    def __hash__(self) -> int:
        return hash((self._start_time, self._end_time))
