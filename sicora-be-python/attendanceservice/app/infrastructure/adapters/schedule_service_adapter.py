import asyncio
import httpx
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime, date

from ...application.interfaces import ScheduleServiceInterface
from ...domain.exceptions import ExternalServiceError


class HTTPScheduleServiceAdapter(ScheduleServiceInterface):
    """
    Adaptador HTTP para comunicación con ScheduleService
    """
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def close(self):
        """Cerrar el cliente HTTP"""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def get_user_schedule_for_date(self, user_id: UUID, date: date) -> Optional[Dict[str, Any]]:
        """
        Obtener el horario de un usuario para una fecha específica
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/schedules/user/{user_id}/date/{date.isoformat()}"
            )
            
            if response.status_code == 404:
                return None
            
            if response.status_code != 200:
                raise ExternalServiceError(
                    f"Error al obtener horario: {response.status_code} - {response.text}"
                )
            
            return response.json()
            
        except httpx.RequestError as e:
            raise ExternalServiceError(f"Error de conexión con ScheduleService: {str(e)}")
        except Exception as e:
            raise ExternalServiceError(f"Error inesperado al obtener horario: {str(e)}")
    
    async def get_user_current_schedule(self, user_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Obtener el horario actual activo de un usuario
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/schedules/user/{user_id}/current"
            )
            
            if response.status_code == 404:
                return None
            
            if response.status_code != 200:
                raise ExternalServiceError(
                    f"Error al obtener horario actual: {response.status_code} - {response.text}"
                )
            
            return response.json()
            
        except httpx.RequestError as e:
            raise ExternalServiceError(f"Error de conexión con ScheduleService: {str(e)}")
        except Exception as e:
            raise ExternalServiceError(f"Error inesperado al obtener horario actual: {str(e)}")
    
    async def get_class_schedule(self, class_id: UUID, date: date) -> Optional[Dict[str, Any]]:
        """
        Obtener el horario de una clase para una fecha específica
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/schedules/class/{class_id}/date/{date.isoformat()}"
            )
            
            if response.status_code == 404:
                return None
            
            if response.status_code != 200:
                raise ExternalServiceError(
                    f"Error al obtener horario de clase: {response.status_code} - {response.text}"
                )
            
            return response.json()
            
        except httpx.RequestError as e:
            raise ExternalServiceError(f"Error de conexión con ScheduleService: {str(e)}")
        except Exception as e:
            raise ExternalServiceError(f"Error inesperado al obtener horario de clase: {str(e)}")
    
    async def get_class_students(self, class_id: UUID) -> List[Dict[str, Any]]:
        """
        Obtener la lista de estudiantes inscritos en una clase
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/schedules/class/{class_id}/students"
            )
            
            if response.status_code != 200:
                raise ExternalServiceError(
                    f"Error al obtener estudiantes de clase: {response.status_code} - {response.text}"
                )
            
            return response.json()
            
        except httpx.RequestError as e:
            raise ExternalServiceError(f"Error de conexión con ScheduleService: {str(e)}")
        except Exception as e:
            raise ExternalServiceError(f"Error inesperado al obtener estudiantes de clase: {str(e)}")
    
    async def validate_user_class_enrollment(self, user_id: UUID, class_id: UUID) -> bool:
        """
        Validar que un usuario esté inscrito en una clase específica
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/schedules/user/{user_id}/class/{class_id}/enrollment"
            )
            
            if response.status_code == 404:
                return False
            
            if response.status_code != 200:
                raise ExternalServiceError(
                    f"Error al validar inscripción: {response.status_code} - {response.text}"
                )
            
            data = response.json()
            return data.get('enrolled', False)
            
        except httpx.RequestError as e:
            raise ExternalServiceError(f"Error de conexión con ScheduleService: {str(e)}")
        except Exception as e:
            raise ExternalServiceError(f"Error inesperado al validar inscripción: {str(e)}")
    
    async def get_active_classes_for_instructor(self, instructor_id: UUID, date: date) -> List[Dict[str, Any]]:
        """
        Obtener las clases activas de un instructor para una fecha específica
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/schedules/instructor/{instructor_id}/classes/active",
                params={"date": date.isoformat()}
            )
            
            if response.status_code != 200:
                raise ExternalServiceError(
                    f"Error al obtener clases activas: {response.status_code} - {response.text}"
                )
            
            return response.json()
            
        except httpx.RequestError as e:
            raise ExternalServiceError(f"Error de conexión con ScheduleService: {str(e)}")
        except Exception as e:
            raise ExternalServiceError(f"Error inesperado al obtener clases activas: {str(e)}")
    
    async def get_class_time_slots(self, class_id: UUID, date: date) -> List[Dict[str, Any]]:
        """
        Obtener los horarios específicos de una clase para una fecha
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/schedules/class/{class_id}/time-slots",
                params={"date": date.isoformat()}
            )
            
            if response.status_code != 200:
                raise ExternalServiceError(
                    f"Error al obtener horarios de clase: {response.status_code} - {response.text}"
                )
            
            return response.json()
            
        except httpx.RequestError as e:
            raise ExternalServiceError(f"Error de conexión con ScheduleService: {str(e)}")
        except Exception as e:
            raise ExternalServiceError(f"Error inesperado al obtener horarios de clase: {str(e)}")
    
    async def is_class_active_now(self, class_id: UUID) -> bool:
        """
        Verificar si una clase está activa en este momento
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/schedules/class/{class_id}/active-now"
            )
            
            if response.status_code == 404:
                return False
            
            if response.status_code != 200:
                raise ExternalServiceError(
                    f"Error al verificar clase activa: {response.status_code} - {response.text}"
                )
            
            data = response.json()
            return data.get('active', False)
            
        except httpx.RequestError as e:
            raise ExternalServiceError(f"Error de conexión con ScheduleService: {str(e)}")
        except Exception as e:
            raise ExternalServiceError(f"Error inesperado al verificar clase activa: {str(e)}")
