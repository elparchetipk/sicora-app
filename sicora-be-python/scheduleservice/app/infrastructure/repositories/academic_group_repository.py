"""SQLAlchemy implementation of the Academic Group Repository."""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select

from ...domain.entities.academic_group_entity import AcademicGroup
from ...domain.repositories.academic_group_repository_interface import AcademicGroupRepositoryInterface
from ..config.models import AcademicGroupModel


class AcademicGroupRepositorySQLAlchemy(AcademicGroupRepositoryInterface):
    """SQLAlchemy implementation of the academic group repository."""

    def __init__(self, db_session: Session):
        self._db = db_session

    async def create(self, group: AcademicGroup) -> AcademicGroup:
        """Create a new academic group."""
        group_model = AcademicGroupModel(
            id=group.id,
            group_number=group.group_number,
            program_id=group.program_id,
            start_date=group.start_date,
            end_date=group.end_date,
            max_students=group.max_students,
            current_students=group.current_students,
            is_active=group.is_active,
            created_at=group.created_at,
            updated_at=group.updated_at,
        )
        self._db.add(group_model)
        self._db.commit()
        self._db.refresh(group_model)
        return self._map_to_entity(group_model)

    async def get_by_id(self, group_id: UUID) -> Optional[AcademicGroup]:
        """Get academic group by ID."""
        stmt = select(AcademicGroupModel).where(AcademicGroupModel.id == group_id)
        group_model = self._db.execute(stmt).scalar_one_or_none()
        return self._map_to_entity(group_model) if group_model else None

    async def get_by_group_number(self, group_number: str) -> Optional[AcademicGroup]:
        """Get academic group by group number."""
        stmt = select(AcademicGroupModel).where(AcademicGroupModel.group_number == group_number)
        group_model = self._db.execute(stmt).scalar_one_or_none()
        return self._map_to_entity(group_model) if group_model else None

    async def update(self, group: AcademicGroup) -> AcademicGroup:
        """Update an existing academic group."""
        stmt = select(AcademicGroupModel).where(AcademicGroupModel.id == group.id)
        group_model = self._db.execute(stmt).scalar_one_or_none()

        if not group_model:
            return None

        group_model.group_number = group.group_number
        group_model.program_id = group.program_id
        group_model.start_date = group.start_date
        group_model.end_date = group.end_date
        group_model.max_students = group.max_students
        group_model.current_students = group.current_students
        group_model.is_active = group.is_active
        group_model.updated_at = datetime.now()

        self._db.commit()
        self._db.refresh(group_model)
        return self._map_to_entity(group_model)

    async def delete(self, group_id: UUID) -> bool:
        """Delete an academic group."""
        stmt = select(AcademicGroupModel).where(AcademicGroupModel.id == group_id)
        group_model = self._db.execute(stmt).scalar_one_or_none()
        if group_model:
            self._db.delete(group_model)
            self._db.commit()
            return True
        return False

    async def get_by_program(self, program_id: UUID) -> List[AcademicGroup]:
        """Get groups by academic program."""
        stmt = select(AcademicGroupModel).where(AcademicGroupModel.program_id == program_id).order_by(AcademicGroupModel.group_number)
        group_models = self._db.execute(stmt).scalars().all()
        return [self._map_to_entity(gm) for gm in group_models]

    async def list_active(self) -> List[AcademicGroup]:
        """List all active academic groups."""
        stmt = select(AcademicGroupModel).where(AcademicGroupModel.is_active == True).order_by(AcademicGroupModel.group_number)
        group_models = self._db.execute(stmt).scalars().all()
        return [self._map_to_entity(gm) for gm in group_models]

    async def list_all(self) -> List[AcademicGroup]:
        """List all academic groups."""
        stmt = select(AcademicGroupModel).order_by(AcademicGroupModel.group_number)
        group_models = self._db.execute(stmt).scalars().all()
        return [self._map_to_entity(gm) for gm in group_models]

    def _map_to_entity(self, model: AcademicGroupModel) -> AcademicGroup:
        """Map SQLAlchemy model to domain entity."""
        if not model:
            return None
        return AcademicGroup(
            id=model.id,
            group_number=model.group_number,
            program_id=model.program_id,
            start_date=model.start_date,
            end_date=model.end_date,
            max_students=model.max_students,
            current_students=model.current_students,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
