"""Router proxy para servicios Go en ApiGateway."""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
import httpx
from typing import Optional, Dict, Any, List

from middleware.auth import get_current_user, get_instructor_user, get_admin_user
from utils.service_discovery import get_service_url

router = APIRouter(tags=["go-services"])

async def forward_request_to_go_service(
    service_name: str,
    method: str,
    endpoint: str,
    user_data: dict = None,
    json_data: dict = None,
    params: dict = None
):
    """Reenvía solicitudes a servicios Go."""
    service_url = get_service_url(f"{service_name}-go")
    url = f"{service_url}{endpoint}"
    
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
                detail=f"{service_name.title()}Service (Go) unavailable: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal error: {str(e)}"
            )

# =============================================================================
# ENDPOINTS DE USER SERVICE GO
# =============================================================================

@router.get("/go/users")
async def get_users_go(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_admin_user)
):
    """Obtener usuarios (Go service)."""
    return await forward_request_to_go_service(
        service_name="user",
        method="GET",
        endpoint="/users",
        params={"skip": skip, "limit": limit},
        user_data=current_user
    )

@router.post("/go/users")
async def create_user_go(
    user_data: Dict[str, Any],
    current_user: dict = Depends(get_admin_user)
):
    """Crear usuario (Go service)."""
    return await forward_request_to_go_service(
        service_name="user",
        method="POST",
        endpoint="/users",
        json_data=user_data,
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE ATTENDANCE SERVICE GO
# =============================================================================

@router.get("/go/attendance")
async def get_attendance_go(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Obtener asistencias (Go service)."""
    return await forward_request_to_go_service(
        service_name="attendance",
        method="GET",
        endpoint="/attendance",
        params={"skip": skip, "limit": limit},
        user_data=current_user
    )

@router.post("/go/attendance")
async def create_attendance_go(
    attendance_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """Registrar asistencia (Go service)."""
    return await forward_request_to_go_service(
        service_name="attendance",
        method="POST",
        endpoint="/attendance",
        json_data=attendance_data,
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE SCHEDULE SERVICE GO
# =============================================================================

@router.get("/go/schedules")
async def get_schedules_go(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Obtener horarios (Go service)."""
    return await forward_request_to_go_service(
        service_name="schedule",
        method="GET",
        endpoint="/schedules",
        params={"skip": skip, "limit": limit},
        user_data=current_user
    )

@router.post("/go/schedules")
async def create_schedule_go(
    schedule_data: Dict[str, Any],
    current_user: dict = Depends(get_instructor_user)
):
    """Crear horario (Go service)."""
    return await forward_request_to_go_service(
        service_name="schedule",
        method="POST",
        endpoint="/schedules",
        json_data=schedule_data,
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE EVALIN SERVICE GO
# =============================================================================

@router.get("/go/evaluations")
async def get_evaluations_go(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Obtener evaluaciones (Go service)."""
    return await forward_request_to_go_service(
        service_name="evalin",
        method="GET",
        endpoint="/evaluations",
        params={"skip": skip, "limit": limit},
        user_data=current_user
    )

@router.post("/go/evaluations")
async def create_evaluation_go(
    evaluation_data: Dict[str, Any],
    current_user: dict = Depends(get_instructor_user)
):
    """Crear evaluación (Go service)."""
    return await forward_request_to_go_service(
        service_name="evalin",
        method="POST",
        endpoint="/evaluations",
        json_data=evaluation_data,
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE PROJECT EVALUATION SERVICE GO
# =============================================================================

@router.get("/go/project-evaluations")
async def get_project_evaluations_go(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Obtener evaluaciones de proyecto (Go service)."""
    return await forward_request_to_go_service(
        service_name="project-eval",
        method="GET",
        endpoint="/project-evaluations",
        params={"skip": skip, "limit": limit},
        user_data=current_user
    )

@router.post("/go/project-evaluations")
async def create_project_evaluation_go(
    project_eval_data: Dict[str, Any],
    current_user: dict = Depends(get_instructor_user)
):
    """Crear evaluación de proyecto (Go service)."""
    return await forward_request_to_go_service(
        service_name="project-eval",
        method="POST",
        endpoint="/project-evaluations",
        json_data=project_eval_data,
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE SOFTWARE FACTORY SERVICE GO
# =============================================================================

@router.get("/go/software-factory/projects")
async def get_software_projects_go(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Obtener proyectos de fábrica de software (Go service)."""
    return await forward_request_to_go_service(
        service_name="software-factory",
        method="GET",
        endpoint="/projects",
        params={"skip": skip, "limit": limit},
        user_data=current_user
    )

@router.post("/go/software-factory/projects")
async def create_software_project_go(
    project_data: Dict[str, Any],
    current_user: dict = Depends(get_instructor_user)
):
    """Crear proyecto de fábrica de software (Go service)."""
    return await forward_request_to_go_service(
        service_name="software-factory",
        method="POST",
        endpoint="/projects",
        json_data=project_data,
        user_data=current_user
    )

@router.get("/go/software-factory/templates")
async def get_project_templates_go(
    current_user: dict = Depends(get_current_user)
):
    """Obtener plantillas de proyecto (Go service)."""
    return await forward_request_to_go_service(
        service_name="software-factory",
        method="GET",
        endpoint="/templates",
        user_data=current_user
    )
