"""
Router para los endpoints de notificaciones.

Define los endpoints de la API REST para las operaciones de notificaciones
y conecta las solicitudes HTTP con los casos de uso de la aplicación.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dtos.notification_dtos import (
    CreateNotificationDTO,
    MarkAsReadDTO,
    NotificationFilterDTO
)
from app.application.use_cases.notification_use_cases import NotificationUseCases
from app.domain.entities.notification import InvalidNotificationDataError
from app.infrastructure.database.database import get_session
from app.infrastructure.repositories.notification_repository_impl import SQLAlchemyNotificationRepository
from app.presentation.schemas.notification_schemas import (
    CreateNotificationRequest,
    ErrorResponse,
    MarkAsReadRequest,
    NotificationListResponse,
    NotificationResponse
)

# Crear router
router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}
    }
)


# Dependencia para obtener los casos de uso
async def get_notification_use_cases(session: AsyncSession = Depends(get_session)) -> NotificationUseCases:
    """
    Proporciona una instancia de NotificationUseCases con el repositorio configurado.
    
    Args:
        session: Sesión de base de datos
        
    Returns:
        Instancia de NotificationUseCases
    """
    repository = SQLAlchemyNotificationRepository(session)
    return NotificationUseCases(repository)


@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear notificación",
    description="Crea una nueva notificación para un usuario"
)
async def create_notification(
    request: CreateNotificationRequest,
    use_cases: NotificationUseCases = Depends(get_notification_use_cases)
):
    """
    Crea una nueva notificación.
    
    Args:
        request: Datos de la notificación a crear
        use_cases: Casos de uso de notificaciones
        
    Returns:
        Notificación creada
        
    Raises:
        HTTPException: Si los datos son inválidos
    """
    try:
        # Convertir request a DTO
        dto = CreateNotificationDTO(
            user_id=request.user_id,
            title=request.title,
            message=request.message,
            type=request.type
        )
        
        # Crear notificación
        result = await use_cases.create_notification(dto)
        
        return result
    except InvalidNotificationDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear notificación: {str(e)}"
        )


@router.get(
    "/{user_id}",
    response_model=NotificationListResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener notificaciones de usuario",
    description="Obtiene las notificaciones de un usuario con paginación y filtros"
)
async def get_notifications_by_user(
    user_id: int,
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=100, description="Elementos por página"),
    read_status: bool = Query(None, description="Filtrar por estado de lectura"),
    type: str = Query(None, description="Filtrar por tipo de notificación"),
    use_cases: NotificationUseCases = Depends(get_notification_use_cases)
):
    """
    Obtiene las notificaciones de un usuario.
    
    Args:
        user_id: ID del usuario
        page: Número de página
        per_page: Elementos por página
        read_status: Filtrar por estado de lectura
        type: Filtrar por tipo de notificación
        use_cases: Casos de uso de notificaciones
        
    Returns:
        Lista paginada de notificaciones
        
    Raises:
        HTTPException: Si ocurre un error
    """
    try:
        # Crear DTO de filtro
        filter_dto = NotificationFilterDTO(
            user_id=user_id,
            page=page,
            per_page=per_page,
            read_status=read_status,
            type=type
        )
        
        # Obtener notificaciones
        result = await use_cases.get_notifications_by_user(filter_dto)
        
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener notificaciones: {str(e)}"
        )


@router.put(
    "/read",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Marcar notificación como leída",
    description="Marca una notificación como leída"
)
async def mark_notification_as_read(
    request: MarkAsReadRequest,
    use_cases: NotificationUseCases = Depends(get_notification_use_cases)
):
    """
    Marca una notificación como leída.
    
    Args:
        request: Datos de la notificación a marcar como leída
        use_cases: Casos de uso de notificaciones
        
    Returns:
        Notificación actualizada
        
    Raises:
        HTTPException: Si la notificación no existe
    """
    try:
        # Convertir request a DTO
        dto = MarkAsReadDTO(
            notification_id=request.notification_id
        )
        
        # Marcar como leída
        result = await use_cases.mark_notification_as_read(dto)
        
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al marcar notificación como leída: {str(e)}"
        )