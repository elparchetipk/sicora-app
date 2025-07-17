from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from contextlib import asynccontextmanager

from app.presentation.routers import (
    question_router,
    questionnaire_router,
    period_router,
    evaluation_router,
    report_router,
    config_router,
    notification_router
)
from app.infrastructure.database.database import engine, Base
from app.infrastructure.database.session import get_db

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación.
    Se ejecuta al inicio y cierre de la aplicación.
    """
    # Startup
    logger.info("Starting EvalinService...")

    # Crear las tablas de la base de datos
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

    # Verificar conexión a servicios externos
    try:
        # TODO: Implementar verificación de servicios externos
        logger.info("External services status checked")
    except Exception as e:
        logger.warning(f"Some external services might not be available: {str(e)}")

    logger.info("EvalinService started successfully")

    yield

    # Shutdown
    logger.info("Shutting down EvalinService...")
    logger.info("EvalinService shut down successfully")

# Crear la aplicación FastAPI
app = FastAPI(
    title="EvalinService",
    description="""
    **Sistema de Evaluación de Instructores**

    Este servicio maneja la evaluación de instructores por parte de estudiantes, incluyendo:

    - **Gestión de Preguntas**: Crear y administrar preguntas de evaluación
    - **Cuestionarios**: Organizar preguntas en cuestionarios estructurados
    - **Períodos de Evaluación**: Definir ventanas temporales para evaluaciones
    - **Evaluaciones**: Permitir a estudiantes evaluar a sus instructores
    - **Reportes**: Generar análisis y reportes de las evaluaciones
    - **Configuración**: Administrar configuraciones del sistema

    ## Autenticación

    Todas las rutas requieren autenticación mediante JWT token.
    Los permisos varían según el rol del usuario:
    - **Admin**: Acceso completo a todas las funcionalidades
    - **Coordinator**: Gestión de evaluaciones y reportes
    - **Instructor**: Consulta de sus propias evaluaciones
    - **Student**: Envío de evaluaciones

    ## Arquitectura

    El servicio sigue los principios de Clean Architecture:
    - **Domain**: Entidades de negocio y reglas
    - **Application**: Casos de uso y servicios de aplicación
    - **Infrastructure**: Persistencia y servicios externos
    - **Presentation**: API REST y validaciones
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de hosts confiables
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # En producción, especificar hosts específicos
)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logging de todas las requests"""
    start_time = time.time()

    # Log de la request entrante
    logger.info(f"Request: {request.method} {request.url}")

    response = await call_next(request)

    # Log de la response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.4f}s")

    return response

# Middleware para manejo de errores globales
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejador global de excepciones"""
    logger.error(f"Global exception: {type(exc).__name__}: {str(exc)}")

    # En desarrollo, mostrar detalles del error
    # En producción, mostrar mensaje genérico
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "type": type(exc).__name__,
            "timestamp": time.time()
        }
    )

# Middleware para manejo de errores HTTP
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Manejador específico de HTTPException"""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "timestamp": time.time()
        }
    )

# Incluir routers
app.include_router(
    question_router.router,
    prefix="/api/v1",
    tags=["questions"]
)

app.include_router(
    questionnaire_router.router,
    prefix="/api/v1",
    tags=["questionnaires"]
)

app.include_router(
    period_router.router,
    prefix="/api/v1",
    tags=["periods"]
)

app.include_router(
    evaluation_router.router,
    prefix="/api/v1",
    tags=["evaluations"]
)

app.include_router(
    report_router.router,
    prefix="/api/v1",
    tags=["reports"]
)

app.include_router(
    config_router.router,
    prefix="/api/v1",
    tags=["configuration"]
)

app.include_router(
    notification_router.router,
    prefix="/api/v1",
    tags=["notifications"]
)

# Rutas de health check
@app.get("/", tags=["health"])
async def root():
    """Endpoint raíz del servicio"""
    return {
        "service": "EvalinService",
        "version": "1.0.0",
        "status": "healthy",
        "message": "Instructor Evaluation Service is running"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint para monitoreo"""
    try:
        # Verificar conexión a la base de datos
        next(get_db())
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "service": "EvalinService",
        "status": "healthy",
        "timestamp": time.time(),
        "database": db_status,
        "version": "1.0.0"
    }

@app.get("/metrics", tags=["monitoring"])
async def get_metrics():
    """Endpoint para métricas básicas del servicio"""
    return {
        "service": "EvalinService",
        "uptime": time.time(),  # Simplificado, en producción usar tiempo real de uptime
        "endpoints": len(app.routes),
        "version": "1.0.0"
    }

# Manejo de rutas no encontradas
@app.get("/{path:path}")
async def catch_all(path: str):
    """Capturar rutas no definidas"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Route not found: /{path}"
    )

if __name__ == "__main__":
    import uvicorn

    # Configuración para desarrollo
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
