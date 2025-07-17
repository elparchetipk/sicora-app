"""Presentation layer routers."""

from .schedule_router import router as schedule_router
from .admin_router import router as admin_router

__all__ = [
    "schedule_router",
    "admin_router",
]
