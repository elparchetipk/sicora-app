from math import ceil
from typing import List, Dict
from uuid import UUID

from ...domain.repositories import AttendanceAlertRepository, AttendanceRecordRepository
from ...domain.value_objects import AlertLevel, AlertType
from ...domain.exceptions import UnauthorizedAccessError
from ..dtos import (
    GetAlertsRequest,
    GetAlertsResponse,
    AlertDetail
)
from ..interfaces import UserServiceInterface


class GetAttendanceAlertsUseCase:
    """
    Caso de uso para obtener alertas de asistencia (HU-BE-026).
    
    Identifica casos críticos de inasistencia consecutiva con filtrado por rol,
    categorización por criticidad y recomendaciones de acción.
    """

    def __init__(
        self,
        alert_repository: AttendanceAlertRepository,
        attendance_repository: AttendanceRecordRepository,
        user_service: UserServiceInterface
    ):
        self.alert_repository = alert_repository
        self.attendance_repository = attendance_repository
        self.user_service = user_service

    async def execute(
        self,
        request: GetAlertsRequest,
        requesting_user_id: UUID
    ) -> GetAlertsResponse:
        """
        Ejecuta la consulta de alertas de asistencia.
        
        Args:
            request: Filtros para las alertas
            requesting_user_id: ID del usuario que solicita
            
        Returns:
            Lista paginada de alertas con recomendaciones
            
        Raises:
            UnauthorizedAccessError: Si el usuario no tiene permisos
        """
        # Obtener rol del usuario solicitante
        user_role = await self.user_service.get_user_role(requesting_user_id)
        
        # Validar permisos y ajustar filtros según el rol
        await self._validate_and_adjust_filters(request, requesting_user_id, user_role)

        # Validar parámetros de paginación
        request.page = max(1, request.page)
        request.page_size = min(50, max(1, request.page_size))

        # Obtener alertas activas desde el repositorio
        alerts = await self.alert_repository.get_active_alerts(
            student_id=request.student_id,
            ficha_id=request.ficha_id,
            instructor_id=request.instructor_id,
            level=request.level,
            alert_type=request.alert_type
        )

        # Filtrar alertas reconocidas si no se incluyen
        if not request.include_acknowledged:
            alerts = [alert for alert in alerts if not alert.acknowledged]

        # Calcular estadísticas
        stats = self._calculate_alert_statistics(alerts)

        # Aplicar paginación
        total_alerts = len(alerts)
        total_pages = ceil(total_alerts / request.page_size)
        start_index = (request.page - 1) * request.page_size
        end_index = start_index + request.page_size
        paginated_alerts = alerts[start_index:end_index]

        # Enriquecer alertas con información adicional
        enriched_alerts = await self._enrich_alerts(paginated_alerts, user_role)

        return GetAlertsResponse(
            alerts=enriched_alerts,
            total_alerts=total_alerts,
            critical_count=stats["critical_count"],
            high_count=stats["high_count"],
            medium_count=stats["medium_count"],
            low_count=stats["low_count"],
            unacknowledged_count=stats["unacknowledged_count"],
            page=request.page,
            page_size=request.page_size,
            total_pages=total_pages
        )

    async def _validate_and_adjust_filters(
        self,
        request: GetAlertsRequest,
        user_id: UUID,
        user_role: str
    ) -> None:
        """Valida permisos y ajusta filtros según el rol del usuario."""
        
        if user_role == "aprendiz":
            # Los aprendices solo pueden ver sus propias alertas
            if request.student_id and request.student_id != user_id:
                raise UnauthorizedAccessError(
                    "alerts of other students",
                    user_role
                )
            request.student_id = user_id
            request.instructor_id = None
            
        elif user_role == "instructor":
            # Los instructores pueden ver alertas de sus fichas asignadas
            if request.ficha_id:
                is_assigned = await self.user_service.validate_instructor_ficha_assignment(
                    user_id,
                    request.ficha_id
                )
                if not is_assigned:
                    raise UnauthorizedAccessError(
                        f"alerts for ficha {request.ficha_id}",
                        user_role
                    )
            
            # Si consultan por estudiante específico, validar que esté en sus fichas
            if request.student_id:
                instructor_fichas = await self.user_service.get_instructor_fichas(user_id)
                student_in_instructor_fichas = False
                
                for ficha in instructor_fichas:
                    if await self.user_service.validate_student_ficha_enrollment(
                        request.student_id, ficha["id"]
                    ):
                        student_in_instructor_fichas = True
                        break
                
                if not student_in_instructor_fichas:
                    raise UnauthorizedAccessError(
                        f"alerts for student {request.student_id}",
                        user_role
                    )
            
            # Si no se especifica ficha, limitar a las fichas del instructor
            if not request.ficha_id and not request.student_id:
                request.instructor_id = user_id
                
        elif user_role in ["admin", "coordinator"]:
            # Administradores y coordinadores tienen acceso completo
            pass
        else:
            raise UnauthorizedAccessError("attendance alerts", user_role)

    def _calculate_alert_statistics(self, alerts: List) -> Dict[str, int]:
        """Calcula estadísticas de las alertas."""
        stats = {
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 0,
            "low_count": 0,
            "unacknowledged_count": 0
        }
        
        for alert in alerts:
            # Contar por nivel
            if alert.level == AlertLevel.CRITICAL:
                stats["critical_count"] += 1
            elif alert.level == AlertLevel.HIGH:
                stats["high_count"] += 1
            elif alert.level == AlertLevel.MEDIUM:
                stats["medium_count"] += 1
            elif alert.level == AlertLevel.LOW:
                stats["low_count"] += 1
            
            # Contar no reconocidas
            if not alert.acknowledged:
                stats["unacknowledged_count"] += 1
        
        return stats

    async def _enrich_alerts(
        self,
        alerts: List,
        user_role: str
    ) -> List[AlertDetail]:
        """Enriquece las alertas con información adicional y recomendaciones."""
        enriched_alerts = []
        
        for alert in alerts:
            # Obtener información del estudiante
            student_info = await self.user_service.get_user_by_id(alert.student_id)
            student_name = "Usuario no encontrado"
            if student_info:
                student_name = f"{student_info.get('first_name', '')} {student_info.get('last_name', '')}".strip()

            # Obtener información del revisor si está reconocida
            acknowledged_by_name = None
            if alert.acknowledged_by:
                reviewer_info = await self.user_service.get_user_by_id(alert.acknowledged_by)
                if reviewer_info:
                    acknowledged_by_name = f"{reviewer_info.get('first_name', '')} {reviewer_info.get('last_name', '')}".strip()

            # Generar recomendaciones de acción
            recommended_actions = self._generate_recommendations(alert, user_role)

            # Crear el detalle enriquecido
            detail = AlertDetail(
                id=alert.id,
                student_id=alert.student_id,
                student_name=student_name,
                ficha_id=alert.ficha_id,
                ficha_name=student_info.get("ficha_name", "Ficha no encontrada") if student_info else "Ficha no encontrada",
                alert_type=alert.alert_type,
                level=alert.level,
                message=alert.message,
                data=alert.data,
                is_active=alert.is_active,
                acknowledged=alert.acknowledged,
                acknowledged_by=alert.acknowledged_by,
                acknowledged_by_name=acknowledged_by_name,
                acknowledged_at=alert.acknowledged_at,
                created_at=alert.created_at,
                days_since_creation=alert.days_since_creation(),
                recommended_actions=recommended_actions
            )
            
            enriched_alerts.append(detail)
        
        return enriched_alerts

    def _generate_recommendations(self, alert, user_role: str) -> List[str]:
        """Genera recomendaciones de acción según el tipo y nivel de alerta."""
        recommendations = []
        
        if alert.alert_type == AlertType.CONSECUTIVE_ABSENCES:
            consecutive_days = alert.data.get("consecutive_days", 0)
            
            if alert.level == AlertLevel.CRITICAL:
                recommendations.extend([
                    "Contactar inmediatamente al estudiante y acudiente",
                    "Programar reunión urgente con coordinación académica",
                    "Evaluar estrategias de recuperación académica",
                    "Considerar apoyo psicosocial"
                ])
            elif alert.level == AlertLevel.HIGH:
                recommendations.extend([
                    "Contactar al estudiante vía telefónica",
                    "Solicitar justificación de ausencias",
                    "Informar a coordinación académica",
                    "Monitorear de cerca próximas clases"
                ])
            else:
                recommendations.extend([
                    "Contactar al estudiante por WhatsApp/email",
                    "Verificar estado de salud y situación personal",
                    "Recordar importancia de la asistencia"
                ])
                
        elif alert.alert_type == AlertType.LOW_ATTENDANCE:
            percentage = alert.data.get("attendance_percentage", 0)
            
            recommendations.extend([
                f"Revisar detalladamente el historial de asistencia",
                "Identificar patrones de inasistencia",
                "Establecer plan de mejoramiento",
                "Hacer seguimiento semanal"
            ])
            
        elif alert.alert_type == AlertType.DESERTION_RISK:
            risk_score = alert.data.get("risk_score", 0)
            factors = alert.data.get("risk_factors", [])
            
            recommendations.extend([
                "Activar protocolo de retención estudiantil",
                "Reunión inmediata con equipo interdisciplinario",
                "Evaluación integral de factores de riesgo",
                "Implementar estrategias personalizadas de apoyo"
            ])
            
        # Agregar recomendaciones específicas por rol
        if user_role == "instructor":
            recommendations.append("Reportar a coordinación académica")
        elif user_role in ["admin", "coordinator"]:
            recommendations.append("Asignar responsable de seguimiento")
            
        return recommendations
