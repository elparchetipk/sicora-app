"""Domain entities for the Schedule service."""

from .schedule_entity import Schedule
from .academic_program_entity import AcademicProgram
from .academic_group_entity import AcademicGroup
from .venue_entity import Venue

__all__ = [
    "Schedule",
    "AcademicProgram", 
    "AcademicGroup",
    "Venue",
]
