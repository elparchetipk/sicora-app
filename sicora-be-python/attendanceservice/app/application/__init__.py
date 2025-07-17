"""
Capa de aplicación del AttendanceService.

Esta capa contiene los casos de uso, DTOs e interfaces que coordinan
la lógica de negocio para el control de asistencia siguiendo Clean Architecture.
"""

from .use_cases import (
    RegisterAttendanceUseCase,
    GetAttendanceSummaryUseCase,
    GetAttendanceHistoryUseCase,
    UploadJustificationUseCase,
    ReviewJustificationUseCase,
    GetJustificationsUseCase,
    GetAttendanceAlertsUseCase,
    GetInstructorNoAttendanceAlertsUseCase,
    AcknowledgeAlertUseCase
)

from .dtos import (
    # Attendance DTOs
    RegisterAttendanceRequest,
    RegisterAttendanceResponse,
    AttendanceSummaryRequest,
    AttendanceSummaryResponse,
    AttendanceHistoryRequest,
    AttendanceHistoryRecord,
    AttendanceHistoryResponse,
    
    # Justification DTOs
    UploadJustificationRequest,
    UploadJustificationResponse,
    ReviewJustificationRequest,
    ReviewJustificationResponse,
    JustificationDetail,
    GetJustificationsRequest,
    GetJustificationsResponse,
    
    # Alert DTOs
    GetAlertsRequest,
    AlertDetail,
    GetAlertsResponse,
    AcknowledgeAlertRequest,
    AcknowledgeAlertResponse,
    InstructorNoAttendanceAlert,
    GetInstructorNoAttendanceAlertsRequest,
    GetInstructorNoAttendanceAlertsResponse,
    AlertStatistics
)

from .interfaces import (
    FileUploadService,
    QRCodeService,
    UserServiceInterface,
    ScheduleServiceInterface
)

__all__ = [
    # Use Cases
    "RegisterAttendanceUseCase",
    "GetAttendanceSummaryUseCase", 
    "GetAttendanceHistoryUseCase",
    "UploadJustificationUseCase",
    "ReviewJustificationUseCase",
    "GetJustificationsUseCase",
    "GetAttendanceAlertsUseCase",
    "GetInstructorNoAttendanceAlertsUseCase",
    "AcknowledgeAlertUseCase",
    
    # DTOs
    "RegisterAttendanceRequest",
    "RegisterAttendanceResponse",
    "AttendanceSummaryRequest", 
    "AttendanceSummaryResponse",
    "AttendanceHistoryRequest",
    "AttendanceHistoryRecord",
    "AttendanceHistoryResponse",
    "UploadJustificationRequest",
    "UploadJustificationResponse",
    "ReviewJustificationRequest",
    "ReviewJustificationResponse",
    "JustificationDetail",
    "GetJustificationsRequest",
    "GetJustificationsResponse",
    "GetAlertsRequest",
    "AlertDetail",
    "GetAlertsResponse",
    "AcknowledgeAlertRequest",
    "AcknowledgeAlertResponse",
    "InstructorNoAttendanceAlert",
    "GetInstructorNoAttendanceAlertsRequest",
    "GetInstructorNoAttendanceAlertsResponse",
    "AlertStatistics",
    
    # Service Interfaces
    "FileUploadService",
    "QRCodeService",
    "UserServiceInterface",
    "ScheduleServiceInterface"
]
