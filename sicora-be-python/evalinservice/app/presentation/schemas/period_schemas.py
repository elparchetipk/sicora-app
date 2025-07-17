"""Evaluation Period Pydantic schemas for API validation."""

from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, validator
from datetime import datetime

from ...domain.value_objects import PeriodStatus


class EvaluationPeriodCreateSchema(BaseModel):
    """Schema para crear un nuevo período de evaluación."""
    
    name: str = Field(..., min_length=3, max_length=200, description="Nombre del período")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción del período")
    start_date: datetime = Field(..., description="Fecha de inicio del período")
    end_date: datetime = Field(..., description="Fecha de fin del período")
    questionnaire_id: UUID = Field(..., description="ID del cuestionario a usar")
    target_groups: List[UUID] = Field(default_factory=list, description="IDs de grupos objetivo")
    is_anonymous: bool = Field(default=True, description="Si las evaluaciones son anónimas")
    
    @validator('name')
    def validate_name(cls, v):
        """Validar que el nombre no esté vacío."""
        if not v or not v.strip():
            raise ValueError('El nombre del período no puede estar vacío')
        return v.strip()
    
    @validator('end_date')
    def validate_dates(cls, v, values):
        """Validar que la fecha de fin sea posterior a la de inicio."""
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
        return v
    
    @validator('target_groups')
    def validate_target_groups(cls, v):
        """Validar que haya al menos un grupo objetivo."""
        if not v:
            raise ValueError('Debe especificar al menos un grupo objetivo')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Evaluación Docente - Período 2025-I",
                "description": "Período de evaluación de instructores para el primer semestre de 2025",
                "start_date": "2025-06-15T00:00:00Z",
                "end_date": "2025-06-30T23:59:59Z",
                "questionnaire_id": "123e4567-e89b-12d3-a456-426614174000",
                "target_groups": ["123e4567-e89b-12d3-a456-426614174001"],
                "is_anonymous": True
            }
        }


class EvaluationPeriodUpdateSchema(BaseModel):
    """Schema para actualizar un período de evaluación."""
    
    name: Optional[str] = Field(None, min_length=3, max_length=200, description="Nombre del período")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción del período")
    start_date: Optional[datetime] = Field(None, description="Fecha de inicio del período")
    end_date: Optional[datetime] = Field(None, description="Fecha de fin del período")
    target_groups: Optional[List[UUID]] = Field(None, description="IDs de grupos objetivo")
    
    @validator('name')
    def validate_name(cls, v):
        """Validar que el nombre no esté vacío si se proporciona."""
        if v is not None:
            if not v or not v.strip():
                raise ValueError('El nombre del período no puede estar vacío')
            return v.strip()
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Evaluación Docente - Período 2025-I Actualizado",
                "description": "Descripción actualizada del período",
                "end_date": "2025-07-15T23:59:59Z",
                "target_groups": ["123e4567-e89b-12d3-a456-426614174001", "123e4567-e89b-12d3-a456-426614174002"]
            }
        }


class EvaluationPeriodResponseSchema(BaseModel):
    """Schema para respuesta de período de evaluación."""
    
    id: UUID
    name: str
    description: Optional[str]
    start_date: datetime
    end_date: datetime
    status: str
    questionnaire_id: UUID
    target_groups: List[UUID]
    is_anonymous: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Evaluación Docente - Período 2025-I",
                "description": "Período de evaluación de instructores",
                "start_date": "2025-06-15T00:00:00Z",
                "end_date": "2025-06-30T23:59:59Z",
                "status": "active",
                "questionnaire_id": "123e4567-e89b-12d3-a456-426614174001",
                "target_groups": ["123e4567-e89b-12d3-a456-426614174002"],
                "is_anonymous": True,
                "created_at": "2025-06-13T10:00:00Z",
                "updated_at": "2025-06-13T10:00:00Z"
            }
        }


class EvaluationPeriodListResponseSchema(BaseModel):
    """Schema para respuesta de lista de períodos."""
    
    periods: List[EvaluationPeriodResponseSchema]
    total: int
    skip: int
    limit: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "periods": [],
                "total": 3,
                "skip": 0,
                "limit": 10
            }
        }
