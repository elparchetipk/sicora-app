import asyncio
import httpx
from typing import Optional, Dict, List
from uuid import UUID

from ...application.interfaces import UserServiceInterface
from ...domain.exceptions import ExternalServiceError


class HTTPUserServiceAdapter(UserServiceInterface):
    """
    Adaptador HTTP para comunicación con UserService.
    
    Implementa la interfaz de UserService utilizando llamadas HTTP
    al microservicio de usuarios con manejo de errores y timeouts.
    """

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = None

    async def _get_session(self) -> httpx.AsyncClient:
        """Obtiene o crea una sesión HTTP."""
        if self.session is None:
            self.session = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "AttendanceService/1.0"
                }
            )
        return self.session

    async def get_user_by_id(self, user_id: UUID) -> Optional[Dict]:
        """
        Obtiene información básica de un usuario por ID.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Diccionario con datos del usuario o None si no existe
        """
        try:
            session = await self._get_session()
            response = await session.get(f"{self.base_url}/admin/users/{user_id}")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                raise ExternalServiceError(
                    "UserService",
                    f"Failed to get user {user_id}: {response.status_code}"
                )
                
        except httpx.RequestError as e:
            raise ExternalServiceError("UserService", f"Request error: {str(e)}")
        except Exception as e:
            raise ExternalServiceError("UserService", f"Unexpected error: {str(e)}")

    async def get_students_by_ficha(self, ficha_id: UUID) -> List[Dict]:
        """
        Obtiene la lista de estudiantes de una ficha.
        
        Args:
            ficha_id: ID de la ficha
            
        Returns:
            Lista de estudiantes con su información básica
        """
        try:
            session = await self._get_session()
            response = await session.get(
                f"{self.base_url}/admin/users",
                params={
                    "ficha_id": str(ficha_id),
                    "role": "aprendiz",
                    "is_active": "true"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("users", [])
            else:
                raise ExternalServiceError(
                    "UserService",
                    f"Failed to get students for ficha {ficha_id}: {response.status_code}"
                )
                
        except httpx.RequestError as e:
            raise ExternalServiceError("UserService", f"Request error: {str(e)}")
        except Exception as e:
            raise ExternalServiceError("UserService", f"Unexpected error: {str(e)}")

    async def get_instructor_fichas(self, instructor_id: UUID) -> List[Dict]:
        """
        Obtiene las fichas asignadas a un instructor.
        
        Args:
            instructor_id: ID del instructor
            
        Returns:
            Lista de fichas asignadas al instructor
        """
        try:
            session = await self._get_session()
            response = await session.get(
                f"{self.base_url}/admin/users/{instructor_id}/fichas"
            )
            
            if response.status_code == 200:
                return response.json().get("fichas", [])
            elif response.status_code == 404:
                return []
            else:
                raise ExternalServiceError(
                    "UserService",
                    f"Failed to get fichas for instructor {instructor_id}: {response.status_code}"
                )
                
        except httpx.RequestError as e:
            raise ExternalServiceError("UserService", f"Request error: {str(e)}")
        except Exception as e:
            raise ExternalServiceError("UserService", f"Unexpected error: {str(e)}")

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
        try:
            instructor_fichas = await self.get_instructor_fichas(instructor_id)
            ficha_ids = [UUID(ficha["id"]) for ficha in instructor_fichas]
            return ficha_id in ficha_ids
            
        except Exception:
            # En caso de error, por seguridad retornamos False
            return False

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
        try:
            student_info = await self.get_user_by_id(student_id)
            if not student_info:
                return False
                
            # Verificar que el usuario es un aprendiz
            if student_info.get("role") != "aprendiz":
                return False
                
            # Verificar que pertenece a la ficha
            student_ficha_id = student_info.get("ficha_id")
            return student_ficha_id and UUID(student_ficha_id) == ficha_id
            
        except Exception:
            # En caso de error, por seguridad retornamos False
            return False

    async def get_user_role(self, user_id: UUID) -> Optional[str]:
        """
        Obtiene el rol de un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Rol del usuario o None si no existe
        """
        try:
            user_info = await self.get_user_by_id(user_id)
            return user_info.get("role") if user_info else None
            
        except Exception:
            return None

    async def close(self):
        """Cierra la sesión HTTP."""
        if self.session:
            await self.session.aclose()
            self.session = None

    def __del__(self):
        """Limpia la sesión al destruir el objeto."""
        if self.session:
            # Crear una nueva loop si es necesario para cerrar la sesión
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(self.close())
                else:
                    loop.run_until_complete(self.close())
            except Exception:
                pass  # Ignorar errores en destructor
