from datetime import date, datetime, timedelta
from typing import Optional, Dict, List
from uuid import UUID

from ...domain.repositories import AttendanceRecordRepository
from ...domain.exceptions import UnauthorizedAccessError
from ..dtos import AttendanceSummaryRequest, AttendanceSummaryResponse
from ..interfaces import UserServiceInterface


class GetAttendanceSummaryUseCase:
    """
    Caso de uso para obtener resumen de asistencia (HU-BE-022).
    
    Proporciona estadísticas de asistencia con filtros opcionales,
    respetando los permisos según el rol del usuario.
    """

    def __init__(
        self,
        attendance_repository: AttendanceRecordRepository,
        user_service: UserServiceInterface
    ):
        self.attendance_repository = attendance_repository
        self.user_service = user_service

    async def execute(
        self,
        request: AttendanceSummaryRequest,
        requesting_user_id: UUID
    ) -> AttendanceSummaryResponse:
        """
        Ejecuta la consulta de resumen de asistencia.
        
        Args:
            request: Filtros para el resumen
            requesting_user_id: ID del usuario que solicita
            
        Returns:
            Resumen estadístico de asistencia
            
        Raises:
            UnauthorizedAccessError: Si el usuario no tiene permisos
        """
        # Obtener rol del usuario solicitante
        user_role = await self.user_service.get_user_role(requesting_user_id)
        
        # Validar permisos y ajustar filtros según el rol
        await self._validate_and_adjust_filters(request, requesting_user_id, user_role)

        # Establecer fechas por defecto si no se proporcionan
        if not request.start_date:
            request.start_date = date.today() - timedelta(days=30)
        if not request.end_date:
            request.end_date = date.today()

        # Obtener resumen desde el repositorio
        summary_data = await self.attendance_repository.get_attendance_summary(
            student_id=request.student_id,
            ficha_id=request.ficha_id,
            instructor_id=request.instructor_id,
            start_date=request.start_date,
            end_date=request.end_date
        )

        # Enriquecer datos según el rol
        enhanced_data = await self._enhance_summary_data(summary_data, user_role, request)

        return AttendanceSummaryResponse(
            total_sessions=summary_data.get("total_sessions", 0),
            present_count=summary_data.get("present_count", 0),
            absent_count=summary_data.get("absent_count", 0),
            justified_count=summary_data.get("justified_count", 0),
            attendance_percentage=summary_data.get("attendance_percentage", 0.0),
            student_details=enhanced_data.get("student_details"),
            top_absent_students=enhanced_data.get("top_absent_students")
        )

    async def _validate_and_adjust_filters(
        self,
        request: AttendanceSummaryRequest,
        user_id: UUID,
        user_role: str
    ) -> None:
        """Valida permisos y ajusta filtros según el rol del usuario."""
        
        if user_role == "aprendiz":
            # Los aprendices solo pueden ver sus propios datos
            if request.student_id and request.student_id != user_id:
                raise UnauthorizedAccessError(
                    "attendance summary of other students",
                    user_role
                )
            request.student_id = user_id
            
            # Los aprendices no pueden filtrar por instructor
            request.instructor_id = None
            
        elif user_role == "instructor":
            # Los instructores pueden ver datos de sus fichas asignadas
            if request.ficha_id:
                is_assigned = await self.user_service.validate_instructor_ficha_assignment(
                    user_id,
                    request.ficha_id
                )
                if not is_assigned:
                    raise UnauthorizedAccessError(
                        f"attendance data for ficha {request.ficha_id}",
                        user_role
                    )
            
            # Si no se especifica ficha, limitar a las fichas del instructor
            if not request.ficha_id:
                request.instructor_id = user_id
                
        elif user_role in ["admin", "coordinator"]:
            # Administradores y coordinadores tienen acceso completo
            pass
        else:
            raise UnauthorizedAccessError("attendance summary", user_role)

    async def _enhance_summary_data(
        self,
        summary_data: Dict,
        user_role: str,
        request: AttendanceSummaryRequest
    ) -> Dict:
        """Enriquece los datos del resumen según el rol y contexto."""
        
        enhanced = {}
        
        # Para aprendices específicos, agregar detalles personalizados
        if request.student_id and user_role in ["instructor", "admin", "coordinator"]:
            student_info = await self.user_service.get_user_by_id(request.student_id)
            if student_info:
                enhanced["student_details"] = {
                    "student_id": request.student_id,
                    "student_name": f"{student_info.get('first_name', '')} {student_info.get('last_name', '')}",
                    "document_number": student_info.get("document_number"),
                    "ficha_name": student_info.get("ficha_name"),
                    "attendance_trend": summary_data.get("attendance_trend", [])
                }
        
        # Para instructores y admins, agregar top de estudiantes con más faltas
        if user_role in ["instructor", "admin", "coordinator"] and not request.student_id:
            enhanced["top_absent_students"] = summary_data.get("top_absent_students", [])
        
        return enhanced
