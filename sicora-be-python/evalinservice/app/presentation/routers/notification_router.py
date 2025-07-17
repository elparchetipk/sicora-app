"""Router for notification endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.presentation.dependencies.auth import get_current_user, require_role, CurrentUser
from app.presentation.dependencies.container import get_send_evaluation_reminder_use_case
from app.presentation.schemas.reminder_schemas import ReminderRequestSchema, ReminderResponseSchema

from app.application.use_cases.send_evaluation_reminder_use_case import SendEvaluationReminderUseCase
from app.application.dtos.reminder_dtos import SendReminderRequest

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
    responses={404: {"description": "Not found"}}
)


@router.post("/reminder/{ficha_id}", response_model=ReminderResponseSchema)
async def send_evaluation_reminder(
    ficha_id: str,
    reminder_data: ReminderRequestSchema,
    current_user: CurrentUser = Depends(get_current_user),
    use_case: SendEvaluationReminderUseCase = Depends(get_send_evaluation_reminder_use_case)
):
    """
    Envía recordatorios de evaluación a los aprendices de una ficha específica.
    
    - Solo administradores y directores de grupo pueden enviar recordatorios.
    - Se puede enviar a todos los aprendices con evaluaciones pendientes o a aprendices específicos.
    - Se puede incluir un mensaje personalizado opcional.
    
    Returns:
        Resumen del envío de recordatorios con resultados detallados por estudiante.
    """
    # Verificar permisos (solo admin o director de grupo)
    require_role(current_user, ["admin", "coordinator", "group_director"])
    
    # Asegurar que el ficha_id en la ruta coincida con el del body
    if ficha_id != reminder_data.ficha_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID de ficha en la ruta debe coincidir con el del cuerpo de la solicitud"
        )
    
    try:
        # Convertir schema a DTO
        request = SendReminderRequest(
            ficha_id=reminder_data.ficha_id,
            custom_message=reminder_data.custom_message,
            student_ids=reminder_data.student_ids
        )
        
        # Ejecutar caso de uso
        result = await use_case.execute(request)
        
        # Devolver respuesta
        return ReminderResponseSchema(
            ficha_id=result.ficha_id,
            total_students=result.total_students,
            pending_students=result.pending_students,
            reminders_sent=result.reminders_sent,
            reminders_failed=result.reminders_failed,
            results=result.results
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al enviar recordatorios: {str(e)}"
        )