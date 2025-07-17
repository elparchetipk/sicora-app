"""Token service interface for application layer."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID


class TokenServiceInterface(ABC):
    """Interface for JWT token management."""
    
    @abstractmethod
    def create_access_token(self, user_id: UUID, role: str, expires_delta: int = None) -> str:
        """Create an access token for a user."""
        pass
    
    @abstractmethod
    def create_refresh_token(self, user_id: UUID) -> str:
        """Create a refresh token for a user."""
        pass
    
    @abstractmethod
    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode and validate a JWT token."""
        pass
    
    @abstractmethod
    def is_token_valid(self, token: str) -> bool:
        """Check if a token is valid and not expired."""
        pass
    
    @abstractmethod
    def get_token_expiration(self, token: str) -> datetime:
        """Get the expiration date of a token."""
        pass
    
    @abstractmethod
    def revoke_token(self, token: str) -> None:
        """Revoke a token (add to blacklist)."""
        pass
    
    @abstractmethod
    def is_token_revoked(self, token: str) -> bool:
        """Check if a token has been revoked."""
        pass
    
    # PASO 5: Métodos adicionales para gestión de tokens
    
    @abstractmethod
    def revoke_all_user_tokens(self, user_id: UUID, exclude_current: bool = False) -> None:
        """Revoke all tokens for a user."""
        pass
    
    # PASO 6: Métodos específicos para refresh tokens
    
    @abstractmethod
    def validate_refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Validate and decode a refresh token."""
        pass
    
    @abstractmethod
    def get_user_id_from_refresh_token(self, refresh_token: str) -> UUID:
        """Extract user ID from refresh token."""
        pass
    
    # PASO FINAL: Password reset token methods
    @abstractmethod
    def create_password_reset_token(self, user_id: UUID) -> str:
        """Create a password reset token for a user."""
        pass
    
    @abstractmethod
    def validate_password_reset_token(self, token: str) -> bool:
        """Validate a password reset token."""
        pass
    
    @abstractmethod
    def get_user_id_from_reset_token(self, token: str) -> str:
        """Get user ID from password reset token."""
        pass
