"""Questionnaire Pydantic schemas for API validation."""

from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, validator
from datetime import datetime


class QuestionnaireCreateSchema(BaseModel):
    """Schema para crear un nuevo cuestionario."""
    
    name: str = Field(..., min_length=3, max_length=200, description="Nombre del cuestionario")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción del cuestionario")
    
    @validator('name')
    def validate_name(cls, v):
        """Validar que el nombre no esté vacío y sea único."""
        if not v or not v.strip():
            raise ValueError('El nombre del cuestionario no puede estar vacío')
        if v.strip() != v:
            raise ValueError('El nombre no puede tener espacios al inicio o final')
        return v.strip()
    
    class Config:
        json_json_schema_extra = {
            "example": {
                "name": "Evaluación Docente Semestre I-2025",
                "description": "Cuestionario para evaluar el desempeño docente en el primer semestre de 2025"
            }
        }


class QuestionnaireUpdateSchema(BaseModel):
    """Schema para actualizar un cuestionario existente."""
    
    name: Optional[str] = Field(None, min_length=3, max_length=200, description="Nombre del cuestionario")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción del cuestionario")
    is_active: Optional[bool] = Field(None, description="Estado activo del cuestionario")
    
    @validator('name')
    def validate_name(cls, v):
        """Validar que el nombre no esté vacío si se proporciona."""
        if v is not None:
            if not v or not v.strip():
                raise ValueError('El nombre del cuestionario no puede estar vacío')
            if v.strip() != v:
                raise ValueError('El nombre no puede tener espacios al inicio o final')
            return v.strip()
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Evaluación Docente Semestre I-2025 Actualizada",
                "description": "Descripción actualizada del cuestionario",
                "is_active": True
            }
        }


class QuestionnaireResponseSchema(BaseModel):
    """Schema para respuesta de cuestionario."""
    
    id: UUID
    name: str
    description: Optional[str]
    is_active: bool
    question_count: int
    question_ids: List[UUID]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Evaluación Docente Semestre I-2025",
                "description": "Cuestionario para evaluar el desempeño docente",
                "is_active": True,
                "question_count": 15,
                "question_ids": [],
                "created_at": "2025-06-13T10:00:00Z",
                "updated_at": "2025-06-13T10:00:00Z"
            }
        }


class QuestionnaireListResponseSchema(BaseModel):
    """Schema para respuesta de lista de cuestionarios."""
    
    questionnaires: List[QuestionnaireResponseSchema]
    total: int
    skip: int
    limit: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "questionnaires": [],
                "total": 5,
                "skip": 0,
                "limit": 10
            }
        }


class AddQuestionToQuestionnaireSchema(BaseModel):
    """Schema para agregar pregunta a cuestionario."""
    
    question_id: UUID = Field(..., description="ID de la pregunta a agregar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class RemoveQuestionFromQuestionnaireSchema(BaseModel):
    """Schema para remover pregunta de cuestionario."""
    
    question_id: UUID = Field(..., description="ID de la pregunta a remover")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }
