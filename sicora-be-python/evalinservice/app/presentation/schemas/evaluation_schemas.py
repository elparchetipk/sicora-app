"""Evaluation Pydantic schemas for API validation."""

from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, validator
from datetime import datetime


class QuestionResponseSchema(BaseModel):
    """Schema para respuesta a una pregunta."""
    
    question_id: UUID = Field(..., description="ID de la pregunta")
    score: float = Field(..., ge=1.0, le=5.0, description="Puntuación (1.0 - 5.0)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question_id": "123e4567-e89b-12d3-a456-426614174000",
                "score": 4.5
            }
        }


class EvaluationCreateSchema(BaseModel):
    """Schema para crear una nueva evaluación."""
    
    instructor_id: UUID = Field(..., description="ID del instructor evaluado")
    evaluation_period_id: UUID = Field(..., description="ID del período de evaluación")
    responses: List[QuestionResponseSchema] = Field(..., description="Respuestas a las preguntas")
    comments: Optional[str] = Field(None, max_length=1000, description="Comentarios adicionales")
    
    @validator('responses')
    def validate_responses(cls, v):
        """Validar que haya al menos una respuesta."""
        if not v:
            raise ValueError('Debe proporcionar al menos una respuesta')
        
        # Verificar que no haya preguntas duplicadas
        question_ids = [resp.question_id for resp in v]
        if len(question_ids) != len(set(question_ids)):
            raise ValueError('No puede haber respuestas duplicadas para la misma pregunta')
        
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "instructor_id": "123e4567-e89b-12d3-a456-426614174000",
                "evaluation_period_id": "123e4567-e89b-12d3-a456-426614174001",
                "responses": [
                    {
                        "question_id": "123e4567-e89b-12d3-a456-426614174002",
                        "score": 4.5
                    },
                    {
                        "question_id": "123e4567-e89b-12d3-a456-426614174003",
                        "score": 3.8
                    }
                ],
                "comments": "Excelente instructor, muy claro en sus explicaciones"
            }
        }


class EvaluationResponseSchema(BaseModel):
    """Schema para respuesta de evaluación."""
    
    id: UUID
    student_id: UUID
    instructor_id: UUID
    evaluation_period_id: UUID
    status: str
    responses: List[QuestionResponseSchema]
    comments: Optional[str]
    submitted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "student_id": "123e4567-e89b-12d3-a456-426614174001",
                "instructor_id": "123e4567-e89b-12d3-a456-426614174002",
                "evaluation_period_id": "123e4567-e89b-12d3-a456-426614174003",
                "status": "submitted",
                "responses": [
                    {
                        "question_id": "123e4567-e89b-12d3-a456-426614174004",
                        "score": 4.5
                    }
                ],
                "comments": "Muy buen instructor",
                "submitted_at": "2025-06-13T10:30:00Z",
                "created_at": "2025-06-13T10:00:00Z",
                "updated_at": "2025-06-13T10:30:00Z"
            }
        }


class EvaluationListResponseSchema(BaseModel):
    """Schema para respuesta de lista de evaluaciones."""
    
    evaluations: List[EvaluationResponseSchema]
    total: int
    skip: int
    limit: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "evaluations": [],
                "total": 45,
                "skip": 0,
                "limit": 10
            }
        }


class MyEvaluationsResponseSchema(BaseModel):
    """Schema para respuesta de mis evaluaciones (estudiante)."""
    
    pending_evaluations: List[dict]
    completed_evaluations: List[EvaluationResponseSchema]
    statistics: dict
    
    class Config:
        json_schema_extra = {
            "example": {
                "pending_evaluations": [
                    {
                        "period_id": "123e4567-e89b-12d3-a456-426614174000",
                        "period_name": "Evaluación 2025-I",
                        "instructor_id": "123e4567-e89b-12d3-a456-426614174001",
                        "instructor_name": "Juan Pérez",
                        "due_date": "2025-06-30T23:59:59Z"
                    }
                ],
                "completed_evaluations": [],
                "statistics": {
                    "total_pending": 1,
                    "total_completed": 0,
                    "completion_rate": 0.0
                }
            }
        }
