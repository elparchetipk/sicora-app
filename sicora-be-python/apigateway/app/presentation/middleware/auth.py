"""
Middleware de autenticación centralizada para APIGateway
"""

from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from typing import Optional, Dict, Any

security = HTTPBearer()

JWT_SECRET = os.getenv("JWT_SECRET", "sicora-secret-key")
JWT_ALGORITHM = "HS256"

class AuthMiddleware:
    """Middleware de autenticación centralizada."""

    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """Verificar y decodificar JWT token."""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token ha expirado"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

    @staticmethod
    async def get_current_user(credentials: HTTPAuthorizationCredentials = security) -> Dict[str, Any]:
        """Obtener usuario actual desde token."""
        return AuthMiddleware.verify_token(credentials.credentials)

    @staticmethod
    async def get_admin_user(credentials: HTTPAuthorizationCredentials = security) -> Dict[str, Any]:
        """Verificar que el usuario tiene rol de admin."""
        user = AuthMiddleware.verify_token(credentials.credentials)
        if user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado: se requiere rol de administrador"
            )
        return user
