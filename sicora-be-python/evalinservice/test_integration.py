#!/usr/bin/env python3
"""
Test de integración completo para EvalinService
Verifica que todos los componentes funcionen correctamente juntos
"""

import os
import sys
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta

# Configurar variables de entorno para testing
os.environ["DATABASE_URL"] = "sqlite:///test_integration.db"
os.environ["SECRET_KEY"] = "test-secret-key-for-integration"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

def print_status(message: str, status: str = "INFO"):
    """Imprime un mensaje con formato."""
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARN": "⚠️"}
    print(f"{icons.get(status, 'ℹ️')} {message}")

async def test_service_health():
    """Test de salud del servicio."""
    print_status("Probando salud del servicio...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8005/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print_status(f"Servicio saludable: {data}", "SUCCESS")
                    return True
                else:
                    print_status(f"Servicio no saludable: {response.status}", "ERROR")
                    return False
    except Exception as e:
        print_status(f"Error conectando al servicio: {e}", "ERROR")
        return False

async def test_questions_endpoints():
    """Test de endpoints de preguntas."""
    print_status("Probando endpoints de preguntas...")
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test GET questions
            async with session.get("http://localhost:8005/api/v1/questions/") as response:
                if response.status == 200:
                    data = await response.json()
                    print_status(f"GET preguntas OK: {len(data.get('questions', []))} preguntas", "SUCCESS")
                    return True
                else:
                    print_status(f"GET preguntas falló: {response.status}", "ERROR")
                    return False
                    
    except Exception as e:
        print_status(f"Error en test de preguntas: {e}", "ERROR")
        return False

async def run_integration_tests():
    """Ejecuta todos los tests de integración."""
    print_status("=== INICIANDO TESTS DE INTEGRACIÓN EVALINSERVICE ===")
    print_status(f"Fecha: {datetime.now()}")
    print_status(f"URL Base: http://localhost:8005")
    print("")
    
    tests = [
        ("Salud del Servicio", test_service_health),
        ("Preguntas", test_questions_endpoints),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print_status(f"--- Ejecutando: {test_name} ---")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print_status(f"{test_name} ERROR: {e}", "ERROR")
            results.append((test_name, False))
        print("")
    
    # Resumen final
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print_status(f"TOTAL: {passed}/{total} tests pasaron")
    return passed == total

def main():
    """Función principal."""
    print_status("EvalinService - Test de Integración")
    
    try:
        result = asyncio.run(run_integration_tests())
        sys.exit(0 if result else 1)
    except Exception as e:
        print_status(f"Error: {e}", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()