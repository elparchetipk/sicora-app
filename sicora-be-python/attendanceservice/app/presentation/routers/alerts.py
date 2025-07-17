"""
Router para endpoints de alertas de asistencia
"""

from datetime import date
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from ...dependencies import (
    GetAttendanceAlertsUseCaseDep,
    GetInstructorNoAttendanceAlertsUseCaseDep,
    AcknowledgeAlertUseCaseDep,
    CurrentUser
)
from ..schemas import (
    GetAlertsRequest,
    GetAlertsResponse,
    AcknowledgeAlertResponse,
    AlertTypeSchema,
    AlertLevelSchema,
    ErrorResponse
)
from ...domain.exceptions import (
    AttendanceServiceError,
    AlertNotFoundError,
    UnauthorizedAccessError
)

router = APIRouter(prefix="/api/v1/alerts", tags=["alerts"])
security = HTTPBearer()


@router.get(
    "/",
    response_model=GetAlertsResponse,
    summary="Obtener alertas de asistencia",
    description="Obtiene una lista paginada de alertas con filtros opcionales"
)
async def get_attendance_alerts(
    use_case: GetAttendanceAlertsUseCaseDep,
    level: Optional[AlertLevelSchema] = None,
    alert_type: Optional[AlertTypeSchema] = None,
    include_acknowledged: bool = False,
    page: int = 1,
    page_size: int = 20,
    current_user: CurrentUser = Depends()
):
    """
    Obtiene alertas de asistencia con filtros opcionales.

    - **level**: Filtro por nivel de alerta (LOW, MEDIUM, HIGH, CRITICAL)
    - **alert_type**: Filtro por tipo de alerta
    - **include_acknowledged**: Incluir alertas ya reconocidas
    - **page**: Número de página
    - **page_size**: Tamaño de página
    """
    try:
        from ..application.dtos import GetAlertsRequest as DTORequest
        from ..domain.value_objects import AlertLevel, AlertType

        # Convertir string a enum si se proporciona
        level_enum = None
        if level:
            level_enum = AlertLevel(level.value)

        alert_type_enum = None
        if alert_type:
            alert_type_enum = AlertType(alert_type.value)

        dto_request = DTORequest(
            level=level_enum,
            alert_type=alert_type_enum,
            include_acknowledged=include_acknowledged,
            page=page,
            page_size=page_size,
            user_id=current_user
        )

        result = await use_case.execute(dto_request)

        return GetAlertsResponse(
            alerts=[alert.__dict__ for alert in result.alerts],
            total_alerts=result.total_alerts,
            critical_count=result.critical_count,
            high_count=result.high_count,
            medium_count=result.medium_count,
            low_count=result.total_alerts - result.critical_count - result.high_count - result.medium_count,
            current_page=page,
            page_size=page_size,
            total_pages=(result.total_alerts + page_size - 1) // page_size
        )

    except AttendanceServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": str(e)}
        )


@router.get(
    "/instructor/{instructor_id}",
    response_model=GetAlertsResponse,
    summary="Obtener alertas de no asistencia de instructor",
    description="Obtiene alertas específicas cuando un instructor no ha registrado asistencia"
)
async def get_instructor_no_attendance_alerts(
    instructor_id: UUID,
    use_case: GetInstructorNoAttendanceAlertsUseCaseDep,
    date_filter: Optional[date] = None,
    page: int = 1,
    page_size: int = 20,
    current_user: CurrentUser = Depends()
):
    """
    Obtiene alertas cuando un instructor no ha registrado asistencia.

    - **instructor_id**: ID del instructor
    - **date_filter**: Fecha específica para filtrar (opcional)
    - **page**: Número de página
    - **page_size**: Tamaño de página
    """
    try:
        from ..application.dtos import GetInstructorNoAttendanceAlertsRequest as DTORequest

        dto_request = DTORequest(
            instructor_id=instructor_id,
            date_filter=date_filter,
            page=page,
            page_size=page_size,
            user_id=current_user
        )

        result = await use_case.execute(dto_request)

        return GetAlertsResponse(
            alerts=[alert.__dict__ for alert in result.alerts],
            total_alerts=result.total_alerts,
            critical_count=result.critical_count,
            high_count=result.high_count,
            medium_count=result.medium_count,
            low_count=result.total_alerts - result.critical_count - result.high_count - result.medium_count,
            current_page=page,
            page_size=page_size,
            total_pages=(result.total_alerts + page_size - 1) // page_size
        )

    except AttendanceServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": str(e)}
        )


