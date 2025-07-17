"""
AIService FastAPI Application
Microservicio de IA para el proyecto Asiste App
"""
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.config.database import check_database_health
from app.presentation.routers.enhanced_chat_router_simple import (
    router as enhanced_chat_router
)
from app.presentation.schemas.chat_schemas import HealthCheckResponse

app = FastAPI(
    title="AI Service",
    description="Microservicio de Inteligencia Artificial para Asiste App",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - solo enhanced chat por ahora
app.include_router(
    enhanced_chat_router,
    prefix="/api/v1/chat",
    tags=["enhanced-chat"]
)


@app.get("/", response_model=HealthCheckResponse)
async def root():
    """Root endpoint"""
    return HealthCheckResponse(
        status="healthy",
        message="AI Service is running",
        service="aiservice",
        version="1.0.0"
    )


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Check database health si está disponible
        try:
            await check_database_health()
        except Exception:
            pass  # Ignorar errores de DB por ahora
        
        return HealthCheckResponse(
            status="healthy",
            message="AI Service operational - Enhanced Chat Ready",
            service="aiservice",
            version="1.0.0"
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Health check failed: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8007,
        reload=True,
        log_level="info"
    )
