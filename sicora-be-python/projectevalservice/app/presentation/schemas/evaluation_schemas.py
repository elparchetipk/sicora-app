from pydantic import BaseModel, Field, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class EvaluationStatusSchema(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class EvaluationTypeSchema(str, Enum):
    IDEA_EVALUATION = "idea_evaluation"
    PROGRESS_EVALUATION = "progress_evaluation"
    FINAL_EVALUATION = "final_evaluation"
    EXTRAORDINARY_EVALUATION = "extraordinary_evaluation"


class EvaluationCreateSchema(BaseModel):
    project_id: UUID4 = Field(..., description="Project ID")
    evaluation_type: EvaluationTypeSchema = Field(..., description="Type of evaluation")
    trimester: int = Field(..., ge=1, le=7, description="Academic trimester")
    academic_year: int = Field(..., ge=2020, description="Academic year")
    scheduled_date: datetime = Field(..., description="Scheduled date and time")
    duration_minutes: int = Field(..., ge=15, le=480, description="Duration in minutes")
    location: str = Field(
        ..., min_length=1, max_length=255, description="Evaluation location"
    )

    class Config:
        schema_extra = {
            "example": {
                "project_id": "123e4567-e89b-12d3-a456-426614174000",
                "evaluation_type": "progress_evaluation",
                "trimester": 3,
                "academic_year": 2025,
                "scheduled_date": "2025-07-15T14:00:00Z",
                "duration_minutes": 60,
                "location": "Aula 201 - CGMLTI",
            }
        }


class EvaluationScoresSchema(BaseModel):
    technical_score: float = Field(
        ..., ge=0.0, le=5.0, description="Technical score (0-5)"
    )
    presentation_score: float = Field(
        ..., ge=0.0, le=5.0, description="Presentation score (0-5)"
    )
    documentation_score: float = Field(
        ..., ge=0.0, le=5.0, description="Documentation score (0-5)"
    )
    innovation_score: float = Field(
        ..., ge=0.0, le=5.0, description="Innovation score (0-5)"
    )
    collaboration_score: float = Field(
        ..., ge=0.0, le=5.0, description="Collaboration score (0-5)"
    )

    class Config:
        schema_extra = {
            "example": {
                "technical_score": 4.2,
                "presentation_score": 3.8,
                "documentation_score": 4.0,
                "innovation_score": 3.5,
                "collaboration_score": 4.5,
            }
        }


class EvaluationFeedbackSchema(BaseModel):
    general_comments: Optional[str] = Field(None, description="General comments")
    technical_feedback: Optional[str] = Field(None, description="Technical feedback")
    presentation_feedback: Optional[str] = Field(
        None, description="Presentation feedback"
    )
    improvement_suggestions: Optional[str] = Field(
        None, description="Improvement suggestions"
    )

    class Config:
        schema_extra = {
            "example": {
                "general_comments": "El proyecto muestra un buen progreso general",
                "technical_feedback": "La arquitectura del código es sólida, pero se pueden mejorar las validaciones",
                "presentation_feedback": "La presentación fue clara y bien estructurada",
                "improvement_suggestions": "Implementar pruebas unitarias y mejorar la documentación técnica",
            }
        }


class EvaluationCompleteSchema(BaseModel):
    scores: EvaluationScoresSchema
    feedback: EvaluationFeedbackSchema

    class Config:
        schema_extra = {
            "example": {
                "scores": {
                    "technical_score": 4.2,
                    "presentation_score": 3.8,
                    "documentation_score": 4.0,
                    "innovation_score": 3.5,
                    "collaboration_score": 4.5,
                },
                "feedback": {
                    "general_comments": "El proyecto muestra un buen progreso general",
                    "technical_feedback": "La arquitectura del código es sólida",
                    "presentation_feedback": "La presentación fue clara y bien estructurada",
                    "improvement_suggestions": "Implementar pruebas unitarias",
                },
            }
        }


class VoiceNotesSchema(BaseModel):
    voice_url: str = Field(..., description="URL of the voice recording")
    transcript: str = Field(..., description="Transcript of the voice recording")

    class Config:
        schema_extra = {
            "example": {
                "voice_url": "https://storage.example.com/evaluations/voice_notes/123.mp3",
                "transcript": "El proyecto demuestra un buen entendimiento de los requisitos...",
            }
        }


class EvaluationRescheduleSchema(BaseModel):
    new_date: datetime = Field(..., description="New scheduled date")
    reason: str = Field(..., min_length=1, description="Reason for rescheduling")

    class Config:
        schema_extra = {
            "example": {
                "new_date": "2025-07-20T14:00:00Z",
                "reason": "Instructor unavailable due to emergency",
            }
        }


class EvaluationResponseSchema(BaseModel):
    id: UUID4
    project_id: UUID4
    evaluation_type: EvaluationTypeSchema
    status: EvaluationStatusSchema
    trimester: int
    academic_year: int
    scheduled_date: datetime
    actual_date: Optional[datetime]
    duration_minutes: int
    location: str

    # Scores
    technical_score: Optional[float]
    presentation_score: Optional[float]
    documentation_score: Optional[float]
    innovation_score: Optional[float]
    collaboration_score: Optional[float]
    overall_score: Optional[float]

    # Feedback
    general_comments: Optional[str]
    technical_feedback: Optional[str]
    presentation_feedback: Optional[str]
    improvement_suggestions: Optional[str]
    voice_notes_url: Optional[str]
    voice_notes_transcript: Optional[str]

    # Metadata
    created_at: datetime
    updated_at: datetime
    created_by: UUID4
    evaluated_by: Optional[UUID4]

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "project_id": "123e4567-e89b-12d3-a456-426614174001",
                "evaluation_type": "progress_evaluation",
                "status": "completed",
                "trimester": 3,
                "academic_year": 2025,
                "scheduled_date": "2025-07-15T14:00:00Z",
                "actual_date": "2025-07-15T14:05:00Z",
                "duration_minutes": 60,
                "location": "Aula 201 - CGMLTI",
                "technical_score": 4.2,
                "presentation_score": 3.8,
                "documentation_score": 4.0,
                "innovation_score": 3.5,
                "collaboration_score": 4.5,
                "overall_score": 4.0,
                "general_comments": "El proyecto muestra un buen progreso general",
                "technical_feedback": "La arquitectura del código es sólida",
                "presentation_feedback": "La presentación fue clara",
                "improvement_suggestions": "Implementar pruebas unitarias",
                "voice_notes_url": None,
                "voice_notes_transcript": None,
                "created_at": "2025-06-17T10:00:00Z",
                "updated_at": "2025-07-15T15:00:00Z",
                "created_by": "123e4567-e89b-12d3-a456-426614174002",
                "evaluated_by": "123e4567-e89b-12d3-a456-426614174003",
            }
        }


