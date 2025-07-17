from uuid import UUID

from ...domain.repositories import JustificationRepository
from ...domain.exceptions import (
    JustificationNotFoundError,
    JustificationAlreadyProcessedError,
    UnauthorizedAccessError
)
from ..dtos import DeleteJustificationRequest, DeleteJustificationResponse
from ..interfaces import UserServiceInterface


class DeleteJustificationUseCase:
    """
    Caso de uso para eliminar justificaciones.
    
    Permite a un estudiante eliminar sus justificaciones pendientes,
    o a un administrador eliminar cualquier justificación pendiente.
    """

    def __init__(
        self,
        justification_repository: JustificationRepository,
        user_service: UserServiceInterface
    ):
        self.justification_repository = justification_repository
        self.user_service = user_service

    async def execute(
        self,
        request: DeleteJustificationRequest
    ) -> DeleteJustificationResponse:
        """
        Ejecuta la eliminación de una justificación.
        
        Args:
            request: Datos de la solicitud de eliminación
            
        Returns:
            Respuesta con el resultado de la eliminación
            
        Raises:
            JustificationNotFoundError: Si no existe la justificación
            JustificationAlreadyProcessedError: Si ya fue procesada
            UnauthorizedAccessError: Si el usuario no tiene permisos
        """
        # Validar que la justificación existe
        justification = await self.justification_repository.get_by_id(
            request.justification_id
        )
        if not justification:
            raise JustificationNotFoundError(str(request.justification_id))

        # Validar que la justificación esté pendiente
        if not justification.is_pending():
            raise JustificationAlreadyProcessedError(
                str(justification.id),
                justification.status.value
            )

        # Validar permisos del usuario
        user_info = await self.user_service.get_user_info(request.user_id)
        is_admin = user_info.get("role") == "admin"
        is_owner = justification.student_id == request.user_id
        
        if not (is_admin or is_owner):
            raise UnauthorizedAccessError(
                f"delete justification {justification.id}",
                "student or admin"
            )

        # Eliminar la justificación
        success = await self.justification_repository.delete(request.justification_id)
        
        if not success:
            return DeleteJustificationResponse(
                success=False,
                message="No se pudo eliminar la justificación",
                details={"justification_id": str(request.justification_id)}
            )
        
        return DeleteJustificationResponse(
            success=True,
            message="Justificación eliminada exitosamente",
            details={
                "justification_id": str(request.justification_id),
                "student_id": str(justification.student_id)
            }
        )