from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Simple FastAPI app for testing
app = FastAPI(
    title="EvalProy Service",
    description="Servicio para gestión de proyectos de evaluación",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "EvalProy Service is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "evalproyservice"}


@app.get("/api/v1/projects")
async def get_projects():
    return {"projects": [], "message": "Projects endpoint working"}
