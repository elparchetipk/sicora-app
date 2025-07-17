"""
Router para endpoints de justificaciones
"""

from datetime import date
from typing import Optional, Dict
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.security import HTTPBearer

from ...dependencies import (
    UploadJustificationUseCaseDep,
    ReviewJustificationUseCaseDep,
    GetJustificationsUseCaseDep,
    DeleteJustificationUseCaseDep,
    CurrentUser
)
from ..schemas import (
    UploadJustificationRequest,
    UploadJustificationResponse,
    ReviewJustificationRequest,
    ReviewJustificationResponse,
    GetJustificationsRequest,
    GetJustificationsResponse,
    JustificationStatusSchema,
    ErrorResponse
)
from ...domain.exceptions import (
    AttendanceServiceError,
    JustificationNotFoundError,
    JustificationAlreadyProcessedError,
    InvalidFileTypeError,
    FileTooLargeError,
    AttendanceNotFoundError,
    UnauthorizedAccessError
)

router = APIRouter(prefix="/api/v1/justifications", tags=["justifications"])
security = HTTPBearer()


@router.post(
    "/upload",
    response_model=UploadJustificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Subir justificación",
    description="Sube una justificación para un registro de asistencia específico"
)
async def upload_justification(
    use_case: UploadJustificationUseCaseDep,
    current_user: CurrentUser,
    attendance_record_id: UUID = Form(...),
    reason: str = Form(..., min_length=10, max_length=1000),
    justification_type: str = Form(...),
    document: Optional[UploadFile] = File(None)
):
    """
    Sube una justificación para una ausencia o tardanza.

    - **attendance_record_id**: ID del registro de asistencia a justificar
    - **reason**: Motivo detallado de la justificación
    - **justification_type**: Tipo de justificación (médica, personal, etc.)
    - **document**: Archivo PDF opcional como soporte
    """
    try:
        from ..application.dtos import UploadJustificationRequest as DTORequest

        # Validar archivo si se proporciona
        file_data = None
        if document:
            if document.content_type != "application/pdf":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"error": "invalid_file_type", "message": "Only PDF files are allowed"}
                )

            content = await document.read()
            file_data = {
                "filename": document.filename,
                "content": content,
                "content_type": document.content_type
            }

        dto_request = DTORequest(
            attendance_record_id=attendance_record_id,
            reason=reason,
            justification_type=justification_type,
            document=file_data
        )

        result = await use_case.execute(dto_request)

        return UploadJustificationResponse(
            success=result.success,
            message=result.message,
            justification=result.justification.__dict__ if result.justification else None
        )

    except AttendanceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "attendance_record_not_found", "message": str(e)}
        )
    except InvalidFileTypeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_file_type", "message": str(e)}
        )
    except FileTooLargeError as e:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={"error": "file_too_large", "message": str(e)}
        )
    except AttendanceServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": str(e)}
        )


@router.put(
    "/{justification_id}/review",
    response_model=ReviewJustificationResponse,
    summary="Revisar justificación",
    description="Permite a un instructor revisar y aprobar/rechazar una justificación"
)
async def review_justification(
    justification_id: UUID,
    request: ReviewJustificationRequest,
    use_case: ReviewJustificationUseCaseDep,
    current_user: CurrentUser
):
    """
    Revisa una justificación pendiente.

    - **justification_id**: ID de la justificación a revisar
    - **status**: Estado de la revisión (APPROVED/REJECTED)
    - **review_notes**: Notas opcionales del revisor
    """
    try:
        from ..application.dtos import ReviewJustificationRequest as DTORequest
        from ..domain.value_objects import JustificationStatus

        # Convertir string a enum
        status_enum = JustificationStatus(request.status.value)

        dto_request = DTORequest(
            justification_id=justification_id,
            status=status_enum,
            review_notes=request.review_notes,
            reviewer_id=current_user
        )

        result = await use_case.execute(dto_request)

        return ReviewJustificationResponse(
            success=result.success,
            message=result.message,
            justification=result.justification.__dict__
        )

    except JustificationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "justification_not_found", "message": str(e)}
        )
    except UnauthorizedAccessError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "unauthorized", "message": str(e)}
        )
    except AttendanceServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": str(e)}
        )


@router.get(
    "/",
    response_model=GetJustificationsResponse,
    summary="Obtener justificaciones",
    description="Obtiene una lista paginada de justificaciones con filtros opcionales"
)
async def get_justifications(
    use_case: GetJustificationsUseCaseDep,
    status: Optional[JustificationStatusSchema] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    page: int = 1,
    page_size: int = 20,
    current_user: CurrentUser = Depends()
):
    """
    Obtiene justificaciones con filtros opcionales.

    - **status**: Filtro por estado de justificación
    - **start_date**: Fecha de inicio del filtro
    - **end_date**: Fecha de fin del filtro
    - **page**: Número de página
    - **page_size**: Tamaño de página
    """
    try:
        from ..application.dtos import GetJustificationsRequest as DTORequest
        from ..domain.value_objects import JustificationStatus

        # Convertir string a enum si se proporciona
        status_enum = None
        if status:
            status_enum = JustificationStatus(status.value)

        dto_request = DTORequest(
            status=status_enum,
            start_date=start_date,
            end_date=end_date,
            page=page,
            page_size=page_size,
            user_id=current_user
        )

        result = await use_case.execute(dto_request)

        return GetJustificationsResponse(
            justifications=[j.__dict__ for j in result.justifications],
            total_justifications=result.total_justifications,
            pending_count=result.pending_count,
            approved_count=result.approved_count,
            rejected_count=result.rejected_count,
            current_page=result.current_page,
            page_size=result.page_size,
            total_pages=result.total_pages
        )

    except AttendanceServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": str(e)}
        )


@router.get(
    "/{justification_id}",
    response_model=Dict,
    summary="Obtener justificación por ID",
    description="Obtiene los detalles de una justificación específica"
)
async def get_justification_by_id(
    justification_id: UUID,
    use_case: GetJustificationsUseCaseDep,
    current_user: CurrentUser
):
    """
    Obtiene una justificación específica por su ID.

    - **justification_id**: ID de la justificación
    """
    try:
        from ..application.dtos import GetJustificationsRequest as DTORequest

        # Obtener solo esta justificación específica
        dto_request = DTORequest(
            justification_id=justification_id,
            page=1,
            page_size=1,
            user_id=current_user
        )

        result = await use_case.execute(dto_request)

        if not result.justifications:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "justification_not_found", "message": "Justification not found"}
            )

        return result.justifications[0].__dict__

    except AttendanceServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": str(e)}
        )


@router.delete(
    "/{justification_id}",
    response_model=Dict,
    summary="Eliminar justificación",
    description="Permite eliminar una justificación pendiente"
)
async def delete_justification(
    justification_id: UUID,
    use_case: DeleteJustificationUseCaseDep,
    current_user: CurrentUser
):
    """
    Elimina una justificación (solo si está pendiente).

    - **justification_id**: ID de la justificación a eliminar
    """
    try:
        from ..application.dtos import DeleteJustificationRequest as DTORequest

        dto_request = DTORequest(
            justification_id=justification_id,
            user_id=current_user
        )

        result = await use_case.execute(dto_request)

        return {
            "success": result.success,
            "message": result.message,
            "details": result.details
        }

    except JustificationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "justification_not_found", "message": str(e)}
        )
    except JustificationAlreadyProcessedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "justification_already_processed", "message": str(e)}
        )
    except UnauthorizedAccessError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "unauthorized", "message": str(e)}
        )
    except AttendanceServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": str(e)}
        )
