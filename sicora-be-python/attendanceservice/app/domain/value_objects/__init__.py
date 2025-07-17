from enum import Enum


class AttendanceStatus(Enum):
    """Estados posibles de un registro de asistencia."""
    PRESENT = "present"
    ABSENT = "absent" 
    JUSTIFIED = "justified"
    LATE = "late"


class JustificationStatus(Enum):
    """Estados posibles de una justificación."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class AlertLevel(Enum):
    """Niveles de criticidad de las alertas."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertType(Enum):
    """Tipos de alertas de asistencia."""
    CONSECUTIVE_ABSENCES = "consecutive_absences"
    LOW_ATTENDANCE = "low_attendance"
    DESERTION_RISK = "desertion_risk"
    PATTERN_ANOMALY = "pattern_anomaly"
    INSTRUCTOR_NO_RECORD = "instructor_no_record"
