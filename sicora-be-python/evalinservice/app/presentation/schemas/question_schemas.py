"""Question Pydantic schemas for API validation."""

from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, validator
from datetime import datetime

from ...domain.value_objects import QuestionType


class QuestionCreateSchema(BaseModel):
    """Schema para crear una nueva pregunta."""
    
    text: str = Field(..., min_length=10, max_length=1000, description="Texto de la pregunta")
    question_type: QuestionType = Field(default=QuestionType.SCALE_1_5, description="Tipo de pregunta")
    category: Optional[str] = Field(None, max_length=100, description="Categoría de la pregunta")
    
    @validator('text')
    def validate_text(cls, v):
        """Validar que el texto no esté vacío y tenga contenido válido."""
        if not v or not v.strip():
            raise ValueError('El texto de la pregunta no puede estar vacío')
        if v.strip() != v:
            raise ValueError('El texto no puede tener espacios al inicio o final')
        return v.strip()
    
    class Config:
        json_json_schema_extra = {
            "example": {
                "text": "¿El instructor demuestra dominio del tema?",
                "question_type": "likert",
                "category": "dominio_tema"
            }
        }


class QuestionUpdateSchema(BaseModel):
    """Schema para actualizar una pregunta existente."""
    
    text: Optional[str] = Field(None, min_length=10, max_length=1000, description="Texto de la pregunta")
    question_type: Optional[QuestionType] = Field(None, description="Tipo de pregunta")
    category: Optional[str] = Field(None, max_length=100, description="Categoría de la pregunta")
    is_active: Optional[bool] = Field(None, description="Estado activo de la pregunta")
    
    @validator('text')
    def validate_text(cls, v):
        """Validar que el texto no esté vacío si se proporciona."""
        if v is not None:
            if not v or not v.strip():
                raise ValueError('El texto de la pregunta no puede estar vacío')
            if v.strip() != v:
                raise ValueError('El texto no puede tener espacios al inicio o final')
            return v.strip()
        return v
    
    class Config:
        json_json_schema_extra = {
            "example": {
                "text": "¿El instructor demuestra dominio del tema actualizado?",
                "category": "dominio_tema_actualizado",
                "is_active": True
            }
        }


class QuestionResponseSchema(BaseModel):
    """Schema para respuesta de pregunta."""
    
    id: UUID
    text: str
    question_type: QuestionType
    category: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "text": "¿El instructor demuestra dominio del tema?",
                "question_type": "likert",
                "category": "dominio_tema",
                "is_active": True,
                "created_at": "2025-06-13T10:00:00Z",
                "updated_at": "2025-06-13T10:00:00Z"
            }
        }


class QuestionListResponseSchema(BaseModel):
    """Schema para respuesta de lista de preguntas."""
    
    questions: List[QuestionResponseSchema]
    total: int
    skip: int
    limit: int
    
    class Config:
        json_json_schema_extra = {
            "example": {
                "questions": [],
                "total": 25,
                "skip": 0,
                "limit": 10
            }
        }


class BulkUploadQuestionSchema(BaseModel):
    """Schema para elemento de carga masiva de preguntas."""
    
    text: str = Field(..., min_length=10, max_length=1000)
    question_type: str = Field(default="likert")
    category: Optional[str] = Field(None, max_length=100)
    
    @validator('question_type')
    def validate_question_type(cls, v):
        """Validar que el tipo de pregunta sea válido."""
        valid_types = [qt.value for qt in QuestionType]
        if v.lower() not in valid_types:
            raise ValueError(f'Tipo de pregunta inválido. Tipos válidos: {valid_types}')
        return v.lower()
    
    class Config:
        json_json_schema_extra = {
            "example": {
                "text": "¿El instructor explica con claridad?",
                "question_type": "likert",
                "category": "comunicacion"
            }
        }


class BulkUploadResponseSchema(BaseModel):
    """Schema para respuesta de carga masiva."""
    
    total_processed: int
    successful: int
    failed: int
    errors: List[str]
    created_questions: List[QuestionResponseSchema]
    
    class Config:
        json_json_schema_extra = {
            "example": {
                "total_processed": 10,
                "successful": 8,
                "failed": 2,
                "errors": ["Fila 3: Texto muy corto", "Fila 7: Tipo de pregunta inválido"],
                "created_questions": []
            }
        }
