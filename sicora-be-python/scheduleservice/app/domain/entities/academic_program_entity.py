"""Academic Program entity."""

from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from ..value_objects.program_type import ProgramType


class AcademicProgram:
    """Academic Program domain entity."""
    
    def __init__(
        self,
        name: str,
        code: str,
        program_type: ProgramType,
        duration_months: int,
        description: Optional[str] = None,
        id: Optional[UUID] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """Initialize Academic Program entity."""
        if len(name.strip()) < 2:
            raise ValueError("Program name must have at least 2 characters")
        if len(code.strip()) < 2:
            raise ValueError("Program code must have at least 2 characters")
        if duration_months < 1:
            raise ValueError("Duration must be at least 1 month")
        
        self.id = id or uuid4()
        self.name = name.strip()
        self.code = code.strip().upper()
        self.program_type = program_type
        self.duration_months = duration_months
        self.description = description.strip() if description else None
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def update_name(self, name: str) -> None:
        """Update program name."""
        if len(name.strip()) < 2:
            raise ValueError("Program name must have at least 2 characters")
        self.name = name.strip()
        self.updated_at = datetime.now()
    
    def update_description(self, description: str) -> None:
        """Update program description."""
        self.description = description.strip() if description else None
        self.updated_at = datetime.now()
    
    def update_duration(self, duration_months: int) -> None:
        """Update program duration."""
        if duration_months < 1:
            raise ValueError("Duration must be at least 1 month")
        self.duration_months = duration_months
        self.updated_at = datetime.now()
    
    def activate(self) -> None:
        """Activate the academic program."""
        self.is_active = True
        self.updated_at = datetime.now()
    
    def deactivate(self) -> None:
        """Deactivate the academic program."""
        self.is_active = False
        self.updated_at = datetime.now()
    
    def __str__(self) -> str:
        return f"{self.code} - {self.name}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, AcademicProgram):
            return False
        return self.id == other.id
