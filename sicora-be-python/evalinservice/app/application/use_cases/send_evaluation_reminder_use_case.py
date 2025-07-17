"""Send evaluation reminder use case."""

from typing import Dict, List, Optional
from uuid import UUID

from ...domain.repositories import EvaluationRepositoryInterface, EvaluationPeriodRepositoryInterface
from ..interfaces import UserServiceInterface, NotificationServiceInterface
from ..dtos.reminder_dtos import SendReminderRequest, SendReminderResponse, ReminderResult


class SendEvaluationReminderUseCase:
    """
    Caso de uso para enviar recordatorios de evaluación a estudiantes.
    
    Responsabilidades:
    - Obtener estudiantes de una ficha específica
    - Identificar estudiantes con evaluaciones pendientes
    - Enviar recordatorios a los estudiantes seleccionados
    - Registrar resultados del envío
    """
    
    def __init__(
        self,
        evaluation_repository: EvaluationRepositoryInterface,
        evaluation_period_repository: EvaluationPeriodRepositoryInterface,
        user_service: UserServiceInterface,
        notification_service: NotificationServiceInterface
    ):
        self._evaluation_repository = evaluation_repository
        self._evaluation_period_repository = evaluation_period_repository
        self._user_service = user_service
        self._notification_service = notification_service
    
    async def execute(self, request: SendReminderRequest) -> SendReminderResponse:
        """
        Ejecuta el caso de uso de envío de recordatorios.
        
        Args:
            request: Datos para el envío de recordatorios
            
        Returns:
            SendReminderResponse: Resultados del envío de recordatorios
        """
        # Obtener todos los estudiantes de la ficha
        students = await self._user_service.get_students_by_ficha(request.ficha_id)
        
        if not students:
            return SendReminderResponse(
                ficha_id=request.ficha_id,
                total_students=0,
                pending_students=0,
                reminders_sent=0,
                reminders_failed=0,
                results=[]
            )
        
        # Obtener período de evaluación activo
        active_periods = await self._evaluation_period_repository.get_active_periods()
        if not active_periods:
            return SendReminderResponse(
                ficha_id=request.ficha_id,
                total_students=len(students),
                pending_students=0,
                reminders_sent=0,
                reminders_failed=0,
                results=[
                    ReminderResult(
                        student_id=UUID(student["id"]),
                        student_name=f"{student['first_name']} {student['last_name']}",
                        success=False,
                        message="No hay períodos de evaluación activos"
                    )
                    for student in students
                ]
            )
        
        # Filtrar estudiantes específicos si se proporcionaron
        if request.student_ids:
            students = [s for s in students if UUID(s["id"]) in request.student_ids]
        
        # Identificar estudiantes con evaluaciones pendientes
        results = []
        pending_students = []
        
        for student in students:
            student_id = UUID(student["id"])
            student_name = f"{student['first_name']} {student['last_name']}"
            
            # Verificar si el estudiante tiene evaluaciones pendientes
            has_pending = False
            
            for period in active_periods:
                # Obtener instructores que el estudiante debe evaluar
                # Esto dependerá de la lógica específica del sistema
                # Por ejemplo, podría ser instructores de cursos en los que está inscrito
                
                # Verificar evaluaciones completadas por el estudiante en este período
                completed_evaluations = await self._evaluation_repository.get_student_evaluations(
                    student_id=student_id,
                    period_id=period.id
                )
                
                # Si hay evaluaciones pendientes, marcar al estudiante
                if not completed_evaluations:
                    has_pending = True
                    break
            
            if has_pending:
                pending_students.append({
                    "id": student_id,
                    "name": student_name
                })
        
        # Si no hay estudiantes con evaluaciones pendientes, retornar respuesta vacía
        if not pending_students:
            return SendReminderResponse(
                ficha_id=request.ficha_id,
                total_students=len(students),
                pending_students=0,
                reminders_sent=0,
                reminders_failed=0,
                results=[
                    ReminderResult(
                        student_id=UUID(student["id"]),
                        student_name=f"{student['first_name']} {student['last_name']}",
                        success=False,
                        message="No tiene evaluaciones pendientes"
                    )
                    for student in students
                ]
            )
        
        # Enviar recordatorios a estudiantes con evaluaciones pendientes
        recipient_ids = [student["id"] for student in pending_students]
        
        try:
            notification_result = await self._notification_service.send_reminder_notification(
                recipients=recipient_ids,
                ficha_id=request.ficha_id,
                custom_message=request.custom_message
            )
            
            # Procesar resultados
            success_count = 0
            failed_count = 0
            
            for student in pending_students:
                student_id = student["id"]
                student_name = student["name"]
                
                # Verificar si el envío fue exitoso para este estudiante
                # La estructura exacta de notification_result dependerá de la implementación
                success = student_id in notification_result.get("success_ids", [])
                
                if success:
                    success_count += 1
                    message = "Recordatorio enviado exitosamente"
                else:
                    failed_count += 1
                    message = notification_result.get("errors", {}).get(str(student_id), "Error al enviar recordatorio")
                
                results.append(
                    ReminderResult(
                        student_id=student_id,
                        student_name=student_name,
                        success=success,
                        message=message
                    )
                )
            
            return SendReminderResponse(
                ficha_id=request.ficha_id,
                total_students=len(students),
                pending_students=len(pending_students),
                reminders_sent=success_count,
                reminders_failed=failed_count,
                results=results
            )
            
        except Exception as e:
            # En caso de error general, marcar todos como fallidos
            return SendReminderResponse(
                ficha_id=request.ficha_id,
                total_students=len(students),
                pending_students=len(pending_students),
                reminders_sent=0,
                reminders_failed=len(pending_students),
                results=[
                    ReminderResult(
                        student_id=student["id"],
                        student_name=student["name"],
                        success=False,
                        message=f"Error al enviar recordatorio: {str(e)}"
                    )
                    for student in pending_students
                ]
            )