from datetime import date, timedelta
from math import ceil
from typing import List
from uuid import UUID

from ...domain.repositories import AttendanceRecordRepository
from ...domain.exceptions import UnauthorizedAccessError
from ..dtos import (
    AttendanceHistoryRequest, 
    AttendanceHistoryResponse, 
    AttendanceHistoryRecord
)
from ..interfaces import UserServiceInterface, ScheduleServiceInterface


class GetAttendanceHistoryUseCase:
    """
    Caso de uso para obtener historial de asistencia (HU-BE-023).
    
    Proporciona el registro detallado de asistencia con paginación,
    filtros avanzados y respeto a permisos por rol.
    """

    def __init__(
        self,
        attendance_repository: AttendanceRecordRepository,
        user_service: UserServiceInterface,
        schedule_service: ScheduleServiceInterface
    ):
        self.attendance_repository = attendance_repository
        self.user_service = user_service
        self.schedule_service = schedule_service

    async def execute(
        self,
        request: AttendanceHistoryRequest,
        requesting_user_id: UUID
    ) -> AttendanceHistoryResponse:
        """
        Ejecuta la consulta de historial de asistencia.
        
        Args:
            request: Filtros y parámetros de paginación
            requesting_user_id: ID del usuario que solicita
            
        Returns:
            Historial paginado de registros de asistencia
            
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

        # Validar parámetros de paginación
        request.page = max(1, request.page)
        request.page_size = min(100, max(1, request.page_size))

        # Obtener registros del repositorio
        if request.student_id:
            attendance_records = await self.attendance_repository.get_by_student_and_period(
                request.student_id,
                request.start_date,
                request.end_date
            )
        elif request.instructor_id:
            attendance_records = await self.attendance_repository.get_by_instructor_and_period(
                request.instructor_id,
                request.start_date,
                request.end_date
            )
        else:
            # Obtener registros generales con filtros
            summary_data = await self.attendance_repository.get_attendance_summary(
                student_id=request.student_id,
                ficha_id=request.ficha_id,
                instructor_id=request.instructor_id,
                start_date=request.start_date,
                end_date=request.end_date
            )
            attendance_records = summary_data.get("detailed_records", [])

        # Aplicar filtro de estado si se especifica
        if request.status:
            attendance_records = [
                record for record in attendance_records 
                if record.status == request.status
            ]

        # Calcular paginación
        total_records = len(attendance_records)
        total_pages = ceil(total_records / request.page_size)
        start_index = (request.page - 1) * request.page_size
        end_index = start_index + request.page_size
        paginated_records = attendance_records[start_index:end_index]

        # Enriquecer registros con información adicional
        enriched_records = await self._enrich_records(paginated_records)

        return AttendanceHistoryResponse(
            records=enriched_records,
            total_records=total_records,
            page=request.page,
            page_size=request.page_size,
            total_pages=total_pages
        )

    async def _validate_and_adjust_filters(
        self,
        request: AttendanceHistoryRequest,
        user_id: UUID,
        user_role: str
    ) -> None:
        """Valida permisos y ajusta filtros según el rol del usuario."""
        
        if user_role == "aprendiz":
            # Los aprendices solo pueden ver su propio historial
            if request.student_id and request.student_id != user_id:
                raise UnauthorizedAccessError(
                    "attendance history of other students",
                    user_role
                )
            request.student_id = user_id
            request.instructor_id = None
            
        elif user_role == "instructor":
            # Los instructores pueden ver historial de sus fichas asignadas
            if request.ficha_id:
                is_assigned = await self.user_service.validate_instructor_ficha_assignment(
                    user_id,
                    request.ficha_id
                )
                if not is_assigned:
                    raise UnauthorizedAccessError(
                        f"attendance history for ficha {request.ficha_id}",
                        user_role
                    )
            
            # Si consultan por estudiante específico, validar que esté en sus fichas
            if request.student_id:
                # Obtener fichas del instructor
                instructor_fichas = await self.user_service.get_instructor_fichas(user_id)
                ficha_ids = [ficha["id"] for ficha in instructor_fichas]
                
                # Verificar que el estudiante esté en alguna de esas fichas
                student_in_instructor_fichas = False
                for ficha_id in ficha_ids:
                    if await self.user_service.validate_student_ficha_enrollment(
                        request.student_id, ficha_id
                    ):
                        student_in_instructor_fichas = True
                        break
                
                if not student_in_instructor_fichas:
                    raise UnauthorizedAccessError(
                        f"attendance history for student {request.student_id}",
                        user_role
                    )
                    
        elif user_role in ["admin", "coordinator"]:
            # Administradores y coordinadores tienen acceso completo
            pass
        else:
            raise UnauthorizedAccessError("attendance history", user_role)

    async def _enrich_records(
        self,
        records: List
    ) -> List[AttendanceHistoryRecord]:
        """Enriquece los registros con información adicional de usuarios y horarios."""
        
        enriched_records = []
        
        for record in records:
            # Obtener información del estudiante
            student_info = await self.user_service.get_user_by_id(record.student_id)
            student_name = "Usuario no encontrado"
            if student_info:
                student_name = f"{student_info.get('first_name', '')} {student_info.get('last_name', '')}".strip()
            
            # Obtener información del instructor
            instructor_info = await self.user_service.get_user_by_id(record.instructor_id)
            instructor_name = "Usuario no encontrado"
            if instructor_info:
                instructor_name = f"{instructor_info.get('first_name', '')} {instructor_info.get('last_name', '')}".strip()
            
            # Obtener información del horario
            schedule_info = await self.schedule_service.get_schedule_by_id(record.schedule_id)
            ficha_name = "Ficha no encontrada"
            if schedule_info:
                ficha_name = schedule_info.get("ficha_name", "Ficha no encontrada")

            enriched_record = AttendanceHistoryRecord(
                id=record.id,
                student_id=record.student_id,
                student_name=student_name,
                instructor_id=record.instructor_id,
                instructor_name=instructor_name,
                ficha_id=schedule_info.get("ficha_id") if schedule_info else record.student_id,  # Temporal
                ficha_name=ficha_name,
                date=record.date.date(),
                block_identifier=record.block_identifier,
                status=record.status,
                notes=record.notes,
                recorded_at=record.recorded_at
            )
            
            enriched_records.append(enriched_record)
        
        return enriched_records
