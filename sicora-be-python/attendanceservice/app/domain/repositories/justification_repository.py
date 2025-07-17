from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from uuid import UUID

from ..entities.justification import Justification
from ..value_objects import JustificationStatus


class JustificationRepository(ABC):
    """Interfaz de repositorio para justificaciones."""

    @abstractmethod
    async def save(self, justification: Justification) -> Justification:
        """Guarda una justificación."""
        pass

    @abstractmethod
    async def get_by_id(self, justification_id: UUID) -> Optional[Justification]:
        """Obtiene una justificación por ID."""
        pass

    @abstractmethod
    async def get_by_student(self, student_id: UUID) -> List[Justification]:
        """Obtiene todas las justificaciones de un estudiante."""
        pass

    @abstractmethod
    async def get_by_attendance_record(
        self, 
        attendance_record_id: UUID
    ) -> Optional[Justification]:
        """Obtiene una justificación por registro de asistencia."""
        pass

    @abstractmethod
    async def get_pending_for_instructor(
        self,
        instructor_id: UUID
    ) -> List[Justification]:
        """Obtiene justificaciones pendientes que puede revisar un instructor."""
        pass

    @abstractmethod
    async def get_by_status(
        self,
        status: JustificationStatus,
        student_id: Optional[UUID] = None,
        instructor_id: Optional[UUID] = None
    ) -> List[Justification]:
        """Obtiene justificaciones por estado con filtros opcionales."""
        pass

    @abstractmethod
    async def get_overdue_justifications(
        self,
        days_threshold: int = 7
    ) -> List[Justification]:
        """Obtiene justificaciones que llevan mucho tiempo pendientes."""
        pass

    @abstractmethod
    async def count_by_student_and_period(
        self,
        student_id: UUID,
        start_date: date,
        end_date: date,
        status: Optional[JustificationStatus] = None
    ) -> int:
        """Cuenta las justificaciones de un estudiante en un período."""
        pass

    @abstractmethod
    async def delete(self, justification_id: UUID) -> bool:
        """Elimina una justificación."""
        pass

    @abstractmethod
    async def exists_for_attendance(
        self,
        attendance_record_id: UUID
    ) -> bool:
        """Verifica si existe una justificación para un registro de asistencia."""
        pass
