"""Schedule status value object."""

from enum import Enum
from typing import Any


class ScheduleStatus(Enum):
    """Schedule status enumeration."""
    
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED" 
    RESCHEDULED = "RESCHEDULED"
    COMPLETED = "COMPLETED"
    
    @property
    def value(self) -> str:
        """Get the string value of the status."""
        return self._value_
    
    @classmethod
    def from_string(cls, value: str) -> 'ScheduleStatus':
        """Create ScheduleStatus from string value."""
        for status in cls:
            if status.value == value.upper():
                return status
        raise ValueError(f"Invalid schedule status: {value}")
    
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ScheduleStatus):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other.upper()
        return False
