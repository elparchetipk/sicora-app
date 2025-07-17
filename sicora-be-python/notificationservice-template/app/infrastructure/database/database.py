"""
Configuración de la base de datos SQLAlchemy.

Este módulo configura la conexión a la base de datos SQLite y define
la sesión y el motor de base de datos para ser utilizados por los repositorios.
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# Definir la URL de la base de datos
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./notifications.db")

# Crear el motor de base de datos
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Cambiar a True para ver las consultas SQL
    future=True
)

# Crear la sesión asíncrona
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Crear la base para los modelos declarativos
Base = declarative_base()


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