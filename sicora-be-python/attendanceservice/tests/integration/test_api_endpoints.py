"""Tests de integración para endpoints de AttendanceService."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4
from datetime import datetime, date

from main import app


class TestAttendanceEndpoints:
    """Tests de integración para endpoints de asistencia."""
    
    @pytest.fixture
    def client(self):
        """Cliente de test para FastAPI."""
        return TestClient(app)
    
    @pytest.fixture
    def mock_dependencies(self):
        """Mock de dependencias externas."""
        with patch('app.dependencies.get_user_service') as mock_user_service, \
             patch('app.dependencies.get_schedule_service') as mock_schedule_service, \
             patch('app.dependencies.get_qr_service') as mock_qr_service:
            
            # Configurar mocks
            mock_user_service.return_value = AsyncMock()
            mock_schedule_service.return_value = AsyncMock()
            mock_qr_service.return_value = Mock()
            
            yield {
                'user_service': mock_user_service.return_value,
                'schedule_service': mock_schedule_service.return_value,
                'qr_service': mock_qr_service.return_value
            }
    
    def test_health_check(self, client):
        """Test del health check."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {
            "status": "healthy",
            "service": "AttendanceService",
            "version": "1.0.0"
        }
    
    def test_register_attendance_success(self, client, mock_dependencies):
        """Test exitoso de registro de asistencia."""
        # Configurar mocks
        mock_dependencies['qr_service'].validate_qr_code.return_value = {
            'valid': True,
            'schedule_id': str(uuid4()),
            'instructor_id': str(uuid4())
        }
        mock_dependencies['user_service'].get_user_role.return_value = "aprendiz"
        mock_dependencies['user_service'].validate_instructor_ficha_assignment.return_value = True
        mock_dependencies['user_service'].validate_student_ficha_membership.return_value = True
        
        # Datos de prueba
        request_data = {
            "qr_code": "valid_qr_code",
            "student_id": str(uuid4()),
            "attendance_date": str(date.today()),
            "notes": "Llegada a tiempo"
        }
        
        # Headers de autorización simulados
        headers = {"Authorization": "Bearer mock_token"}
        
        # Realizar solicitud
        response = client.post("/attendance/register", json=request_data, headers=headers)
        
        # Verificaciones
        assert response.status_code == 200
        data = response.json()
        assert "attendance_id" in data
        assert data["status"] == "present"
        assert data["message"] == "Asistencia registrada exitosamente"
    
    def test_get_attendance_summary_success(self, client, mock_dependencies):
        """Test exitoso de consulta de resumen de asistencia."""
        # Configurar mock
        mock_dependencies['user_service'].get_user_role.return_value = "aprendiz"
        
        # Parámetros de consulta
        params = {
            "student_id": str(uuid4()),
            "start_date": "2024-01-01",
            "end_date": "2024-12-31"
        }
        
        headers = {"Authorization": "Bearer mock_token"}
        
        # Realizar solicitud
        response = client.get("/attendance/summary", params=params, headers=headers)
        
        # Verificaciones
        assert response.status_code == 200
        data = response.json()
        assert "total_classes" in data
        assert "present_count" in data
        assert "absent_count" in data
        assert "attendance_percentage" in data
    
    def test_get_attendance_history_success(self, client, mock_dependencies):
        """Test exitoso de consulta de historial de asistencia."""
        # Configurar mock
        mock_dependencies['user_service'].get_user_role.return_value = "aprendiz"
        
        # Parámetros de consulta
        params = {
            "student_id": str(uuid4()),
            "page": 1,
            "page_size": 10
        }
        
        headers = {"Authorization": "Bearer mock_token"}
        
        # Realizar solicitud
        response = client.get("/attendance/history", params=params, headers=headers)
        
        # Verificaciones
        assert response.status_code == 200
        data = response.json()
        assert "records" in data
        assert "pagination" in data
        assert isinstance(data["records"], list)
    
    def test_upload_justification_success(self, client, mock_dependencies):
        """Test exitoso de subida de justificación."""
        # Configurar mock
        mock_dependencies['user_service'].get_user_role.return_value = "aprendiz"
        
        # Datos de formulario simulados
        form_data = {
            "attendance_id": str(uuid4()),
            "reason": "Cita médica",
            "description": "Cita médica de emergencia"
        }
        
        # Archivo simulado
        files = {
            "file": ("justification.pdf", b"fake pdf content", "application/pdf")
        }
        
        headers = {"Authorization": "Bearer mock_token"}
        
        # Realizar solicitud
        response = client.post("/justifications/upload", data=form_data, files=files, headers=headers)
        
        # Verificaciones
        assert response.status_code == 200
        data = response.json()
        assert "justification_id" in data
        assert data["status"] == "pending"
    
    def test_register_attendance_invalid_qr(self, client, mock_dependencies):
        """Test de registro con QR inválido."""
        # Configurar mock para QR inválido
        mock_dependencies['qr_service'].validate_qr_code.return_value = {
            'valid': False,
            'error': 'Invalid QR code'
        }
        
        request_data = {
            "qr_code": "invalid_qr_code",
            "student_id": str(uuid4()),
            "attendance_date": str(date.today())
        }
        
        headers = {"Authorization": "Bearer mock_token"}
        
        response = client.post("/attendance/register", json=request_data, headers=headers)
        
        # Verificar error
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
    
    def test_unauthorized_access(self, client):
        """Test de acceso sin autorización."""
        request_data = {
            "qr_code": "some_code",
            "student_id": str(uuid4()),
            "attendance_date": str(date.today())
        }
        
        # Sin headers de autorización
        response = client.post("/attendance/register", json=request_data)
        
        # Verificar que se requiere autorización
        assert response.status_code == 401
    
    def test_alerts_endpoints(self, client, mock_dependencies):
        """Test de endpoints de alertas."""
        mock_dependencies['user_service'].get_user_role.return_value = "instructor"
        
        headers = {"Authorization": "Bearer mock_token"}
        
        # Test obtener alertas
        response = client.get("/alerts/", headers=headers)
        assert response.status_code == 200
        
        # Test crear alerta
        alert_data = {
            "student_id": str(uuid4()),
            "alert_type": "absence",
            "level": "medium",
            "message": "Estudiante con múltiples ausencias"
        }
        
        response = client.post("/alerts/", json=alert_data, headers=headers)
        assert response.status_code == 200


