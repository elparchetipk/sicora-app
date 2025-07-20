"""Router proxy para EvalinService en ApiGateway."""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
import httpx
from typing import Optional, Dict, Any, List

from middleware.auth import get_current_user, get_instructor_user
from utils.service_discovery import get_service_url

router = APIRouter(tags=["evalin"])

# URL del servicio de evaluaciones internas
EVALIN_SERVICE_URL = get_service_url("evalin")

async def forward_request_to_evalin_service(
    method: str,
    endpoint: str,
    user_data: dict = None,
    json_data: dict = None,
    params: dict = None
):
    """Reenvía solicitudes al EvalinService."""
    url = f"{EVALIN_SERVICE_URL}{endpoint}"
    
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
                detail=f"EvalinService unavailable: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal error: {str(e)}"
            )

# =============================================================================
# ENDPOINTS DE EVALUACIONES INTERNAS
# =============================================================================

@router.get("/evaluations")
async def get_evaluations(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Obtener evaluaciones internas."""
    params = {"skip": skip, "limit": limit}
    if status:
        params["status"] = status
        
    return await forward_request_to_evalin_service(
        method="GET",
        endpoint="/evaluations",
        params=params,
        user_data=current_user
    )

@router.get("/evaluations/{evaluation_id}")
async def get_evaluation(
    evaluation_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Obtener evaluación por ID."""
    return await forward_request_to_evalin_service(
        method="GET",
        endpoint=f"/evaluations/{evaluation_id}",
        user_data=current_user
    )

@router.post("/evaluations")
async def create_evaluation(
    evaluation_data: Dict[str, Any],
    current_user: dict = Depends(get_instructor_user)
):
    """Crear nueva evaluación (solo instructores)."""
    return await forward_request_to_evalin_service(
        method="POST",
        endpoint="/evaluations",
        json_data=evaluation_data,
        user_data=current_user
    )

@router.put("/evaluations/{evaluation_id}")
async def update_evaluation(
    evaluation_id: str,
    evaluation_data: Dict[str, Any],
    current_user: dict = Depends(get_instructor_user)
):
    """Actualizar evaluación."""
    return await forward_request_to_evalin_service(
        method="PUT",
        endpoint=f"/evaluations/{evaluation_id}",
        json_data=evaluation_data,
        user_data=current_user
    )

@router.delete("/evaluations/{evaluation_id}")
async def delete_evaluation(
    evaluation_id: str,
    current_user: dict = Depends(get_instructor_user)
):
    """Eliminar evaluación."""
    return await forward_request_to_evalin_service(
        method="DELETE",
        endpoint=f"/evaluations/{evaluation_id}",
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE RESPUESTAS DE EVALUACIÓN
# =============================================================================

@router.get("/evaluations/{evaluation_id}/responses")
async def get_evaluation_responses(
    evaluation_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Obtener respuestas de una evaluación."""
    return await forward_request_to_evalin_service(
        method="GET",
        endpoint=f"/evaluations/{evaluation_id}/responses",
        user_data=current_user
    )

@router.post("/evaluations/{evaluation_id}/responses")
async def submit_evaluation_response(
    evaluation_id: str,
    response_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """Enviar respuesta a evaluación."""
    return await forward_request_to_evalin_service(
        method="POST",
        endpoint=f"/evaluations/{evaluation_id}/responses",
        json_data=response_data,
        user_data=current_user
    )

@router.get("/evaluations/{evaluation_id}/results")
async def get_evaluation_results(
    evaluation_id: str,
    current_user: dict = Depends(get_instructor_user)
):
    """Obtener resultados de evaluación (solo instructores)."""
    return await forward_request_to_evalin_service(
        method="GET",
        endpoint=f"/evaluations/{evaluation_id}/results",
        user_data=current_user
    )