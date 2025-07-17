"""Academic program type value object."""

from enum import Enum
from typing import Any


class ProgramType(Enum):
    """Academic program type enumeration."""
    
    TECNICO = "TECNICO"
    TECNOLOGO = "TECNOLOGO"
    ESPECIALIZACION = "ESPECIALIZACION"
    COMPLEMENTARIO = "COMPLEMENTARIO"
    
    @property
    def value(self) -> str:
        """Get the string value of the program type."""
        return self._value_
    
    @classmethod
    def from_string(cls, value: str) -> 'ProgramType':
        """Create ProgramType from string value."""
        for program_type in cls:
            if program_type.value == value.upper():
                return program_type
        raise ValueError(f"Invalid program type: {value}")
    
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ProgramType):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other.upper()
        return False