class TestJustificationEndpoints:
    """Tests de integración para endpoints de justificaciones."""
    
    @pytest.fixture
    def client(self):
        """Cliente de test para FastAPI."""
        return TestClient(app)
    
    @pytest.fixture
    def mock_dependencies(self):
        """Mock de dependencias externas."""
        with patch('app.dependencies.get_user_service') as mock_user_service:
            mock_user_service.return_value = AsyncMock()
            yield {'user_service': mock_user_service.return_value}
    
    def test_review_justification_success(self, client, mock_dependencies):
        """Test exitoso de revisión de justificación."""
        mock_dependencies['user_service'].get_user_role.return_value = "instructor"
        
        justification_id = str(uuid4())
        review_data = {
            "status": "approved",
            "reviewer_comments": "Justificación válida y bien documentada"
        }
        
        headers = {"Authorization": "Bearer mock_token"}
        
        response = client.put(f"/justifications/{justification_id}/review", json=review_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "approved"
    
    def test_get_justifications_list(self, client, mock_dependencies):
        """Test de listado de justificaciones."""
        mock_dependencies['user_service'].get_user_role.return_value = "instructor"
        
        params = {"status": "pending", "page": 1, "page_size": 10}
        headers = {"Authorization": "Bearer mock_token"}
        
        response = client.get("/justifications/", params=params, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "justifications" in data
        assert "pagination" in data


class TestAlertEndpoints:
    """Tests de integración para endpoints de alertas."""
    
    @pytest.fixture
    def client(self):
        """Cliente de test para FastAPI."""
        return TestClient(app)
    
    @pytest.fixture
    def mock_dependencies(self):
        """Mock de dependencias externas."""
        with patch('app.dependencies.get_user_service') as mock_user_service:
            mock_user_service.return_value = AsyncMock()
            yield {'user_service': mock_user_service.return_value}
    
    def test_mark_alert_as_read(self, client, mock_dependencies):
        """Test de marcar alerta como leída."""
        mock_dependencies['user_service'].get_user_role.return_value = "instructor"
        
        alert_id = str(uuid4())
        headers = {"Authorization": "Bearer mock_token"}
        
        response = client.put(f"/alerts/{alert_id}/read", headers=headers)
        
        assert response.status_code == 200
    
    def test_delete_alert(self, client, mock_dependencies):
        """Test de eliminación de alerta."""
        mock_dependencies['user_service'].get_user_role.return_value = "admin"
        
        alert_id = str(uuid4())
        headers = {"Authorization": "Bearer mock_token"}
        
        response = client.delete(f"/alerts/{alert_id}", headers=headers)
        
        assert response.status_code == 200
