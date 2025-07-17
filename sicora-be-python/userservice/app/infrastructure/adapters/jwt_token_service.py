"""JWT token service implementation."""

import os
from datetime import datetime, timedelta
from typing import Dict, Any, Set
from uuid import UUID

import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, PyJWTError

from app.config import settings
from app.application.interfaces.token_service_interface import TokenServiceInterface
from app.domain.exceptions.user_exceptions import InvalidTokenError as DomainInvalidTokenError


class JWTTokenService(TokenServiceInterface):
    """JWT implementation of TokenServiceInterface."""
    
    def __init__(self):
        self._secret_key = settings.JWT_SECRET_KEY
        self._algorithm = settings.JWT_ALGORITHM
        self._access_token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self._refresh_token_expire_days = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        
        # In production, this should be stored in Redis or a database
        self._revoked_tokens: Set[str] = set()
    
    def create_access_token(self, user_id: UUID, role: str, expires_delta: int = None) -> str:
        """Create an access token for a user."""
        if expires_delta:
            expire = datetime.utcnow() + timedelta(minutes=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=self._access_token_expire_minutes)
        
        to_encode = {
            "sub": str(user_id),
            "role": role,
            "type": "access",
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        
        encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, user_id: UUID) -> str:
        """Create a refresh token for a user."""
        expire = datetime.utcnow() + timedelta(days=self._refresh_token_expire_days)
        
        to_encode = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        
        encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return encoded_jwt
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode and validate a JWT token."""
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return payload
        except ExpiredSignatureError:
            raise InvalidTokenError("Token has expired")
        except InvalidTokenError as e:
            raise InvalidTokenError(f"Invalid token: {str(e)}")
    
    def is_token_valid(self, token: str) -> bool:
        """Check if a token is valid and not expired."""
        try:
            self.decode_token(token)
            return True
        except InvalidTokenError:
            return False
    
    def get_token_expiration(self, token: str) -> datetime:
        """Get the expiration date of a token."""
        payload = self.decode_token(token)
        exp_timestamp = payload.get("exp")
        if not exp_timestamp:
            raise InvalidTokenError("Token does not have expiration")
        
        return datetime.fromtimestamp(exp_timestamp)
    
    def revoke_token(self, token: str) -> None:
        """Revoke a token (add to blacklist)."""
        # In production, store this in Redis with expiration
        self._revoked_tokens.add(token)
    
    def is_token_revoked(self, token: str) -> bool:
        """Check if a token has been revoked."""
        return token in self._revoked_tokens
    
    def revoke_all_user_tokens(self, user_id: UUID, exclude_current: bool = False) -> None:
        """
        Revoke all tokens for a specific user.
        
        In a production environment, this would typically:
        1. Update a blacklist in Redis/database with user_id and timestamp
        2. When validating tokens, check if token.iat < blacklist.timestamp
        
        For now, we'll use a simple in-memory approach.
        """
        # In production, this would be implemented with Redis:
        # redis.set(f"user_blacklist:{user_id}", datetime.utcnow().timestamp())
        # 
        # For development, we'll track revoked user IDs with timestamps
        if not hasattr(self, '_revoked_users'):
            self._revoked_users = {}
        
        self._revoked_users[str(user_id)] = datetime.utcnow().timestamp()
    
    def is_user_token_revoked(self, user_id: UUID, token_issued_at: datetime) -> bool:
        """Check if a user's token was revoked after it was issued."""
        if not hasattr(self, '_revoked_users'):
            return False
            
        user_blacklist_time = self._revoked_users.get(str(user_id))
        if not user_blacklist_time:
            return False
            
        return token_issued_at.timestamp() < user_blacklist_time
    
    # PASO FINAL: Password reset token methods
    
    def create_password_reset_token(self, user_id: UUID) -> str:
        """Create a password reset token with 1 hour expiration."""
        now = datetime.utcnow()
        payload = {
            "sub": str(user_id),
            "type": "password_reset",
            "iat": now,
            "exp": now + timedelta(hours=1),  # 1 hour expiration
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)
    
    def validate_password_reset_token(self, token: str) -> bool:
        """Validate a password reset token."""
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return payload.get("type") == "password_reset"
        except PyJWTError:
            return False
    
    def get_user_id_from_reset_token(self, token: str) -> str:
        """Get user ID from password reset token."""
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            if payload.get("type") != "password_reset":
                raise ValueError("Invalid token type")
            return payload.get("sub")
        except PyJWTError as e:
            raise ValueError(f"Invalid token: {e}")
    
    def validate_refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Validate and decode a refresh token."""
        try:
            payload = jwt.decode(refresh_token, self._secret_key, algorithms=[self._algorithm])
            if payload.get("type") != "refresh":
                raise ValueError("Invalid token type")
            return payload
        except PyJWTError as e:
            raise ValueError(f"Invalid refresh token: {e}")
    
    def get_user_id_from_refresh_token(self, refresh_token: str) -> UUID:
        """Extract user ID from refresh token."""
        payload = self.validate_refresh_token(refresh_token)
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise ValueError("No user ID in token")
        return UUID(user_id_str)
