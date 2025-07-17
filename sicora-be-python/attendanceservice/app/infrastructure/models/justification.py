from sqlalchemy import Column, String, Text, DateTime, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
import enum

from .base import BaseModel


class JustificationStatusEnum(enum.Enum):
    """Enum para estados de justificación."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class JustificationModel(BaseModel):
    """Modelo SQLAlchemy para justificaciones de inasistencia."""
    
    __tablename__ = "justifications"
    
    # Campos principales
    student_id = Column(UUID(as_uuid=True), nullable=False)
    attendance_record_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attendanceservice_schema.attendance_records.id", ondelete="CASCADE"),
        nullable=False,
        unique=True  # Una justificación por registro de asistencia
    )
    
    # Contenido de la justificación
    reason = Column(Text, nullable=False)
    file_path = Column(String(500), nullable=False)
    
    # Estado y fechas
    status = Column(
        ENUM(JustificationStatusEnum, name="justification_status"),
        default=JustificationStatusEnum.PENDING,
        nullable=False
    )
    submitted_at = Column(DateTime(timezone=True), nullable=False)
    
    # Campos de revisión
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    reviewed_by = Column(UUID(as_uuid=True), nullable=True)
    review_comments = Column(Text, nullable=True)
    
    # Relación con el registro de asistencia
    attendance_record = relationship(
        "AttendanceRecordModel",
        back_populates="justification"
    )
    
    # Índices para optimizar consultas
    __table_args__ = (
        # Índice para consultas por estudiante
        Index(
            "idx_justification_student",
            "student_id"
        ),
        # Índice para consultas por estado
        Index(
            "idx_justification_status",
            "status"
        ),
        # Índice para justificaciones pendientes por fecha
        Index(
            "idx_justification_pending_date",
            "status", "submitted_at"
        ),
        # Índice para consultas por revisor
        Index(
            "idx_justification_reviewer",
            "reviewed_by"
        ),
        # Índice compuesto para consultas frecuentes
        Index(
            "idx_justification_student_status",
            "student_id", "status"
        ),
        {"schema": "attendanceservice_schema"}
    )
    
    def __repr__(self):
        return (
            f"<Justification(id={self.id}, student_id={self.student_id}, "
            f"status={self.status.value})>"
        )
