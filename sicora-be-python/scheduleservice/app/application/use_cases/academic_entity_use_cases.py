"""Academic entity management use cases."""

from typing import List
from uuid import UUID

from ..dtos.schedule_dtos import (
    CreateAcademicProgramDTO,
    UpdateAcademicProgramDTO,
    AcademicProgramResponseDTO,
    CreateAcademicGroupDTO,
    UpdateAcademicGroupDTO,
    AcademicGroupResponseDTO,
    CreateVenueDTO,
    UpdateVenueDTO,
    VenueResponseDTO,
)
from ...domain.repositories.academic_program_repository_interface import AcademicProgramRepositoryInterface
from ...domain.repositories.academic_group_repository_interface import AcademicGroupRepositoryInterface
from ...domain.repositories.venue_repository_interface import VenueRepositoryInterface
from ...domain.entities.academic_program_entity import AcademicProgram
from ...domain.entities.academic_group_entity import AcademicGroup
from ...domain.entities.venue_entity import Venue
from ...domain.value_objects.program_type import ProgramType
from ...domain.exceptions.schedule_exceptions import (
    AcademicProgramNotFoundError,
    AcademicGroupNotFoundError,
    VenueNotFoundError,
    DuplicateEntityError,
)


# Academic Program Use Cases
class CreateAcademicProgramUseCase:
    """Use case for creating academic programs."""
    
    def __init__(self, program_repository: AcademicProgramRepositoryInterface):
        self._program_repository = program_repository
    
    async def execute(self, program_data: CreateAcademicProgramDTO) -> AcademicProgramResponseDTO:
        """Create a new academic program."""
        # Check for duplicate code
        existing = await self._program_repository.get_by_code(program_data.code)
        if existing:
            raise DuplicateEntityError("Academic Program", "code", program_data.code)
        
        # Create program entity
        program_type = ProgramType.from_string(program_data.program_type)
        program = AcademicProgram(
            name=program_data.name,
            code=program_data.code,
            program_type=program_type,
            duration_months=program_data.duration_months,
            description=program_data.description,
        )
        
        # Save program
        created_program = await self._program_repository.create(program)
        
        return AcademicProgramResponseDTO(
            id=created_program.id,
            name=created_program.name,
            code=created_program.code,
            program_type=created_program.program_type.value,
            duration_months=created_program.duration_months,
            description=created_program.description,
            is_active=created_program.is_active,
            created_at=created_program.created_at.date(),
            updated_at=created_program.updated_at.date(),
        )


class ListAcademicProgramsUseCase:
    """Use case for listing academic programs."""
    
    def __init__(self, program_repository: AcademicProgramRepositoryInterface):
        self._program_repository = program_repository
    
    async def execute(self, active_only: bool = True) -> List[AcademicProgramResponseDTO]:
        """List academic programs."""
        if active_only:
            programs = await self._program_repository.list_active()
        else:
            programs = await self._program_repository.list_all()
        
        return [
            AcademicProgramResponseDTO(
                id=program.id,
                name=program.name,
                code=program.code,
                program_type=program.program_type.value,
                duration_months=program.duration_months,
                description=program.description,
                is_active=program.is_active,
                created_at=program.created_at.date(),
                updated_at=program.updated_at.date(),
            )
            for program in programs
        ]


