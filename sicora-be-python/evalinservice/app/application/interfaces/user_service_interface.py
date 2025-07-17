"""Interface for User Service integration."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from uuid import UUID


class UserServiceInterface(ABC):
    """
    Interface para integración con UserService.
    Define el contrato para obtener información de usuarios.
    """
    
    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> Optional[Dict]:
        """Obtiene información de un usuario por ID."""
        pass
    
    @abstractmethod
    async def get_users_by_ids(self, user_ids: List[UUID]) -> List[Dict]:
        """Obtiene información de múltiples usuarios por IDs."""
        pass
    
    @abstractmethod
    async def get_instructors(self) -> List[Dict]:
        """Obtiene lista de todos los instructores."""
        pass
    
    @abstractmethod
    async def get_students_by_ficha(self, ficha_id: str) -> List[Dict]:
        """Obtiene estudiantes de una ficha específica."""
        pass
    
    @abstractmethod
    async def get_user_role(self, user_id: UUID) -> Optional[str]:
        """Obtiene el rol de un usuario."""
        pass
    
    @abstractmethod
    async def is_instructor(self, user_id: UUID) -> bool:
        """Verifica si un usuario es instructor."""
        pass
    
    @abstractmethod
    async def is_student(self, user_id: UUID) -> bool:
        """Verifica si un usuario es estudiante."""
        pass
    
    @abstractmethod
    async def is_admin(self, user_id: UUID) -> bool:
        """Verifica si un usuario es administrador."""
        pass
    
    @abstractmethod
    async def get_user_fichas(self, user_id: UUID) -> List[str]:
        """Obtiene las fichas asociadas a un usuario."""
        pass
