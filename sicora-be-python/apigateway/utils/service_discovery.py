"""Utilidades para descubrimiento de servicios."""

import os
from typing import Dict

# URLs de servicios actualizadas con puertos correctos
DEFAULT_SERVICE_URLS = {
    # Stack Python
    "user": "http://userservice:8001",
    "schedule": "http://scheduleservice:8002", 
    "attendance": "http://attendanceservice:8003",
    "evalin": "http://evalinservice:8004",
    "meval": "http://mevalservice:8005",
    "kb": "http://kbservice:8006",
    "ai": "http://aiservice:8007",
    
    # Stack Go
    "user-go": "http://userservice-go:8101",
    "schedule-go": "http://scheduleservice-go:8102",
    "attendance-go": "http://attendanceservice-go:8103",
    "evalin-go": "http://evalinservice-go:8104",
    "meval-go": "http://mevalservice-go:8105",
    "kb-go": "http://kbservice-go:8106",
    "project-eval-go": "http://projectevalservice-go:8107",
    "software-factory-go": "http://softwarefactoryservice-go:8108",
    
    # Servicios de infraestructura
    "apigateway": "http://apigateway:8000",
    "notification": "http://notificationservice:8009"
}

def get_service_url(service_name: str) -> str:
    """Obtiene la URL de un servicio."""
    env_var = f"{service_name.upper()}_SERVICE_URL"
    return os.getenv(env_var, DEFAULT_SERVICE_URLS.get(service_name, f"http://{service_name}service:8000"))

def get_all_service_urls() -> Dict[str, str]:
    """Obtiene todas las URLs de servicios."""
    return {name: get_service_url(name) for name in DEFAULT_SERVICE_URLS.keys()}

def get_python_services() -> Dict[str, str]:
    """Obtiene solo los servicios del stack Python."""
    python_services = ["user", "schedule", "attendance", "evalin", "meval", "kb", "ai"]
    return {name: get_service_url(name) for name in python_services}

def get_go_services() -> Dict[str, str]:
    """Obtiene solo los servicios del stack Go."""
    go_services = ["user-go", "schedule-go", "attendance-go", "evalin-go", "meval-go", "kb-go", "project-eval-go", "software-factory-go"]
    return {name: get_service_url(name) for name in go_services}
