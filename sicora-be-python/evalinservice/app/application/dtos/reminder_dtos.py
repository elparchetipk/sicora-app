"""DTOs for evaluation reminders."""

from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class SendReminderRequest(BaseModel):
    """
    DTO para solicitud de envío de recordatorios de evaluación.
    
    Attributes:
        ficha_id: ID de la ficha para enviar recordatorios
        custom_message: Mensaje personalizado opcional
        student_ids: IDs específicos de estudiantes (opcional, si no se proporciona se envía a todos los estudiantes pendientes)
    """
    ficha_id: str = Field(..., description="ID de la ficha para enviar recordatorios")
    custom_message: Optional[str] = Field(None, description="Mensaje personalizado opcional")
    student_ids: Optional[List[UUID]] = Field(None, description="IDs específicos de estudiantes (opcional)")


class ReminderResult(BaseModel):
    """
    DTO para resultado de envío de recordatorio a un estudiante.
    
    Attributes:
        student_id: ID del estudiante
        student_name: Nombre del estudiante
        success: Indica si el envío fue exitoso
        message: Mensaje de error o éxito
    """
    student_id: UUID
    student_name: str
    success: bool
    message: str


class SendReminderResponse(BaseModel):
    """
    DTO para respuesta de envío de recordatorios.
    
    Attributes:
        ficha_id: ID de la ficha
        total_students: Total de estudiantes en la ficha
        pending_students: Estudiantes con evaluaciones pendientes
        reminders_sent: Número de recordatorios enviados exitosamente
        reminders_failed: Número de recordatorios fallidos
        results: Resultados detallados por estudiante
    """
    ficha_id: str
    total_students: int
    pending_students: int
    reminders_sent: int
    reminders_failed: int
    results: List[ReminderResult]