"""
FastAPI NotificationService - Main Module

Este es el punto de entrada principal para el NotificationService.
Implementa Clean Architecture siguiendo los patrones de UserService y EvalinService.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.presentation.routers import notification_router
from app.infrastructure.database.database import init_db, engine
from app.infrastructure.database.models import Base
from app.domain.entities.notification import (
    NotificationError,
    InvalidNotificationDataError,
)

# Configuración de logging
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
    # Startup
    logger.info("Starting NotificationService...")

    # Crear tablas de base de datos
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database initialized successfully")

    yield

    # Shutdown
    logger.info("Shutting down NotificationService...")
    await engine.dispose()
    logger.info("Resources cleaned up successfully")


# Configurar la aplicación FastAPI
app = FastAPI(
    title="SICORA NotificationService API",
    description="""
    Microservicio de notificaciones para el Sistema SICORA.

    Funcionalidades:
    - Crear notificaciones para usuarios
    - Marcar notificaciones como leídas
    - Obtener notificaciones por usuario

    Implementa Clean Architecture con FastAPI.
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware de logging de requests
@app.middleware("http")
async def log_requests(request, call_next):
    """Middleware para logging de requests de notificaciones."""
    import time

    start_time = time.time()

    # Procesar request
    response = await call_next(request)

    # Calcular tiempo de respuesta
    process_time = (time.time() - start_time) * 1000

    # Log básico
    logger.info(
        f"NOTIFICATION-SERVICE: {request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.2f}ms"
    )

    return response


# Incluir routers
app.include_router(notification_router.router, prefix="/api/v1")


# Endpoints de sistema
@app.get("/metrics", tags=["system"])
async def get_metrics():
    """Métricas del servicio de notificaciones."""
    from app.infrastructure.database.database import AsyncSessionLocal
    from app.infrastructure.database.models import NotificationModel
    from sqlalchemy import func, select

    try:
        async with AsyncSessionLocal() as session:
            # Contar notificaciones totales
            total_notifications = await session.scalar(
                select(func.count(NotificationModel.id))
            )

            # Contar notificaciones leídas (como indicador de éxito)
            read_notifications = await session.scalar(
                select(func.count(NotificationModel.id)).where(
                    NotificationModel.read_status == True
                )
            )

            # Calcular tasa de lectura
            read_rate = (
                (read_notifications / total_notifications * 100)
                if total_notifications > 0
                else 0
            )

            return {
                "total_notifications": total_notifications or 0,
                "read_notifications": read_notifications or 0,
                "read_rate_percent": round(read_rate, 2),
                "status": "operational",
            }

    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return {
            "total_notifications": 0,
            "read_notifications": 0,
            "read_rate_percent": 0,
            "status": "error",
            "error": str(e),
        }


# Implementar health check
@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Verifica el estado del servicio y sus dependencias.
    """
    # TODO: Expandir para verificar estado de base de datos y servicios externos
    return {"status": "healthy", "service": "NotificationService", "version": "1.0.0"}


# Implementar manejo global de excepciones
@app.exception_handler(NotificationError)
async def notification_exception_handler(request: Request, exc: NotificationError):
    """
    Manejador de excepciones para errores de notificación.
    """
    status_code = 400
    if isinstance(exc, InvalidNotificationDataError):
        status_code = 422

    return JSONResponse(status_code=status_code, content={"detail": str(exc)})


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Manejador de excepciones general.
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500, content={"detail": "Error interno del servidor"}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True, log_level="info")
