from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import structlog
from contextlib import asynccontextmanager

from app.infrastructure.database.connection import database
from app.presentation.api.v1.router import api_router
from app.core.config import settings

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("🚀 Starting EvalProy Service")
    await database.connect()
    logger.info("✅ Database connected")

    yield

    # Shutdown
    logger.info("🔄 Shutting down EvalProy Service")
    await database.disconnect()
    logger.info("✅ Database disconnected")


# FastAPI app initialization
app = FastAPI(
    title="EvalProy Service",
    description="Sistema de Evaluación de Proyectos Formativos ADSO/PSW",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Security middlewares
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check."""
    return {"status": "healthy", "service": "evalproj-service", "version": "1.0.0"}


@app.get("/health/db", tags=["Health"])
async def health_check_db():
    """Database health check."""
    try:
        # Simple query to check DB connection
        await database.fetch_one("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "schema": settings.DB_SCHEMA,
        }
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with service information."""
    return {
        "service": "EvalProy Service",
        "description": "Sistema de Evaluación de Proyectos Formativos ADSO/PSW",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "stack": "FastAPI + SQLAlchemy + PostgreSQL 15",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8007, reload=True, log_level="info")
