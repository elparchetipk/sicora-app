from sqlalchemy import Column, String, Text, Boolean, DateTime, Index, JSON
from sqlalchemy.dialects.postgresql import UUID, ENUM
import enum

from .base import BaseModel


class AlertLevelEnum(enum.Enum):
    """Enum para niveles de criticidad de alertas."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertTypeEnum(enum.Enum):
    """Enum para tipos de alertas."""
    CONSECUTIVE_ABSENCES = "consecutive_absences"
    LOW_ATTENDANCE = "low_attendance"
    DESERTION_RISK = "desertion_risk"
    PATTERN_ANOMALY = "pattern_anomaly"
    INSTRUCTOR_NO_RECORD = "instructor_no_record"


class AttendanceAlertModel(BaseModel):
    """Modelo SQLAlchemy para alertas de asistencia."""
    
    __tablename__ = "attendance_alerts"
    
    # Campos principales
    student_id = Column(UUID(as_uuid=True), nullable=False)
    ficha_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Tipo y nivel de alerta
    alert_type = Column(
        ENUM(AlertTypeEnum, name="alert_type"),
        nullable=False
    )
    level = Column(
        ENUM(AlertLevelEnum, name="alert_level"),
        nullable=False
    )
    
    # Contenido de la alerta
    message = Column(Text, nullable=False)
    data = Column(JSON, nullable=False, default=dict)  # Datos específicos de la alerta
    
    # Estado de la alerta
    is_active = Column(Boolean, default=True, nullable=False)
    acknowledged = Column(Boolean, default=False, nullable=False)
    acknowledged_by = Column(UUID(as_uuid=True), nullable=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    
    # Índices para optimizar consultas
    __table_args__ = (
        # Índice para consultas por estudiante
        Index(
            "idx_alert_student",
            "student_id"
        ),
        # Índice para consultas por ficha
        Index(
            "idx_alert_ficha",
            "ficha_id"
        ),
        # Índice para alertas activas
        Index(
            "idx_alert_active",
            "is_active"
        ),
        # Índice para alertas no reconocidas
        Index(
            "idx_alert_unacknowledged",
            "acknowledged", "is_active"
        ),
        # Índice por nivel de criticidad
        Index(
            "idx_alert_level",
            "level", "is_active"
        ),
        # Índice por tipo de alerta
        Index(
            "idx_alert_type",
            "alert_type", "is_active"
        ),
        # Índice compuesto para consultas frecuentes
        Index(
            "idx_alert_student_active",
            "student_id", "is_active", "acknowledged"
        ),
        # Índice para alertas críticas
        Index(
            "idx_alert_critical",
            "level", "is_active", "acknowledged"
        ),
        # Índice por fecha de creación para alertas vencidas
        Index(
            "idx_alert_created_date",
            "created_at", "acknowledged"
        ),
        {"schema": "attendanceservice_schema"}
    )
    
    def __repr__(self):
        return (
            f"<AttendanceAlert(id={self.id}, student_id={self.student_id}, "
            f"type={self.alert_type.value}, level={self.level.value})>"
        )
