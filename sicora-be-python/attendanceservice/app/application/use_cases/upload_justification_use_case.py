from datetime import datetime
from typing import Dict
from uuid import UUID

from ...domain.entities import Justification, AttendanceRecord
from ...domain.repositories import JustificationRepository, AttendanceRecordRepository
from ...domain.value_objects import JustificationStatus, AttendanceStatus
from ...domain.exceptions import (
    AttendanceNotFoundError,
    InvalidJustificationFileError,
    JustificationAlreadyProcessedError,
    UnauthorizedAccessError
)
from ..dtos import UploadJustificationRequest, UploadJustificationResponse
from ..interfaces import FileUploadService, UserServiceInterface


class UploadJustificationUseCase:
    """
    Caso de uso para subir justificación de inasistencia (HU-BE-024).
    
    Permite a un aprendiz adjuntar documentos PDF que justifiquen ausencias,
    con validaciones completas de archivos y permisos.
    """

    def __init__(
        self,
        justification_repository: JustificationRepository,
        attendance_repository: AttendanceRecordRepository,
        file_upload_service: FileUploadService,
        user_service: UserServiceInterface
    ):
        self.justification_repository = justification_repository
        self.attendance_repository = attendance_repository
        self.file_upload_service = file_upload_service
        self.user_service = user_service

    async def execute(
        self,
        request: UploadJustificationRequest,
        student_id: UUID
    ) -> UploadJustificationResponse:
        """
        Ejecuta la subida de justificación.
        
        Args:
            request: Datos de la justificación a subir
            student_id: ID del estudiante que sube la justificación
            
        Returns:
            Respuesta con la justificación creada
            
        Raises:
            AttendanceNotFoundError: Si no existe el registro de asistencia
            InvalidJustificationFileError: Si el archivo no es válido
            JustificationAlreadyProcessedError: Si ya existe justificación
            UnauthorizedAccessError: Si el estudiante no tiene permisos
        """
        # Validar que el registro de asistencia existe
        attendance_record = await self.attendance_repository.get_by_id(
            request.attendance_record_id
        )
        if not attendance_record:
            raise AttendanceNotFoundError(str(request.attendance_record_id))

        # Validar que el estudiante es el dueño del registro de asistencia
        if attendance_record.student_id != student_id:
            raise UnauthorizedAccessError(
                f"attendance record {request.attendance_record_id}",
                "aprendiz"
            )

        # Validar que el registro esté marcado como ausente
        if not attendance_record.is_absent():
            raise InvalidJustificationFileError(
                f"Cannot justify attendance with status {attendance_record.status.value}"
            )

        # Verificar que no exista ya una justificación
        existing_justification = await self.justification_repository.get_by_attendance_record(
            request.attendance_record_id
        )
        if existing_justification:
            raise JustificationAlreadyProcessedError(
                str(existing_justification.id),
                existing_justification.status.value
            )

        # Validar archivo PDF
        await self._validate_pdf_file(request)

        # Subir archivo al almacenamiento
        file_path = await self.file_upload_service.upload_file(
            file_content=request.file_content,
            file_name=request.file_name,
            file_type="application/pdf",
            max_size_mb=5
        )

        # Crear entidad de justificación
        justification = Justification(
            student_id=student_id,
            attendance_record_id=request.attendance_record_id,
            reason=request.reason.strip(),
            file_path=file_path,
            status=JustificationStatus.PENDING,
            submitted_at=datetime.now()
        )

        # Guardar en repositorio
        saved_justification = await self.justification_repository.save(justification)

        # Preparar respuesta
        return UploadJustificationResponse(
            id=saved_justification.id,
            attendance_record_id=saved_justification.attendance_record_id,
            student_id=saved_justification.student_id,
            reason=saved_justification.reason,
            file_path=saved_justification.file_path,
            status=saved_justification.status,
            submitted_at=saved_justification.submitted_at,
            message="Justificación subida exitosamente. Está pendiente de revisión por parte del instructor."
        )

    async def _validate_pdf_file(self, request: UploadJustificationRequest) -> None:
        """Valida que el archivo sea un PDF válido."""
        
        # Validar tamaño del archivo
        max_size_bytes = 5 * 1024 * 1024  # 5MB
        if request.file_size > max_size_bytes:
            raise InvalidJustificationFileError(
                f"File size {request.file_size} bytes exceeds maximum of {max_size_bytes} bytes"
            )

        # Validar extensión del archivo
        if not request.file_name.lower().endswith('.pdf'):
            raise InvalidJustificationFileError(
                "Only PDF files are allowed for justifications"
            )

        # Validar contenido del archivo usando el servicio
        is_valid = self.file_upload_service.validate_file(
            file_content=request.file_content,
            file_name=request.file_name,
            allowed_types=["application/pdf"]
        )
        
        if not is_valid:
            raise InvalidJustificationFileError(
                "Invalid PDF file or corrupted content"
            )

        # Validar que la razón no esté vacía
        if not request.reason or not request.reason.strip():
            raise InvalidJustificationFileError(
                "Justification reason cannot be empty"
            )

        # Validar longitud mínima de la razón
        if len(request.reason.strip()) < 10:
            raise InvalidJustificationFileError(
                "Justification reason must be at least 10 characters long"
            )
