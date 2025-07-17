"""
Routers para los endpoints de la API
"""

from .attendance import router as attendance_router
from .justifications import router as justifications_router
from .alerts import router as alerts_router

__all__ = [
    'attendance_router',
    'justifications_router',
    'alerts_router'
]
