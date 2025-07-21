"""
Configuración de la base de datos SQLAlchemy.

Este módulo configura la conexión a la base de datos PostgreSQL y define
la sesión y el motor de base de datos para ser utilizados por los repositorios.
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Definir la URL de la base de datos - PostgreSQL por defecto
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://sicora_user:sicora_password@localhost:5433/sicora_notifications",
)

# Crear el motor de base de datos
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries en desarrollo
    pool_pre_ping=True,
    pool_recycle=300,
    future=True,
)

# Crear la sesión asíncrona
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Crear la base para los modelos declarativos
Base = declarative_base()


async def get_db():
    """Dependency para obtener session de base de datos."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Inicializar base de datos."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """
    Proporciona una sesión de base de datos asíncrona.

    Yields:
        AsyncSession: Sesión de base de datos asíncrona
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """
    Inicializa la base de datos creando todas las tablas definidas.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
