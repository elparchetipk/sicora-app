"""Configuración del API Gateway."""

import os
from typing import Dict, List


class Config:
    """Configuración principal del API Gateway."""
    
    # Configuración del servidor
    HOST = os.getenv("GATEWAY_HOST", "0.0.0.0")
    PORT = int(os.getenv("GATEWAY_PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # Configuración de CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    
    # Timeouts para servicios
    SERVICE_TIMEOUT = int(os.getenv("SERVICE_TIMEOUT", "30"))
    HEALTH_CHECK_TIMEOUT = int(os.getenv("HEALTH_CHECK_TIMEOUT", "5"))
    
    # Configuración de autenticación
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))
    
    # Configuración de logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Servicios habilitados
    PYTHON_SERVICES_ENABLED = os.getenv("PYTHON_SERVICES_ENABLED", "true").lower() == "true"
    GO_SERVICES_ENABLED = os.getenv("GO_SERVICES_ENABLED", "true").lower() == "true"
    
    # Rate limiting
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "false").lower() == "true"
    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "60"))


class ServiceConfig:
    """Configuración específica de servicios."""
    
    # Puertos por defecto para servicios Python
    PYTHON_SERVICES = {
        "user": 8001,
        "schedule": 8002,
        "attendance": 8003,
        "evalin": 8004,
        "meval": 8005,
        "kb": 8006,
        "ai": 8007,
    }
    
    # Puertos por defecto para servicios Go
    GO_SERVICES = {
        "user-go": 8101,
        "schedule-go": 8102,
        "attendance-go": 8103,
        "evalin-go": 8104,
        "meval-go": 8105,
        "kb-go": 8106,
        "project-eval-go": 8107,
        "software-factory-go": 8108,
    }
    
    # Servicios críticos que deben estar disponibles
    CRITICAL_SERVICES = ["user", "ai", "kb"]
    
    # Servicios opcionales
    OPTIONAL_SERVICES = ["meval", "project-eval-go", "software-factory-go"]


# Instancia global de configuración
config = Config()
service_config = ServiceConfig()
