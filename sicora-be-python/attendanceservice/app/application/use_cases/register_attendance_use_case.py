from datetime import datetime, date
from typing import Dict
from uuid import UUID

from ...domain.entities import AttendanceRecord
from ...domain.repositories import AttendanceRecordRepository
from ...domain.value_objects import AttendanceStatus
from ...domain.exceptions import (
    DuplicateAttendanceError,
    InvalidQRCodeError,
    InstructorNotAssignedError,
    StudentNotInFichaError,
    FutureDateNotAllowedError
)
from ..dtos import RegisterAttendanceRequest, RegisterAttendanceResponse
from ..interfaces import QRCodeService, UserServiceInterface, ScheduleServiceInterface


class RegisterAttendanceUseCase:
    """
    Caso de uso para registrar asistencia de estudiantes (HU-BE-021).
    
    Permite a un instructor registrar la asistencia de estudiantes mediante
    código QR con validaciones de negocio completas.
    """

    def __init__(
        self,
        attendance_repository: AttendanceRecordRepository,
        qr_service: QRCodeService,
        user_service: UserServiceInterface,
        schedule_service: ScheduleServiceInterface
    ):
        self.attendance_repository = attendance_repository
        self.qr_service = qr_service
        self.user_service = user_service
        self.schedule_service = schedule_service

    async def execute(
        self,
        request: RegisterAttendanceRequest,
        instructor_id: UUID
    ) -> RegisterAttendanceResponse:
        """
        Ejecuta el registro de asistencia.
        
        Args:
            request: Datos de la solicitud de registro
            instructor_id: ID del instructor que registra
            
        Returns:
            Respuesta con el registro de asistencia creado
            
        Raises:
            DuplicateAttendanceError: Si ya existe registro para el día
            InvalidQRCodeError: Si el código QR es inválido
            InstructorNotAssignedError: Si el instructor no está asignado
            StudentNotInFichaError: Si el estudiante no pertenece a la ficha
            FutureDateNotAllowedError: Si se intenta registrar fecha futura
        """
        current_date = datetime.now().date()
        
        # Validar que no sea fecha futura
        if current_date > date.today():
            raise FutureDateNotAllowedError(current_date.isoformat())

        # Validar código QR
        qr_data = await self.qr_service.validate_qr_code(
            request.qr_code,
            str(request.student_id),
            str(request.ficha_id)
        )

        # Extraer datos del QR validado
        schedule_id = UUID(qr_data["schedule_id"])
        venue_id = UUID(qr_data["venue_id"])

        # Validar que el instructor esté asignado a la ficha
        is_assigned = await self.user_service.validate_instructor_ficha_assignment(
            instructor_id,
            request.ficha_id
        )
        if not is_assigned:
            raise InstructorNotAssignedError(
                str(instructor_id),
                str(request.ficha_id),
                request.block_identifier
            )

        # Validar que el estudiante pertenezca a la ficha
        is_enrolled = await self.user_service.validate_student_ficha_enrollment(
            request.student_id,
            request.ficha_id
        )
        if not is_enrolled:
            raise StudentNotInFichaError(
                str(request.student_id),
                str(request.ficha_id)
            )

        # Verificar que no exista registro duplicado
        existing_record = await self.attendance_repository.get_by_student_and_date(
            request.student_id,
            current_date,
            request.block_identifier
        )
        if existing_record:
            raise DuplicateAttendanceError(
                str(request.student_id),
                current_date.isoformat(),
                request.block_identifier
            )

        # Crear registro de asistencia
        attendance_record = AttendanceRecord(
            student_id=request.student_id,
            schedule_id=schedule_id,
            instructor_id=instructor_id,
            date=datetime.combine(current_date, datetime.min.time()),
            block_identifier=request.block_identifier,
            venue_id=venue_id,
            status=AttendanceStatus.PRESENT,
            qr_code_used=request.qr_code,
            notes=request.notes,
            recorded_at=datetime.now()
        )

        # Guardar en repositorio
        saved_record = await self.attendance_repository.save(attendance_record)

        # Preparar respuesta
        return RegisterAttendanceResponse(
            id=saved_record.id,
            student_id=saved_record.student_id,
            instructor_id=saved_record.instructor_id,
            ficha_id=request.ficha_id,
            date=saved_record.date.date(),
            block_identifier=saved_record.block_identifier,
            status=saved_record.status,
            qr_code_used=saved_record.qr_code_used,
            notes=saved_record.notes,
            recorded_at=saved_record.recorded_at,
            message="Asistencia registrada exitosamente"
        )
