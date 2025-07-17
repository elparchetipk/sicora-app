"""Tests unitarios para GetAttendanceHistoryUseCase."""

import pytest
from unittest.mock import AsyncMock
from datetime import date, timedelta, datetime
from uuid import uuid4
from math import ceil

from app.application.use_cases.get_attendance_history_use_case import GetAttendanceHistoryUseCase
from app.application.dtos.attendance_dtos import (
    AttendanceHistoryRequest, 
    AttendanceHistoryResponse, 
    AttendanceHistoryRecord
)
from app.domain.value_objects import AttendanceStatus
from app.domain.exceptions import UnauthorizedAccessError


class TestGetAttendanceHistoryUseCase:
    """Test cases para GetAttendanceHistoryUseCase."""

    @pytest.fixture
    def use_case(self, mock_attendance_repository, mock_user_service, mock_schedule_service):
        """Instancia del caso de uso con dependencias mockeadas."""
        return GetAttendanceHistoryUseCase(
            attendance_repository=mock_attendance_repository,
            user_service=mock_user_service,
            schedule_service=mock_schedule_service
        )

    @pytest.fixture
    def sample_attendance_records(self, sample_student_id, sample_instructor_id):
        """Registros de asistencia de ejemplo."""
        records = []
        for i in range(5):
            record = type('Record', (), {
                'id': uuid4(),
                'student_id': sample_student_id,
                'instructor_id': sample_instructor_id,
                'schedule_id': uuid4(),
                'date': datetime.now() - timedelta(days=i),
                'block_identifier': f'BLOQUE_{i+1}',
                'status': AttendanceStatus.PRESENT if i % 2 == 0 else AttendanceStatus.ABSENT,
                'notes': f'Notes for record {i}',
                'recorded_at': datetime.now() - timedelta(days=i)
            })()
            records.append(record)
        return records

    @pytest.mark.asyncio
    async def test_get_history_student_own_data_success(
        self,
        use_case,
        mock_attendance_repository,
        mock_user_service,
        mock_schedule_service,
        sample_student_id,
        sample_attendance_records,
        sample_user_info,
        sample_instructor_info,
        sample_schedule_info
    ):
        """Test exitoso: estudiante consulta su propio historial."""
        # Arrange
        request = AttendanceHistoryRequest(
            student_id=sample_student_id,
            page=1,
            page_size=10
        )

        mock_user_service.get_user_role.return_value = "aprendiz"
        mock_attendance_repository.get_by_student_and_period.return_value = sample_attendance_records
        
        # Mock get_user_by_id para devolver info apropiada según el ID
        async def mock_get_user_by_id(user_id):
            if user_id == sample_student_id:
                return sample_user_info
            return sample_instructor_info
        
        mock_user_service.get_user_by_id.side_effect = mock_get_user_by_id
        mock_schedule_service.get_schedule_by_id.return_value = sample_schedule_info

        # Act
        result = await use_case.execute(request, sample_student_id)

        # Assert
        assert isinstance(result, AttendanceHistoryResponse)
        assert len(result.records) == 5
        assert result.total_records == 5
        assert result.page == 1
        assert result.page_size == 10
        assert result.total_pages == 1

        # Verificar que los registros están enriquecidos
        first_record = result.records[0]
        assert isinstance(first_record, AttendanceHistoryRecord)
        assert first_record.student_name == "Juan Pérez"
        assert first_record.instructor_name == "María García"
        assert first_record.ficha_name == "ADSI_2024_01"

        # Verificar que el filtro se ajustó al estudiante
        mock_attendance_repository.get_by_student_and_period.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_history_student_unauthorized_other_data(
        self,
        use_case,
        mock_user_service,
        sample_student_id
    ):
        """Test falla: estudiante intenta ver historial de otro estudiante."""
        # Arrange
        other_student_id = uuid4()
        request = AttendanceHistoryRequest(student_id=other_student_id)

        mock_user_service.get_user_role.return_value = "aprendiz"

        # Act & Assert
        with pytest.raises(UnauthorizedAccessError) as exc_info:
            await use_case.execute(request, sample_student_id)

        assert "attendance history of other students" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_history_instructor_assigned_ficha_success(
        self,
        use_case,
        mock_attendance_repository,
        mock_user_service,
        mock_schedule_service,
        sample_instructor_id,
        sample_ficha_id,
        sample_attendance_records,
        sample_user_info,
        sample_instructor_info,
        sample_schedule_info
    ):
        """Test exitoso: instructor consulta historial de su ficha asignada."""
        # Arrange
        request = AttendanceHistoryRequest(
            ficha_id=sample_ficha_id,
            page=1,
            page_size=10
        )

        mock_user_service.get_user_role.return_value = "instructor"
        mock_user_service.validate_instructor_ficha_assignment.return_value = True
        
        # Simular que get_attendance_summary devuelve registros detallados
        summary_data = {"detailed_records": sample_attendance_records}
        mock_attendance_repository.get_attendance_summary.return_value = summary_data
        
        # Mock get_user_by_id para devolver info apropiada según el ID
        async def mock_get_user_by_id(user_id):
            # Devuelve info de estudiante para student_ids, info de instructor para instructor_ids
            for record in sample_attendance_records:
                if hasattr(record, 'student_id') and user_id == record.student_id:
                    return sample_user_info
                if hasattr(record, 'instructor_id') and user_id == record.instructor_id:
                    return sample_instructor_info
            # Default fallback
            return sample_user_info
        
        mock_user_service.get_user_by_id.side_effect = mock_get_user_by_id
        mock_schedule_service.get_schedule_by_id.return_value = sample_schedule_info

        # Act
        result = await use_case.execute(request, sample_instructor_id)

        # Assert
        assert isinstance(result, AttendanceHistoryResponse)
        assert len(result.records) == 5

        # Verificar validación de asignación
        mock_user_service.validate_instructor_ficha_assignment.assert_called_once_with(
            sample_instructor_id,
            sample_ficha_id
        )

    @pytest.mark.asyncio
    async def test_get_history_instructor_unauthorized_ficha(
        self,
        use_case,
        mock_user_service,
        sample_instructor_id,
        sample_ficha_id
    ):
        """Test falla: instructor intenta ver historial de ficha no asignada."""
        # Arrange
        request = AttendanceHistoryRequest(ficha_id=sample_ficha_id)

        mock_user_service.get_user_role.return_value = "instructor"
        mock_user_service.validate_instructor_ficha_assignment.return_value = False

        # Act & Assert
        with pytest.raises(UnauthorizedAccessError) as exc_info:
            await use_case.execute(request, sample_instructor_id)

        assert f"attendance history for ficha {sample_ficha_id}" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_history_instructor_student_not_in_fichas(
        self,
        use_case,
        mock_user_service,
        sample_instructor_id,
        sample_student_id
    ):
        """Test falla: instructor intenta ver estudiante que no está en sus fichas."""
        # Arrange
        request = AttendanceHistoryRequest(student_id=sample_student_id)

        mock_user_service.get_user_role.return_value = "instructor"
        mock_user_service.get_instructor_fichas.return_value = [
            {"id": uuid4()}, {"id": uuid4()}
        ]
        mock_user_service.validate_student_ficha_enrollment.return_value = False

        # Act & Assert
        with pytest.raises(UnauthorizedAccessError) as exc_info:
            await use_case.execute(request, sample_instructor_id)

        assert f"attendance history for student {sample_student_id}" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_history_admin_full_access(
        self,
        use_case,
        mock_attendance_repository,
        mock_user_service,
        mock_schedule_service,
        sample_attendance_records,
        sample_user_info,
        sample_instructor_info,
        sample_schedule_info
    ):
        """Test: administrador tiene acceso completo sin restricciones."""
        # Arrange
        admin_id = uuid4()
        student_id = uuid4()
        
        request = AttendanceHistoryRequest(
            student_id=student_id,
            page=1,
            page_size=10
        )

        mock_user_service.get_user_role.return_value = "admin"
        mock_attendance_repository.get_by_student_and_period.return_value = sample_attendance_records
        
        # Mock get_user_by_id para devolver info apropiada según el ID
        async def mock_get_user_by_id(user_id):
            # Para admins, devolver info apropiada según context
            for record in sample_attendance_records:
                if hasattr(record, 'student_id') and user_id == record.student_id:
                    return sample_user_info
                if hasattr(record, 'instructor_id') and user_id == record.instructor_id:
                    return sample_instructor_info
            # Default fallback
            return sample_user_info
        
        mock_user_service.get_user_by_id.side_effect = mock_get_user_by_id
        mock_schedule_service.get_schedule_by_id.return_value = sample_schedule_info

        # Act
        result = await use_case.execute(request, admin_id)

        # Assert
        assert isinstance(result, AttendanceHistoryResponse)
        assert len(result.records) == 5

        # Verificar que no se hicieron validaciones de permisos específicas
        mock_user_service.validate_instructor_ficha_assignment.assert_not_called()
        mock_user_service.get_instructor_fichas.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_history_pagination_works_correctly(
        self,
        use_case,
        mock_attendance_repository,
        mock_user_service,
        mock_schedule_service,
        sample_student_id,
        sample_user_info,
        sample_instructor_info,
        sample_schedule_info
    ):
        """Test verifica que la paginación funciona correctamente."""
        # Arrange - crear 25 registros para probar paginación
        large_record_set = []
        for i in range(25):
            record = type('Record', (), {
                'id': uuid4(),
                'student_id': sample_student_id,
                'instructor_id': uuid4(),
                'schedule_id': uuid4(),
                'date': datetime.now() - timedelta(days=i),
                'block_identifier': f'BLOQUE_{i+1}',
                'status': AttendanceStatus.PRESENT,
                'notes': f'Notes {i}',
                'recorded_at': datetime.now() - timedelta(days=i)
            })()
            large_record_set.append(record)

        request = AttendanceHistoryRequest(
            student_id=sample_student_id,
            page=2,
            page_size=10
        )

        mock_user_service.get_user_role.return_value = "aprendiz"
        mock_attendance_repository.get_by_student_and_period.return_value = large_record_set
        mock_user_service.get_user_by_id.side_effect = [
            sample_user_info,
            sample_instructor_info
        ] * 15  # Suficientes para enriquecer todos los registros
        mock_schedule_service.get_schedule_by_id.return_value = sample_schedule_info

        # Act
        result = await use_case.execute(request, sample_student_id)

        # Assert
        assert result.total_records == 25
        assert result.page == 2
        assert result.page_size == 10
        assert result.total_pages == ceil(25 / 10)
        assert len(result.records) == 10  # Página 2, 10 registros

    @pytest.mark.asyncio
    async def test_get_history_status_filter_works(
        self,
        use_case,
        mock_attendance_repository,
        mock_user_service,
        mock_schedule_service,
        sample_student_id,
        sample_user_info,
        sample_instructor_info,
        sample_schedule_info
    ):
        """Test verifica que el filtro de estado funciona."""
        # Arrange - crear registros mixtos
        mixed_records = []
        for i in range(6):
            record = type('Record', (), {
                'id': uuid4(),
                'student_id': sample_student_id,
                'instructor_id': uuid4(),
                'schedule_id': uuid4(),
                'date': datetime.now() - timedelta(days=i),
                'block_identifier': f'BLOQUE_{i+1}',
                'status': AttendanceStatus.PRESENT if i < 3 else AttendanceStatus.ABSENT,
                'notes': f'Notes {i}',
                'recorded_at': datetime.now() - timedelta(days=i)
            })()
            mixed_records.append(record)

        request = AttendanceHistoryRequest(
            student_id=sample_student_id,
            status=AttendanceStatus.PRESENT,
            page=1,
            page_size=10
        )

        mock_user_service.get_user_role.return_value = "aprendiz"
        mock_attendance_repository.get_by_student_and_period.return_value = mixed_records
        mock_user_service.get_user_by_id.side_effect = [
            sample_user_info,
            sample_instructor_info
        ] * 5
        mock_schedule_service.get_schedule_by_id.return_value = sample_schedule_info

        # Act
        result = await use_case.execute(request, sample_student_id)

        # Assert - solo debería devolver registros PRESENT (3 de 6)
        assert len(result.records) == 3
        assert result.total_records == 3
        for record in result.records:
            assert record.status == AttendanceStatus.PRESENT

    @pytest.mark.asyncio
    async def test_get_history_sets_default_dates(
        self,
        use_case,
        mock_attendance_repository,
        mock_user_service,
        sample_student_id
    ):
        """Test verifica que se establecen fechas por defecto."""
        # Arrange
        request = AttendanceHistoryRequest(student_id=sample_student_id)

        mock_user_service.get_user_role.return_value = "aprendiz"
        mock_attendance_repository.get_by_student_and_period.return_value = []

        # Act
        await use_case.execute(request, sample_student_id)

        # Assert - verificar fechas por defecto (últimos 30 días)
        call_args = mock_attendance_repository.get_by_student_and_period.call_args[0]
        start_date = call_args[1]
        end_date = call_args[2]
        
        assert start_date == date.today() - timedelta(days=30)
        assert end_date == date.today()

    @pytest.mark.asyncio
    async def test_get_history_validates_pagination_parameters(
        self,
        use_case,
        mock_attendance_repository,
        mock_user_service,
        sample_student_id
    ):
        """Test verifica validación de parámetros de paginación."""
        # Arrange - parámetros de paginación inválidos
        request = AttendanceHistoryRequest(
            student_id=sample_student_id,
            page=-1,  # Inválido
            page_size=200  # Muy grande
        )

        mock_user_service.get_user_role.return_value = "aprendiz"
        mock_attendance_repository.get_by_student_and_period.return_value = []

        # Act
        result = await use_case.execute(request, sample_student_id)

        # Assert - página debe ser mínimo 1, page_size máximo 100
        assert result.page == 1
        assert result.page_size == 100  # Debe ser limitado a 100
