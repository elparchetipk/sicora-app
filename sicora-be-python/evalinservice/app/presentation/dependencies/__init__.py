"""Presentation dependencies module."""

from .container import container, DependencyContainer
from .auth import (
    CurrentUser,
    get_current_user,
    get_admin_user,
    get_instructor_user,
    get_student_user,
    require_roles
)

__all__ = [
    "container",
    "DependencyContainer",
    "CurrentUser",
    "get_current_user",
    "get_admin_user",
    "get_instructor_user",
    "get_student_user",
    "require_roles",
]
