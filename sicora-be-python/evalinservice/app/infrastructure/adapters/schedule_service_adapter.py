"""Schedule Service adapter."""

from typing import Optional, List
from uuid import UUID
import httpx

from ...application.interfaces import ScheduleServiceInterface


class ScheduleServiceAdapter(ScheduleServiceInterface):
    """
    Adaptador para comunicación con ScheduleService.
    
    Responsabilidades:
    - Implementar interfaz de ScheduleService
    - Realizar llamadas HTTP al microservicio ScheduleService
    - Manejar errores de comunicación
    """
    
    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient()
    
    async def get_group_by_id(self, group_id: UUID) -> Optional[dict]:
        """
        Obtener información de grupo por ID.
        
        Args:
            group_id: ID del grupo
            
        Returns:
            dict: Información del grupo o None si no existe
        """
        try:
            response = await self._client.get(f"{self._base_url}/api/v1/groups/{group_id}")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                response.raise_for_status()
                
        except httpx.RequestError as e:
            print(f"Error al conectar con ScheduleService: {e}")
            return None
        
        return None
    
    async def get_instructor_groups(self, instructor_id: UUID) -> List[dict]:
        """
        Obtener grupos asignados a un instructor.
        
        Args:
            instructor_id: ID del instructor
            
        Returns:
            List[dict]: Lista de grupos del instructor
        """
        try:
            response = await self._client.get(
                f"{self._base_url}/api/v1/groups",
                params={"instructor_id": str(instructor_id)}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                response.raise_for_status()
                
        except httpx.RequestError as e:
            print(f"Error al conectar con ScheduleService: {e}")
            return []
        
        return []
    
    async def get_student_groups(self, student_id: UUID) -> List[dict]:
        """
        Obtener grupos en los que está inscrito un estudiante.
        
        Args:
            student_id: ID del estudiante
            
        Returns:
            List[dict]: Lista de grupos del estudiante
        """
        try:
            response = await self._client.get(
                f"{self._base_url}/api/v1/enrollments",
                params={"student_id": str(student_id)}
            )
            
            if response.status_code == 200:
                enrollments = response.json()
                # Extraer grupos de las inscripciones
                groups = []
                for enrollment in enrollments:
                    if "group" in enrollment:
                        groups.append(enrollment["group"])
                return groups
            else:
                response.raise_for_status()
                
        except httpx.RequestError as e:
            print(f"Error al conectar con ScheduleService: {e}")
            return []
        
        return []
    
    async def group_exists(self, group_id: UUID) -> bool:
        """
        Verificar si un grupo existe.
        
        Args:
            group_id: ID del grupo
            
        Returns:
            bool: True si el grupo existe
        """
        group = await self.get_group_by_id(group_id)
        return group is not None
    
    async def close(self):
        """Cerrar el cliente HTTP."""
        await self._client.aclose()
