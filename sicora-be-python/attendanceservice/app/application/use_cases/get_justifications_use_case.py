from math import ceil
from typing import List
from uuid import UUID

from ...domain.repositories import JustificationRepository
from ...domain.value_objects import JustificationStatus
from ...domain.exceptions import UnauthorizedAccessError
from ..dtos import (
    GetJustificationsRequest,
    GetJustificationsResponse,
    JustificationDetail
)
from ..interfaces import UserServiceInterface, ScheduleServiceInterface


class GetJustificationsUseCase:
    """
    Caso de uso para obtener lista de justificaciones.
    
    Permite consultar justificaciones con filtros por estado, estudiante,
    instructor o ficha, respetando permisos por rol.
    """

    def __init__(
        self,
        justification_repository: JustificationRepository,
        user_service: UserServiceInterface,
        schedule_service: ScheduleServiceInterface
    ):
        self.justification_repository = justification_repository
        self.user_service = user_service
        self.schedule_service = schedule_service

    async def execute(
        self,
        request: GetJustificationsRequest,
        requesting_user_id: UUID
    ) -> GetJustificationsResponse:
        """
        Ejecuta la consulta de justificaciones.
        
        Args:
            request: Filtros para la consulta
            requesting_user_id: ID del usuario que solicita
            
        Returns:
            Lista paginada de justificaciones con detalles
            
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

        # Obtener justificaciones según los filtros
        if request.student_id:
            justifications = await self.justification_repository.get_by_student(
                request.student_id
            )
        elif request.instructor_id:
            justifications = await self.justification_repository.get_pending_for_instructor(
                request.instructor_id
            )
        elif request.status:
            justifications = await self.justification_repository.get_by_status(
                request.status,
                student_id=request.student_id,
                instructor_id=request.instructor_id
            )
        else:
            # Para administradores, obtener todas según filtros
            justifications = await self.justification_repository.get_by_status(
                request.status or JustificationStatus.PENDING
            )

        # Aplicar filtros adicionales si es necesario
        if request.ficha_id:
            justifications = await self._filter_by_ficha(justifications, request.ficha_id)

        # Calcular estadísticas
        stats = self._calculate_statistics(justifications)

        # Aplicar paginación
        total_justifications = len(justifications)
        total_pages = ceil(total_justifications / request.page_size)
        start_index = (request.page - 1) * request.page_size
        end_index = start_index + request.page_size
        paginated_justifications = justifications[start_index:end_index]

        # Enriquecer justificaciones con información adicional
        enriched_justifications = await self._enrich_justifications(
            paginated_justifications
        )

        return GetJustificationsResponse(
            justifications=enriched_justifications,
            total_justifications=total_justifications,
            pending_count=stats["pending_count"],
            approved_count=stats["approved_count"],
            rejected_count=stats["rejected_count"],
            page=request.page,
            page_size=request.page_size,
            total_pages=total_pages
        )

    async def _validate_and_adjust_filters(
        self,
        request: GetJustificationsRequest,
        user_id: UUID,
        user_role: str
    ) -> None:
        """Valida permisos y ajusta filtros según el rol del usuario."""
        
        if user_role == "aprendiz":
            # Los aprendices solo pueden ver sus propias justificaciones
            if request.student_id and request.student_id != user_id:
                raise UnauthorizedAccessError(
                    "justifications of other students",
                    user_role
                )
            request.student_id = user_id
            request.instructor_id = None
            
        elif user_role == "instructor":
            # Los instructores pueden ver justificaciones de sus fichas
            if request.student_id:
                # Verificar que el estudiante esté en las fichas del instructor
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
                        f"justifications for student {request.student_id}",
                        user_role
                    )
            
            # Si no se especifica estudiante, obtener justificaciones pendientes del instructor
            if not request.student_id:
                request.instructor_id = user_id
                
        elif user_role in ["admin", "coordinator"]:
            # Administradores y coordinadores tienen acceso completo
            pass
        else:
            raise UnauthorizedAccessError("justifications", user_role)

    async def _filter_by_ficha(
        self,
        justifications: List,
        ficha_id: UUID
    ) -> List:
        """Filtra justificaciones por ficha específica."""
        filtered_justifications = []
        
        for justification in justifications:
            # Verificar si el estudiante pertenece a la ficha
            is_enrolled = await self.user_service.validate_student_ficha_enrollment(
                justification.student_id,
                ficha_id
            )
            if is_enrolled:
                filtered_justifications.append(justification)
        
        return filtered_justifications

    def _calculate_statistics(self, justifications: List) -> dict:
        """Calcula estadísticas de las justificaciones."""
        pending_count = sum(1 for j in justifications if j.status == JustificationStatus.PENDING)
        approved_count = sum(1 for j in justifications if j.status == JustificationStatus.APPROVED)
        rejected_count = sum(1 for j in justifications if j.status == JustificationStatus.REJECTED)
        
        return {
            "pending_count": pending_count,
            "approved_count": approved_count,
            "rejected_count": rejected_count
        }

    async def _enrich_justifications(
        self,
        justifications: List
    ) -> List[JustificationDetail]:
        """Enriquece las justificaciones con información adicional."""
        enriched_justifications = []
        
        for justification in justifications:
            # Obtener información del estudiante
            student_info = await self.user_service.get_user_by_id(justification.student_id)
            student_name = "Usuario no encontrado"
            if student_info:
                student_name = f"{student_info.get('first_name', '')} {student_info.get('last_name', '')}".strip()

            # Obtener información del revisor si existe
            reviewed_by_name = None
            if justification.reviewed_by:
                reviewer_info = await self.user_service.get_user_by_id(justification.reviewed_by)
                if reviewer_info:
                    reviewed_by_name = f"{reviewer_info.get('first_name', '')} {reviewer_info.get('last_name', '')}".strip()

            # Crear el detalle enriquecido
            detail = JustificationDetail(
                id=justification.id,
                attendance_record_id=justification.attendance_record_id,
                student_id=justification.student_id,
                student_name=student_name,
                ficha_id=student_info.get("ficha_id") if student_info else justification.student_id,  # Temporal
                ficha_name=student_info.get("ficha_name", "Ficha no encontrada") if student_info else "Ficha no encontrada",
                absence_date=justification.submitted_at,  # Temporal, debería ser fecha de inasistencia
                block_identifier="N/A",  # Se debería obtener del attendance_record
                reason=justification.reason,
                file_path=justification.file_path,
                status=justification.status,
                submitted_at=justification.submitted_at,
                reviewed_at=justification.reviewed_at,
                reviewed_by=justification.reviewed_by,
                reviewed_by_name=reviewed_by_name,
                review_comments=justification.review_comments,
                days_since_submission=justification.days_since_submission()
            )
            
            enriched_justifications.append(detail)
        
        return enriched_justifications
