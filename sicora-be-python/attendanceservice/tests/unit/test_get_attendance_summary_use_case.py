"""Tests unitarios para GetAttendanceSummaryUseCase."""

import pytest
from unittest.mock import AsyncMock
from datetime import date, timedelta
from uuid import uuid4

from app.application.use_cases.get_attendance_summary_use_case import GetAttendanceSummaryUseCase
from app.application.dtos.attendance_dtos import AttendanceSummaryRequest, AttendanceSummaryResponse
from app.domain.exceptions import UnauthorizedAccessError


class TestGetAttendanceSummaryUseCase:
    """Test cases para GetAttendanceSummaryUseCase."""

    @pytest.fixture
    def use_case(self, mock_attendance_repository, mock_user_service):
        """Instancia del caso de uso con dependencias mockeadas."""
        return GetAttendanceSummaryUseCase(
            attendance_repository=mock_attendance_repository,
            user_service=mock_user_service
        )

    @pytest.fixture
    def sample_summary_data(self):
        """Datos de resumen de ejemplo."""
        return {
            "total_sessions": 20,
            "present_count": 16,
            "absent_count": 4,
            "justified_count": 2,
            "attendance_percentage": 80.0,
            "attendance_trend": [
                {"date": "2024-06-01", "status": "present"},
                {"date": "2024-06-02", "status": "absent"},
                {"date": "2024-06-03", "status": "present"}
            ],
            "top_absent_students": [
                {"student_id": str(uuid4()), "name": "Juan Pérez", "absences": 5},
                {"student_id": str(uuid4()), "name": "María García", "absences": 3}
            ]
        }

    @pytest.mark.asyncio
    async def test_get_summary_student_own_data_success(
        self,
        use_case,
        mock_attendance_repository,
        mock_user_service,
        sample_student_id,
        sample_summary_data
    ):
        """Test exitoso: estudiante consulta sus propios datos."""
        # Arrange
        request = AttendanceSummaryRequest(
            student_id=sample_student_id,
            start_date=date.today() - timedelta(days=30),
            end_date=date.today()
        )

        mock_user_service.get_user_role.return_value = "aprendiz"
        mock_attendance_repository.get_attendance_summary.return_value = sample_summary_data

        # Act
        result = await use_case.execute(request, sample_student_id)

        # Assert
        assert isinstance(result, AttendanceSummaryResponse)
        assert result.total_sessions == 20
        assert result.present_count == 16
        assert result.absent_count == 4
        assert result.justified_count == 2
        assert result.attendance_percentage == 80.0
        assert result.student_details is None  # Los aprendices no ven detalles extra
        assert result.top_absent_students is None  # Los aprendices no ven tops

        # Verificar que se validó que el estudiante solo vea sus datos
        repo_call_args = mock_attendance_repository.get_attendance_summary.call_args[1]
        assert repo_call_args["student_id"] == sample_student_id

    @pytest.mark.asyncio
    async def test_get_summary_student_unauthorized_other_data(
        self,
        use_case,
        mock_user_service,
        sample_student_id
    ):
        """Test falla: estudiante intenta ver datos de otro estudiante."""
        # Arrange
        other_student_id = uuid4()
        request = AttendanceSummaryRequest(student_id=other_student_id)

        mock_user_service.get_user_role.return_value = "aprendiz"

        # Act & Assert
        with pytest.raises(UnauthorizedAccessError) as exc_info:
            await use_case.execute(request, sample_student_id)

        assert "attendance summary of other students" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_summary_instructor_assigned_ficha_success(
        self,
        use_case,
        mock_attendance_repository,
        mock_user_service,
        sample_instructor_id,
        sample_ficha_id,
        sample_summary_data,
        sample_user_info
    ):
        """Test exitoso: instructor consulta datos de su ficha asignada."""
        # Arrange
        request = AttendanceSummaryRequest(
            ficha_id=sample_ficha_id,
            start_date=date.today() - timedelta(days=30),
            end_date=date.today()
        )

        mock_user_service.get_user_role.return_value = "instructor"
        mock_user_service.validate_instructor_ficha_assignment.return_value = True
        mock_attendance_repository.get_attendance_summary.return_value = sample_summary_data

        # Act
        result = await use_case.execute(request, sample_instructor_id)

        # Assert
        assert isinstance(result, AttendanceSummaryResponse)
        assert result.total_sessions == 20
        assert result.top_absent_students == sample_summary_data["top_absent_students"]

        # Verificar validación de asignación
        mock_user_service.validate_instructor_ficha_assignment.assert_called_once_with(
            sample_instructor_id,
            sample_ficha_id
        )

    @pytest.mark.asyncio
    async def test_get_summary_instructor_unauthorized_ficha(
        self,
        use_case,
        mock_user_service,
        sample_instructor_id,
        sample_ficha_id
    ):
        """Test falla: instructor intenta ver datos de ficha no asignada."""
        # Arrange
        request = AttendanceSummaryRequest(ficha_id=sample_ficha_id)

        mock_user_service.get_user_role.return_value = "instructor"
        mock_user_service.validate_instructor_ficha_assignment.return_value = False

        # Act & Assert
        with pytest.raises(UnauthorizedAccessError) as exc_info:
            await use_case.execute(request, sample_instructor_id)

        assert f"attendance data for ficha {sample_ficha_id}" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_summary_instructor_no_ficha_uses_instructor_id(
        self,
        use_case,
        mock_attendance_repository,
        mock_user_service,
        sample_instructor_id,
        sample_summary_data
    ):
        """Test: instructor sin ficha específica usa su ID como filtro."""
        # Arrange
        request = AttendanceSummaryRequest()

        mock_user_service.get_user_role.return_value = "instructor"
        mock_attendance_repository.get_attendance_summary.return_value = sample_summary_data

        # Act
        result = await use_case.execute(request, sample_instructor_id)

        # Assert
        assert isinstance(result, AttendanceSummaryResponse)

        # Verificar que se usó instructor_id como filtro
        repo_call_args = mock_attendance_repository.get_attendance_summary.call_args[1]
        assert repo_call_args["instructor_id"] == sample_instructor_id

    @pytest.mark.asyncio
    async def test_get_summary_admin_full_access(
        self,
        use_case,
        mock_attendance_repository,
        mock_user_service,
        sample_summary_data
    ):
        """Test: administrador tiene acceso completo sin restricciones."""
        # Arrange
        admin_id = uuid4()
        student_id = uuid4()
        ficha_id = uuid4()
        instructor_id = uuid4()

        request = AttendanceSummaryRequest(
            student_id=student_id,
            ficha_id=ficha_id,
            instructor_id=instructor_id
        )

        mock_user_service.get_user_role.return_value = "admin"
        mock_user_service.get_user_by_id.return_value = {
            "first_name": "Juan",
            "last_name": "Pérez",
            "document_number": "12345678",
            "ficha_name": "ADSI_2024"
        }
        mock_attendance_repository.get_attendance_summary.return_value = sample_summary_data

        # Act
        result = await use_case.execute(request, admin_id)

        # Assert
        assert isinstance(result, AttendanceSummaryResponse)
        assert result.student_details is not None  # Admin ve detalles

        # Verificar que no se hicieron validaciones de permisos específicas
        mock_user_service.validate_instructor_ficha_assignment.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_summary_sets_default_dates(
        self,
        use_case,
        mock_attendance_repository,
        mock_user_service,
        sample_student_id,
        sample_summary_data
    ):
        """Test verifica que se establecen fechas por defecto."""
        # Arrange
        request = AttendanceSummaryRequest(student_id=sample_student_id)

        mock_user_service.get_user_role.return_value = "aprendiz"
        mock_attendance_repository.get_attendance_summary.return_value = sample_summary_data

        # Act
        await use_case.execute(request, sample_student_id)

        # Assert
        repo_call_args = mock_attendance_repository.get_attendance_summary.call_args[1]
        assert repo_call_args["start_date"] == date.today() - timedelta(days=30)
        assert repo_call_args["end_date"] == date.today()

    @pytest.mark.asyncio
    async def test_get_summary_preserves_provided_dates(
        self,
        use_case,
        mock_attendance_repository,
        mock_user_service,
        sample_student_id,
        sample_summary_data
    ):
        """Test verifica que se respetan las fechas proporcionadas."""
        # Arrange
        start_date = date(2024, 5, 1)
        end_date = date(2024, 5, 31)
        request = AttendanceSummaryRequest(
            student_id=sample_student_id,
            start_date=start_date,
            end_date=end_date
        )

        mock_user_service.get_user_role.return_value = "aprendiz"
        mock_attendance_repository.get_attendance_summary.return_value = sample_summary_data

        # Act
        await use_case.execute(request, sample_student_id)

        # Assert
        repo_call_args = mock_attendance_repository.get_attendance_summary.call_args[1]
        assert repo_call_args["start_date"] == start_date
        assert repo_call_args["end_date"] == end_date

    @pytest.mark.asyncio
    async def test_get_summary_coordinator_full_access(
        self,
        use_case,
        mock_attendance_repository,
        mock_user_service,
        sample_summary_data
    ):
        """Test: coordinador tiene acceso completo como admin."""
        # Arrange
        coordinator_id = uuid4()
        request = AttendanceSummaryRequest(
            student_id=uuid4(),
            ficha_id=uuid4(),
            instructor_id=uuid4()
        )

        mock_user_service.get_user_role.return_value = "coordinator"
        mock_attendance_repository.get_attendance_summary.return_value = sample_summary_data

        # Act
        result = await use_case.execute(request, coordinator_id)

        # Assert
        assert isinstance(result, AttendanceSummaryResponse)
        # Coordinador tiene acceso sin validaciones adicionales
        mock_user_service.validate_instructor_ficha_assignment.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_summary_invalid_role_unauthorized(
        self,
        use_case,
        mock_user_service
    ):
        """Test falla: rol inválido no tiene acceso."""
        # Arrange
        user_id = uuid4()
        request = AttendanceSummaryRequest()

        mock_user_service.get_user_role.return_value = "invalid_role"

        # Act & Assert
        with pytest.raises(UnauthorizedAccessError) as exc_info:
            await use_case.execute(request, user_id)

        assert "attendance summary" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_summary_student_filters_instructor_field(
        self,
        use_case,
        mock_attendance_repository,
        mock_user_service,
        sample_student_id,
        sample_summary_data
    ):
        """Test: estudiante no puede filtrar por instructor."""
        # Arrange
        request = AttendanceSummaryRequest(
            student_id=sample_student_id,
            instructor_id=uuid4()  # Esto debería ser ignorado
        )

        mock_user_service.get_user_role.return_value = "aprendiz"
        mock_attendance_repository.get_attendance_summary.return_value = sample_summary_data

        # Act
        await use_case.execute(request, sample_student_id)

        # Assert - instructor_id debe ser None para estudiantes
        repo_call_args = mock_attendance_repository.get_attendance_summary.call_args[1]
        assert repo_call_args["instructor_id"] is None
