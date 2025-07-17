"""SQLAlchemy models for schedule service."""

from .base import Base
from .campus_model import CampusModel
from .academic_program_model import AcademicProgramModel
from .academic_group_model import AcademicGroupModel
from .venue_model import VenueModel
from .schedule_model import ScheduleModel

__all__ = [
  "Base",
  "CampusModel",
  "AcademicProgramModel", 
  "AcademicGroupModel",
  "VenueModel",
  "ScheduleModel",
]
