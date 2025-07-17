"""Repository interfaces for the Schedule domain."""

from .schedule_repository_interface import ScheduleRepositoryInterface
from .academic_program_repository_interface import AcademicProgramRepositoryInterface
from .academic_group_repository_interface import AcademicGroupRepositoryInterface
from .venue_repository_interface import VenueRepositoryInterface

__all__ = [
    "ScheduleRepositoryInterface",
    "AcademicProgramRepositoryInterface",
    "AcademicGroupRepositoryInterface", 
    "VenueRepositoryInterface",
]