# Academic Group Use Cases
class CreateAcademicGroupUseCase:
    """Use case for creating academic groups."""
    
    def __init__(
        self,
        group_repository: AcademicGroupRepositoryInterface,
        program_repository: AcademicProgramRepositoryInterface,
    ):
        self._group_repository = group_repository
        self._program_repository = program_repository
    
    async def execute(self, group_data: CreateAcademicGroupDTO) -> AcademicGroupResponseDTO:
        """Create a new academic group."""
        # Validate program exists
        program = await self._program_repository.get_by_id(group_data.program_id)
        if not program or not program.is_active:
            raise AcademicProgramNotFoundError("id", str(group_data.program_id))
        
        # Check for duplicate group number
        existing = await self._group_repository.get_by_group_number(group_data.group_number)
        if existing:
            raise DuplicateEntityError("Academic Group", "group_number", group_data.group_number)
        
        # Create group entity
        group = AcademicGroup(
            group_number=group_data.group_number,
            program_id=group_data.program_id,
            start_date=group_data.start_date,
            end_date=group_data.end_date,
            max_students=group_data.max_students,
        )
        
        # Save group
        created_group = await self._group_repository.create(group)
        
        return AcademicGroupResponseDTO(
            id=created_group.id,
            group_number=created_group.group_number,
            program_id=created_group.program_id,
            start_date=created_group.start_date,
            end_date=created_group.end_date,
            max_students=created_group.max_students,
            current_students=created_group.current_students,
            is_active=created_group.is_active,
            created_at=created_group.created_at.date(),
            updated_at=created_group.updated_at.date(),
        )


class ListAcademicGroupsUseCase:
    """Use case for listing academic groups."""
    
    def __init__(self, group_repository: AcademicGroupRepositoryInterface):
        self._group_repository = group_repository
    
    async def execute(self, program_id: UUID = None, active_only: bool = True) -> List[AcademicGroupResponseDTO]:
        """List academic groups."""
        if program_id:
            groups = await self._group_repository.get_by_program(program_id)
            if active_only:
                groups = [g for g in groups if g.is_active]
        elif active_only:
            groups = await self._group_repository.list_active()
        else:
            groups = await self._group_repository.list_all()
        
        return [
            AcademicGroupResponseDTO(
                id=group.id,
                group_number=group.group_number,
                program_id=group.program_id,
                start_date=group.start_date,
                end_date=group.end_date,
                max_students=group.max_students,
                current_students=group.current_students,
                is_active=group.is_active,
                created_at=group.created_at.date(),
                updated_at=group.updated_at.date(),
            )
            for group in groups
        ]


# Venue Use Cases
class CreateVenueUseCase:
    """Use case for creating venues."""
    
    def __init__(self, venue_repository: VenueRepositoryInterface):
        self._venue_repository = venue_repository
    
    async def execute(self, venue_data: CreateVenueDTO) -> VenueResponseDTO:
        """Create a new venue."""
        # Check for duplicate code
        existing = await self._venue_repository.get_by_code(venue_data.code)
        if existing:
            raise DuplicateEntityError("Venue", "code", venue_data.code)
        
        # Create venue entity
        venue = Venue(
            name=venue_data.name,
            code=venue_data.code,
            capacity=venue_data.capacity,
            venue_type=venue_data.venue_type,
            building=venue_data.building,
            floor=venue_data.floor,
            campus_id=venue_data.campus_id,
            description=venue_data.description,
            equipment=venue_data.equipment,
        )
        
        # Save venue
        created_venue = await self._venue_repository.create(venue)
        
        return VenueResponseDTO(
            id=created_venue.id,
            name=created_venue.name,
            code=created_venue.code,
            capacity=created_venue.capacity,
            venue_type=created_venue.venue_type,
            building=created_venue.building,
            floor=created_venue.floor,
            campus_id=created_venue.campus_id,
            description=created_venue.description,
            equipment=created_venue.equipment,
            is_active=created_venue.is_active,
            created_at=created_venue.created_at.date(),
            updated_at=created_venue.updated_at.date(),
        )


class ListVenuesUseCase:
    """Use case for listing venues."""
    
    def __init__(self, venue_repository: VenueRepositoryInterface):
        self._venue_repository = venue_repository
    
    async def execute(self, campus_id: UUID = None, active_only: bool = True) -> List[VenueResponseDTO]:
        """List venues."""
        if campus_id:
            venues = await self._venue_repository.get_by_campus(campus_id)
            if active_only:
                venues = [v for v in venues if v.is_active]
        elif active_only:
            venues = await self._venue_repository.list_active()
        else:
            venues = await self._venue_repository.list_all()
        
        return [
            VenueResponseDTO(
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
                created_at=venue.created_at.date(),
                updated_at=venue.updated_at.date(),
            )
            for venue in venues
        ]
