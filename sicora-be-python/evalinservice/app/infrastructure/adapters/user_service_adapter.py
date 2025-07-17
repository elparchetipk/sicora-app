"""User Service adapter."""

from typing import Optional
from uuid import UUID
import httpx

from ...application.interfaces import UserServiceInterface


class UserServiceAdapter(UserServiceInterface):
    """
    Adaptador para comunicación con UserService.
    
    Responsabilidades:
    - Implementar interfaz de UserService 
    - Realizar llamadas HTTP al microservicio UserService
    - Manejar errores de comunicación
    """
    
    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient()
    
    async def get_user_by_id(self, user_id: UUID) -> Optional[dict]:
        """
        Obtener información de usuario por ID.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            dict: Información del usuario o None si no existe
        """
        try:
            response = await self._client.get(f"{self._base_url}/api/v1/users/{user_id}")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                response.raise_for_status()
                
        except httpx.RequestError as e:
            # Log error en producción
            print(f"Error al conectar con UserService: {e}")
            return None
        
        return None
    
    async def get_users_by_role(self, role: str) -> list:
        """
        Obtener usuarios por rol.
        
        Args:
            role: Rol de los usuarios a buscar
            
        Returns:
            list: Lista de usuarios con el rol especificado
        """
        try:
            response = await self._client.get(
                f"{self._base_url}/api/v1/users",
                params={"role": role}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                response.raise_for_status()
                
        except httpx.RequestError as e:
            print(f"Error al conectar con UserService: {e}")
            return []
        
        return []
    
    async def user_exists(self, user_id: UUID) -> bool:
        """
        Verificar si un usuario existe.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            bool: True si el usuario existe
        """
        user = await self.get_user_by_id(user_id)
        return user is not None
    
    async def close(self):
        """Cerrar el cliente HTTP."""
        await self._client.aclose()
