from sqlalchemy import Column, String, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
import enum

from .base import BaseModel


class AttendanceStatusEnum(enum.Enum):
    """Enum para estados de asistencia."""
    PRESENT = "present"
    ABSENT = "absent"
    JUSTIFIED = "justified"
    LATE = "late"


class AttendanceRecordModel(BaseModel):
    """Modelo SQLAlchemy para registros de asistencia."""
    
    __tablename__ = "attendance_records"
    
    # Campos principales
    student_id = Column(UUID(as_uuid=True), nullable=False)
    schedule_id = Column(UUID(as_uuid=True), nullable=False)
    instructor_id = Column(UUID(as_uuid=True), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    block_identifier = Column(String(50), nullable=False)
    venue_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Estado y detalles
    status = Column(
        ENUM(AttendanceStatusEnum, name="attendance_status"),
        default=AttendanceStatusEnum.ABSENT,
        nullable=False
    )
    
    qr_code_used = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    recorded_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relación con justificación
    justification = relationship(
        "JustificationModel",
        back_populates="attendance_record",
        uselist=False,  # Una justificación por registro
        cascade="all, delete-orphan"
    )
    
    # Índices para optimizar consultas frecuentes
    __table_args__ = (
        # Índice único para evitar duplicados por estudiante, fecha y bloque
        Index(
            "idx_attendance_unique_student_date_block",
            "student_id", "date", "block_identifier",
            unique=True
        ),
        # Índice para consultas por estudiante y período
        Index(
            "idx_attendance_student_date",
            "student_id", "date"
        ),
        # Índice para consultas por instructor y fecha
        Index(
            "idx_attendance_instructor_date",
            "instructor_id", "date"
        ),
        # Índice para consultas por horario
        Index(
            "idx_attendance_schedule",
            "schedule_id"
        ),
        # Índice para consultas por estado
        Index(
            "idx_attendance_status",
            "status"
        ),
        # Índice compuesto para consultas frecuentes de resumen
        Index(
            "idx_attendance_summary",
            "student_id", "status", "date"
        ),
        {"schema": "attendanceservice_schema"}
    )
    
    def __repr__(self):
        return (
            f"<AttendanceRecord(id={self.id}, student_id={self.student_id}, "
            f"date={self.date}, status={self.status.value})>"
        )
