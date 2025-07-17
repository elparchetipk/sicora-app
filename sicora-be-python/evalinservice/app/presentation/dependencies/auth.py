"""Authentication dependencies for EvalinService."""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import os
from uuid import UUID

security = HTTPBearer()


class CurrentUser:
    """Información del usuario actual."""
    
    def __init__(self, user_id: UUID, email: str, role: str, first_name: str, last_name: str):
        self.user_id = user_id
        self.email = email
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
    
    def is_admin(self) -> bool:
        """Verificar si el usuario es administrador."""
        return self.role in ["admin", "super_admin"]
    
    def is_instructor(self) -> bool:
        """Verificar si el usuario es instructor."""
        return self.role in ["instructor", "admin", "super_admin"]
    
    def is_student(self) -> bool:
        """Verificar si el usuario es estudiante."""
        return self.role == "student"


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> CurrentUser:
    """
    Obtener información del usuario actual desde el token JWT.
    
    Args:
        credentials: Credenciales HTTP Bearer
        
    Returns:
        CurrentUser: Información del usuario autenticado
        
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    token = credentials.credentials
    
    # Validar token con UserService
    user_service_url = os.getenv("USER_SERVICE_URL", "http://userservice:8000")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{user_service_url}/auth/validate",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido o expirado",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            user_data = response.json()
            
            return CurrentUser(
                user_id=UUID(user_data["user_id"]),
                email=user_data["email"],
                role=user_data["role"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"]
            )
            
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio de autenticación no disponible"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error al validar token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_admin_user(
    current_user: CurrentUser = Depends(get_current_user)
) -> CurrentUser:
    """
    Dependency que requiere usuario administrador.
    
    Args:
        current_user: Usuario actual
        
    Returns:
        CurrentUser: Usuario administrador
        
    Raises:
        HTTPException: Si el usuario no es administrador
    """
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos de administrador requeridos"
        )
    
    return current_user


async def get_instructor_user(
    current_user: CurrentUser = Depends(get_current_user)
) -> CurrentUser:
    """
    Dependency que requiere usuario instructor o superior.
    
    Args:
        current_user: Usuario actual
        
    Returns:
        CurrentUser: Usuario instructor
        
    Raises:
        HTTPException: Si el usuario no es instructor o superior
    """
    if not current_user.is_instructor():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos de instructor requeridos"
        )
    
    return current_user


async def get_student_user(
    current_user: CurrentUser = Depends(get_current_user)
) -> CurrentUser:
    """
    Dependency que requiere usuario estudiante.
    
    Args:
        current_user: Usuario actual
        
    Returns:
        CurrentUser: Usuario estudiante
        
    Raises:
        HTTPException: Si el usuario no es estudiante
    """
    if not current_user.is_student():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos de estudiante requeridos"
        )
    
    return current_user


def require_roles(*roles: str):
    """
    Decorator para requerir roles específicos.
    
    Args:
        *roles: Roles permitidos
        
    Returns:
        Función dependency
    """
    async def check_roles(
        current_user: CurrentUser = Depends(get_current_user)
    ) -> CurrentUser:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permisos requeridos: {', '.join(roles)}"
            )
        return current_user
    
    return check_roles


def require_role(user: CurrentUser, allowed_roles: list[str]) -> None:
    """
    Verificar que el usuario tenga uno de los roles permitidos.
    
    Args:
        user: Usuario actual
        allowed_roles: Lista de roles permitidos
        
    Raises:
        HTTPException: Si el usuario no tiene permisos
    """
    if user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permisos requeridos: {', '.join(allowed_roles)}"
        )
