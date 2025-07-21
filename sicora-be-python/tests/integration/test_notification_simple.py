"""
Tests de integración simplificados para NotificationService.
Enfoque en tests HTTP sin imports complejos de modelos.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import text
import asyncio
import subprocess
import os


@pytest_asyncio.fixture
async def notification_service_url():
    """
    Fixture que inicia el NotificationService en un puerto separado.
    """
    notification_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "notificationservice-template"
    )

    # Configurar environment para el proceso
    env = os.environ.copy()
    env["PYTHONPATH"] = notification_dir
    env["PORT"] = "8999"

    # Iniciar el servicio
    process = subprocess.Popen(
        [
            "python",
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8999",
        ],
        cwd=notification_dir,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Esperar a que se inicie
    await asyncio.sleep(3)

    # Verificar que está ejecutándose
    try:
        async with AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8999/health")
            if response.status_code != 200:
                raise Exception("Service not responding")
    except Exception:
        process.terminate()
        raise Exception("Failed to start NotificationService")

    yield "http://127.0.0.1:8999"

    # Cleanup
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


@pytest.mark.integration
class TestNotificationServiceHealthSimple:
    """Tests simplificados para health check del NotificationService."""

    async def test_health_endpoint_returns_healthy_status(
        self, notification_service_url
    ):
        """Test que el endpoint de health devuelve estado saludable."""
        async with AsyncClient() as client:
            response = await client.get(f"{notification_service_url}/health")

            assert response.status_code == 200
            data = response.json()

            assert "status" in data
            assert "service" in data
            assert "timestamp" in data
            assert data["status"] == "healthy"
            assert data["service"] == "NotificationService"


@pytest.mark.integration
class TestNotificationServiceMetricsSimple:
    """Tests simplificados para métricas del NotificationService."""

    async def test_metrics_endpoint_returns_operational_status(
        self, notification_service_url
    ):
        """Test que el endpoint de métricas devuelve información."""
        async with AsyncClient() as client:
            response = await client.get(f"{notification_service_url}/metrics")

            assert response.status_code == 200
            data = response.json()

            # Verificar que hay respuesta válida
            assert "status" in data
            assert data["status"] == "operational"


@pytest.mark.integration
class TestNotificationServiceAPISimple:
    """Tests simplificados para endpoints API del NotificationService."""

    async def test_notification_api_endpoints_exist(
        self, notification_service_url
    ):
        """Test que los endpoints principales de la API existen."""
        async with AsyncClient() as client:
            # Test endpoint de health (debe existir)
            response = await client.get(f"{notification_service_url}/health")
            assert response.status_code == 200

            # Test endpoint de métricas (debe existir)
            response = await client.get(f"{notification_service_url}/metrics")
            assert response.status_code == 200


@pytest.mark.integration
class TestNotificationServiceErrorHandlingSimple:
    """Tests simplificados para manejo de errores del NotificationService."""

    async def test_invalid_endpoints_return_404(
        self, notification_service_url
    ):
        """Test que endpoints inválidos devuelven 404."""
        async with AsyncClient() as client:
            response = await client.get(
                f"{notification_service_url}/nonexistent"
            )
            assert response.status_code == 404


@pytest.mark.integration
class TestNotificationServiceDatabaseSimple:
    """Tests simplificados para verificar conectividad de base de datos."""

    async def test_database_connectivity_via_health(
        self, notification_service_url
    ):
        """Test conectividad de base de datos vía endpoint de health."""
        async with AsyncClient() as client:
            response = await client.get(f"{notification_service_url}/health")

            assert response.status_code == 200
            data = response.json()

            # Si el servicio responde healthy, la DB está conectada
            assert data["status"] == "healthy"


# Tests que usan base de datos directamente (sin imports problemáticos)
@pytest.mark.integration
class TestNotificationServiceDatabaseDirect:
    """Tests que acceden directamente a la base de datos de test."""

    async def test_notifications_table_exists(self):
        """Test que la tabla de notificaciones existe."""
        from sqlalchemy.ext.asyncio import create_async_engine

        # Conectar directamente a la base de datos de test
        db_url = (
            "postgresql+asyncpg://sicora_user:sicora_password@localhost:"
            "5433/sicora_test"
        )
        engine = create_async_engine(db_url, echo=False)

        async with engine.begin() as conn:
            # Verificar que la tabla existe
            query = text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public' "
                "AND table_name = 'notifications'"
            )
            result = await conn.execute(query)
            tables = [row[0] for row in result.fetchall()]

            assert (
                "notifications" in tables
            ), "Table 'notifications' not found in database"

        await engine.dispose()

    async def test_notifications_table_structure(self):
        """Test que la tabla de notificaciones tiene la estructura correcta."""
        from sqlalchemy.ext.asyncio import create_async_engine

        db_url = (
            "postgresql+asyncpg://sicora_user:sicora_password@localhost:"
            "5433/sicora_test"
        )
        engine = create_async_engine(db_url, echo=False)

        async with engine.begin() as conn:
            # Verificar estructura de la tabla
            query = text(
                "SELECT column_name, data_type "
                "FROM information_schema.columns "
                "WHERE table_name = 'notifications' "
                "ORDER BY ordinal_position"
            )
            result = await conn.execute(query)
            columns = {row[0]: row[1] for row in result.fetchall()}

            # Verificar columnas esenciales
            essential_columns = [
                "id",
                "user_id",
                "title",
                "message",
                "type",
                "read_status",
                "created_at",
            ]
            for col_name in essential_columns:
                assert (
                    col_name in columns
                ), f"Column '{col_name}' not found in notifications table"

        await engine.dispose()

    async def test_basic_database_operations(self):
        """Test operaciones básicas de base de datos usando SQL directo."""
        from sqlalchemy.ext.asyncio import create_async_engine
        from datetime import datetime

        db_url = (
            "postgresql+asyncpg://sicora_user:sicora_password@localhost:"
            "5433/sicora_test"
        )
        engine = create_async_engine(db_url, echo=False)

        async with engine.begin() as conn:
            # Limpiar datos de test previos
            await conn.execute(
                text("DELETE FROM notifications WHERE user_id = 999")
            )

            # Insertar un registro de test
            insert_query = text(
                """
                INSERT INTO notifications 
                (user_id, title, message, type, read_status, created_at)
                VALUES (999, 'Test Notification', 'Test message', 
                        'info', false, :timestamp)
                """
            )
            await conn.execute(insert_query, {"timestamp": datetime.now()})

            # Verificar que se insertó
            result = await conn.execute(
                text("SELECT COUNT(*) FROM notifications WHERE user_id = 999")
            )
            count = result.scalar()
            assert count == 1, "Failed to insert test notification"

            # Limpiar
            await conn.execute(
                text("DELETE FROM notifications WHERE user_id = 999")
            )

        await engine.dispose()