class EvaluationStartSchema(BaseModel):
    evaluator_id: UUID4 = Field(..., description="ID of the evaluator starting the session")

    class Config:
        schema_extra = {
            "example": {
                "evaluator_id": "123e4567-e89b-12d3-a456-426614174003",
            }
        }


class EvaluationVoiceNoteSchema(BaseModel):
    voice_url: str = Field(..., description="URL of the voice recording")
    transcript: str = Field(..., description="Transcript of the voice recording")

    class Config:
        schema_extra = {
            "example": {
                "voice_url": "https://storage.example.com/evaluations/voice_notes/123.mp3",
                "transcript": "El proyecto demuestra un buen entendimiento de los requisitos...",
            }
        }


class EvaluationListResponseSchema(BaseModel):
    evaluations: List[EvaluationResponseSchema]
    total_count: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        schema_extra = {
            "example": {
                "evaluations": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "project_id": "123e4567-e89b-12d3-a456-426614174001",
                        "evaluation_type": "progress_evaluation",
                        "status": "completed",
                        "trimester": 3,
                        "academic_year": 2025,
                        "scheduled_date": "2025-07-15T14:00:00Z",
                        "actual_date": "2025-07-15T14:05:00Z",
                        "duration_minutes": 60,
                        "location": "Aula 201 - CGMLTI",
                        "technical_score": 4.2,
                        "presentation_score": 3.8,
                        "documentation_score": 4.0,
                        "innovation_score": 3.5,
                        "collaboration_score": 4.5,
                        "overall_score": 4.0,
                        "general_comments": "El proyecto muestra un buen progreso general",
                        "technical_feedback": "La arquitectura del código es sólida",
                        "presentation_feedback": "La presentación fue clara",
                        "improvement_suggestions": "Implementar pruebas unitarias",
                        "voice_notes_url": None,
                        "voice_notes_transcript": None,
                        "created_at": "2025-06-17T10:00:00Z",
                        "updated_at": "2025-07-15T15:00:00Z",
                        "created_by": "123e4567-e89b-12d3-a456-426614174002",
                        "evaluated_by": "123e4567-e89b-12d3-a456-426614174003",
                    }
                ],
                "total_count": 10,
                "page": 1,
                "page_size": 10,
                "total_pages": 1,
            }
        }
