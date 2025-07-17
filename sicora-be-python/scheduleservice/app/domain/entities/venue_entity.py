"""Venue entity for managing physical spaces."""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class Venue:
    """Venue domain entity representing a physical learning space."""
    
    def __init__(
        self,
        name: str,
        code: str,
        capacity: int,
        venue_type: str,
        building: str,
        floor: str,
        campus_id: UUID,
        id: Optional[UUID] = None,
        description: Optional[str] = None,
        equipment: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """Initialize Venue entity."""
        if len(name.strip()) < 2:
            raise ValueError("Venue name must have at least 2 characters")
        if len(code.strip()) < 1:
            raise ValueError("Venue code must not be empty")
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        if len(venue_type.strip()) < 2:
            raise ValueError("Venue type must have at least 2 characters")
        
        self.id = id or uuid4()
        self.name = name.strip()
        self.code = code.strip().upper()
        self.capacity = capacity
        self.venue_type = venue_type.strip()
        self.building = building.strip()
        self.floor = floor.strip()
        self.campus_id = campus_id
        self.description = description.strip() if description else None
        self.equipment = equipment.strip() if equipment else None
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def update_name(self, name: str) -> None:
        """Update venue name."""
        if len(name.strip()) < 2:
            raise ValueError("Venue name must have at least 2 characters")
        self.name = name.strip()
        self.updated_at = datetime.now()
    
    def update_capacity(self, capacity: int) -> None:
        """Update venue capacity."""
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        self.capacity = capacity
        self.updated_at = datetime.now()
    
    def update_description(self, description: str) -> None:
        """Update venue description."""
        self.description = description.strip() if description else None
        self.updated_at = datetime.now()
    
    def update_equipment(self, equipment: str) -> None:
        """Update venue equipment."""
        self.equipment = equipment.strip() if equipment else None
        self.updated_at = datetime.now()
    
    def activate(self) -> None:
        """Activate the venue."""
        self.is_active = True
        self.updated_at = datetime.now()
    
    def deactivate(self) -> None:
        """Deactivate the venue."""
        self.is_active = False
        self.updated_at = datetime.now()
    
    def __str__(self) -> str:
        return f"{self.code} - {self.name} (Cap: {self.capacity})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Venue):
            return False
        return self.id == other.id
