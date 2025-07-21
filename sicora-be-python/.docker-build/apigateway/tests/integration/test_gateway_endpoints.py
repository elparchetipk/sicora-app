"""
Tests de integración para APIGateway
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test del endpoint de health check."""
    response = client.get("/health")
    assert response.status_code == 200

def test_metrics_endpoint():
    """Test del endpoint de métricas."""
    response = client.get("/metrics")
    assert response.status_code == 200
