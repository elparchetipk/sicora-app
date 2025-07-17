from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from uuid import UUID

from ..entities.attendance_alert import AttendanceAlert
from ..value_objects import AlertLevel, AlertType


class AttendanceAlertRepository(ABC):
    """Interfaz de repositorio para alertas de asistencia."""

    @abstractmethod
    async def save(self, alert: AttendanceAlert) -> AttendanceAlert:
        """Guarda una alerta."""
        pass

    @abstractmethod
    async def get_by_id(self, alert_id: UUID) -> Optional[AttendanceAlert]:
        """Obtiene una alerta por ID."""
        pass

    @abstractmethod
    async def get_active_alerts(
        self,
        student_id: Optional[UUID] = None,
        ficha_id: Optional[UUID] = None,
        instructor_id: Optional[UUID] = None,
        level: Optional[AlertLevel] = None,
        alert_type: Optional[AlertType] = None
    ) -> List[AttendanceAlert]:
        """Obtiene alertas activas con filtros opcionales."""
        pass

    @abstractmethod
    async def get_by_student(
        self,
        student_id: UUID,
        include_inactive: bool = False
    ) -> List[AttendanceAlert]:
        """Obtiene todas las alertas de un estudiante."""
        pass

    @abstractmethod
    async def get_by_ficha(
        self,
        ficha_id: UUID,
        include_inactive: bool = False
    ) -> List[AttendanceAlert]:
        """Obtiene todas las alertas de una ficha."""
        pass

    @abstractmethod
    async def get_critical_alerts(self) -> List[AttendanceAlert]:
        """Obtiene todas las alertas críticas activas."""
        pass

    @abstractmethod
    async def get_unacknowledged_alerts(
        self,
        instructor_id: Optional[UUID] = None,
        max_days: int = 7
    ) -> List[AttendanceAlert]:
        """Obtiene alertas sin reconocer que superen el tiempo límite."""
        pass

    @abstractmethod
    async def get_alerts_by_type(
        self,
        alert_type: AlertType,
        include_inactive: bool = False
    ) -> List[AttendanceAlert]:
        """Obtiene alertas por tipo específico."""
        pass

    @abstractmethod
    async def deactivate_resolved_alerts(
        self,
        student_id: UUID,
        alert_type: AlertType
    ) -> int:
        """Desactiva alertas resueltas de un estudiante y tipo específico."""
        pass

    @abstractmethod
    async def get_alert_statistics(
        self,
        start_date: date,
        end_date: date,
        ficha_id: Optional[UUID] = None
    ) -> dict:
        """Obtiene estadísticas de alertas en un período."""
        pass

    @abstractmethod
    async def exists_active_alert(
        self,
        student_id: UUID,
        alert_type: AlertType
    ) -> bool:
        """Verifica si existe una alerta activa del tipo especificado para un estudiante."""
        pass

    @abstractmethod
    async def delete(self, alert_id: UUID) -> bool:
        """Elimina una alerta."""
        pass
