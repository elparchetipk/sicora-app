"""
Tests unitarios para AuthMiddleware
"""

import pytest
from fastapi import HTTPException
from app.presentation.middleware.auth import AuthMiddleware
import jwt

JWT_SECRET = "sicora-secret-key"

def test_verify_valid_token():
    """Test verificación de token válido."""
    payload = {"user_id": "123", "role": "user"}
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    result = AuthMiddleware.verify_token(token)
    assert result["user_id"] == "123"
    assert result["role"] == "user"

def test_verify_invalid_token():
    """Test verificación de token inválido."""
    with pytest.raises(HTTPException):
        AuthMiddleware.verify_token("invalid-token")

def test_verify_expired_token():
    """Test verificación de token expirado."""
    import time
    payload = {"user_id": "123", "exp": int(time.time()) - 3600}  # Expirado hace 1 hora
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    with pytest.raises(HTTPException):
        AuthMiddleware.verify_token(token)
