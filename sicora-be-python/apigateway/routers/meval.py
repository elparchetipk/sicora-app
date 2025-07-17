"""Router proxy para MevalService en ApiGateway."""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
import httpx
from typing import Optional, Dict, Any, List

from middleware.auth import get_current_user, get_instructor_user
from utils.service_discovery import get_service_url

router = APIRouter(tags=["meval"])

# URL del servicio de meta-evaluaciones
MEVAL_SERVICE_URL = get_service_url("meval")

async def forward_request_to_meval_service(
    method: str,
    endpoint: str,
    user_data: dict = None,
    json_data: dict = None,
    params: dict = None
):
    """Reenvía solicitudes al MevalService."""
    url = f"{MEVAL_SERVICE_URL}{endpoint}"
    
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
                detail=f"MevalService unavailable: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal error: {str(e)}"
            )

# =============================================================================
# ENDPOINTS DE META-EVALUACIONES
# =============================================================================

@router.get("/meta-evaluations")
async def get_meta_evaluations(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Obtener meta-evaluaciones."""
    params = {"skip": skip, "limit": limit}
    if status:
        params["status"] = status
        
    return await forward_request_to_meval_service(
        method="GET",
        endpoint="/meta-evaluations",
        params=params,
        user_data=current_user
    )

@router.get("/meta-evaluations/{meval_id}")
async def get_meta_evaluation(
    meval_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Obtener meta-evaluación por ID."""
    return await forward_request_to_meval_service(
        method="GET",
        endpoint=f"/meta-evaluations/{meval_id}",
        user_data=current_user
    )

@router.post("/meta-evaluations")
async def create_meta_evaluation(
    meval_data: Dict[str, Any],
    current_user: dict = Depends(get_instructor_user)
):
    """Crear nueva meta-evaluación (solo instructores)."""
    return await forward_request_to_meval_service(
        method="POST",
        endpoint="/meta-evaluations",
        json_data=meval_data,
        user_data=current_user
    )

@router.put("/meta-evaluations/{meval_id}")
async def update_meta_evaluation(
    meval_id: str,
    meval_data: Dict[str, Any],
    current_user: dict = Depends(get_instructor_user)
):
    """Actualizar meta-evaluación."""
    return await forward_request_to_meval_service(
        method="PUT",
        endpoint=f"/meta-evaluations/{meval_id}",
        json_data=meval_data,
        user_data=current_user
    )

@router.delete("/meta-evaluations/{meval_id}")
async def delete_meta_evaluation(
    meval_id: str,
    current_user: dict = Depends(get_instructor_user)
):
    """Eliminar meta-evaluación."""
    return await forward_request_to_meval_service(
        method="DELETE",
        endpoint=f"/meta-evaluations/{meval_id}",
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE ANÁLISIS Y REPORTES
# =============================================================================

@router.get("/analytics/performance")
async def get_performance_analytics(
    student_id: Optional[str] = None,
    program_id: Optional[str] = None,
    current_user: dict = Depends(get_instructor_user)
):
    """Obtener análisis de rendimiento."""
    params = {}
    if student_id:
        params["student_id"] = student_id
    if program_id:
        params["program_id"] = program_id
        
    return await forward_request_to_meval_service(
        method="GET",
        endpoint="/analytics/performance",
        params=params,
        user_data=current_user
    )

@router.get("/analytics/trends")
async def get_evaluation_trends(
    period: Optional[str] = "month",
    current_user: dict = Depends(get_instructor_user)
):
    """Obtener tendencias de evaluación."""
    return await forward_request_to_meval_service(
        method="GET",
        endpoint="/analytics/trends",
        params={"period": period},
        user_data=current_user
    )

@router.get("/reports/summary")
async def get_evaluation_summary(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: dict = Depends(get_instructor_user)
):
    """Obtener resumen de evaluaciones."""
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
        
    return await forward_request_to_meval_service(
        method="GET",
        endpoint="/reports/summary",
        params=params,
        user_data=current_user
    )
