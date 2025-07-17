from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.presentation.dependencies.auth import get_current_user, require_role, CurrentUser
from app.presentation.dependencies.container import get_get_system_config_use_case
from app.presentation.schemas.config_schemas import (
    SystemConfigResponseSchema
)

from app.application.use_cases.get_system_config_use_case import GetSystemConfigUseCase

router = APIRouter(
    prefix="/config",
    tags=["configuration"],
    responses={404: {"description": "Not found"}}
)

class SystemStatusResponse(BaseModel):
    """Esquema para la respuesta del estado del sistema"""
    service_name: str
    version: str
    status: str
    database_status: str
    external_services: Dict[str, str]
    uptime: str

class SystemMetricsResponse(BaseModel):
    """Esquema para métricas del sistema"""
    total_questions: int
    total_questionnaires: int
    total_periods: int
    total_evaluations: int
    active_periods: int
    pending_evaluations: int

@router.get("/", response_model=SystemConfigResponseSchema)
async def get_evaluation_config(
    current_user: CurrentUser = Depends(get_current_user),
    use_case: ManageEvaluationConfigUseCase = Depends(get_manage_evaluation_config_use_case)
):
    """
    Obtener la configuración actual del sistema de evaluaciones.
    Todos los usuarios autenticados pueden consultar la configuración.
    """
    try:
        config = use_case.get_config()
        
        return SystemConfigResponseSchema(
            default_questionnaire_id=config.default_questionnaire_id,
            min_questions_per_questionnaire=config.min_questions_per_questionnaire,
            max_questions_per_questionnaire=config.max_questions_per_questionnaire,
            evaluation_deadline_days=config.evaluation_deadline_days,
            allow_anonymous_evaluations=config.allow_anonymous_evaluations,
            require_comments=config.require_comments,
            auto_close_periods=config.auto_close_periods,
            notification_settings=config.notification_settings,
            grading_scale=config.grading_scale,
            mandatory_question_types=config.mandatory_question_types,
            created_at=config.created_at,
            updated_at=config.updated_at
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.put("/", response_model=SystemConfigResponseSchema)
async def update_evaluation_config(
    config_data: EvaluationConfigUpdateSchema,
    current_user: CurrentUser = Depends(get_current_user),
    use_case: ManageEvaluationConfigUseCase = Depends(get_manage_evaluation_config_use_case)
):
    """
    Actualizar la configuración del sistema de evaluaciones.
    Solo los administradores pueden modificar la configuración.
    """
    require_role(current_user, ["admin"])
    
    try:
        config = use_case.update_config(
            default_questionnaire_id=config_data.default_questionnaire_id,
            min_questions_per_questionnaire=config_data.min_questions_per_questionnaire,
            max_questions_per_questionnaire=config_data.max_questions_per_questionnaire,
            evaluation_deadline_days=config_data.evaluation_deadline_days,
            allow_anonymous_evaluations=config_data.allow_anonymous_evaluations,
            require_comments=config_data.require_comments,
            auto_close_periods=config_data.auto_close_periods,
            notification_settings=config_data.notification_settings,
            grading_scale=config_data.grading_scale,
            mandatory_question_types=config_data.mandatory_question_types
        )
        
        return SystemConfigResponseSchema(
            default_questionnaire_id=config.default_questionnaire_id,
            min_questions_per_questionnaire=config.min_questions_per_questionnaire,
            max_questions_per_questionnaire=config.max_questions_per_questionnaire,
            evaluation_deadline_days=config.evaluation_deadline_days,
            allow_anonymous_evaluations=config.allow_anonymous_evaluations,
            require_comments=config.require_comments,
            auto_close_periods=config.auto_close_periods,
            notification_settings=config.notification_settings,
            grading_scale=config.grading_scale,
            mandatory_question_types=config.mandatory_question_types,
            created_at=config.created_at,
            updated_at=config.updated_at
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/system/status", response_model=SystemStatusResponse)
async def get_system_status(
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Obtener el estado general del sistema.
    Solo los administradores pueden consultar el estado del sistema.
    """
    require_role(current_user, ["admin"])
    
    try:
        # TODO: Implement actual system status checks
        return SystemStatusResponse(
            service_name="EvalinService",
            version="1.0.0",
            status="healthy",
            database_status="connected",
            external_services={
                "userservice": "connected",
                "scheduleservice": "connected",
                "notificationservice": "connected"
            },
            uptime="0 days, 0 hours, 0 minutes"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/system/metrics", response_model=SystemMetricsResponse)
async def get_system_metrics(
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Obtener métricas del sistema.
    Solo los administradores pueden consultar las métricas del sistema.
    """
    require_role(current_user, ["admin"])
    
    try:
        # TODO: Implement actual metrics collection
        return SystemMetricsResponse(
            total_questions=0,
            total_questionnaires=0,
            total_periods=0,
            total_evaluations=0,
            active_periods=0,
            pending_evaluations=0
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/system/maintenance")
async def toggle_maintenance_mode(
    enable: bool,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Activar o desactivar el modo de mantenimiento.
    Solo los administradores pueden cambiar el modo de mantenimiento.
    """
    require_role(current_user, ["admin"])
    
    try:
        # TODO: Implement maintenance mode toggle
        action = "enabled" if enable else "disabled"
        return {
            "message": f"Maintenance mode {action}",
            "maintenance_mode": enable,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/templates/question-types")
async def get_question_type_templates(
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Obtener plantillas de tipos de preguntas disponibles.
    Los administradores y coordinadores pueden consultar las plantillas.
    """
    require_role(current_user, ["admin", "coordinator"])
    
    try:
        templates = {
            "multiple_choice": {
                "name": "Opción Múltiple",
                "description": "Pregunta con múltiples opciones de respuesta",
                "example": {
                    "question": "¿Cómo calificarías la claridad de las explicaciones del instructor?",
                    "options": ["Excelente", "Muy bueno", "Bueno", "Regular", "Deficiente"],
                    "type": "single_select"
                }
            },
            "likert_scale": {
                "name": "Escala Likert",
                "description": "Pregunta con escala de valoración",
                "example": {
                    "question": "El instructor domina el contenido de la materia",
                    "scale": {
                        "min": 1,
                        "max": 5,
                        "labels": ["Totalmente en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Totalmente de acuerdo"]
                    }
                }
            },
            "text_response": {
                "name": "Respuesta Abierta",
                "description": "Pregunta que permite respuesta de texto libre",
                "example": {
                    "question": "¿Qué aspectos del curso consideras que podrían mejorarse?",
                    "max_length": 500,
                    "required": False
                }
            },
            "rating": {
                "name": "Calificación",
                "description": "Pregunta con calificación numérica",
                "example": {
                    "question": "Califica la puntualidad del instructor",
                    "scale": {
                        "min": 1,
                        "max": 10,
                        "step": 1
                    }
                }
            }
        }
        
        return {
            "templates": templates,
            "total_templates": len(templates)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/validation/rules")
async def get_validation_rules(
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Obtener reglas de validación del sistema.
    Los administradores y coordinadores pueden consultar las reglas.
    """
    require_role(current_user, ["admin", "coordinator"])
    
    try:
        rules = {
            "questions": {
                "min_text_length": 10,
                "max_text_length": 500,
                "required_fields": ["text", "type"],
                "allowed_types": ["multiple_choice", "likert_scale", "text_response", "rating"]
            },
            "questionnaires": {
                "min_questions": 5,
                "max_questions": 50,
                "required_question_types": ["rating"],
                "max_name_length": 100
            },
            "evaluation_periods": {
                "min_duration_days": 7,
                "max_duration_days": 90,
                "advance_notice_days": 3
            },
            "evaluations": {
                "max_response_length": 1000,
                "required_responses": True,
                "allow_partial_submission": False
            }
        }
        
        return {
            "validation_rules": rules,
            "last_updated": "2024-01-01T00:00:00Z"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
