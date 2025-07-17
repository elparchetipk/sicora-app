"""Individual model files for better organization."""

from .schedule_model import ScheduleModel
from .academic_program_model import AcademicProgramModel
from .academic_group_model import AcademicGroupModel
from .venue_model import VenueModel

__all__ = [
    "ScheduleModel",
    "AcademicProgramModel",
    "AcademicGroupModel",
    "VenueModel",
]
