"""Tests unitarios para RegisterAttendanceUseCase."""

import pytest
from unittest.mock import AsyncMock, Mock
from datetime import datetime, date, timedelta
from uuid import uuid4

from app.application.use_cases.register_attendance_use_case import RegisterAttendanceUseCase
from app.application.dtos.attendance_dtos import RegisterAttendanceRequest, RegisterAttendanceResponse
from app.domain.entities.attendance_record import AttendanceRecord
from app.domain.value_objects import AttendanceStatus
from app.domain.exceptions import (
    DuplicateAttendanceError,
    InvalidQRCodeError,
    InstructorNotAssignedError,
    StudentNotInFichaError,
    FutureDateNotAllowedError
)


class TestRegisterAttendanceUseCase:
    """Test cases para RegisterAttendanceUseCase."""

    @pytest.fixture
    def use_case(self, mock_attendance_repository, mock_qr_service, mock_user_service, mock_schedule_service):
        """Instancia del caso de uso con dependencias mockeadas."""
        return RegisterAttendanceUseCase(
            attendance_repository=mock_attendance_repository,
            qr_service=mock_qr_service,
            user_service=mock_user_service,
            schedule_service=mock_schedule_service
        )

    @pytest.fixture
    def valid_request(self, sample_student_id, sample_ficha_id, sample_qr_code):
        """Request válido para registro de asistencia."""
        return RegisterAttendanceRequest(
            student_id=sample_student_id,
            ficha_id=sample_ficha_id,
            block_identifier="BLOQUE_1",
            qr_code=sample_qr_code,
            notes="Asistencia puntual"
        )

    @pytest.mark.asyncio
    async def test_register_attendance_success(
        self,
        use_case,
        valid_request,
        mock_attendance_repository,
        mock_qr_service,
        mock_user_service,
        mock_schedule_service,
        sample_instructor_id,
        valid_qr_data,
        sample_attendance_record
    ):
        """Test exitoso de registro de asistencia."""
        # Arrange
        mock_qr_service.validate_qr_code.return_value = valid_qr_data
        mock_user_service.validate_instructor_ficha_assignment.return_value = True
        mock_user_service.validate_student_ficha_enrollment.return_value = True
        mock_attendance_repository.get_by_student_and_date.return_value = None
        mock_attendance_repository.save.return_value = sample_attendance_record

        # Act
        result = await use_case.execute(valid_request, sample_instructor_id)

        # Assert
        assert isinstance(result, RegisterAttendanceResponse)
        assert result.student_id == valid_request.student_id
        assert result.instructor_id == sample_instructor_id
        assert result.ficha_id == valid_request.ficha_id
        assert result.block_identifier == valid_request.block_identifier
        assert result.status == AttendanceStatus.PRESENT
        assert result.message == "Asistencia registrada exitosamente"

        # Verificar llamadas a servicios
        mock_qr_service.validate_qr_code.assert_called_once_with(
            valid_request.qr_code,
            str(valid_request.student_id),
            str(valid_request.ficha_id)
        )
        mock_user_service.validate_instructor_ficha_assignment.assert_called_once_with(
            sample_instructor_id,
            valid_request.ficha_id
        )
        mock_user_service.validate_student_ficha_enrollment.assert_called_once_with(
            valid_request.student_id,
            valid_request.ficha_id
        )
        mock_attendance_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_attendance_invalid_qr_code(
        self,
        use_case,
        valid_request,
        mock_qr_service,
        sample_instructor_id
    ):
        """Test falla con código QR inválido."""
        # Arrange
        mock_qr_service.validate_qr_code.side_effect = InvalidQRCodeError("Invalid QR code")

        # Act & Assert
        with pytest.raises(InvalidQRCodeError):
            await use_case.execute(valid_request, sample_instructor_id)

        mock_qr_service.validate_qr_code.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_attendance_instructor_not_assigned(
        self,
        use_case,
        valid_request,
        mock_qr_service,
        mock_user_service,
        sample_instructor_id,
        valid_qr_data
    ):
        """Test falla cuando instructor no está asignado a la ficha."""
        # Arrange
        mock_qr_service.validate_qr_code.return_value = valid_qr_data
        mock_user_service.validate_instructor_ficha_assignment.return_value = False

        # Act & Assert
        with pytest.raises(InstructorNotAssignedError):
            await use_case.execute(valid_request, sample_instructor_id)

        mock_user_service.validate_instructor_ficha_assignment.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_attendance_student_not_in_ficha(
        self,
        use_case,
        valid_request,
        mock_qr_service,
        mock_user_service,
        sample_instructor_id,
        valid_qr_data
    ):
        """Test falla cuando estudiante no pertenece a la ficha."""
        # Arrange
        mock_qr_service.validate_qr_code.return_value = valid_qr_data
        mock_user_service.validate_instructor_ficha_assignment.return_value = True
        mock_user_service.validate_student_ficha_enrollment.return_value = False

        # Act & Assert
        with pytest.raises(StudentNotInFichaError):
            await use_case.execute(valid_request, sample_instructor_id)

        mock_user_service.validate_student_ficha_enrollment.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_attendance_duplicate_record(
        self,
        use_case,
        valid_request,
        mock_attendance_repository,
        mock_qr_service,
        mock_user_service,
        sample_instructor_id,
        valid_qr_data,
        sample_attendance_record
    ):
        """Test falla cuando ya existe registro duplicado."""
        # Arrange
        mock_qr_service.validate_qr_code.return_value = valid_qr_data
        mock_user_service.validate_instructor_ficha_assignment.return_value = True
        mock_user_service.validate_student_ficha_enrollment.return_value = True
        mock_attendance_repository.get_by_student_and_date.return_value = sample_attendance_record

        # Act & Assert
        with pytest.raises(DuplicateAttendanceError):
            await use_case.execute(valid_request, sample_instructor_id)

        mock_attendance_repository.get_by_student_and_date.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_attendance_validates_qr_parameters(
        self,
        use_case,
        valid_request,
        mock_qr_service,
        sample_instructor_id
    ):
        """Test verifica que los parámetros correctos se pasan al servicio QR."""
        # Arrange
        mock_qr_service.validate_qr_code.side_effect = InvalidQRCodeError("Test error")

        # Act & Assert
        with pytest.raises(InvalidQRCodeError):
            await use_case.execute(valid_request, sample_instructor_id)

        # Verificar parámetros exactos
        mock_qr_service.validate_qr_code.assert_called_once_with(
            valid_request.qr_code,
            str(valid_request.student_id),
            str(valid_request.ficha_id)
        )

    @pytest.mark.asyncio
    async def test_register_attendance_creates_correct_entity(
        self,
        use_case,
        valid_request,
        mock_attendance_repository,
        mock_qr_service,
        mock_user_service,
        sample_instructor_id,
        valid_qr_data
    ):
        """Test verifica que se crea la entidad correctamente."""
        # Arrange
        saved_record = AttendanceRecord(
            id=uuid4(),
            student_id=valid_request.student_id,
            schedule_id=uuid4(),
            instructor_id=sample_instructor_id,
            date=datetime.now(),
            block_identifier=valid_request.block_identifier,
            venue_id=uuid4(),
            status=AttendanceStatus.PRESENT,
            qr_code_used=valid_request.qr_code,
            notes=valid_request.notes
        )

        mock_qr_service.validate_qr_code.return_value = valid_qr_data
        mock_user_service.validate_instructor_ficha_assignment.return_value = True
        mock_user_service.validate_student_ficha_enrollment.return_value = True
        mock_attendance_repository.get_by_student_and_date.return_value = None
        mock_attendance_repository.save.return_value = saved_record

        # Act
        result = await use_case.execute(valid_request, sample_instructor_id)

        # Assert
        # Verificar que save fue llamado con una entidad AttendanceRecord
        save_call_args = mock_attendance_repository.save.call_args[0][0]
        assert isinstance(save_call_args, AttendanceRecord)
        assert save_call_args.student_id == valid_request.student_id
        assert save_call_args.instructor_id == sample_instructor_id
        assert save_call_args.block_identifier == valid_request.block_identifier
        assert save_call_args.status == AttendanceStatus.PRESENT
        assert save_call_args.qr_code_used == valid_request.qr_code
        assert save_call_args.notes == valid_request.notes

        # Verificar respuesta
        assert result.id == saved_record.id
        assert result.student_id == saved_record.student_id
        assert result.instructor_id == saved_record.instructor_id

    @pytest.mark.asyncio
    async def test_register_attendance_handles_none_notes(
        self,
        use_case,
        sample_student_id,
        sample_ficha_id,
        sample_qr_code,
        mock_attendance_repository,
        mock_qr_service,
        mock_user_service,
        sample_instructor_id,
        valid_qr_data,
        sample_attendance_record
    ):
        """Test maneja correctamente notas nulas."""
        # Arrange
        request_without_notes = RegisterAttendanceRequest(
            student_id=sample_student_id,
            ficha_id=sample_ficha_id,
            block_identifier="BLOQUE_1",
            qr_code=sample_qr_code,
            notes=None
        )

        mock_qr_service.validate_qr_code.return_value = valid_qr_data
        mock_user_service.validate_instructor_ficha_assignment.return_value = True
        mock_user_service.validate_student_ficha_enrollment.return_value = True
        mock_attendance_repository.get_by_student_and_date.return_value = None
        mock_attendance_repository.save.return_value = sample_attendance_record

        # Act
        result = await use_case.execute(request_without_notes, sample_instructor_id)

        # Assert
        assert isinstance(result, RegisterAttendanceResponse)
        save_call_args = mock_attendance_repository.save.call_args[0][0]
        assert save_call_args.notes is None

    @pytest.mark.asyncio
    async def test_register_attendance_correct_date_validation(
        self,
        use_case,
        valid_request,
        mock_attendance_repository,
        mock_qr_service,
        mock_user_service,
        sample_instructor_id,
        valid_qr_data
    ):
        """Test verifica validación correcta de fecha."""
        # Arrange
        mock_qr_service.validate_qr_code.return_value = valid_qr_data
        mock_user_service.validate_instructor_ficha_assignment.return_value = True
        mock_user_service.validate_student_ficha_enrollment.return_value = True
        mock_attendance_repository.get_by_student_and_date.return_value = None

        # Act
        await use_case.execute(valid_request, sample_instructor_id)

        # Assert - verificar que get_by_student_and_date fue llamado con fecha de hoy
        call_args = mock_attendance_repository.get_by_student_and_date.call_args
        called_date = call_args[0][1]  # segundo parámetro
        assert isinstance(called_date, date)
        assert called_date == date.today()
