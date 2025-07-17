"""Middleware de autenticación mejorado para ApiGateway."""

from fastapi import HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import asyncio
from typing import Dict, Any
import logging

from utils.service_discovery import get_service_url
from config import config


# Configurar logging
logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)

# Cache simple para tokens válidos (en producción usar Redis)
_token_cache = {}
_cache_ttl = 300  # 5 minutos


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Valida el token JWT y obtiene información del usuario."""

    # Verificar si el endpoint requiere autenticación
    if _is_public_endpoint(request.url.path):
        return {"user_id": "anonymous", "role": "public", "email": ""}

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autorización requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    # Verificar cache de tokens
    if token in _token_cache:
        cached_data = _token_cache[token]
        if cached_data.get("expires_at", 0) > asyncio.get_event_loop().time():
            return cached_data["user_data"]
        else:
            # Token expirado en cache
            del _token_cache[token]

    # Validar token con UserService
    user_data = await _validate_token_with_service(token)

    # Guardar en cache
    _token_cache[token] = {
        "user_data": user_data,
        "expires_at": asyncio.get_event_loop().time() + _cache_ttl
    }

    return user_data


async def _validate_token_with_service(token: str) -> Dict[str, Any]:
    """Valida el token con el UserService."""
    user_service_url = get_service_url("user")

    timeout = config.SERVICE_TIMEOUT
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            # Intentar validar con UserService Python
            response = await client.post(
                f"{user_service_url}/auth/validate",
                json={"token": token},
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                user_data = response.json()
                user_id = user_data.get('user_id')
                logger.info(f"Token validado para usuario: {user_id}")
                return user_data
            elif response.status_code == 401:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido o expirado",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                code = response.status_code
                logger.warning(f"UserService respondió con código: {code}")

        except httpx.RequestError as e:
            logger.warning(f"Error conectando con UserService: {e}")

            # Fallback: intentar con UserService Go
            try:
                user_go_service_url = get_service_url("user-go")
                response = await client.post(
                    f"{user_go_service_url}/auth/validate",
                    json={"token": token}
                )

                if response.status_code == 200:
                    user_data = response.json()
                    user_id = user_data.get('user_id')
                    msg = f"Token validado con Go service para usuario: {user_id}"
                    logger.info(msg)
                    return user_data

            except httpx.RequestError:
                logger.error("UserService Go también falló")

        except Exception as e:
            logger.error(f"Error inesperado validando token: {e}")

    # Si llegamos aquí, no se pudo validar el token
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Servicios de autenticación no disponibles"
    )


def _is_public_endpoint(path: str) -> bool:
    """Verifica si un endpoint es público (no requiere autenticación)."""
    public_endpoints = [
        "/",
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/users/auth/login",
        "/api/v1/users/auth/register",
        "/api/v1/go/users/auth/login",
    ]

    return any(path.startswith(endpoint) for endpoint in public_endpoints)


def require_role(required_roles: list):
    """Decorador para requerir roles específicos."""
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in required_roles:
            roles_str = ', '.join(required_roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere rol: {roles_str}"
            )
        return current_user
    return role_checker


# Dependencias específicas por rol
async def get_admin_user(
    current_user: dict = Depends(require_role(["admin"]))
):
    """Requiere rol de administrador."""
    return current_user


async def get_instructor_user(
    current_user: dict = Depends(
        require_role(["instructor", "coordinador", "admin"])
    )
):
    """Requiere rol de instructor, coordinador o admin."""
    return current_user


async def get_student_user(
    current_user: dict = Depends(
        require_role(["aprendiz", "instructor", "coordinador", "admin"])
    )
):
    """Requiere cualquier rol autenticado."""
    return current_user


# Función para limpiar cache periódicamente
async def cleanup_token_cache():
    """Limpia tokens expirados del cache."""
    current_time = asyncio.get_event_loop().time()
    expired_tokens = [
        token for token, data in _token_cache.items()
        if data.get("expires_at", 0) <= current_time
    ]

    for token in expired_tokens:
        del _token_cache[token]

    count = len(expired_tokens)
    logger.info(f"Cache limpiado: {count} tokens expirados eliminados")
