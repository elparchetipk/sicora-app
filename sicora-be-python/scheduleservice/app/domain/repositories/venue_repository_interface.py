"""Venue repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.venue_entity import Venue


class VenueRepositoryInterface(ABC):
    """Interface for venue repository."""
    
    @abstractmethod
    async def create(self, venue: Venue) -> Venue:
        """Create a new venue."""
        pass
    
    @abstractmethod
    async def get_by_id(self, venue_id: UUID) -> Optional[Venue]:
        """Get venue by ID."""
        pass
    
    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[Venue]:
        """Get venue by code."""
        pass
    
    @abstractmethod
    async def update(self, venue: Venue) -> Venue:
        """Update an existing venue."""
        pass
    
    @abstractmethod
    async def delete(self, venue_id: UUID) -> bool:
        """Delete a venue."""
        pass
    
    @abstractmethod
    async def get_by_campus(self, campus_id: UUID) -> List[Venue]:
        """Get venues by campus."""
        pass
    
    @abstractmethod
    async def list_active(self) -> List[Venue]:
        """List all active venues."""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[Venue]:
        """List all venues."""
        pass
