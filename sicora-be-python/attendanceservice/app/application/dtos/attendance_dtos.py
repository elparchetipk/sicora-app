from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from uuid import UUID

from ...domain.value_objects import AttendanceStatus


@dataclass
class RegisterAttendanceRequest:
    """DTO para registrar asistencia (HU-BE-021)."""
    student_id: UUID
    ficha_id: UUID
    block_identifier: str
    qr_code: str
    notes: Optional[str] = None


@dataclass
class RegisterAttendanceResponse:
    """DTO de respuesta para registro de asistencia."""
    id: UUID
    student_id: UUID
    instructor_id: UUID
    ficha_id: UUID
    date: date
    block_identifier: str
    status: AttendanceStatus
    qr_code_used: str
    notes: Optional[str]
    recorded_at: datetime
    message: str


@dataclass
class AttendanceSummaryRequest:
    """DTO para solicitar resumen de asistencia (HU-BE-022)."""
    student_id: Optional[UUID] = None
    ficha_id: Optional[UUID] = None
    instructor_id: Optional[UUID] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


@dataclass
class AttendanceSummaryResponse:
    """DTO de respuesta para resumen de asistencia."""
    total_sessions: int
    present_count: int
    absent_count: int
    justified_count: int
    attendance_percentage: float
    student_details: Optional[dict] = None  # Para aprendices específicos
    top_absent_students: Optional[list] = None  # Para instructores/admins


@dataclass
class AttendanceHistoryRequest:
    """DTO para solicitar historial de asistencia (HU-BE-023)."""
    student_id: Optional[UUID] = None
    ficha_id: Optional[UUID] = None
    instructor_id: Optional[UUID] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[AttendanceStatus] = None
    page: int = 1
    page_size: int = 50


@dataclass
class AttendanceHistoryRecord:
    """DTO para un registro individual en el historial."""
    id: UUID
    student_id: UUID
    student_name: str
    instructor_id: UUID
    instructor_name: str
    ficha_id: UUID
    ficha_name: str
    date: date
    block_identifier: str
    status: AttendanceStatus
    notes: Optional[str]
    recorded_at: datetime


@dataclass
class AttendanceHistoryResponse:
    """DTO de respuesta para historial de asistencia."""
    records: list[AttendanceHistoryRecord]
    total_records: int
    page: int
    page_size: int
    total_pages: int
