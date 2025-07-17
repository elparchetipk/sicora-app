"""Router proxy para AttendanceService en ApiGateway."""

from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile, Form
from fastapi.responses import JSONResponse
import httpx
import asyncio
from typing import Optional, List
from datetime import date

from middleware.auth import get_current_user
from utils.service_discovery import get_service_url

router = APIRouter(tags=["attendance"])

# URL del servicio de asistencia
ATTENDANCE_SERVICE_URL = get_service_url("attendance")


async def forward_request_to_attendance_service(
    method: str,
    endpoint: str,
    user_data: dict = None,
    json_data: dict = None,
    params: dict = None,
    files: dict = None,
    form_data: dict = None
):
    """Reenvía solicitudes al AttendanceService."""
    url = f"{ATTENDANCE_SERVICE_URL}{endpoint}"
    
    headers = {}
    if user_data:
        # Agregar información del usuario autenticado a los headers
        headers["X-User-ID"] = str(user_data.get("user_id"))
        headers["X-User-Role"] = user_data.get("role", "")
        headers["X-User-Email"] = user_data.get("email", "")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, params=params, headers=headers)
            elif method.upper() == "POST":
                if files or form_data:
                    # Para upload de archivos
                    response = await client.post(url, data=form_data, files=files, headers=headers)
                else:
                    response = await client.post(url, json=json_data, headers=headers)
            elif method.upper() == "PUT":
                if files or form_data:
                    response = await client.put(url, data=form_data, files=files, headers=headers)
                else:
                    response = await client.put(url, json=json_data, headers=headers)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                raise HTTPException(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                    detail=f"Method {method} not allowed"
                )
            
            return JSONResponse(
                status_code=response.status_code,
                content=response.json() if response.content else {}
            )
            
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"AttendanceService unavailable: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal error: {str(e)}"
            )


# =============================================================================
# ENDPOINTS DE ASISTENCIA
# =============================================================================

@router.post("/register")
async def register_attendance(
    qr_code: str,
    student_id: str,
    attendance_date: date,
    notes: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Registrar asistencia mediante código QR."""
    json_data = {
        "qr_code": qr_code,
        "student_id": student_id,
        "attendance_date": str(attendance_date),
        "notes": notes
    }
    
    return await forward_request_to_attendance_service(
        method="POST",
        endpoint="/attendance/register",
        user_data=current_user,
        json_data=json_data
    )


@router.get("/summary")
async def get_attendance_summary(
    student_id: Optional[str] = None,
    ficha_id: Optional[str] = None,
    instructor_id: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: dict = Depends(get_current_user)
):
    """Obtener resumen de asistencia."""
    params = {}
    if student_id:
        params["student_id"] = student_id
    if ficha_id:
        params["ficha_id"] = ficha_id
    if instructor_id:
        params["instructor_id"] = instructor_id
    if start_date:
        params["start_date"] = str(start_date)
    if end_date:
        params["end_date"] = str(end_date)
    
    return await forward_request_to_attendance_service(
        method="GET",
        endpoint="/attendance/summary",
        user_data=current_user,
        params=params
    )


@router.get("/history")
async def get_attendance_history(
    student_id: Optional[str] = None,
    ficha_id: Optional[str] = None,
    instructor_id: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    page: int = 1,
    page_size: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Obtener historial de asistencia."""
    params = {
        "page": page,
        "page_size": page_size
    }
    if student_id:
        params["student_id"] = student_id
    if ficha_id:
        params["ficha_id"] = ficha_id
    if instructor_id:
        params["instructor_id"] = instructor_id
    if status:
        params["status"] = status
    if start_date:
        params["start_date"] = str(start_date)
    if end_date:
        params["end_date"] = str(end_date)
    
    return await forward_request_to_attendance_service(
        method="GET",
        endpoint="/attendance/history",
        user_data=current_user,
        params=params
    )


# =============================================================================
# ENDPOINTS DE JUSTIFICACIONES
# =============================================================================

@router.post("/justifications/upload")
async def upload_justification(
    attendance_id: str = Form(...),
    reason: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Subir justificación con archivo."""
    form_data = {
        "attendance_id": attendance_id,
        "reason": reason,
        "description": description
    }
    
    files = {"file": (file.filename, await file.read(), file.content_type)}
    
    return await forward_request_to_attendance_service(
        method="POST",
        endpoint="/justifications/upload",
        user_data=current_user,
        form_data=form_data,
        files=files
    )


@router.get("/justifications/")
async def get_justifications(
    status: Optional[str] = None,
    student_id: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Obtener lista de justificaciones."""
    params = {
        "page": page,
        "page_size": page_size
    }
    if status:
        params["status"] = status
    if student_id:
        params["student_id"] = student_id
    
    return await forward_request_to_attendance_service(
        method="GET",
        endpoint="/justifications/",
        user_data=current_user,
        params=params
    )


@router.get("/justifications/{justification_id}")
async def get_justification(
    justification_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Obtener justificación específica."""
    return await forward_request_to_attendance_service(
        method="GET",
        endpoint=f"/justifications/{justification_id}",
        user_data=current_user
    )


@router.put("/justifications/{justification_id}/review")
async def review_justification(
    justification_id: str,
    status: str,
    reviewer_comments: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Revisar justificación (solo instructores/coordinadores)."""
    json_data = {
        "status": status,
        "reviewer_comments": reviewer_comments
    }
    
    return await forward_request_to_attendance_service(
        method="PUT",
        endpoint=f"/justifications/{justification_id}/review",
        user_data=current_user,
        json_data=json_data
    )


# =============================================================================
# ENDPOINTS DE ALERTAS
# =============================================================================

@router.get("/alerts/")
async def get_alerts(
    student_id: Optional[str] = None,
    alert_type: Optional[str] = None,
    level: Optional[str] = None,
    is_read: Optional[bool] = None,
    page: int = 1,
    page_size: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Obtener alertas."""
    params = {
        "page": page,
        "page_size": page_size
    }
    if student_id:
        params["student_id"] = student_id
    if alert_type:
        params["alert_type"] = alert_type
    if level:
        params["level"] = level
    if is_read is not None:
        params["is_read"] = is_read
    
    return await forward_request_to_attendance_service(
        method="GET",
        endpoint="/alerts/",
        user_data=current_user,
        params=params
    )


@router.post("/alerts/")
async def create_alert(
    student_id: str,
    alert_type: str,
    level: str,
    message: str,
    current_user: dict = Depends(get_current_user)
):
    """Crear nueva alerta."""
    json_data = {
        "student_id": student_id,
        "alert_type": alert_type,
        "level": level,
        "message": message
    }
    
    return await forward_request_to_attendance_service(
        method="POST",
        endpoint="/alerts/",
        user_data=current_user,
        json_data=json_data
    )


@router.put("/alerts/{alert_id}/read")
async def mark_alert_as_read(
    alert_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Marcar alerta como leída."""
    return await forward_request_to_attendance_service(
        method="PUT",
        endpoint=f"/alerts/{alert_id}/read",
        user_data=current_user
    )


@router.delete("/alerts/{alert_id}")
async def delete_alert(
    alert_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Eliminar alerta."""
    return await forward_request_to_attendance_service(
        method="DELETE",
        endpoint=f"/alerts/{alert_id}",
        user_data=current_user
    )
