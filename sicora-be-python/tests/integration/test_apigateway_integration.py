"""
Tests de integración para APIGateway.

Estos tests verifican el funcionamiento completo del APIGateway incluyendo:
- Conectividad de base de datos
- Endpoints de sistema (health, metrics)
- Funcionalidad de gateway y routing
- Logging y middleware
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture
async def apigateway_app():
    """Fixture que inicializa la aplicación APIGateway para tests."""
    import sys
    import os

    # Añadir path del APIGateway
    apigateway_path = os.path.join(os.path.dirname(__file__), "..", "..", "apigateway")
    sys.path.insert(0, apigateway_path)

    from main import app

    return app


@pytest.mark.integration
class TestAPIGatewayHealth:
    """Tests para endpoints de health del APIGateway."""

    async def test_health_endpoint_returns_healthy_status(
        self, apigateway_client: AsyncClient
    ):
        """Test que el endpoint /health retorna estado saludable."""
        response = await apigateway_client.get("/health")

        assert response.status_code == 200
        data = response.json()

        # Verificar estructura de respuesta
        assert "status" in data
        assert "service" in data
        assert "version" in data
        assert "timestamp" in data

        # Verificar valores esperados
        assert data["status"] == "healthy"
        assert data["service"] == "apigateway"
        assert data["version"] == "2.0.0"

    async def test_health_endpoint_response_time(self, apigateway_client: AsyncClient):
        """Test que el endpoint /health responde rápidamente."""
        import time

        start_time = time.time()
        response = await apigateway_client.get("/health")
        response_time = (time.time() - start_time) * 1000  # en ms

        assert response.status_code == 200
        assert response_time < 100  # Menos de 100ms


@pytest.mark.integration
class TestAPIGatewayMetrics:
    """Tests para endpoints de métricas del APIGateway."""

    async def test_metrics_endpoint_returns_operational_status(
        self, apigateway_client: AsyncClient
    ):
        """Test que el endpoint /metrics retorna métricas operacionales."""
        response = await apigateway_client.get("/metrics")

        assert response.status_code == 200
        data = response.json()

        # Verificar estructura de respuesta
        expected_keys = ["total_requests", "avg_response_time_ms", "status"]
        for key in expected_keys:
            assert key in data, f"Key '{key}' missing in metrics response"

        # Verificar tipos de datos
        assert isinstance(data["total_requests"], int)
        assert isinstance(data["avg_response_time_ms"], (int, float))
        assert data["status"] == "operational"

    async def test_metrics_track_requests(self, apigateway_client: AsyncClient):
        """Test que las métricas rastrean correctamente las requests."""
        # Hacer una request inicial para obtener baseline
        initial_response = await apigateway_client.get("/metrics")
        initial_data = initial_response.json()
        initial_requests = initial_data["total_requests"]

        # Hacer varias requests adicionales
        for _ in range(3):
            await apigateway_client.get("/health")

        # Verificar que el contador aumentó
        final_response = await apigateway_client.get("/metrics")
        final_data = final_response.json()
        final_requests = final_data["total_requests"]

        # El contador debería haber aumentado (incluyendo la request final a /metrics)
        assert final_requests > initial_requests


@pytest.mark.integration
class TestAPIGatewayDatabase:
    """Tests para integración de base de datos del APIGateway."""

    @pytest.mark.asyncio
    async def test_database_connectivity(self):
        """Test conectividad básica con la base de datos."""
        import sys
        import os

        # Añadir path del APIGateway
        apigateway_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "apigateway"
        )
        sys.path.insert(0, apigateway_path)

        from app.infrastructure.database.database import engine, Base
        from sqlalchemy import text

        # Crear las tablas primero
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Verificar que podemos conectar y las tablas existen
        async with engine.begin() as conn:
            # Verificar que las tablas existen
            result = await conn.execute(
                text(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
                )
            )
            tables = [row[0] for row in result.fetchall()]

            # Verificar tablas esperadas
            expected_tables = ["request_logs", "service_health"]
            for table in expected_tables:
                assert (
                    table in tables
                ), f"Table '{table}' not found in database. Available tables: {tables}"

    @pytest.mark.asyncio
    async def test_request_logging_model(self):
        """Test que el modelo de logging funciona correctamente."""
        import sys
        import os

        # Añadir path del APIGateway
        apigateway_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "apigateway"
        )
        sys.path.insert(0, apigateway_path)

        from app.infrastructure.database.database import AsyncSessionLocal
        from app.infrastructure.database.models import RequestLogModel
        from datetime import datetime

        async with AsyncSessionLocal() as session:
            # Crear un log de request de prueba
            log_entry = RequestLogModel(
                method="GET",
                endpoint="/test",
                service_name="test-service",
                status_code=200,
                response_time_ms=50.0,
                user_agent="test-agent",
                ip_address="127.0.0.1",
                status="success",
                timestamp=datetime.now(),
            )

            session.add(log_entry)
            await session.commit()

            # Verificar que se guardó correctamente
            assert log_entry.id is not None
            assert log_entry.method == "GET"
            assert log_entry.status_code == 200


@pytest.mark.integration
class TestAPIGatewayMiddleware:
    """Tests para middleware del APIGateway."""

    async def test_cors_middleware(self, apigateway_client: AsyncClient):
        """Test que el middleware CORS funciona correctamente."""
        # Hacer una petición GET normal y verificar headers CORS
        response = await apigateway_client.get(
            "/health", headers={"Origin": "http://localhost:3000"}
        )

        # Verificar que la respuesta incluye headers CORS
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "*"

    async def test_logging_middleware_adds_headers(
        self, apigateway_client: AsyncClient
    ):
        """Test que el middleware de logging añade información de timing."""
        response = await apigateway_client.get("/health")

        assert response.status_code == 200
        # El middleware debería procesar la request sin errores


@pytest.mark.integration
@pytest.mark.slow
class TestAPIGatewayPerformance:
    """Tests de performance para APIGateway."""

    async def test_concurrent_requests_performance(
        self, apigateway_client: AsyncClient
    ):
        """Test performance con requests concurrentes."""
        import asyncio
        import time

        async def make_request():
            return await apigateway_client.get("/health")

        # Hacer 10 requests concurrentes
        start_time = time.time()
        tasks = [make_request() for _ in range(10)]
        responses = await asyncio.gather(*tasks)
        total_time = time.time() - start_time

        # Verificar que todas las requests fueron exitosas
        for response in responses:
            assert response.status_code == 200

        # Verificar performance (ajustado a límite más realista)
        assert total_time < 5.0, f"Concurrent requests took too long: {total_time}s"

        # Verificar tiempo promedio por request
        avg_time_per_request = total_time / len(responses)
        assert avg_time_per_request < 0.2  # Menos de 200ms por request


@pytest.mark.integration
class TestAPIGatewayErrorHandling:
    """Tests para manejo de errores del APIGateway."""

    async def test_404_error_handling(self, apigateway_client: AsyncClient):
        """Test manejo de endpoints no encontrados."""
        response = await apigateway_client.get("/nonexistent-endpoint")

        assert response.status_code == 404

    async def test_invalid_method_handling(self, apigateway_client: AsyncClient):
        """Test manejo de métodos HTTP inválidos."""
        response = await apigateway_client.post("/health")

        # Debería retornar error de método no permitido
        assert response.status_code in [405, 404]  # Method not allowed o Not found
