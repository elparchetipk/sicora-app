from abc import ABC, abstractmethod
from typing import Optional, Dict, List
from uuid import UUID


class UserServiceInterface(ABC):
    """Interfaz para comunicación con UserService."""

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> Optional[Dict]:
        """
        Obtiene información básica de un usuario por ID.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Diccionario con datos del usuario o None si no existe
        """
        pass

    @abstractmethod
    async def get_students_by_ficha(self, ficha_id: UUID) -> List[Dict]:
        """
        Obtiene la lista de estudiantes de una ficha.
        
        Args:
            ficha_id: ID de la ficha
            
        Returns:
            Lista de estudiantes con su información básica
        """
        pass

    @abstractmethod
    async def get_instructor_fichas(self, instructor_id: UUID) -> List[Dict]:
        """
        Obtiene las fichas asignadas a un instructor.
        
        Args:
            instructor_id: ID del instructor
            
        Returns:
            Lista de fichas asignadas al instructor
        """
        pass

    @abstractmethod
    async def validate_instructor_ficha_assignment(
        self,
        instructor_id: UUID,
        ficha_id: UUID
    ) -> bool:
        """
        Valida que un instructor esté asignado a una ficha.
        
        Args:
            instructor_id: ID del instructor
            ficha_id: ID de la ficha
            
        Returns:
            True si el instructor está asignado a la ficha
        """
        pass

    @abstractmethod
    async def validate_student_ficha_enrollment(
        self,
        student_id: UUID,
        ficha_id: UUID
    ) -> bool:
        """
        Valida que un estudiante esté matriculado en una ficha.
        
        Args:
            student_id: ID del estudiante
            ficha_id: ID de la ficha
            
        Returns:
            True si el estudiante está matriculado en la ficha
        """
        pass

    @abstractmethod
    async def get_user_role(self, user_id: UUID) -> Optional[str]:
        """
        Obtiene el rol de un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Rol del usuario o None si no existe
        """
        pass
