"""
Dominio del AttendanceService.

Este módulo contiene las entidades, value objects, repositorios y excepciones
del dominio de control de asistencia siguiendo los principios de Clean Architecture.
"""

from .entities import AttendanceRecord, Justification, AttendanceAlert
from .value_objects import AttendanceStatus, JustificationStatus, AlertLevel, AlertType
from .repositories import (
    AttendanceRecordRepository, 
    JustificationRepository, 
    AttendanceAlertRepository
)
from .exceptions import (
    AttendanceError,
    AttendanceNotFoundError,
    DuplicateAttendanceError,
    InvalidAttendanceStatusError,
    AttendanceUpdateNotAllowedError,
    InvalidQRCodeError,
    JustificationError,
    JustificationNotFoundError,
    InvalidJustificationFileError,
    JustificationAlreadyProcessedError,
    AlertError,
    AlertNotFoundError,
    UnauthorizedAccessError,
    InstructorNotAssignedError,
    StudentNotInFichaError,
    FutureDateNotAllowedError,
    ExternalServiceError
)

__all__ = [
    # Entities
    "AttendanceRecord",
    "Justification", 
    "AttendanceAlert",
    
    # Value Objects
    "AttendanceStatus",
    "JustificationStatus",
    "AlertLevel",
    "AlertType",
    
    # Repository Interfaces
    "AttendanceRecordRepository",
    "JustificationRepository",
    "AttendanceAlertRepository",
    
    # Exceptions
    "AttendanceError",
    "AttendanceNotFoundError",
    "DuplicateAttendanceError",
    "InvalidAttendanceStatusError", 
    "AttendanceUpdateNotAllowedError",
    "InvalidQRCodeError",
    "JustificationError",
    "JustificationNotFoundError",
    "InvalidJustificationFileError",
    "JustificationAlreadyProcessedError",
    "AlertError",
    "AlertNotFoundError",
    "UnauthorizedAccessError",
    "InstructorNotAssignedError",
    "StudentNotInFichaError",
    "FutureDateNotAllowedError",
    "ExternalServiceError"
]
