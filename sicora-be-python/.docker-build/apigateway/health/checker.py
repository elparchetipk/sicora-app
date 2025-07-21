"""Verificación de salud de servicios."""

import httpx
import asyncio
from typing import Dict, Any
from utils.service_discovery import get_all_service_urls

async def check_service_health(service_name: str, service_url: str) -> Dict[str, Any]:
    """Verifica la salud de un servicio individual."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{service_url}/health")
            if response.status_code == 200:
                return {
                    "name": service_name,
                    "status": "healthy",
                    "url": service_url,
                    "response_time": response.elapsed.total_seconds() if hasattr(response, 'elapsed') else None
                }
            else:
                return {
                    "name": service_name,
                    "status": "unhealthy",
                    "url": service_url,
                    "error": f"HTTP {response.status_code}"
                }
    except httpx.RequestError as e:
        return {
            "name": service_name,
            "status": "unreachable",
            "url": service_url,
            "error": str(e)
        }
    except Exception as e:
        return {
            "name": service_name,
            "status": "error",
            "url": service_url,
            "error": str(e)
        }

async def check_all_services() -> Dict[str, Any]:
    """Verifica la salud de todos los servicios."""
    service_urls = get_all_service_urls()
    
    # Crear tareas para verificar todos los servicios en paralelo
    tasks = [
        check_service_health(name, url) 
        for name, url in service_urls.items()
    ]
    
    # Ejecutar todas las verificaciones en paralelo
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Procesar resultados
    services_status = {}
    healthy_count = 0
    total_count = len(service_urls)
    
    for result in results:
        if isinstance(result, dict):
            service_name = result["name"]
            services_status[service_name] = result
            if result["status"] == "healthy":
                healthy_count += 1
        else:
            # En caso de excepción
            services_status["unknown"] = {
                "status": "error",
                "error": str(result)
            }
    
    # Determinar estado general
    overall_status = "healthy" if healthy_count == total_count else "degraded" if healthy_count > 0 else "unhealthy"
    
    return {
        "overall_status": overall_status,
        "healthy_services": healthy_count,
        "total_services": total_count,
        "services": services_status
    }
