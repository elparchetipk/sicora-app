from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Text,
    DateTime,
    Boolean,
    Float,
    Enum as SQLEnum,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
import uuid

# Database setup
DATABASE_URL = "sqlite:///./evalproyservice.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Enums
class ProjectStatus(str, Enum):
    IDEA_PROPOSAL = "idea_proposal"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProjectType(str, Enum):
    FORMATIVE = "formative"
    PRODUCTIVE = "productive"
    RESEARCH = "research"
    INNOVATION = "innovation"


# Database Model
class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.IDEA_PROPOSAL)
    project_type = Column(SQLEnum(ProjectType), nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    budget = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Pydantic models
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.IDEA_PROPOSAL
    project_type: ProjectType
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# FastAPI app
app = FastAPI(
    title="EvalProy Service",
    description="Servicio para gestión de proyectos de evaluación",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoints
@app.get("/")
async def root():
    return {"message": "EvalProy Service is running", "database": "connected"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "evalproyservice", "database": "sqlite"}


@app.get("/api/v1/projects", response_model=List[ProjectResponse])
async def get_projects(db: Session = Depends(get_db)):
    projects = db.query(ProjectModel).filter(ProjectModel.is_active == True).all()
    return projects


@app.post("/api/v1/projects", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = ProjectModel(id=str(uuid.uuid4()), **project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@app.get("/api/v1/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str, db: Session = Depends(get_db)):
    project = (
        db.query(ProjectModel)
        .filter(ProjectModel.id == project_id, ProjectModel.is_active == True)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.put("/api/v1/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str, project: ProjectCreate, db: Session = Depends(get_db)
):
    db_project = (
        db.query(ProjectModel)
        .filter(ProjectModel.id == project_id, ProjectModel.is_active == True)
        .first()
    )
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in project.dict().items():
        setattr(db_project, key, value)

    db_project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_project)
    return db_project


@app.delete("/api/v1/projects/{project_id}")
async def delete_project(project_id: str, db: Session = Depends(get_db)):
    db_project = (
        db.query(ProjectModel)
        .filter(ProjectModel.id == project_id, ProjectModel.is_active == True)
        .first()
    )
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    db_project.is_active = False
    db_project.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Project deleted successfully"}
