"""
AttendanceService - Microservicio de Gestión de Asistencia
Aplicación principal FastAPI
"""

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.presentation.routers import (
    attendance_router,
    justifications_router,
    alerts_router
)
from app.config import settings
from app.dependencies import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    print("🚀 AttendanceService iniciando...")
    yield
    # Shutdown
    print("🔴 AttendanceService cerrando...")
    await engine.dispose()


app = FastAPI(
    title="AttendanceService",
    description="""
    ## 📋 Microservicio de Gestión de Asistencia
    
    Sistema completo para el registro, control y análisis de asistencia estudiantil.
    
    ### 🎯 Funcionalidades principales:
    
    * **📱 Registro de Asistencia**: Registro usando códigos QR dinámicos
    * **📝 Gestión de Justificaciones**: Subida y revisión de justificaciones con documentos
    * **🚨 Sistema de Alertas**: Alertas inteligentes por patrones de asistencia
    * **📊 Reportes**: Resúmenes y análisis de asistencia
    * **🔄 Integración**: Comunicación con UserService y ScheduleService
    
    ### 🏗️ Arquitectura:
    
    Implementado siguiendo **Clean Architecture** con:
    - **Domain**: Entidades, Value Objects y reglas de negocio
    - **Application**: Casos de uso y DTOs
    - **Infrastructure**: Repositorios y adaptadores externos
    - **Presentation**: API REST con FastAPI
    
    ### 🔐 Autenticación:
    
    Requiere token JWT válido en el header Authorization.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(attendance_router)
app.include_router(justifications_router)
app.include_router(alerts_router)


@app.get(
    "/health",
    tags=["health"],
    summary="Health Check",
    description="Endpoint para verificar el estado del servicio"
)
async def health_check():
    """
    Verifica que el servicio esté funcionando correctamente.
    """
    return {
        "status": "healthy",
        "service": "AttendanceService",
        "version": "1.0.0",
        "timestamp": "2025-06-12T12:00:00Z"
    }


@app.get(
    "/",
    tags=["root"],
    summary="Root Endpoint",
    description="Endpoint raíz con información del servicio"
)
async def root():
    """
    Información básica del servicio.
    """
    return {
        "service": "AttendanceService",
        "description": "Microservicio de Gestión de Asistencia",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Manejador global de excepciones no capturadas.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Internal server error",
            "details": str(exc) if settings.DATABASE_ECHO else "Contact system administrator"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003,
        reload=True
    )
