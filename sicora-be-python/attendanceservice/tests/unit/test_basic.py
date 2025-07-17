"""Test simple para verificar funcionamiento."""

import pytest
import asyncio
from unittest.mock import AsyncMock
from uuid import uuid4

# Test básico sin dependencias complejas
@pytest.mark.asyncio
async def test_basic_functionality():
    """Test básico de funcionamiento."""
    # Crear UUIDs de prueba
    student_id = uuid4()
    instructor_id = uuid4()
    
    # Verificar que podemos crear objetos básicos
    assert isinstance(student_id, type(uuid4()))
    assert isinstance(instructor_id, type(uuid4()))
    
    # Test básico de mock async
    mock_service = AsyncMock()
    mock_service.some_method.return_value = {"test": "data"}
    
    result = await mock_service.some_method()
    assert result == {"test": "data"}
    
    print("✅ Test básico exitoso")
