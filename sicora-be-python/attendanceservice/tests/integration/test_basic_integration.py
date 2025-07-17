"""Test básico de integración para verificar que la app funciona."""

import pytest
from fastapi.testclient import TestClient


def test_app_import():
    """Test que verifica que la app se puede importar."""
    from main import app
    assert app is not None


def test_health_endpoint():
    """Test del endpoint de health."""
    from main import app
    client = TestClient(app)
    
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_app_has_expected_routes():
    """Test que verifica que la app tiene las rutas esperadas."""
    from main import app
    
    # Verificar que tenemos rutas
    assert len(app.routes) > 0
    
    # Obtener paths de las rutas
    route_paths = []
    for route in app.routes:
        if hasattr(route, 'path'):
            route_paths.append(route.path)
    
    # Verificar rutas principales
    expected_paths = ["/health", "/attendance/register", "/attendance/summary", "/attendance/history"]
    
    for expected_path in expected_paths:
        # Verificar que la ruta existe o una variación de ella
        path_exists = any(expected_path in path for path in route_paths)
        assert path_exists, f"Expected path {expected_path} not found in {route_paths}"


def test_openapi_docs_accessible():
    """Test que verifica que la documentación OpenAPI es accesible."""
    from main import app
    client = TestClient(app)
    
    # Test de acceso a documentación
    response = client.get("/docs")
    assert response.status_code == 200
    
    # Test de schema OpenAPI
    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi_data = response.json()
    assert "openapi" in openapi_data
    assert "paths" in openapi_data
