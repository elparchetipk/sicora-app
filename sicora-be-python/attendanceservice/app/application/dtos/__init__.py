from .attendance_dtos import (
    RegisterAttendanceRequest,
    RegisterAttendanceResponse,
    AttendanceSummaryRequest,
    AttendanceSummaryResponse,
    AttendanceHistoryRequest,
    AttendanceHistoryRecord,
    AttendanceHistoryResponse
)

from .justification_dtos import (
    UploadJustificationRequest,
    UploadJustificationResponse,
    ReviewJustificationRequest,
    ReviewJustificationResponse,
    JustificationDetail,
    GetJustificationsRequest,
    GetJustificationsResponse,
    DeleteJustificationRequest,
    DeleteJustificationResponse
)

from .alert_dtos import (
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

__all__ = [
    # Attendance DTOs
    "RegisterAttendanceRequest",
    "RegisterAttendanceResponse",
    "AttendanceSummaryRequest",
    "AttendanceSummaryResponse",
    "AttendanceHistoryRequest",
    "AttendanceHistoryRecord",
    "AttendanceHistoryResponse",
    
    # Justification DTOs
    "UploadJustificationRequest",
    "UploadJustificationResponse",
    "ReviewJustificationRequest",
    "ReviewJustificationResponse",
    "JustificationDetail",
    "GetJustificationsRequest",
    "GetJustificationsResponse",
    "DeleteJustificationRequest",
    "DeleteJustificationResponse",
    
    # Alert DTOs
    "GetAlertsRequest",
    "AlertDetail",
    "GetAlertsResponse",
    "AcknowledgeAlertRequest",
    "AcknowledgeAlertResponse",
    "InstructorNoAttendanceAlert",
    "GetInstructorNoAttendanceAlertsRequest",
    "GetInstructorNoAttendanceAlertsResponse",
    "AlertStatistics"
]
