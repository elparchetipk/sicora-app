"""Configuration router for EvalinService API."""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status

from app.presentation.dependencies.auth import get_current_user, CurrentUser
from app.presentation.dependencies.container import get_get_system_config_use_case
from app.presentation.schemas.config_schemas import SystemConfigResponseSchema
from app.application.use_cases.get_system_config_use_case import GetSystemConfigUseCase

router = APIRouter(
    prefix="/config",
    tags=["configuration"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=SystemConfigResponseSchema)
async def get_system_config(
    current_user: CurrentUser = Depends(get_current_user),
    use_case: GetSystemConfigUseCase = Depends(get_get_system_config_use_case)
):
    """
    Obtener la configuración actual del sistema de evaluaciones.
    Accesible para todos los usuarios autenticados.
    """
    try:
        config = use_case.execute()
        
        return SystemConfigResponseSchema(
            max_questions_per_questionnaire=config.max_questions_per_questionnaire,
            min_questions_per_questionnaire=config.min_questions_per_questionnaire,
            max_evaluation_period_days=config.max_evaluation_period_days,
            min_evaluation_period_days=config.min_evaluation_period_days,
            max_score_value=config.max_score_value,
            min_score_value=config.min_score_value,
            default_question_types=config.default_question_types,
            max_comment_length=config.max_comment_length,
            evaluation_timeout_hours=config.evaluation_timeout_hours,
            anonymous_evaluation_enabled=config.anonymous_evaluation_enabled,
            bulk_upload_max_questions=config.bulk_upload_max_questions,
            export_formats=config.export_formats,
            notification_settings=config.notification_settings
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