@router.put(
    "/{alert_id}/acknowledge",
    response_model=AcknowledgeAlertResponse,
    summary="Reconocer alerta",
    description="Marca una alerta como reconocida por un usuario autorizado"
)
async def acknowledge_alert(
    alert_id: UUID,
    use_case: AcknowledgeAlertUseCaseDep,
    current_user: CurrentUser
):
    """
    Reconoce una alerta específica.

    - **alert_id**: ID de la alerta a reconocer
    """
    try:
        from ..application.dtos import AcknowledgeAlertRequest as DTORequest

        dto_request = DTORequest(
            alert_id=alert_id,
            acknowledged_by=current_user
        )

        result = await use_case.execute(dto_request)

        return AcknowledgeAlertResponse(
            success=result.success,
            message=result.message,
            alert=result.alert.__dict__
        )

    except AlertNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "alert_not_found", "message": str(e)}
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
    "/{alert_id}",
    summary="Obtener alerta por ID",
    description="Obtiene los detalles de una alerta específica"
)
async def get_alert_by_id(
    alert_id: UUID,
    use_case: GetAttendanceAlertsUseCaseDep,
    current_user: CurrentUser
):
    """
    Obtiene una alerta específica por su ID.

    - **alert_id**: ID de la alerta
    """
    try:
        from ..application.dtos import GetAlertsRequest as DTORequest

        # Usar filtro específico para obtener solo esta alerta
        dto_request = DTORequest(
            alert_id=alert_id,
            include_acknowledged=True,
            page=1,
            page_size=1,
            user_id=current_user
        )

        result = await use_case.execute(dto_request)

        if not result.alerts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "alert_not_found", "message": "Alert not found"}
            )

        return result.alerts[0].__dict__

    except AttendanceServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": str(e)}
        )


@router.get(
    "/student/{student_id}",
    response_model=GetAlertsResponse,
    summary="Obtener alertas de un estudiante",
    description="Obtiene todas las alertas relacionadas con un estudiante específico"
)
async def get_student_alerts(
    student_id: UUID,
    use_case: GetAttendanceAlertsUseCaseDep,
    include_acknowledged: bool = False,
    page: int = 1,
    page_size: int = 20,
    current_user: CurrentUser = Depends()
):
    """
    Obtiene alertas específicas de un estudiante.

    - **student_id**: ID del estudiante
    - **include_acknowledged**: Incluir alertas reconocidas
    - **page**: Número de página
    - **page_size**: Tamaño de página
    """
    try:
        from ..application.dtos import GetAlertsRequest as DTORequest

        dto_request = DTORequest(
            student_id=student_id,
            include_acknowledged=include_acknowledged,
            page=page,
            page_size=page_size,
            user_id=current_user
        )

        result = await use_case.execute(dto_request)

        return GetAlertsResponse(
            alerts=[alert.__dict__ for alert in result.alerts],
            total_alerts=result.total_alerts,
            critical_count=result.critical_count,
            high_count=result.high_count,
            medium_count=result.medium_count,
            low_count=result.total_alerts - result.critical_count - result.high_count - result.medium_count,
            current_page=page,
            page_size=page_size,
            total_pages=(result.total_alerts + page_size - 1) // page_size
        )

    except AttendanceServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": str(e)}
        )
