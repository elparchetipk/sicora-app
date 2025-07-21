"""
SICORA API Gateway
Gateway principal para todos los microservicios
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
import sys

# Añadir la ruta del directorio shared al path para importar la configuración
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Importar configuración centralizada
from shared.config import get_settings

# Importar configuración de base de datos
from app.infrastructure.database.database import init_db, engine
from app.infrastructure.database.models import Base

# Importar middleware
from app.presentation.middleware.auth import AuthMiddleware

# Importar todos los routers desde la nueva estructura
from app.presentation.routers.users import router as users_router
from app.presentation.routers.attendance import router as attendance_router
from app.presentation.routers.evalin import router as evalin_router
from app.presentation.routers.schedules import router as schedules_router
from app.presentation.routers.meval import router as meval_router
from app.presentation.routers.knowledge_base import router as kb_router
from app.presentation.routers.ai import router as ai_router
from app.presentation.routers.go_services import router as go_services_router
from health.checker import check_all_services

# Configuración de logging básica (se refinará en lifespan)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación.
    Inicializa la base de datos al iniciar y limpia los recursos al cerrar.
    """
    # Cargar configuración centralizada
    settings = get_settings()

    # Configurar logging con configuración centralizada
    logging.basicConfig(
        level=getattr(logging, settings.log_level.value),
        format=settings.log_format,
        force=True,  # Sobrescribir configuración anterior
    )

    # Startup
    logger.info("Starting APIGateway...")
    logger.info(f"Environment: {settings.environment.value}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"API Host: {settings.api.host}:{settings.api.port}")

    # Crear tablas de base de datos
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database initialized successfully")

    yield

    # Shutdown
    logger.info("Shutting down APIGateway...")
    await engine.dispose()
    logger.info("Resources cleaned up successfully")


app = FastAPI(
    title="SICORA API Gateway",
    version="2.0.0",
    description="Gateway central para todos los microservicios de SICORA",
    lifespan=lifespan,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware de logging de requests
@app.middleware("http")
async def log_requests(request, call_next):
    """Middleware para logging de requests."""
    import time
    from app.infrastructure.database.models import RequestLogModel
    from app.infrastructure.database.database import AsyncSessionLocal

    start_time = time.time()

    # Procesar request
    response = await call_next(request)

    # Calcular tiempo de respuesta
    process_time = (time.time() - start_time) * 1000

    # Log básico
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.2f}ms"
    )

    # Guardar en base de datos (async)
    try:
        async with AsyncSessionLocal() as session:
            log_entry = RequestLogModel(
                service_name="apigateway",
                endpoint=str(request.url.path),
                method=request.method,
                status_code=response.status_code,
                response_time_ms=process_time,
                request_size_bytes=0,  # Simplificado por ahora
                response_size_bytes=0,  # Simplificado por ahora
                ip_address=request.client.host if request.client else "unknown",
                user_agent=request.headers.get("user-agent", ""),
                status="success" if response.status_code < 400 else "error",
            )
            session.add(log_entry)
            await session.commit()
    except Exception as e:
        logger.error(f"Error saving request log: {e}")

    return response


# Endpoints de sistema
@app.get("/health", tags=["system"])
async def health_check():
    """Health check del APIGateway."""
    return {
        "status": "healthy",
        "service": "apigateway",
        "version": "2.0.0",
        "timestamp": "2025-07-19T20:00:00Z",
    }


@app.get("/metrics", tags=["system"])
async def get_metrics():
    """Métricas básicas del APIGateway."""
    from app.infrastructure.database.database import AsyncSessionLocal
    from app.infrastructure.database.models import RequestLogModel
    from sqlalchemy import func, select

    try:
        async with AsyncSessionLocal() as session:
            # Contar total de requests
            total_requests = await session.scalar(
                select(func.count(RequestLogModel.id))
            )

            # Promedio de tiempo de respuesta
            avg_response_time = await session.scalar(
                select(func.avg(RequestLogModel.response_time_ms))
            )

            return {
                "total_requests": total_requests or 0,
                "avg_response_time_ms": round(avg_response_time or 0, 2),
                "status": "operational",
            }
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return {
            "total_requests": 0,
            "avg_response_time_ms": 0,
            "status": "error",
            "error": str(e),
        }


# Incluir routers del stack Python
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(attendance_router, prefix="/api/v1/attendance", tags=["attendance"])
app.include_router(evalin_router, prefix="/api/v1/evalin", tags=["evalin"])
app.include_router(schedules_router, prefix="/api/v1/schedules", tags=["schedules"])
app.include_router(meval_router, prefix="/api/v1/meval", tags=["meval"])
app.include_router(kb_router, prefix="/api/v1/kb", tags=["knowledge-base"])
app.include_router(ai_router, prefix="/api/v1/ai", tags=["ai"])

# Incluir router para servicios Go
app.include_router(go_services_router, prefix="/api/v1", tags=["go-services"])


@app.get("/")
async def root():
    """Endpoint raíz."""
    return {
        "message": "SICORA API Gateway",
        "version": "2.0.0",
        "status": "operational",
        "available_services": {
            "python_stack": [
                "users",
                "attendance",
                "evalin",
                "schedules",
                "meval",
                "knowledge-base",
                "ai",
            ],
            "go_stack": [
                "user-go",
                "attendance-go",
                "schedule-go",
                "evalin-go",
                "meval-go",
                "kb-go",
                "project-eval-go",
                "software-factory-go",
            ],
        },
    }
