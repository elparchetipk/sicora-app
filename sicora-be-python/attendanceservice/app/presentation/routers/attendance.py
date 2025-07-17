"""
Router para endpoints de asistencia
"""

from datetime import date
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.security import HTTPBearer

from ...dependencies import (
    RegisterAttendanceUseCaseDep,
    GetAttendanceSummaryUseCaseDep,
    GetAttendanceHistoryUseCaseDep,
    QRCodeService,
    CurrentUser
)
from ..schemas import (
    RegisterAttendanceRequest,
    RegisterAttendanceResponse,
    AttendanceSummaryResponse,
    AttendanceHistoryResponse,
    GetAttendanceHistoryRequest,
    QRCodeResponse,
    ErrorResponse
)
from ...domain.exceptions import (
    AttendanceServiceError,
    InvalidQRCodeError,
    DuplicateAttendanceError,
    InvalidBlockStatusError,
    StudentNotInFichaError
)

router = APIRouter(prefix="/api/v1/attendance", tags=["attendance"])
security = HTTPBearer()


@router.post(
    "/register",
    response_model=RegisterAttendanceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar asistencia",
    description="Registra la asistencia de un estudiante usando código QR"
)
async def register_attendance(
    request: RegisterAttendanceRequest,
    use_case: RegisterAttendanceUseCaseDep,
    current_user: CurrentUser
):
    """
    Registra la asistencia de un estudiante.

    - **qr_code**: Código QR escaneado por el estudiante
    - **student_id**: ID del estudiante que registra asistencia
    - **location**: Ubicación opcional donde se registra la asistencia
    """
    try:
        # Convertir el esquema Pydantic a DTO
        from ..application.dtos import RegisterAttendanceRequest as DTORequest
        dto_request = DTORequest(
            qr_code=request.qr_code,
            student_id=request.student_id,
            location=request.location
        )

        result = await use_case.execute(dto_request)

        # Convertir DTO response a esquema Pydantic
        return RegisterAttendanceResponse(
            success=result.success,
            message=result.message,
            attendance_record=result.attendance_record.__dict__ if result.attendance_record else None
        )

    except InvalidQRCodeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_qr_code", "message": str(e)}
        )
    except DuplicateAttendanceError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "attendance_already_registered", "message": str(e)}
        )
    except InvalidBlockStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "class_not_active", "message": str(e)}
        )
    except StudentNotInFichaError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "student_not_enrolled", "message": str(e)}
        )
    except AttendanceServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": str(e)}
        )


@router.get(
    "/summary/{student_id}",
    response_model=AttendanceSummaryResponse,
    summary="Obtener resumen de asistencia",
    description="Obtiene el resumen de asistencia de un estudiante"
)
async def get_attendance_summary(
    student_id: UUID,
    use_case: GetAttendanceSummaryUseCaseDep,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: CurrentUser = Depends()
):
    """
    Obtiene el resumen de asistencia de un estudiante.

    - **student_id**: ID del estudiante
    - **start_date**: Fecha de inicio del período (opcional)
    - **end_date**: Fecha de fin del período (opcional)
    """
    try:
        from ..application.dtos import GetAttendanceSummaryRequest
        dto_request = GetAttendanceSummaryRequest(
            student_id=student_id,
            start_date=start_date,
            end_date=end_date
        )

        result = await use_case.execute(dto_request)

        return AttendanceSummaryResponse(**result.__dict__)

    except AttendanceServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": str(e)}
        )


@router.get(
    "/history/{student_id}",
    response_model=AttendanceHistoryResponse,
    summary="Obtener historial de asistencia",
    description="Obtiene el historial paginado de asistencia de un estudiante"
)
async def get_attendance_history(
    student_id: UUID,
    use_case: GetAttendanceHistoryUseCaseDep,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    current_user: CurrentUser = Depends()
):
    """
    Obtiene el historial de asistencia de un estudiante.

    - **student_id**: ID del estudiante
    - **start_date**: Fecha de inicio del filtro
    - **end_date**: Fecha de fin del filtro
    - **status**: Filtro por estado de asistencia
    - **page**: Número de página
    - **page_size**: Tamaño de página
    """
    try:
        from ..application.dtos import GetAttendanceHistoryRequest
        from ..domain.value_objects import AttendanceStatus

        # Convertir string a enum si se proporciona
        status_enum = None
        if status:
            try:
                status_enum = AttendanceStatus(status.upper())
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"error": "invalid_status", "message": f"Invalid status: {status}"}
                )

        dto_request = GetAttendanceHistoryRequest(
            student_id=student_id,
            start_date=start_date,
            end_date=end_date,
            status=status_enum,
            page=page,
            page_size=page_size
        )

        result = await use_case.execute(dto_request)

        return AttendanceHistoryResponse(
            records=[record.__dict__ for record in result.records],
            total_records=result.total_records,
            current_page=result.current_page,
            page_size=result.page_size,
            total_pages=result.total_pages
        )

    except AttendanceServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": str(e)}
        )


@router.post(
    "/qr-code/{class_id}",
    response_model=QRCodeResponse,
    summary="Generar código QR para clase",
    description="Genera un código QR temporal para registro de asistencia en una clase"
)
async def generate_qr_code(
    class_id: UUID,
    qr_service: QRCodeService,
    current_user: CurrentUser = Depends()
):
    """
    Genera un código QR temporal para una clase.

    - **class_id**: ID de la clase para la cual generar el código QR
    """
    try:
        qr_data = await qr_service.generate_qr_code(class_id)

        return QRCodeResponse(
            qr_code=qr_data.qr_code,
            expires_at=qr_data.expires_at,
            class_id=qr_data.class_id,
            class_name=qr_data.class_name
        )

    except AttendanceServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": str(e)}
        )


@router.get(
    "/qr-code/{class_id}/validate",
    summary="Validar código QR",
    description="Valida si un código QR está activo y es válido"
)
async def validate_qr_code(
    class_id: UUID,
    qr_code: str,
    qr_service: QRCodeService,
    current_user: CurrentUser = Depends()
):
    """
    Valida un código QR.

    - **class_id**: ID de la clase
    - **qr_code**: Código QR a validar
    """
    try:
        is_valid = await qr_service.validate_qr_code(qr_code, class_id)

        return {
            "valid": is_valid,
            "message": "QR code is valid" if is_valid else "QR code is invalid or expired"
        }

    except AttendanceServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": str(e)}
        )
