"""
ScheduleService - Main application module.

This microservice handles schedule management including:
- Schedule CRUD operations  
- Academic programs and groups management
- Facilities and venues management
- Bulk schedule uploads
- Filtered schedule queries

Following Clean Architecture principles with:
- Domain Layer: Entities, Value Objects, Repository Interfaces
- Application Layer: Use Cases, DTOs, Service Interfaces  
- Infrastructure Layer: Repository Implementations, External Services
- Presentation Layer: FastAPI routers, Request/Response schemas
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.infrastructure.config.database import engine, Base
from app.presentation.routers.schedule_router import router as schedule_router
from app.presentation.routers.admin_router import router as admin_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ScheduleService API",
    description="Microservice for schedule and academic entity management",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Schedule",
            "description": "Schedule management operations"
        },
        {
            "name": "Admin",
            "description": "Administrative operations for schedules and entities"
        }
    ]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(schedule_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {
        "service": "ScheduleService",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
