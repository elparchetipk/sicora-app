"""
Entidades del dominio APIGateway
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class RequestStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"

@dataclass
class RequestLog:
    """Entidad para logging de requests."""
    id: Optional[int]
    user_id: Optional[str]
    service_name: str
    endpoint: str
    method: str
    status_code: int
    response_time_ms: float
    request_size_bytes: int
    response_size_bytes: int
    ip_address: str
    user_agent: str
    timestamp: datetime
    status: RequestStatus
    error_message: Optional[str] = None

@dataclass
class ServiceHealth:
    """Entidad para health status de servicios."""
    service_name: str
    is_healthy: bool
    last_check: datetime
    response_time_ms: Optional[float]
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
