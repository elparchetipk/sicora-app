"""Database configuration for AI service."""

import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text, URL
import logging

from app.config import settings
from ..models import Base

logger = logging.getLogger(__name__)
# Configurar nivel de logging para diagnóstico
logger.setLevel(logging.DEBUG)


class DatabaseConfig:
    """Database configuration class for AI Service."""
    
    def __init__(self):
        self.db_schema = settings.DB_SCHEMA
        
        # Construir la URL de la base de datos con el schema
        if self.db_schema and self.db_schema.strip():
            query = {"options": f"-csearch_path={self.db_schema}"}
        else:
            query = {}
            
        # Parsear la URL original
        url = settings.DATABASE_URL
        
        logger.debug(f"Initializing DatabaseConfig with URL: {url} and schema: {self.db_schema}")
        
        # Different engine configuration for SQLite vs PostgreSQL
        if "sqlite" in url.lower():
            logger.debug("Using SQLite configuration")
            self.engine = create_async_engine(
                url,
                echo=settings.DATABASE_ECHO,
                poolclass=NullPool
            )
        else:
            logger.debug("Using PostgreSQL configuration")
            self.engine = create_async_engine(
                url,
                echo=settings.DATABASE_ECHO,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                execution_options={"schema_translate_map": {None: self.db_schema}} if self.db_schema else {}
            )
            logger.debug("Engine created successfully")

        self.async_session_maker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        logger.debug("Session maker initialized")
    
    async def create_tables(self) -> None:
        """Create database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def drop_tables(self) -> None:
        """Drop database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session."""
        async with self.async_session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# Global database configuration instance
db_config = DatabaseConfig()

# Create database engine and session maker
engine = db_config.engine
SessionLocal = db_config.async_session_maker


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency."""
    async for session in db_config.get_session():
        yield session


async def check_database_health() -> bool:
    """Check database connection health."""
    try:
        async with SessionLocal() as session:
            await session.execute(text("SELECT 1"))
            await session.commit()
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return False


async def initialize_database() -> None:
    """Initialize database with tables."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise


async def close_database() -> None:
    """Close database connections."""
    try:
        await engine.dispose()
        logger.info("Database connections closed successfully")
    except Exception as e:
        logger.error(f"Failed to close database connections: {str(e)}")
        raise
