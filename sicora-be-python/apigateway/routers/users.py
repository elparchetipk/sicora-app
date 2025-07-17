"""Router proxy para UserService en ApiGateway."""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
import httpx
from typing import Optional, Dict, Any

from middleware.auth import get_current_user, get_admin_user
from utils.service_discovery import get_service_url

router = APIRouter(tags=["users"])

# URL del servicio de usuarios
USER_SERVICE_URL = get_service_url("user")

async def forward_request_to_user_service(
    method: str,
    endpoint: str,
    user_data: dict = None,
    json_data: dict = None,
    params: dict = None
):
    """Reenvía solicitudes al UserService."""
    url = f"{USER_SERVICE_URL}{endpoint}"
    
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
                detail=f"UserService unavailable: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal error: {str(e)}"
            )

# =============================================================================
# ENDPOINTS DE AUTENTICACIÓN
# =============================================================================

@router.post("/auth/login")
async def login(credentials: Dict[str, Any]):
    """Autenticación de usuario."""
    return await forward_request_to_user_service(
        method="POST",
        endpoint="/auth/login",
        json_data=credentials
    )

@router.post("/auth/register")
async def register(user_data: Dict[str, Any]):
    """Registro de nuevo usuario."""
    return await forward_request_to_user_service(
        method="POST",
        endpoint="/auth/register",
        json_data=user_data
    )

@router.post("/auth/validate")
async def validate_token(token_data: Dict[str, Any]):
    """Validación de token JWT."""
    return await forward_request_to_user_service(
        method="POST",
        endpoint="/auth/validate",
        json_data=token_data
    )

@router.post("/auth/refresh")
async def refresh_token(
    refresh_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """Renovación de token JWT."""
    return await forward_request_to_user_service(
        method="POST",
        endpoint="/auth/refresh",
        json_data=refresh_data,
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE GESTIÓN DE USUARIOS
# =============================================================================

@router.get("/users")
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_admin_user)
):
    """Obtener lista de usuarios (solo admins)."""
    return await forward_request_to_user_service(
        method="GET",
        endpoint="/users",
        params={"skip": skip, "limit": limit},
        user_data=current_user
    )

@router.get("/users/{user_id}")
async def get_user(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Obtener usuario por ID."""
    return await forward_request_to_user_service(
        method="GET",
        endpoint=f"/users/{user_id}",
        user_data=current_user
    )

@router.get("/users/me")
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user)
):
    """Obtener perfil del usuario actual."""
    return await forward_request_to_user_service(
        method="GET",
        endpoint="/users/me",
        user_data=current_user
    )

@router.put("/users/{user_id}")
async def update_user(
    user_id: str,
    user_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """Actualizar usuario."""
    return await forward_request_to_user_service(
        method="PUT",
        endpoint=f"/users/{user_id}",
        json_data=user_data,
        user_data=current_user
    )

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(get_admin_user)
):
    """Eliminar usuario (solo admins)."""
    return await forward_request_to_user_service(
        method="DELETE",
        endpoint=f"/users/{user_id}",
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE PERFIL
# =============================================================================

@router.put("/profile")
async def update_profile(
    profile_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """Actualizar perfil del usuario."""
    return await forward_request_to_user_service(
        method="PUT",
        endpoint="/profile",
        json_data=profile_data,
        user_data=current_user
    )

@router.post("/profile/change-password")
async def change_password(
    password_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """Cambiar contraseña del usuario."""
    return await forward_request_to_user_service(
        method="POST",
        endpoint="/profile/change-password",
        json_data=password_data,
        user_data=current_user
    )
