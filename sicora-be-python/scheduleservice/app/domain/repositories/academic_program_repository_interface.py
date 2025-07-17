"""Academic program repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.academic_program_entity import AcademicProgram


class AcademicProgramRepositoryInterface(ABC):
    """Interface for academic program repository."""
    
    @abstractmethod
    async def create(self, program: AcademicProgram) -> AcademicProgram:
        """Create a new academic program."""
        pass
    
    @abstractmethod
    async def get_by_id(self, program_id: UUID) -> Optional[AcademicProgram]:
        """Get academic program by ID."""
        pass
    
    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[AcademicProgram]:
        """Get academic program by code."""
        pass
    
    @abstractmethod
    async def update(self, program: AcademicProgram) -> AcademicProgram:
        """Update an existing academic program."""
        pass
    
    @abstractmethod
    async def delete(self, program_id: UUID) -> bool:
        """Delete an academic program."""
        pass
    
    @abstractmethod
    async def list_active(self) -> List[AcademicProgram]:
        """List all active academic programs."""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[AcademicProgram]:
        """List all academic programs."""
        pass
