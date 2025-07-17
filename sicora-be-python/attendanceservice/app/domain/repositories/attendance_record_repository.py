from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from ..entities.attendance_record import AttendanceRecord


class AttendanceRecordRepository(ABC):
    """Interfaz de repositorio para registros de asistencia."""

    @abstractmethod
    async def save(self, attendance_record: AttendanceRecord) -> AttendanceRecord:
        """Guarda un registro de asistencia."""
        pass

    @abstractmethod
    async def get_by_id(self, attendance_id: UUID) -> Optional[AttendanceRecord]:
        """Obtiene un registro de asistencia por ID."""
        pass

    @abstractmethod
    async def get_by_student_and_date(
        self, 
        student_id: UUID, 
        date: date,
        block_identifier: str
    ) -> Optional[AttendanceRecord]:
        """Obtiene un registro de asistencia por estudiante, fecha y bloque."""
        pass

    @abstractmethod
    async def get_by_student_and_period(
        self,
        student_id: UUID,
        start_date: date,
        end_date: date
    ) -> List[AttendanceRecord]:
        """Obtiene registros de asistencia de un estudiante en un período."""
        pass

    @abstractmethod
    async def get_by_ficha_and_date(
        self,
        ficha_id: UUID,
        date: date
    ) -> List[AttendanceRecord]:
        """Obtiene todos los registros de asistencia de una ficha en una fecha."""
        pass

    @abstractmethod
    async def get_by_instructor_and_period(
        self,
        instructor_id: UUID,
        start_date: date,
        end_date: date
    ) -> List[AttendanceRecord]:
        """Obtiene registros de asistencia de un instructor en un período."""
        pass

    @abstractmethod
    async def get_consecutive_absences(
        self,
        student_id: UUID,
        ficha_id: UUID,
        end_date: date,
        max_days: int = 30
    ) -> int:
        """Calcula las inasistencias consecutivas de un estudiante."""
        pass

    @abstractmethod
    async def get_attendance_percentage(
        self,
        student_id: UUID,
        start_date: date,
        end_date: date
    ) -> float:
        """Calcula el porcentaje de asistencia de un estudiante en un período."""
        pass

    @abstractmethod
    async def get_attendance_summary(
        self,
        student_id: Optional[UUID] = None,
        ficha_id: Optional[UUID] = None,
        instructor_id: Optional[UUID] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> dict:
        """Obtiene un resumen estadístico de asistencia con filtros opcionales."""
        pass

    @abstractmethod
    async def delete(self, attendance_id: UUID) -> bool:
        """Elimina un registro de asistencia."""
        pass

    @abstractmethod
    async def exists(
        self,
        student_id: UUID,
        date: date,
        block_identifier: str
    ) -> bool:
        """Verifica si existe un registro de asistencia."""
        pass
