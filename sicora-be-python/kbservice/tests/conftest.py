"""Pytest configuration for KbService tests."""

import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from httpx import AsyncClient

import sys
import os

# Add the parent directory to the path so we can import from the root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.infrastructure.models.kb_models import Base
from app.infrastructure.config.database import get_db_session
from app.config import settings


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    # Use in-memory SQLite for tests
    test_database_url = "sqlite+aiosqlite:///:memory:"
    
    engine = create_async_engine(
        test_database_url,
        echo=False,
        future=True
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    SessionLocal = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with SessionLocal() as session:
        yield session


@pytest.fixture
async def test_client(test_session) -> AsyncGenerator[AsyncClient, None]:
    """Create test HTTP client."""
    
    async def override_get_db():
        yield test_session
    
    app.dependency_overrides[get_db_session] = override_get_db
    
    async with AsyncClient(base_url="http://testserver") as client:
        yield client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_knowledge_item():
    """Sample knowledge item data for testing."""
    return {
        "title": "Cómo registrar asistencia",
        "content": "Para registrar asistencia, sigue estos pasos: 1. Ingresa a la aplicación...",
        "content_type": "guide",
        "category": "asistencia",
        "target_audience": "student",
        "tags": ["asistencia", "registro", "guía"],
        "status": "published"
    }


@pytest.fixture
def admin_user():
    """Sample admin user data for testing."""
    return {
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "email": "admin@test.com",
        "role": "admin"
    }


@pytest.fixture
def student_user():
    """Sample student user data for testing."""
    return {
        "user_id": "123e4567-e89b-12d3-a456-426614174001",
        "email": "student@test.com",
        "role": "student"
    }


@pytest.fixture
def instructor_user():
    """Sample instructor user data for testing."""
    return {
        "user_id": "123e4567-e89b-12d3-a456-426614174002",
        "email": "instructor@test.com",
        "role": "instructor"
    }
