"""PostgreSQL configuration and pgvector setup for Knowledge Base Service."""

import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError

from app.config import settings

logger = logging.getLogger(__name__)


async def enable_pgvector_extension(engine: AsyncEngine) -> bool:
    """Enable pgvector extension in PostgreSQL."""
    try:
        async with engine.begin() as conn:
            # Check if pgvector extension is available
            result = await conn.execute(
                text("SELECT 1 FROM pg_available_extensions WHERE name = 'vector'")
            )
            if not result.fetchone():
                logger.warning("pgvector extension is not available in this PostgreSQL installation")
                return False
            
            # Enable the extension
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            logger.info("✅ pgvector extension enabled successfully")
            return True
            
    except ProgrammingError as e:
        logger.error(f"Failed to enable pgvector extension: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error enabling pgvector: {e}")
        return False


async def create_vector_indexes(engine: AsyncEngine) -> bool:
    """Create vector indexes for efficient similarity search."""
    try:
        async with engine.begin() as conn:
            # Check if the table exists
            result = await conn.execute(
                text("""
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = 'knowledge_items'
                """)
            )
            
            if not result.fetchone():
                logger.warning("knowledge_items table does not exist yet")
                return False
            
            # Create HNSW index for vector similarity search
            await conn.execute(
                text("""
                CREATE INDEX IF NOT EXISTS idx_knowledge_items_embedding_hnsw
                ON knowledge_items 
                USING hnsw (embedding vector_cosine_ops)
                WITH (m = 16, ef_construction = 64)
                """)
            )
            
            # Create IVFFlat index as alternative
            await conn.execute(
                text("""
                CREATE INDEX IF NOT EXISTS idx_knowledge_items_embedding_ivfflat
                ON knowledge_items 
                USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 100)
                """)
            )
            
            logger.info("✅ Vector indexes created successfully")
            return True
            
    except ProgrammingError as e:
        logger.error(f"Failed to create vector indexes: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error creating vector indexes: {e}")
        return False


async def verify_pgvector_setup(engine: AsyncEngine) -> dict:
    """Verify pgvector setup and return status information."""
    status = {
        "extension_available": False,
        "extension_enabled": False,
        "vector_indexes": False,
        "database_type": "unknown"
    }
    
    try:
        async with engine.connect() as conn:
            # Check database type
            result = await conn.execute(text("SELECT version()"))
            version_info = result.fetchone()[0]
            
            if "PostgreSQL" in version_info:
                status["database_type"] = "postgresql"
                
                # Check if pgvector extension is enabled
                result = await conn.execute(
                    text("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
                )
                status["extension_enabled"] = result.fetchone() is not None
                
                # Check if pgvector is available
                result = await conn.execute(
                    text("SELECT 1 FROM pg_available_extensions WHERE name = 'vector'")
                )
                status["extension_available"] = result.fetchone() is not None
                
                # Check vector indexes
                result = await conn.execute(
                    text("""
                    SELECT 1 FROM pg_indexes 
                    WHERE tablename = 'knowledge_items' 
                    AND indexname LIKE '%embedding%'
                    """)
                )
                status["vector_indexes"] = result.fetchone() is not None
                
            elif "SQLite" in version_info:
                status["database_type"] = "sqlite"
                
    except Exception as e:
        logger.error(f"Error verifying pgvector setup: {e}")
    
    return status


async def setup_postgresql_for_vectors(engine: AsyncEngine) -> bool:
    """Complete setup of PostgreSQL with pgvector."""
    logger.info("🔧 Setting up PostgreSQL with pgvector...")
    
    # Verify current status
    status = await verify_pgvector_setup(engine)
    logger.info(f"Current status: {status}")
    
    if status["database_type"] != "postgresql":
        logger.info(f"Database type is {status['database_type']}, skipping pgvector setup")
        return True
    
    success = True
    
    # Enable pgvector extension
    if not status["extension_enabled"]:
        if status["extension_available"]:
            success &= await enable_pgvector_extension(engine)
        else:
            logger.warning("⚠️ pgvector extension not available - install it first")
            return False
    else:
        logger.info("✅ pgvector extension already enabled")
    
    # Create vector indexes (will be done after migrations)
    # This is commented out because indexes should be created after table creation
    # success &= await create_vector_indexes(engine)
    
    return success


def is_postgresql_database() -> bool:
    """Check if the configured database is PostgreSQL."""
    return settings.DATABASE_URL.startswith(("postgresql://", "postgresql+asyncpg://"))


def is_sqlite_database() -> bool:
    """Check if the configured database is SQLite."""
    return settings.DATABASE_URL.startswith(("sqlite://", "sqlite+aiosqlite://"))
