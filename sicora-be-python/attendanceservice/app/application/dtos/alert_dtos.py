from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from uuid import UUID

from ...domain.value_objects import AlertLevel, AlertType


@dataclass
class GetAlertsRequest:
    """DTO para obtener alertas (HU-BE-026)."""
    student_id: Optional[UUID] = None
    ficha_id: Optional[UUID] = None
    instructor_id: Optional[UUID] = None
    level: Optional[AlertLevel] = None
    alert_type: Optional[AlertType] = None
    include_acknowledged: bool = False
    page: int = 1
    page_size: int = 20


@dataclass
class AlertDetail:
    """DTO para detalles de una alerta."""
    id: UUID
    student_id: UUID
    student_name: str
    ficha_id: UUID
    ficha_name: str
    alert_type: AlertType
    level: AlertLevel
    message: str
    data: Dict
    is_active: bool
    acknowledged: bool
    created_at: datetime
    days_since_creation: int
    recommended_actions: List[str]
    acknowledged_by: Optional[UUID] = None
    acknowledged_by_name: Optional[str] = None
    acknowledged_at: Optional[datetime] = None


@dataclass
class GetAlertsResponse:
    """DTO de respuesta para obtener alertas."""
    alerts: List[AlertDetail]
    total_alerts: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    unacknowledged_count: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class GetInstructorNoAttendanceAlertsRequest:
    """DTO para obtener alertas de instructores sin registro."""
    instructor_id: UUID
    date_filter: Optional[date] = None
    page: int = 1
    page_size: int = 20
    user_id: Optional[UUID] = None


@dataclass
class GetInstructorNoAttendanceAlertsResponse:
    """DTO de respuesta para alertas de instructores sin registro."""
    alerts: List[AlertDetail]
    total_alerts: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int


@dataclass
class AcknowledgeAlertRequest:
    """DTO para reconocer una alerta."""
    alert_id: UUID
    acknowledged_by: UUID


@dataclass
class AcknowledgeAlertResponse:
    """DTO de respuesta para reconocimiento de alerta."""
    success: bool
    message: str
    alert: AlertDetail


@dataclass
class InstructorNoAttendanceAlert:
    """DTO para alertas de instructores sin registro (HU-BE-027)."""
    instructor_id: UUID
    instructor_name: str
    ficha_id: UUID
    ficha_name: str
    block_identifier: str
    venue_name: str
    date: date
    start_time: str
    end_time: str
    sede_name: str
    programa_name: str


@dataclass
class AlertStatistics:
    """DTO para estadísticas de alertas."""
    total_alerts: int
    by_level: Dict[str, int]
    by_type: Dict[str, int]
    resolution_rate: float
    average_response_time: float  # en horas
    most_affected_fichas: List[Dict[str, Any]]
    trend_data: List[Dict[str, Any]]
