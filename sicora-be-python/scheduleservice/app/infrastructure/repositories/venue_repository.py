"""SQLAlchemy implementation of the Venue Repository."""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select

from ...domain.entities.venue_entity import Venue
from ...domain.repositories.venue_repository_interface import VenueRepositoryInterface
from ..config.models import VenueModel


class VenueRepositorySQLAlchemy(VenueRepositoryInterface):
    """SQLAlchemy implementation of the venue repository."""

    def __init__(self, db_session: Session):
        self._db = db_session

    async def create(self, venue: Venue) -> Venue:
        """Create a new venue."""
        venue_model = VenueModel(
            id=venue.id,
            name=venue.name,
            code=venue.code,
            capacity=venue.capacity,
            venue_type=venue.venue_type,
            building=venue.building,
            floor=venue.floor,
            campus_id=venue.campus_id,
            description=venue.description,
            equipment=venue.equipment,
            is_active=venue.is_active,
            created_at=venue.created_at,
            updated_at=venue.updated_at,
        )
        self._db.add(venue_model)
        self._db.commit()
        self._db.refresh(venue_model)
        return self._map_to_entity(venue_model)

    async def get_by_id(self, venue_id: UUID) -> Optional[Venue]:
        """Get venue by ID."""
        stmt = select(VenueModel).where(VenueModel.id == venue_id)
        venue_model = self._db.execute(stmt).scalar_one_or_none()
        return self._map_to_entity(venue_model) if venue_model else None

    async def get_by_code(self, code: str) -> Optional[Venue]:
        """Get venue by code."""
        stmt = select(VenueModel).where(VenueModel.code == code)
        venue_model = self._db.execute(stmt).scalar_one_or_none()
        return self._map_to_entity(venue_model) if venue_model else None

    async def update(self, venue: Venue) -> Venue:
        """Update an existing venue."""
        stmt = select(VenueModel).where(VenueModel.id == venue.id)
        venue_model = self._db.execute(stmt).scalar_one_or_none()

        if not venue_model:
            return None

        venue_model.name = venue.name
        venue_model.code = venue.code
        venue_model.capacity = venue.capacity
        venue_model.venue_type = venue.venue_type
        venue_model.building = venue.building
        venue_model.floor = venue.floor
        venue_model.campus_id = venue.campus_id
        venue_model.description = venue.description
        venue_model.equipment = venue.equipment
        venue_model.is_active = venue.is_active
        venue_model.updated_at = datetime.now()

        self._db.commit()
        self._db.refresh(venue_model)
        return self._map_to_entity(venue_model)

    async def delete(self, venue_id: UUID) -> bool:
        """Delete a venue."""
        stmt = select(VenueModel).where(VenueModel.id == venue_id)
        venue_model = self._db.execute(stmt).scalar_one_or_none()
        if venue_model:
            self._db.delete(venue_model)
            self._db.commit()
            return True
        return False

    async def get_by_campus(self, campus_id: UUID) -> List[Venue]:
        """Get venues by campus."""
        stmt = select(VenueModel).where(VenueModel.campus_id == campus_id).order_by(VenueModel.name)
        venue_models = self._db.execute(stmt).scalars().all()
        return [self._map_to_entity(vm) for vm in venue_models]

    async def list_active(self) -> List[Venue]:
        """List all active venues."""
        stmt = select(VenueModel).where(VenueModel.is_active == True).order_by(VenueModel.name)
        venue_models = self._db.execute(stmt).scalars().all()
        return [self._map_to_entity(vm) for vm in venue_models]

    async def list_all(self) -> List[Venue]:
        """List all venues."""
        stmt = select(VenueModel).order_by(VenueModel.name)
        venue_models = self._db.execute(stmt).scalars().all()
        return [self._map_to_entity(vm) for vm in venue_models]

    def _map_to_entity(self, model: VenueModel) -> Venue:
        """Map SQLAlchemy model to domain entity."""
        if not model:
            return None
        return Venue(
            id=model.id,
            name=model.name,
            code=model.code,
            capacity=model.capacity,
            venue_type=model.venue_type,
            building=model.building,
            floor=model.floor,
            campus_id=model.campus_id,
            description=model.description,
            equipment=model.equipment,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
