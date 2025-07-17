"""
NotificationType - Value Object para representar los tipos de notificaciones

Este value object define los tipos de notificaciones soportados por el sistema.
"""

from enum import Enum, auto


class NotificationType(str, Enum):
    """
    Tipos de notificaciones soportados por el sistema.
    
    Hereda de str para facilitar la serialización/deserialización.
    """
    EMAIL = "email"
    PUSH = "push"
    IN_APP = "in_app"
    
    @classmethod
    def from_string(cls, value: str) -> "NotificationType":
        """
        Convierte un string a NotificationType.
        
        Args:
            value: String a convertir
            
        Returns:
            NotificationType correspondiente
            
        Raises:
            ValueError: Si el string no corresponde a un tipo válido
        """
        try:
            return cls(value.lower())
        except ValueError:
            valid_types = ", ".join([t.value for t in cls])
            raise ValueError(f"Tipo de notificación inválido. Valores válidos: {valid_types}")