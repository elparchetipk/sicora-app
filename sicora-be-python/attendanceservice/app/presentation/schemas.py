"""
Esquemas Pydantic para validación de entrada y salida de la API
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


# Enums para esquemas
class AttendanceStatusSchema(str, Enum):
    """Esquema para el estado de asistencia"""
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    LATE = "LATE"
    EXCUSED = "EXCUSED"


class JustificationStatusSchema(str, Enum):
    """Esquema para el estado de justificación"""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class AlertTypeSchema(str, Enum):
    """Esquema para el tipo de alerta"""
    CONSECUTIVE_ABSENCES = "CONSECUTIVE_ABSENCES"
    LOW_ATTENDANCE = "LOW_ATTENDANCE"
    FREQUENT_LATE = "FREQUENT_LATE"
    NO_INSTRUCTOR_ATTENDANCE = "NO_INSTRUCTOR_ATTENDANCE"


class AlertLevelSchema(str, Enum):
    """Esquema para el nivel de alerta"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# Esquemas base
class BaseSchema(BaseModel):
    """Esquema base con configuración común"""
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        str_strip_whitespace=True
    )


# Esquemas de solicitud
class RegisterAttendanceRequest(BaseSchema):
    """Esquema para registrar asistencia"""
    qr_code: str = Field(..., description="Código QR escaneado")
    student_id: UUID = Field(..., description="ID del estudiante")
    location: Optional[str] = Field(None, description="Ubicación opcional")


class UploadJustificationRequest(BaseSchema):
    """Esquema para subir justificación"""
    attendance_record_id: UUID = Field(..., description="ID del registro de asistencia")
    reason: str = Field(..., min_length=10, max_length=1000, description="Motivo de la justificación")
    justification_type: str = Field(..., description="Tipo de justificación")


class ReviewJustificationRequest(BaseSchema):
    """Esquema para revisar justificación"""
    status: JustificationStatusSchema = Field(..., description="Estado de la revisión")
    review_notes: Optional[str] = Field(None, max_length=1000, description="Notas de la revisión")


class GetAttendanceHistoryRequest(BaseSchema):
    """Esquema para obtener historial de asistencia"""
    start_date: Optional[date] = Field(None, description="Fecha de inicio")
    end_date: Optional[date] = Field(None, description="Fecha de fin")
    status: Optional[AttendanceStatusSchema] = Field(None, description="Filtro por estado")
    page: int = Field(1, ge=1, description="Número de página")
    page_size: int = Field(20, ge=1, le=100, description="Tamaño de página")


class GetJustificationsRequest(BaseSchema):
    """Esquema para obtener justificaciones"""
    status: Optional[JustificationStatusSchema] = Field(None, description="Filtro por estado")
    start_date: Optional[date] = Field(None, description="Fecha de inicio")
    end_date: Optional[date] = Field(None, description="Fecha de fin")
    page: int = Field(1, ge=1, description="Número de página")
    page_size: int = Field(20, ge=1, le=100, description="Tamaño de página")


class GetAlertsRequest(BaseSchema):
    """Esquema para obtener alertas"""
    level: Optional[AlertLevelSchema] = Field(None, description="Filtro por nivel")
    alert_type: Optional[AlertTypeSchema] = Field(None, description="Filtro por tipo")
    include_acknowledged: bool = Field(False, description="Incluir alertas reconocidas")
    page: int = Field(1, ge=1, description="Número de página")
    page_size: int = Field(20, ge=1, le=100, description="Tamaño de página")


# Esquemas de respuesta
class AttendanceRecordResponse(BaseSchema):
    """Esquema de respuesta para registro de asistencia"""
    id: UUID
    student_id: UUID
    student_name: str
    ficha_id: UUID
    ficha_name: str
    class_id: Optional[UUID] = None
    class_name: Optional[str] = None
    status: AttendanceStatusSchema
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    date: date
    late_minutes: Optional[int] = None
    notes: Optional[str] = None
    is_justified: bool
    created_at: datetime
    updated_at: datetime


class RegisterAttendanceResponse(BaseSchema):
    """Esquema de respuesta para registro de asistencia"""
    success: bool
    message: str
    attendance_record: Optional[AttendanceRecordResponse] = None


class AttendanceSummaryResponse(BaseSchema):
    """Esquema de respuesta para resumen de asistencia"""
    student_id: UUID
    student_name: str
    ficha_id: UUID
    ficha_name: str
    total_classes: int
    present_count: int
    absent_count: int
    late_count: int
    excused_count: int
    attendance_percentage: float
    consecutive_absences: int
    period_start: date
    period_end: date


class AttendanceHistoryResponse(BaseSchema):
    """Esquema de respuesta para historial de asistencia"""
    records: List[AttendanceRecordResponse]
    total_records: int
    current_page: int
    page_size: int
    total_pages: int


class JustificationResponse(BaseSchema):
    """Esquema de respuesta para justificación"""
    id: UUID
    attendance_record_id: UUID
    student_id: UUID
    student_name: str
    reason: str
    justification_type: str
    document_path: Optional[str] = None
    document_name: Optional[str] = None
    status: JustificationStatusSchema
    reviewed_by: Optional[UUID] = None
    reviewed_by_name: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    review_notes: Optional[str] = None
    submitted_at: datetime
    created_at: datetime
    updated_at: datetime


class UploadJustificationResponse(BaseSchema):
    """Esquema de respuesta para subir justificación"""
    success: bool
    message: str
    justification: Optional[JustificationResponse] = None


class ReviewJustificationResponse(BaseSchema):
    """Esquema de respuesta para revisar justificación"""
    success: bool
    message: str
    justification: JustificationResponse


class GetJustificationsResponse(BaseSchema):
    """Esquema de respuesta para obtener justificaciones"""
    justifications: List[JustificationResponse]
    total_justifications: int
    pending_count: int
    approved_count: int
    rejected_count: int
    current_page: int
    page_size: int
    total_pages: int


class AlertResponse(BaseSchema):
    """Esquema de respuesta para alerta"""
    id: UUID
    student_id: UUID
    student_name: str
    ficha_id: UUID
    ficha_name: str
    alert_type: AlertTypeSchema
    level: AlertLevelSchema
    message: str
    data: Dict[str, Any]
    is_active: bool
    acknowledged: bool
    acknowledged_by: Optional[UUID] = None
    acknowledged_by_name: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    created_at: datetime
    days_since_creation: int
    recommended_actions: List[str]


class GetAlertsResponse(BaseSchema):
    """Esquema de respuesta para obtener alertas"""
    alerts: List[AlertResponse]
    total_alerts: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    current_page: int
    page_size: int
    total_pages: int


class AcknowledgeAlertResponse(BaseSchema):
    """Esquema de respuesta para reconocer alerta"""
    success: bool
    message: str
    alert: AlertResponse


class QRCodeResponse(BaseSchema):
    """Esquema de respuesta para código QR"""
    qr_code: str = Field(..., description="Código QR generado")
    expires_at: datetime = Field(..., description="Fecha de expiración")
    class_id: UUID = Field(..., description="ID de la clase")
    class_name: str = Field(..., description="Nombre de la clase")


class ErrorResponse(BaseSchema):
    """Esquema de respuesta para errores"""
    error: bool = True
    message: str
    details: Optional[Dict[str, Any]] = None
    error_code: Optional[str] = None


class SuccessResponse(BaseSchema):
    """Esquema de respuesta genérico de éxito"""
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None
