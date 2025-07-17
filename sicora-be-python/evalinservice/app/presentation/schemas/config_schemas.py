"""Configuration Pydantic schemas for API validation."""

from typing import Dict, List, Any
from pydantic import BaseModel, Field


class SystemConfigResponseSchema(BaseModel):
    """Schema para configuración del sistema."""
    
    max_questions_per_questionnaire: int
    min_questions_per_questionnaire: int
    max_evaluation_period_days: int
    min_evaluation_period_days: int
    max_score_value: float
    min_score_value: float
    default_question_types: List[str]
    max_comment_length: int
    evaluation_timeout_hours: int
    anonymous_evaluation_enabled: bool
    bulk_upload_max_questions: int
    export_formats: List[str]
    notification_settings: Dict[str, bool]
    
    class Config:
        json_schema_extra = {
            "example": {
                "max_questions_per_questionnaire": 50,
                "min_questions_per_questionnaire": 1,
                "max_evaluation_period_days": 365,
                "min_evaluation_period_days": 1,
                "max_score_value": 5.0,
                "min_score_value": 1.0,
                "default_question_types": ["likert", "text", "multiple_choice"],
                "max_comment_length": 1000,
                "evaluation_timeout_hours": 72,
                "anonymous_evaluation_enabled": True,
                "bulk_upload_max_questions": 1000,
                "export_formats": ["csv", "excel", "pdf"],
                "notification_settings": {
                    "period_start": True,
                    "period_end": True,
                    "evaluation_submitted": False,
                    "report_generated": True
                }
            }
        }
