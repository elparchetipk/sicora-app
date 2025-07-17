"""Academic group repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.academic_group_entity import AcademicGroup


class AcademicGroupRepositoryInterface(ABC):
    """Interface for academic group repository."""
    
    @abstractmethod
    async def create(self, group: AcademicGroup) -> AcademicGroup:
        """Create a new academic group."""
        pass
    
    @abstractmethod
    async def get_by_id(self, group_id: UUID) -> Optional[AcademicGroup]:
        """Get academic group by ID."""
        pass
    
    @abstractmethod
    async def get_by_group_number(self, group_number: str) -> Optional[AcademicGroup]:
        """Get academic group by group number."""
        pass
    
    @abstractmethod
    async def update(self, group: AcademicGroup) -> AcademicGroup:
        """Update an existing academic group."""
        pass
    
    @abstractmethod
    async def delete(self, group_id: UUID) -> bool:
        """Delete an academic group."""
        pass
    
    @abstractmethod
    async def get_by_program(self, program_id: UUID) -> List[AcademicGroup]:
        """Get groups by academic program."""
        pass
    
    @abstractmethod
    async def list_active(self) -> List[AcademicGroup]:
        """List all active academic groups."""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[AcademicGroup]:
        """List all academic groups."""
        pass
