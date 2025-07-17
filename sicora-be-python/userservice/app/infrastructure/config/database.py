"""Database configuration for user service."""

import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text
import logging

from app.config import settings
from ..models import Base

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Database configuration class."""
    
    def __init__(self):
        self.database_url = settings.DATABASE_URL
        self.db_schema = getattr(settings, 'DB_SCHEMA', 'public')
        
        logger.debug(f"Initializing DatabaseConfig with URL: {self.database_url} and schema: {self.db_schema}")
        
        # Configuration for PostgreSQL with asyncpg
        if "sqlite" in self.database_url.lower():
            self.engine = create_async_engine(
                self.database_url,
                echo=settings.DATABASE_ECHO,
                poolclass=NullPool
            )
        else:
            execution_options = {}
            if self.db_schema and self.db_schema.strip() and self.db_schema != 'public':
                execution_options = {"schema_translate_map": {None: self.db_schema}}
            
            self.engine = create_async_engine(
                self.database_url,
                echo=settings.DATABASE_ECHO,
                poolclass=NullPool if os.getenv("ENVIRONMENT") == "test" else None,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                execution_options=execution_options
            )
        
        self.async_session_maker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        logger.debug("Database configuration initialized successfully")
    
    
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
    
    async def close(self) -> None:
        """Close database engine."""
        await self.engine.dispose()


# Global database configuration instance
database_config = DatabaseConfig()
engine = database_config.engine


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session for dependency injection."""
    async with database_config.async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_database_health() -> bool:
    """Check database connection health."""
    try:
        async with database_config.async_session_maker() as session:
            await session.execute(text("SELECT 1"))
            return True
    except Exception:
        return False
