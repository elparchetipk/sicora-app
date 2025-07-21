"""
SICORA API Gateway
Gateway principal para todos los microservicios
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar todos los routers
from routers.users import router as users_router
from routers.attendance import router as attendance_router
from routers.evalin import router as evalin_router
from routers.schedules import router as schedules_router
from routers.meval import router as meval_router
from routers.knowledge_base import router as kb_router
from routers.ai import router as ai_router
from routers.go_services import router as go_services_router
from health.checker import check_all_services

app = FastAPI(
    title="SICORA API Gateway",
    version="2.0.0",
    description="Gateway central para todos los microservicios de SICORA"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir routers del stack Python
app.include_router(
    users_router, prefix="/api/v1/users", tags=["users"]
)
app.include_router(
    attendance_router, prefix="/api/v1/attendance", tags=["attendance"]
)
app.include_router(
    evalin_router, prefix="/api/v1/evalin", tags=["evalin"]
)
app.include_router(
    schedules_router, prefix="/api/v1/schedules", tags=["schedules"]
)
app.include_router(
    meval_router, prefix="/api/v1/meval", tags=["meval"]
)
app.include_router(
    kb_router, prefix="/api/v1/kb", tags=["knowledge-base"]
)
app.include_router(
    ai_router, prefix="/api/v1/ai", tags=["ai"]
)

# Incluir router para servicios Go
app.include_router(
    go_services_router, prefix="/api/v1", tags=["go-services"]
)


@app.get("/health")
async def health_check():
    """Verificación de salud del gateway y servicios."""
    services_status = await check_all_services()
    return {
        "status": "healthy",
        "gateway": "operational",
        "services": services_status
    }


@app.get("/")
async def root():
    """Endpoint raíz."""
    return {
        "message": "SICORA API Gateway",
        "version": "2.0.0",
        "status": "operational",
        "available_services": {
            "python_stack": [
                "users", "attendance", "evalin", "schedules",
                "meval", "knowledge-base", "ai"
            ],
            "go_stack": [
                "user-go", "attendance-go", "schedule-go", "evalin-go",
                "meval-go", "kb-go", "project-eval-go", "software-factory-go"
            ]
        }
    }