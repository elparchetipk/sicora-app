from datetime import date, datetime, timedelta
from typing import List, Dict
from uuid import UUID

from ...domain.exceptions import UnauthorizedAccessError
from ..dtos import (
    GetInstructorNoAttendanceAlertsRequest,
    GetInstructorNoAttendanceAlertsResponse,
    InstructorNoAttendanceAlert
)
from ..interfaces import UserServiceInterface, ScheduleServiceInterface


class GetInstructorNoAttendanceAlertsUseCase:
    """
    Caso de uso para alertas de instructores sin registro (HU-BE-027).
    
    Identifica instructores que no registraron asistencia el día anterior,
    con filtrado por sede/programa/ficha y validación de rol administrativo.
    """

    def __init__(
        self,
        user_service: UserServiceInterface,
        schedule_service: ScheduleServiceInterface
    ):
        self.user_service = user_service
        self.schedule_service = schedule_service

    async def execute(
        self,
        request: GetInstructorNoAttendanceAlertsRequest,
        requesting_user_id: UUID
    ) -> GetInstructorNoAttendanceAlertsResponse:
        """
        Ejecuta la consulta de alertas de instructores sin registro.
        
        Args:
            request: Filtros para las alertas
            requesting_user_id: ID del usuario administrador que solicita
            
        Returns:
            Lista de instructores que no registraron asistencia
            
        Raises:
            UnauthorizedAccessError: Si el usuario no es administrador
        """
        # Validar que el usuario tenga rol de administrador
        user_role = await self.user_service.get_user_role(requesting_user_id)
        if user_role not in ["admin", "coordinator"]:
            raise UnauthorizedAccessError(
                "instructor attendance alerts",
                user_role
            )

        # Establecer fecha por defecto (día anterior) si no se proporciona
        target_date = request.date if request.date else date.today() - timedelta(days=1)

        # Obtener instructores que tenían horario pero no registraron asistencia
        instructors_without_attendance = await self.schedule_service.get_instructors_without_attendance(
            date=target_date,
            sede_id=request.sede_id,
            programa_id=request.programa_id,
            ficha_id=request.ficha_id
        )

        # Enriquecer datos con información adicional
        enriched_alerts = await self._enrich_instructor_alerts(
            instructors_without_attendance,
            target_date
        )

        # Calcular estadísticas
        stats = self._calculate_statistics(enriched_alerts)

        return GetInstructorNoAttendanceAlertsResponse(
            alerts=enriched_alerts,
            total_alerts=stats["total_alerts"],
            affected_instructors=stats["affected_instructors"],
            affected_fichas=stats["affected_fichas"],
            date=target_date
        )

    async def _enrich_instructor_alerts(
        self,
        instructor_data: List[Dict],
        target_date: date
    ) -> List[InstructorNoAttendanceAlert]:
        """Enriquece los datos de instructores con información adicional."""
        enriched_alerts = []
        
        for instructor_info in instructor_data:
            # Obtener información completa del instructor
            instructor_id = instructor_info.get("instructor_id")
            instructor_details = await self.user_service.get_user_by_id(instructor_id)
            
            instructor_name = "Usuario no encontrado"
            if instructor_details:
                instructor_name = f"{instructor_details.get('first_name', '')} {instructor_details.get('last_name', '')}".strip()

            # Crear alerta enriquecida
            alert = InstructorNoAttendanceAlert(
                instructor_id=instructor_id,
                instructor_name=instructor_name,
                ficha_id=instructor_info.get("ficha_id"),
                ficha_name=instructor_info.get("ficha_name", "Ficha no encontrada"),
                block_identifier=instructor_info.get("block_identifier", "N/A"),
                venue_name=instructor_info.get("venue_name", "Ambiente no especificado"),
                date=target_date,
                start_time=instructor_info.get("start_time", "00:00"),
                end_time=instructor_info.get("end_time", "00:00"),
                sede_name=instructor_info.get("sede_name", "Sede no especificada"),
                programa_name=instructor_info.get("programa_name", "Programa no especificado")
            )
            
            enriched_alerts.append(alert)
        
        return enriched_alerts

    def _calculate_statistics(
        self,
        alerts: List[InstructorNoAttendanceAlert]
    ) -> Dict[str, int]:
        """Calcula estadísticas de las alertas de instructores."""
        
        # Contar instructores únicos
        unique_instructors = set(alert.instructor_id for alert in alerts)
        
        # Contar fichas únicas afectadas
        unique_fichas = set(alert.ficha_id for alert in alerts)
        
        return {
            "total_alerts": len(alerts),
            "affected_instructors": len(unique_instructors),
            "affected_fichas": len(unique_fichas)
        }
