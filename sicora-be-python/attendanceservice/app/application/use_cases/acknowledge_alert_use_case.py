from uuid import UUID

from ...domain.repositories import AttendanceAlertRepository
from ...domain.exceptions import AlertNotFoundError, UnauthorizedAccessError
from ..dtos import AcknowledgeAlertRequest, AcknowledgeAlertResponse
from ..interfaces import UserServiceInterface


class AcknowledgeAlertUseCase:
    """
    Caso de uso para reconocer alertas de asistencia.
    
    Permite a instructores y administradores marcar alertas como reconocidas,
    indicando que han tomado conocimiento y acción sobre la situación.
    """

    def __init__(
        self,
        alert_repository: AttendanceAlertRepository,
        user_service: UserServiceInterface
    ):
        self.alert_repository = alert_repository
        self.user_service = user_service

    async def execute(
        self,
        request: AcknowledgeAlertRequest,
        user_id: UUID
    ) -> AcknowledgeAlertResponse:
        """
        Ejecuta el reconocimiento de una alerta.
        
        Args:
            request: Datos de la alerta a reconocer
            user_id: ID del usuario que reconoce la alerta
            
        Returns:
            Respuesta con el estado actualizado de la alerta
            
        Raises:
            AlertNotFoundError: Si no existe la alerta
            UnauthorizedAccessError: Si el usuario no tiene permisos
        """
        # Validar que la alerta existe
        alert = await self.alert_repository.get_by_id(request.alert_id)
        if not alert:
            raise AlertNotFoundError(str(request.alert_id))

        # Validar permisos del usuario
        await self._validate_user_permissions(alert, user_id)

        # Reconocer la alerta
        alert.acknowledge(user_id)

        # Guardar la alerta actualizada
        saved_alert = await self.alert_repository.save(alert)

        return AcknowledgeAlertResponse(
            id=saved_alert.id,
            acknowledged=saved_alert.acknowledged,
            acknowledged_by=saved_alert.acknowledged_by,
            acknowledged_at=saved_alert.acknowledged_at,
            message="Alerta reconocida exitosamente"
        )

    async def _validate_user_permissions(self, alert, user_id: UUID) -> None:
        """
        Valida que el usuario tenga permisos para reconocer la alerta.
        
        Args:
            alert: Alerta a reconocer
            user_id: ID del usuario
            
        Raises:
            UnauthorizedAccessError: Si el usuario no tiene permisos
        """
        user_role = await self.user_service.get_user_role(user_id)
        
        if user_role == "aprendiz":
            # Los aprendices no pueden reconocer alertas
            raise UnauthorizedAccessError(
                f"acknowledge alert {alert.id}",
                user_role
            )
        elif user_role == "instructor":
            # Los instructores solo pueden reconocer alertas de sus fichas
            is_assigned = await self.user_service.validate_instructor_ficha_assignment(
                user_id,
                alert.ficha_id
            )
            if not is_assigned:
                raise UnauthorizedAccessError(
                    f"acknowledge alert {alert.id} (not assigned to ficha)",
                    user_role
                )
        elif user_role in ["admin", "coordinator"]:
            # Administradores y coordinadores pueden reconocer cualquier alerta
            pass
        else:
            raise UnauthorizedAccessError(
                f"acknowledge alert {alert.id}",
                user_role
            )
