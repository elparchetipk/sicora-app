"""
JWT decoder for extracting user information from tokens.
"""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID

from ...config import settings
from ...domain.exceptions import UnauthorizedAccessError

security = HTTPBearer()


class JWTDecoder:
    """
    Utility class for decoding JWT tokens and extracting user information.
    """

    @staticmethod
    def decode_token(token: str) -> dict:
        """
        Decode a JWT token and return its payload.
        
        Args:
            token: The JWT token to decode
            
        Returns:
            The decoded token payload
            
        Raises:
            UnauthorizedAccessError: If the token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise UnauthorizedAccessError("token", "valid token (token expired)")
        except jwt.InvalidTokenError:
            raise UnauthorizedAccessError("token", "valid token (invalid token)")

    @staticmethod
    def get_user_id(token: str) -> UUID:
        """
        Extract the user ID from a JWT token.
        
        Args:
            token: The JWT token
            
        Returns:
            The user ID as UUID
            
        Raises:
            UnauthorizedAccessError: If the token is invalid or doesn't contain a user ID
        """
        payload = JWTDecoder.decode_token(token)
        
        # The user ID should be in the 'sub' claim
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedAccessError("token", "token with user ID")
        
        try:
            return UUID(user_id)
        except ValueError:
            raise UnauthorizedAccessError("token", "token with valid user ID format")


async def get_user_id_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UUID:
    """
    FastAPI dependency for extracting the user ID from the JWT token.
    
    Args:
        credentials: The HTTP Authorization credentials
        
    Returns:
        The user ID as UUID
        
    Raises:
        HTTPException: If the token is invalid or doesn't contain a user ID
    """
    try:
        return JWTDecoder.get_user_id(credentials.credentials)
    except UnauthorizedAccessError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "unauthorized", "message": str(e)},
            headers={"WWW-Authenticate": "Bearer"},
        )