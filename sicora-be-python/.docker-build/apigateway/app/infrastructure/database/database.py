"""
Configuración de base de datos para APIGateway
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://sicora_user:sicora_password@localhost:5433/sicora_gateway"
)

# Crear engine async
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries en desarrollo
    pool_pre_ping=True,
    pool_recycle=300,
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

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
