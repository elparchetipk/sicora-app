"""
Configuración global para tests de SICORA Backend Python.

Este módulo configura fixtures globales, configuración de base de datos de tests,
y utilidades comunes para todos los tests del proyecto.
"""

import asyncio
import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

# Configurar variables de entorno para tests
os.environ["DATABASE_URL"] = (
    "postgresql+asyncpg://sicora_user:sicora_password@localhost:5433/sicora_test"
)
os.environ["ENVIRONMENT"] = "test"
os.environ["DEBUG"] = "true"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Fixture para el event loop de asyncio en tests.
    Necesario para tests async con pytest-asyncio.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db_engine():
    """
    Fixture para el motor de base de datos de tests.
    Crea un motor separado para tests que usa la BD de test.
    """
    # URL de base de datos de test
    test_database_url = (
        "postgresql+asyncpg://sicora_user:sicora_password@localhost:5433/sicora_test"
    )

    engine = create_async_engine(
        test_database_url,
        echo=False,  # No echo en tests para mantener output limpio
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

    yield engine

    # Cleanup
    await engine.dispose()


@pytest_asyncio.fixture
async def test_db_session(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture para sesión de base de datos de tests.
    Cada test obtiene una sesión limpia con rollback automático.
    """
    # Crear sessionmaker
    async_session_maker = async_sessionmaker(
        test_db_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        # Comenzar transacción
        await session.begin()

        yield session

        # Rollback al final del test
        await session.rollback()


@pytest_asyncio.fixture
async def apigateway_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture para cliente HTTP de APIGateway.
    Proporciona un cliente configurado para hacer requests al servicio.
    """
    import sys
    import os
    from httpx import ASGITransport

    # Añadir path del APIGateway al PYTHONPATH
    apigateway_path = os.path.join(os.path.dirname(__file__), "..", "apigateway")
    if apigateway_path not in sys.path:
        sys.path.insert(0, apigateway_path)

    # Cambiar directorio para imports relativos
    original_cwd = os.getcwd()
    os.chdir(apigateway_path)

    try:
        from main import app

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client
    finally:
        # Restaurar directorio y limpiar path
        os.chdir(original_cwd)
        if apigateway_path in sys.path:
            sys.path.remove(apigateway_path)


@pytest_asyncio.fixture
async def notification_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture para cliente HTTP de NotificationService.
    Proporciona un cliente configurado para hacer requests al servicio.
    """
    import sys
    import os
    from httpx import ASGITransport

    # Limpiar módulos cacheados para evitar conflictos
    modules_to_remove = []
    for module_name in sys.modules.keys():
        if module_name.startswith("app.") or module_name == "main":
            modules_to_remove.append(module_name)

    for module_name in modules_to_remove:
        del sys.modules[module_name]

    # Añadir path del servicio (usar notificationservice-template)
    notification_path = os.path.join(
        os.path.dirname(__file__), "..", "notificationservice-template"
    )
    if notification_path not in sys.path:
        sys.path.insert(0, notification_path)

    # Cambiar directorio para imports relativos
    original_cwd = os.getcwd()
    os.chdir(notification_path)

    try:
        from main import app

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client
    finally:
        # Restaurar directorio y limpiar path
        os.chdir(original_cwd)
        if notification_path in sys.path:
            sys.path.remove(notification_path)

        # Limpiar módulos cacheados nuevamente
        modules_to_remove = []
        for module_name in sys.modules.keys():
            if module_name.startswith("app.") or module_name == "main":
                modules_to_remove.append(module_name)

        for module_name in modules_to_remove:
            del sys.modules[module_name]


@pytest.fixture
def sample_notification_data():
    """
    Fixture con datos de ejemplo para notificaciones.
    """
    return {
        "user_id": 1,
        "title": "Test Notification",
        "message": "This is a test notification message",
        "type": "info",
    }


@pytest.fixture
def sample_user_data():
    """
    Fixture con datos de ejemplo para usuarios.
    """
    return {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "is_active": True,
    }


@pytest.fixture
def api_headers():
    """
    Fixture con headers estándar para requests de API.
    """
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "SICORA-Test-Client/1.0",
    }


class DatabaseTestUtils:
    """Utilidades para tests de base de datos."""

    @staticmethod
    async def clean_tables(session: AsyncSession, *table_names):
        """Limpiar tablas específicas en tests."""
        for table_name in table_names:
            await session.execute(f"DELETE FROM {table_name}")
        await session.commit()

    @staticmethod
    async def count_records(session: AsyncSession, table_name: str) -> int:
        """Contar registros en una tabla."""
        result = await session.execute(f"SELECT COUNT(*) FROM {table_name}")
        return result.scalar()


class APITestUtils:
    """Utilidades para tests de API."""

    @staticmethod
    def assert_response_structure(response_json: dict, expected_keys: list):
        """Verificar que una respuesta JSON tiene las claves esperadas."""
        for key in expected_keys:
            assert key in response_json, f"Key '{key}' missing in response"

    @staticmethod
    def assert_error_response(response_json: dict, expected_status: str = "error"):
        """Verificar estructura de respuesta de error."""
        assert "status" in response_json
        assert response_json["status"] == expected_status
        assert "error" in response_json or "message" in response_json


# Hacer disponibles las utilidades globalmente
@pytest.fixture
def db_utils():
    """Fixture para utilidades de base de datos."""
    return DatabaseTestUtils


@pytest.fixture
def api_utils():
    """Fixture para utilidades de API."""
    return APITestUtils
