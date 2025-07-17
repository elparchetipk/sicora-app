from datetime import datetime
from uuid import UUID

from ...domain.entities import Justification, AttendanceRecord
from ...domain.repositories import JustificationRepository, AttendanceRecordRepository
from ...domain.value_objects import JustificationStatus, AttendanceStatus
from ...domain.exceptions import (
    JustificationNotFoundError,
    JustificationAlreadyProcessedError,
    UnauthorizedAccessError,
    AttendanceNotFoundError
)
from ..dtos import ReviewJustificationRequest, ReviewJustificationResponse
from ..interfaces import UserServiceInterface


class ReviewJustificationUseCase:
    """
    Caso de uso para revisar justificaciones (HU-BE-025).
    
    Permite a un instructor aprobar o rechazar justificaciones de aprendices,
    con workflow de aprobación/rechazo y actualización automática de asistencia.
    """

    def __init__(
        self,
        justification_repository: JustificationRepository,
        attendance_repository: AttendanceRecordRepository,
        user_service: UserServiceInterface
    ):
        self.justification_repository = justification_repository
        self.attendance_repository = attendance_repository
        self.user_service = user_service

    async def execute(
        self,
        request: ReviewJustificationRequest,
        instructor_id: UUID
    ) -> ReviewJustificationResponse:
        """
        Ejecuta la revisión de una justificación.
        
        Args:
            request: Datos de la revisión (aprobar/rechazar)
            instructor_id: ID del instructor que revisa
            
        Returns:
            Respuesta con el resultado de la revisión
            
        Raises:
            JustificationNotFoundError: Si no existe la justificación
            JustificationAlreadyProcessedError: Si ya fue procesada
            UnauthorizedAccessError: Si el instructor no tiene permisos
        """
        # Validar que la justificación existe
        justification = await self.justification_repository.get_by_id(
            request.justification_id
        )
        if not justification:
            raise JustificationNotFoundError(str(request.justification_id))

        # Validar que la justificación esté pendiente
        if not justification.is_pending():
            raise JustificationAlreadyProcessedError(
                str(justification.id),
                justification.status.value
            )

        # Obtener el registro de asistencia asociado
        attendance_record = await self.attendance_repository.get_by_id(
            justification.attendance_record_id
        )
        if not attendance_record:
            raise AttendanceNotFoundError(str(justification.attendance_record_id))

        # Validar permisos del instructor (debe estar asignado a la ficha del estudiante)
        await self._validate_instructor_permissions(
            instructor_id,
            justification.student_id
        )

        # Procesar la justificación según la acción
        attendance_updated = False
        
        if request.action.lower() == "approve":
            # Aprobar justificación
            justification.approve(instructor_id, request.comments)
            
            # Actualizar estado de asistencia a justificado
            attendance_record.mark_justified(
                notes=f"Justificación aprobada. {request.comments or ''}".strip()
            )
            await self.attendance_repository.save(attendance_record)
            attendance_updated = True
            
        elif request.action.lower() == "reject":
            # Validar que se proporcionen comentarios para rechazo
            if not request.comments or not request.comments.strip():
                raise ValueError("Comments are required when rejecting a justification")
            
            # Rechazar justificación
            justification.reject(instructor_id, request.comments)
            
            # Mantener el registro de asistencia como ausente
            attendance_record.notes = f"Justificación rechazada. {request.comments}".strip()
            await self.attendance_repository.save(attendance_record)
            
        else:
            raise ValueError(f"Invalid action: {request.action}. Must be 'approve' or 'reject'")

        # Guardar justificación actualizada
        saved_justification = await self.justification_repository.save(justification)

        # Preparar respuesta
        action_message = "aprobada" if request.action.lower() == "approve" else "rechazada"
        status_message = "justificada" if request.action.lower() == "approve" else "ausente"
        
        return ReviewJustificationResponse(
            id=saved_justification.id,
            attendance_record_id=saved_justification.attendance_record_id,
            student_id=saved_justification.student_id,
            status=saved_justification.status,
            reviewed_by=saved_justification.reviewed_by,
            reviewed_at=saved_justification.reviewed_at,
            review_comments=saved_justification.review_comments,
            attendance_updated=attendance_updated,
            message=f"Justificación {action_message} exitosamente. La asistencia quedó marcada como {status_message}."
        )

    async def _validate_instructor_permissions(
        self,
        instructor_id: UUID,
        student_id: UUID
    ) -> None:
        """
        Valida que el instructor tenga permisos para revisar justificaciones del estudiante.
        
        Args:
            instructor_id: ID del instructor
            student_id: ID del estudiante
            
        Raises:
            UnauthorizedAccessError: Si el instructor no tiene permisos
        """
        # Obtener las fichas del instructor
        instructor_fichas = await self.user_service.get_instructor_fichas(instructor_id)
        
        if not instructor_fichas:
            raise UnauthorizedAccessError(
                f"justification review for student {student_id}",
                "instructor"
            )

        # Verificar que el estudiante esté en alguna de las fichas del instructor
        student_in_instructor_fichas = False
        
        for ficha in instructor_fichas:
            ficha_id = ficha.get("id")
            if ficha_id:
                is_enrolled = await self.user_service.validate_student_ficha_enrollment(
                    student_id,
                    ficha_id
                )
                if is_enrolled:
                    student_in_instructor_fichas = True
                    break

        if not student_in_instructor_fichas:
            raise UnauthorizedAccessError(
                f"justification review for student {student_id} (not in instructor's fichas)",
                "instructor"
            )
