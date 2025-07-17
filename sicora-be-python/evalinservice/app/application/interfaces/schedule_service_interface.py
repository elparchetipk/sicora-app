"""Interface for Schedule Service integration."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from uuid import UUID


class ScheduleServiceInterface(ABC):
    """
    Interface para integración con ScheduleService.
    Define el contrato para obtener información de horarios y entidades académicas.
    """
    
    @abstractmethod
    async def get_instructor_fichas(self, instructor_id: UUID) -> List[Dict]:
        """Obtiene las fichas donde enseña un instructor."""
        pass
    
    @abstractmethod
    async def get_student_instructors(self, student_id: UUID) -> List[Dict]:
        """Obtiene los instructores que enseñan a un estudiante."""
        pass
    
    @abstractmethod
    async def get_ficha_instructors(self, ficha_id: str) -> List[Dict]:
        """Obtiene los instructores de una ficha específica."""
        pass
    
    @abstractmethod
    async def get_ficha_students(self, ficha_id: str) -> List[Dict]:
        """Obtiene los estudiantes de una ficha específica."""
        pass
    
    @abstractmethod
    async def get_programa_info(self, programa_id: UUID) -> Optional[Dict]:
        """Obtiene información de un programa académico."""
        pass
    
    @abstractmethod
    async def get_ficha_info(self, ficha_id: str) -> Optional[Dict]:
        """Obtiene información de una ficha."""
        pass
    
    @abstractmethod
    async def get_active_fichas(self) -> List[Dict]:
        """Obtiene todas las fichas activas."""
        pass
    
    @abstractmethod
    async def validate_instructor_teaches_student(
        self, 
        instructor_id: UUID, 
        student_id: UUID
    ) -> bool:
        """Valida si un instructor enseña a un estudiante específico."""
        pass
