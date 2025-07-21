"""Router proxy para ScheduleService en ApiGateway."""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
import httpx
from typing import Optional, Dict, Any, List
from datetime import date

from middleware.auth import get_current_user, get_instructor_user
from utils.service_discovery import get_service_url

router = APIRouter(tags=["schedules"])

# URL del servicio de horarios
SCHEDULE_SERVICE_URL = get_service_url("schedule")

async def forward_request_to_schedule_service(
    method: str,
    endpoint: str,
    user_data: dict = None,
    json_data: dict = None,
    params: dict = None
):
    """Reenvía solicitudes al ScheduleService."""
    url = f"{SCHEDULE_SERVICE_URL}{endpoint}"
    
    headers = {}
    if user_data:
        headers["X-User-ID"] = str(user_data.get("user_id"))
        headers["X-User-Role"] = user_data.get("role", "")
        headers["X-User-Email"] = user_data.get("email", "")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, params=params, headers=headers)
            elif method.upper() == "POST":
                response = await client.post(url, json=json_data, headers=headers)
            elif method.upper() == "PUT":
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
                detail=f"ScheduleService unavailable: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal error: {str(e)}"
            )

# =============================================================================
# ENDPOINTS DE HORARIOS
# =============================================================================

@router.get("/schedules")
async def get_schedules(
    skip: int = 0,
    limit: int = 100,
    program_id: Optional[str] = None,
    instructor_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Obtener horarios."""
    params = {"skip": skip, "limit": limit}
    if program_id:
        params["program_id"] = program_id
    if instructor_id:
        params["instructor_id"] = instructor_id
        
    return await forward_request_to_schedule_service(
        method="GET",
        endpoint="/schedules",
        params=params,
        user_data=current_user
    )

@router.get("/schedules/{schedule_id}")
async def get_schedule(
    schedule_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Obtener horario por ID."""
    return await forward_request_to_schedule_service(
        method="GET",
        endpoint=f"/schedules/{schedule_id}",
        user_data=current_user
    )

@router.post("/schedules")
async def create_schedule(
    schedule_data: Dict[str, Any],
    current_user: dict = Depends(get_instructor_user)
):
    """Crear nuevo horario (solo instructores)."""
    return await forward_request_to_schedule_service(
        method="POST",
        endpoint="/schedules",
        json_data=schedule_data,
        user_data=current_user
    )

@router.put("/schedules/{schedule_id}")
async def update_schedule(
    schedule_id: str,
    schedule_data: Dict[str, Any],
    current_user: dict = Depends(get_instructor_user)
):
    """Actualizar horario."""
    return await forward_request_to_schedule_service(
        method="PUT",
        endpoint=f"/schedules/{schedule_id}",
        json_data=schedule_data,
        user_data=current_user
    )

@router.delete("/schedules/{schedule_id}")
async def delete_schedule(
    schedule_id: str,
    current_user: dict = Depends(get_instructor_user)
):
    """Eliminar horario."""
    return await forward_request_to_schedule_service(
        method="DELETE",
        endpoint=f"/schedules/{schedule_id}",
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE CONSULTA DE HORARIOS
# =============================================================================

@router.get("/schedules/by-date/{target_date}")
async def get_schedules_by_date(
    target_date: date,
    current_user: dict = Depends(get_current_user)
):
    """Obtener horarios por fecha."""
    return await forward_request_to_schedule_service(
        method="GET",
        endpoint=f"/schedules/by-date/{target_date}",
        user_data=current_user
    )

@router.get("/schedules/my-schedule")
async def get_my_schedule(
    current_user: dict = Depends(get_current_user)
):
    """Obtener horario del usuario actual."""
    return await forward_request_to_schedule_service(
        method="GET",
        endpoint="/schedules/my-schedule",
        user_data=current_user
    )

@router.get("/schedules/conflicts")
async def check_schedule_conflicts(
    start_time: str,
    end_time: str,
    instructor_id: Optional[str] = None,
    current_user: dict = Depends(get_instructor_user)
):
    """Verificar conflictos de horario."""
    params = {"start_time": start_time, "end_time": end_time}
    if instructor_id:
        params["instructor_id"] = instructor_id
        
    return await forward_request_to_schedule_service(
        method="GET",
        endpoint="/schedules/conflicts",
        params=params,
        user_data=current_user
    )
