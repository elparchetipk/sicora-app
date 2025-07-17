"""Period status value object."""

from enum import Enum


class PeriodStatus(Enum):
    """
    Value object que define los estados posibles de un período de evaluación.
    """
    SCHEDULED = "scheduled"  # Programado para el futuro
    ACTIVE = "active"  # Activo, evaluaciones pueden ser realizadas
    INACTIVE = "inactive"  # Inactivo temporalmente
    CLOSED = "closed"  # Cerrado, no se pueden realizar más evaluaciones
    EXPIRED = "expired"  # Expirado por fecha
    
    @classmethod
    def get_display_name(cls, status: "PeriodStatus") -> str:
        """Retorna el nombre para mostrar del estado."""
        display_names = {
            cls.SCHEDULED: "Programado",
            cls.ACTIVE: "Activo",
            cls.INACTIVE: "Inactivo",
            cls.CLOSED: "Cerrado",
            cls.EXPIRED: "Expirado"
        }
        return display_names.get(status, status.value)
    
    @classmethod
    def get_description(cls, status: "PeriodStatus") -> str:
        """Retorna una descripción del estado."""
        descriptions = {
            cls.SCHEDULED: "El período está programado para iniciar en el futuro",
            cls.ACTIVE: "El período está activo y se pueden realizar evaluaciones",
            cls.INACTIVE: "El período está temporalmente inactivo",
            cls.CLOSED: "El período ha sido cerrado manualmente",
            cls.EXPIRED: "El período ha expirado por fecha"
        }
        return descriptions.get(status, "Estado desconocido")
    
    @classmethod
    def allows_evaluations(cls, status: "PeriodStatus") -> bool:
        """Verifica si el estado permite realizar evaluaciones."""
        return status == cls.ACTIVE
    
    @classmethod
    def can_be_modified(cls, status: "PeriodStatus") -> bool:
        """Verifica si el período puede ser modificado en este estado."""
        return status in [cls.SCHEDULED, cls.INACTIVE]
    
    @classmethod
    def is_final_state(cls, status: "PeriodStatus") -> bool:
        """Verifica si el estado es final (no se puede cambiar)."""
        return status in [cls.CLOSED, cls.EXPIRED]
