"""Configuración de tests para AttendanceService."""

import pytest
import asyncio
from unittest.mock import AsyncMock, Mock
from uuid import uuid4, UUID
from datetime import datetime, date, timedelta

# Configurar event loop para tests async

# Mocks para repositorios
@pytest.fixture
def mock_attendance_repository():
    """Mock del repositorio de asistencia."""
    return AsyncMock()


@pytest.fixture
def mock_justification_repository():
    """Mock del repositorio de justificaciones."""
    return AsyncMock()


@pytest.fixture
def mock_alert_repository():
    """Mock del repositorio de alertas."""
    return AsyncMock()


# Mocks para servicios
@pytest.fixture
def mock_user_service():
    """Mock del servicio de usuarios."""
    return AsyncMock()


@pytest.fixture
def mock_schedule_service():
    """Mock del servicio de horarios."""
    return AsyncMock()


@pytest.fixture
def mock_qr_service():
    """Mock del servicio QR."""
    service = AsyncMock()
    service.validate_qr_code = AsyncMock()
    return service


@pytest.fixture
def mock_file_service():
    """Mock del servicio de archivos."""
    return AsyncMock()


# Datos de prueba comunes
@pytest.fixture
def sample_student_id():
    """ID de estudiante para tests."""
    return uuid4()


@pytest.fixture
def sample_instructor_id():
    """ID de instructor para tests."""
    return uuid4()


@pytest.fixture
def sample_ficha_id():
    """ID de ficha para tests."""
    return uuid4()


@pytest.fixture
def sample_schedule_id():
    """ID de horario para tests."""
    return uuid4()


@pytest.fixture
def sample_venue_id():
    """ID de venue para tests."""
    return uuid4()


@pytest.fixture
def sample_qr_code():
    """Código QR para tests."""
    return "QR_12345_ABCDEF_20240612"


@pytest.fixture
def sample_date():
    """Fecha para tests."""
    return date.today()


@pytest.fixture
def sample_datetime():
    """Datetime para tests."""
    return datetime.now()


# Datos QR válidos
@pytest.fixture
def valid_qr_data(sample_schedule_id, sample_venue_id):
    """Datos QR válidos para tests."""
    return {
        "schedule_id": str(sample_schedule_id),
        "venue_id": str(sample_venue_id),
        "valid_until": (datetime.now() + timedelta(minutes=15)).isoformat(),
        "block_identifier": "BLOQUE_1",
        "ficha_id": str(uuid4())
    }


# Entidades de dominio mock
@pytest.fixture
def sample_attendance_record(sample_student_id, sample_instructor_id, sample_schedule_id, sample_venue_id):
    """Registro de asistencia de ejemplo."""
    from app.domain.entities import AttendanceRecord
    from app.domain.value_objects import AttendanceStatus
    
    return AttendanceRecord(
        id=uuid4(),
        student_id=sample_student_id,
        schedule_id=sample_schedule_id,
        instructor_id=sample_instructor_id,
        date=datetime.now(),
        block_identifier="BLOQUE_1",
        venue_id=sample_venue_id,
        status=AttendanceStatus.PRESENT,
        qr_code_used="QR_TEST_123",
        notes="Test attendance record"
    )


@pytest.fixture
def sample_justification(sample_student_id):
    """Justificación de ejemplo."""
    from app.domain.entities import Justification
    from app.domain.value_objects import JustificationStatus
    
    return Justification(
        id=uuid4(),
        attendance_record_id=uuid4(),
        student_id=sample_student_id,
        reason="Medical appointment",
        file_path="/uploads/justification.pdf",
        status=JustificationStatus.PENDING,
        submitted_at=datetime.now()
    )


@pytest.fixture
def sample_alert(sample_student_id, sample_instructor_id):
    """Alerta de ejemplo."""
    from app.domain.entities import AttendanceAlert
    from app.domain.value_objects import AlertLevel, AlertType
    
    return AttendanceAlert(
        id=uuid4(),
        student_id=sample_student_id,
        instructor_id=sample_instructor_id,
        ficha_id=uuid4(),
        alert_type=AlertType.CONSECUTIVE_ABSENCES,
        level=AlertLevel.HIGH,
        title="Multiple consecutive absences",
        description="Student has 3 consecutive absences",
        consecutive_absences=3,
        total_absences=5,
        absence_dates=[
            date.today() - timedelta(days=3),
            date.today() - timedelta(days=2),
            date.today() - timedelta(days=1)
        ]
    )


# User info mocks
@pytest.fixture
def sample_user_info():
    """Información de usuario de ejemplo."""
    return {
        "id": str(uuid4()),
        "first_name": "Juan",
        "last_name": "Pérez",
        "document_number": "12345678",
        "email": "juan.perez@example.com",
        "role": "aprendiz",
        "ficha_id": str(uuid4()),
        "ficha_name": "ADSI_2024_01"
    }


@pytest.fixture
def sample_instructor_info():
    """Información de instructor de ejemplo."""
    return {
        "id": str(uuid4()),
        "first_name": "María",
        "last_name": "García",
        "document_number": "87654321",
        "email": "maria.garcia@example.com",
        "role": "instructor",
        "assigned_fichas": [str(uuid4()), str(uuid4())]
    }


@pytest.fixture
def sample_schedule_info(sample_ficha_id):
    """Información de horario de ejemplo."""
    return {
        "id": str(uuid4()),
        "ficha_id": str(sample_ficha_id),
        "ficha_name": "ADSI_2024_01",
        "program_name": "Análisis y Desarrollo de Software",
        "venue_name": "Aula 201",
        "block_identifier": "BLOQUE_1",
        "start_time": "08:00:00",
        "end_time": "10:00:00",
        "is_active": True
    }
