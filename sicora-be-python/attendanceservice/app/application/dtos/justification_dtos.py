from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

from ...domain.value_objects import JustificationStatus


@dataclass
class UploadJustificationRequest:
    """DTO para subir justificación (HU-BE-024)."""
    attendance_record_id: UUID
    reason: str
    file_content: bytes
    file_name: str
    file_size: int


@dataclass
class UploadJustificationResponse:
    """DTO de respuesta para subida de justificación."""
    id: UUID
    attendance_record_id: UUID
    student_id: UUID
    reason: str
    file_path: str
    status: JustificationStatus
    submitted_at: datetime
    message: str


@dataclass
class ReviewJustificationRequest:
    """DTO para revisar justificación (HU-BE-025)."""
    justification_id: UUID
    action: str  # "approve" or "reject"
    comments: Optional[str] = None


@dataclass
class ReviewJustificationResponse:
    """DTO de respuesta para revisión de justificación."""
    id: UUID
    attendance_record_id: UUID
    student_id: UUID
    status: JustificationStatus
    reviewed_by: UUID
    reviewed_at: datetime
    review_comments: Optional[str]
    attendance_updated: bool
    message: str


@dataclass
class JustificationDetail:
    """DTO para detalles de una justificación."""
    id: UUID
    attendance_record_id: UUID
    student_id: UUID
    student_name: str
    ficha_id: UUID
    ficha_name: str
    absence_date: datetime
    block_identifier: str
    reason: str
    file_path: str
    status: JustificationStatus
    submitted_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[UUID] = None
    reviewed_by_name: Optional[str] = None
    review_comments: Optional[str] = None
    days_since_submission: int = 0


@dataclass
class GetJustificationsRequest:
    """DTO para obtener lista de justificaciones."""
    student_id: Optional[UUID] = None
    instructor_id: Optional[UUID] = None
    status: Optional[JustificationStatus] = None
    ficha_id: Optional[UUID] = None
    page: int = 1
    page_size: int = 20


@dataclass
class GetJustificationsResponse:
    """DTO de respuesta para lista de justificaciones."""
    justifications: list[JustificationDetail]
    total_justifications: int
    pending_count: int
    approved_count: int
    rejected_count: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class DeleteJustificationRequest:
    """DTO para eliminar justificación."""
    justification_id: UUID
    user_id: UUID


@dataclass
class DeleteJustificationResponse:
    """DTO de respuesta para eliminación de justificación."""
    success: bool
    message: str
    details: Optional[Dict[str, Any]] = None
