from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from ..value_objects import AlertLevel, AlertType


@dataclass
class AttendanceAlert:
    """
    Entidad de dominio que representa una alerta de asistencia.
    
    Las alertas identifican patrones problemáticos de asistencia como inasistencias
    consecutivas, bajo porcentaje de asistencia, o riesgo de deserción.
    """
    
    student_id: UUID
    ficha_id: UUID
    alert_type: AlertType
    level: AlertLevel
    message: str
    data: Dict
    id: UUID = field(default_factory=uuid4)
    is_active: bool = field(default=True)
    acknowledged: bool = field(default=False)
    acknowledged_by: Optional[UUID] = None
    acknowledged_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def create_consecutive_absences_alert(
        cls,
        student_id: UUID,
        ficha_id: UUID,
        consecutive_days: int,
        level: AlertLevel = AlertLevel.HIGH
    ) -> "AttendanceAlert":
        """
        Crea una alerta por inasistencias consecutivas.
        
        Args:
            student_id: ID del estudiante
            ficha_id: ID de la ficha
            consecutive_days: Número de días consecutivos de inasistencia
            level: Nivel de criticidad de la alerta
            
        Returns:
            Nueva instancia de AttendanceAlert
        """
        return cls(
            student_id=student_id,
            ficha_id=ficha_id,
            alert_type=AlertType.CONSECUTIVE_ABSENCES,
            level=level,
            message=f"Estudiante con {consecutive_days} inasistencias consecutivas",
            data={
                "consecutive_days": consecutive_days,
                "threshold": 3,
                "alert_reason": "consecutive_absences"
            }
        )

    @classmethod
    def create_low_attendance_alert(
        cls,
        student_id: UUID,
        ficha_id: UUID,
        attendance_percentage: float,
        period_days: int,
        level: AlertLevel = AlertLevel.MEDIUM
    ) -> "AttendanceAlert":
        """
        Crea una alerta por bajo porcentaje de asistencia.
        
        Args:
            student_id: ID del estudiante
            ficha_id: ID de la ficha
            attendance_percentage: Porcentaje actual de asistencia
            period_days: Días del período evaluado
            level: Nivel de criticidad de la alerta
            
        Returns:
            Nueva instancia de AttendanceAlert
        """
        return cls(
            student_id=student_id,
            ficha_id=ficha_id,
            alert_type=AlertType.LOW_ATTENDANCE,
            level=level,
            message=f"Estudiante con {attendance_percentage:.1f}% de asistencia en últimos {period_days} días",
            data={
                "attendance_percentage": attendance_percentage,
                "period_days": period_days,
                "threshold": 80.0,
                "alert_reason": "low_attendance"
            }
        )

    @classmethod
    def create_desertion_risk_alert(
        cls,
        student_id: UUID,
        ficha_id: UUID,
        risk_score: float,
        factors: List[str],
        level: AlertLevel = AlertLevel.CRITICAL
    ) -> "AttendanceAlert":
        """
        Crea una alerta por riesgo de deserción.
        
        Args:
            student_id: ID del estudiante
            ficha_id: ID de la ficha
            risk_score: Puntuación de riesgo (0-100)
            factors: Factores que contribuyen al riesgo
            level: Nivel de criticidad de la alerta
            
        Returns:
            Nueva instancia de AttendanceAlert
        """
        return cls(
            student_id=student_id,
            ficha_id=ficha_id,
            alert_type=AlertType.DESERTION_RISK,
            level=level,
            message=f"Estudiante en riesgo de deserción (score: {risk_score:.1f})",
            data={
                "risk_score": risk_score,
                "risk_factors": factors,
                "threshold": 70.0,
                "alert_reason": "desertion_risk"
            }
        )

    def acknowledge(self, acknowledged_by: UUID) -> None:
        """
        Marca la alerta como reconocida por un instructor/administrador.
        
        Args:
            acknowledged_by: ID del usuario que reconoce la alerta
        """
        self.acknowledged = True
        self.acknowledged_by = acknowledged_by
        self.acknowledged_at = datetime.now()
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        """Desactiva la alerta cuando ya no sea relevante."""
        self.is_active = False
        self.updated_at = datetime.now()

    def escalate_level(self) -> None:
        """Escala el nivel de criticidad de la alerta."""
        if self.level == AlertLevel.LOW:
            self.level = AlertLevel.MEDIUM
        elif self.level == AlertLevel.MEDIUM:
            self.level = AlertLevel.HIGH
        elif self.level == AlertLevel.HIGH:
            self.level = AlertLevel.CRITICAL
        
        self.updated_at = datetime.now()

    def is_critical(self) -> bool:
        """Verifica si la alerta es de nivel crítico."""
        return self.level == AlertLevel.CRITICAL

    def is_high(self) -> bool:
        """Verifica si la alerta es de nivel alto."""
        return self.level == AlertLevel.HIGH

    def is_overdue(self, max_days: int = 7) -> bool:
        """
        Verifica si la alerta lleva demasiado tiempo sin ser reconocida.
        
        Args:
            max_days: Máximo número de días antes de considerar la alerta vencida
            
        Returns:
            True si la alerta está vencida
        """
        if self.acknowledged:
            return False
            
        days_since_created = (datetime.now() - self.created_at).days
        return days_since_created > max_days

    def days_since_creation(self) -> int:
        """Calcula los días transcurridos desde la creación de la alerta."""
        return (datetime.now() - self.created_at).days

    def __eq__(self, other) -> bool:
        if not isinstance(other, AttendanceAlert):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self) -> str:
        return f"AttendanceAlert(id={self.id}, student_id={self.student_id}, type={self.alert_type.value}, level={self.level.value})"
