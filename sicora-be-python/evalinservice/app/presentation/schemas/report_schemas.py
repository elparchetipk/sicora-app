"""Report Pydantic schemas for API validation."""

from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime


class QuestionStatsSchema(BaseModel):
    """Schema para estadísticas de pregunta."""
    
    question_id: UUID
    question_text: str
    response_count: int
    average_score: float
    min_score: float
    max_score: float
    score_distribution: Dict[str, int]
    
    class Config:
        json_schema_extra = {
            "example": {
                "question_id": "123e4567-e89b-12d3-a456-426614174000",
                "question_text": "¿El instructor demuestra dominio del tema?",
                "response_count": 25,
                "average_score": 4.2,
                "min_score": 2.0,
                "max_score": 5.0,
                "score_distribution": {
                    "muy_bajo": 0,
                    "bajo": 2,
                    "medio": 5,
                    "alto": 10,
                    "muy_alto": 8
                }
            }
        }


class InstructorReportSchema(BaseModel):
    """Schema para reporte de instructor."""
    
    instructor_id: UUID
    instructor_name: str
    evaluation_period_id: UUID
    period_name: str
    total_evaluations: int
    question_stats: List[QuestionStatsSchema]
    overall_average: float
    comments: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "instructor_id": "123e4567-e89b-12d3-a456-426614174000",
                "instructor_name": "Juan Pérez",
                "evaluation_period_id": "123e4567-e89b-12d3-a456-426614174001",
                "period_name": "Evaluación 2025-I",
                "total_evaluations": 25,
                "question_stats": [],
                "overall_average": 4.2,
                "comments": [
                    "Excelente instructor",
                    "Muy claro en sus explicaciones"
                ]
            }
        }


class PeriodReportSchema(BaseModel):
    """Schema para reporte de período."""
    
    period_id: UUID
    period_name: str
    start_date: datetime
    end_date: datetime
    total_evaluations: int
    total_instructors: int
    completion_rate: float
    instructor_reports: List[InstructorReportSchema]
    period_stats: Dict[str, Any]
    
    class Config:
        json_schema_extra = {
            "example": {
                "period_id": "123e4567-e89b-12d3-a456-426614174000",
                "period_name": "Evaluación 2025-I",
                "start_date": "2025-06-15T00:00:00Z",
                "end_date": "2025-06-30T23:59:59Z",
                "total_evaluations": 150,
                "total_instructors": 6,
                "completion_rate": 85.5,
                "instructor_reports": [],
                "period_stats": {
                    "average_score": 4.1,
                    "best_rated_instructor": "Juan Pérez",
                    "most_evaluated_instructor": "María García"
                }
            }
        }


class ExportRequestSchema(BaseModel):
    """Schema para solicitud de exportación."""
    
    evaluation_period_id: UUID = Field(..., description="ID del período de evaluación")
    instructor_id: Optional[UUID] = Field(None, description="ID del instructor (opcional)")
    format: str = Field(default="csv", pattern="^(csv|excel|pdf)$", description="Formato de exportación")
    include_comments: bool = Field(default=True, description="Incluir comentarios en la exportación")
    include_anonymous: bool = Field(default=True, description="Incluir evaluaciones anónimas")
    
    class Config:
        json_schema_extra = {
            "example": {
                "evaluation_period_id": "123e4567-e89b-12d3-a456-426614174000",
                "instructor_id": "123e4567-e89b-12d3-a456-426614174001",
                "format": "csv",
                "include_comments": True,
                "include_anonymous": True
            }
        }


class ExportResponseSchema(BaseModel):
    """Schema para respuesta de exportación."""
    
    filename: str
    file_path: str
    file_size: int
    total_records: int
    generated_at: datetime
    download_url: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "filename": "evaluaciones_2025-I_20250613_143022.csv",
                "file_path": "/tmp/evalin_exports/evaluaciones_2025-I_20250613_143022.csv",
                "file_size": 15420,
                "total_records": 150,
                "generated_at": "2025-06-13T14:30:22Z",
                "download_url": "/api/v1/exports/evaluaciones_2025-I_20250613_143022.csv"
            }
        }
