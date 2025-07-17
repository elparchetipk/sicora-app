from abc import ABC, abstractmethod
from datetime import date, time
from typing import Optional, Dict, List
from uuid import UUID


class ScheduleServiceInterface(ABC):
    """Interfaz para comunicación con ScheduleService."""

    @abstractmethod
    async def get_schedule_by_id(self, schedule_id: UUID) -> Optional[Dict]:
        """
        Obtiene información de un horario por ID.
        
        Args:
            schedule_id: ID del horario
            
        Returns:
            Diccionario con datos del horario o None si no existe
        """
        pass

    @abstractmethod
    async def get_active_schedules_by_ficha(
        self,
        ficha_id: UUID,
        date: date
    ) -> List[Dict]:
        """
        Obtiene los horarios activos de una ficha para una fecha específica.
        
        Args:
            ficha_id: ID de la ficha
            date: Fecha para consultar horarios
            
        Returns:
            Lista de horarios activos para la fecha
        """
        pass

    @abstractmethod
    async def get_instructor_schedule(
        self,
        instructor_id: UUID,
        date: date
    ) -> List[Dict]:
        """
        Obtiene el horario de un instructor para una fecha específica.
        
        Args:
            instructor_id: ID del instructor
            date: Fecha para consultar horario
            
        Returns:
            Lista de horarios del instructor para la fecha
        """
        pass

    @abstractmethod
    async def validate_instructor_schedule(
        self,
        instructor_id: UUID,
        ficha_id: UUID,
        date: date,
        block_identifier: str
    ) -> bool:
        """
        Valida que un instructor tenga horario asignado para una ficha y bloque específicos.
        
        Args:
            instructor_id: ID del instructor
            ficha_id: ID de la ficha
            date: Fecha del horario
            block_identifier: Identificador del bloque
            
        Returns:
            True si el instructor tiene horario asignado
        """
        pass

    @abstractmethod
    async def get_venue_info(self, venue_id: UUID) -> Optional[Dict]:
        """
        Obtiene información de un lugar/aula.
        
        Args:
            venue_id: ID del lugar
            
        Returns:
            Diccionario con datos del lugar o None si no existe
        """
        pass

    @abstractmethod
    async def get_block_info(
        self,
        ficha_id: UUID,
        date: date,
        block_identifier: str
    ) -> Optional[Dict]:
        """
        Obtiene información detallada de un bloque específico.
        
        Args:
            ficha_id: ID de la ficha
            date: Fecha del bloque
            block_identifier: Identificador del bloque
            
        Returns:
            Diccionario con datos del bloque o None si no existe
        """
        pass

    @abstractmethod
    async def get_instructors_without_attendance(
        self,
        date: date,
        sede_id: Optional[UUID] = None,
        programa_id: Optional[UUID] = None,
        ficha_id: Optional[UUID] = None
    ) -> List[Dict]:
        """
        Obtiene instructores que tenían horario pero no registraron asistencia.
        
        Args:
            date: Fecha a consultar
            sede_id: ID de la sede (filtro opcional)
            programa_id: ID del programa (filtro opcional)
            ficha_id: ID de la ficha (filtro opcional)
            
        Returns:
            Lista de instructores sin registro de asistencia
        """
        pass
