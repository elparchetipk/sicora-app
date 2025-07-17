"""SQLAlchemy implementation of the Academic Program Repository."""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select

from ...domain.entities.academic_program_entity import AcademicProgram
from ...domain.repositories.academic_program_repository_interface import AcademicProgramRepositoryInterface
from ...domain.value_objects.program_type import ProgramType
from ..config.models import AcademicProgramModel


class AcademicProgramRepositorySQLAlchemy(AcademicProgramRepositoryInterface):
    """SQLAlchemy implementation of the academic program repository."""

    def __init__(self, db_session: Session):
        self._db = db_session

    async def create(self, program: AcademicProgram) -> AcademicProgram:
        """Create a new academic program."""
        program_model = AcademicProgramModel(
            id=program.id,
            name=program.name,
            code=program.code,
            program_type=program.program_type.value,
            duration_months=program.duration_months,
            description=program.description,
            is_active=program.is_active,
            created_at=program.created_at,
            updated_at=program.updated_at,
        )
        self._db.add(program_model)
        self._db.commit()
        self._db.refresh(program_model)
        return self._map_to_entity(program_model)

    async def get_by_id(self, program_id: UUID) -> Optional[AcademicProgram]:
        """Get academic program by ID."""
        stmt = select(AcademicProgramModel).where(AcademicProgramModel.id == program_id)
        program_model = self._db.execute(stmt).scalar_one_or_none()
        return self._map_to_entity(program_model) if program_model else None

    async def get_by_code(self, code: str) -> Optional[AcademicProgram]:
        """Get academic program by code."""
        stmt = select(AcademicProgramModel).where(AcademicProgramModel.code == code)
        program_model = self._db.execute(stmt).scalar_one_or_none()
        return self._map_to_entity(program_model) if program_model else None

    async def update(self, program: AcademicProgram) -> AcademicProgram:
        """Update an existing academic program."""
        stmt = select(AcademicProgramModel).where(AcademicProgramModel.id == program.id)
        program_model = self._db.execute(stmt).scalar_one_or_none()

        if not program_model:
            return None # Or raise an exception

        program_model.name = program.name
        program_model.description = program.description
        program_model.duration_months = program.duration_months
        program_model.is_active = program.is_active
        program_model.program_type = program.program_type.value # Ensure this is updated
        program_model.updated_at = datetime.now()

        self._db.commit()
        self._db.refresh(program_model)
        return self._map_to_entity(program_model)

    async def delete(self, program_id: UUID) -> bool:
        """Delete an academic program."""
        stmt = select(AcademicProgramModel).where(AcademicProgramModel.id == program_id)
        program_model = self._db.execute(stmt).scalar_one_or_none()
        if program_model:
            self._db.delete(program_model)
            self._db.commit()
            return True
        return False

    async def list_active(self) -> List[AcademicProgram]:
        """List all active academic programs."""
        stmt = select(AcademicProgramModel).where(AcademicProgramModel.is_active == True).order_by(AcademicProgramModel.name)
        program_models = self._db.execute(stmt).scalars().all()
        return [self._map_to_entity(pm) for pm in program_models]

    async def list_all(self) -> List[AcademicProgram]:
        """List all academic programs."""
        stmt = select(AcademicProgramModel).order_by(AcademicProgramModel.name)
        program_models = self._db.execute(stmt).scalars().all()
        return [self._map_to_entity(pm) for pm in program_models]

    def _map_to_entity(self, model: AcademicProgramModel) -> AcademicProgram:
        """Map SQLAlchemy model to domain entity."""
        if not model:
            return None
        return AcademicProgram(
            id=model.id,
            name=model.name,
            code=model.code,
            program_type=ProgramType(model.program_type),
            duration_months=model.duration_months,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
