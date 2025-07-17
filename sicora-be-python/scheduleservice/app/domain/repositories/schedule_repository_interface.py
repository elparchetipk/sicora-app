"""Schedule repository interface."""

from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from uuid import UUID

from ..entities.schedule_entity import Schedule


class ScheduleRepositoryInterface(ABC):
    """Interface for schedule repository."""
    
    @abstractmethod
    async def create(self, schedule: Schedule) -> Schedule:
        """Create a new schedule."""
        pass
    
    @abstractmethod
    async def get_by_id(self, schedule_id: UUID) -> Optional[Schedule]:
        """Get schedule by ID."""
        pass
    
    @abstractmethod
    async def update(self, schedule: Schedule) -> Schedule:
        """Update an existing schedule."""
        pass
    
    @abstractmethod
    async def delete(self, schedule_id: UUID) -> bool:
        """Delete a schedule."""
        pass
    
    @abstractmethod
    async def get_by_date_range(self, start_date: date, end_date: date) -> List[Schedule]:
        """Get schedules by date range."""
        pass
    
    @abstractmethod
    async def get_by_instructor(self, instructor_id: UUID) -> List[Schedule]:
        """Get schedules by instructor."""
        pass
    
    @abstractmethod
    async def get_by_group(self, group_id: UUID) -> List[Schedule]:
        """Get schedules by group."""
        pass
    
    @abstractmethod
    async def get_by_venue(self, venue_id: UUID) -> List[Schedule]:
        """Get schedules by venue."""
        pass
    
    @abstractmethod
    async def get_active_schedules(self) -> List[Schedule]:
        """Get all active schedules."""
        pass
    
    @abstractmethod
    async def check_instructor_conflict(
        self, 
        instructor_id: UUID, 
        start_date: date, 
        end_date: date,
        exclude_schedule_id: Optional[UUID] = None
    ) -> bool:
        """Check if instructor has scheduling conflicts."""
        pass
    
    @abstractmethod
    async def check_venue_conflict(
        self, 
        venue_id: UUID, 
        start_date: date, 
        end_date: date,
        exclude_schedule_id: Optional[UUID] = None
    ) -> bool:
        """Check if venue has scheduling conflicts."""
        pass
