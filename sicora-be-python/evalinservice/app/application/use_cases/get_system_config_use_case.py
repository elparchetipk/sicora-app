"""Get System Configuration use case."""

from ..dtos.config_dtos import SystemConfigResponse


class GetSystemConfigUseCase:
    """
    Caso de uso para obtener la configuración del sistema de evaluaciones.
    
    Responsabilidades:
    - Retornar configuración predeterminada del sistema
    - Incluir límites, validaciones y parámetros operativos
    """
    
    def __init__(self):
        pass
    
    async def execute(self) -> SystemConfigResponse:
        """
        Ejecuta el caso de uso de obtención de configuración del sistema.
        
        Returns:
            SystemConfigResponse: Configuración del sistema
        """
        return SystemConfigResponse(
            max_questions_per_questionnaire=50,
            min_questions_per_questionnaire=1,
            max_evaluation_period_days=365,
            min_evaluation_period_days=1,
            max_score_value=5.0,
            min_score_value=1.0,
            default_question_types=["likert", "text", "multiple_choice"],
            max_comment_length=1000,
            evaluation_timeout_hours=72,
            anonymous_evaluation_enabled=True,
            bulk_upload_max_questions=1000,
            export_formats=["csv", "excel", "pdf"],
            notification_settings={
                "period_start": True,
                "period_end": True,
                "evaluation_submitted": False,
                "report_generated": True
            }
        )
