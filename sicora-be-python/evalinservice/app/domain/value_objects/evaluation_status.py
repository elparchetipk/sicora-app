"""Evaluation status value object."""

from enum import Enum


class EvaluationStatus(Enum):
    """
    Value object que define los estados posibles de una evaluación.
    """
    DRAFT = "draft"  # Borrador, en proceso de creación
    SUBMITTED = "submitted"  # Enviada para procesamiento
    PROCESSED = "processed"  # Procesada y agregada a estadísticas
    ARCHIVED = "archived"  # Archivada
    
    @classmethod
    def get_display_name(cls, status: "EvaluationStatus") -> str:
        """Retorna el nombre para mostrar del estado."""
        display_names = {
            cls.DRAFT: "Borrador",
            cls.SUBMITTED: "Enviada",
            cls.PROCESSED: "Procesada",
            cls.ARCHIVED: "Archivada"
        }
        return display_names.get(status, status.value)
    
    @classmethod
    def get_description(cls, status: "EvaluationStatus") -> str:
        """Retorna una descripción del estado."""
        descriptions = {
            cls.DRAFT: "La evaluación está en proceso de creación",
            cls.SUBMITTED: "La evaluación ha sido enviada para procesamiento",
            cls.PROCESSED: "La evaluación ha sido procesada y agregada a las estadísticas",
            cls.ARCHIVED: "La evaluación ha sido archivada"
        }
        return descriptions.get(status, "Estado desconocido")
    
    @classmethod
    def can_be_modified(cls, status: "EvaluationStatus") -> bool:
        """Verifica si la evaluación puede ser modificada en este estado."""
        return status == cls.DRAFT
    
    @classmethod
    def is_complete(cls, status: "EvaluationStatus") -> bool:
        """Verifica si la evaluación está completa."""
        return status in [cls.SUBMITTED, cls.PROCESSED, cls.ARCHIVED]
    
    @classmethod
    def is_counted_in_statistics(cls, status: "EvaluationStatus") -> bool:
        """Verifica si la evaluación debe ser contada en estadísticas."""
        return status in [cls.SUBMITTED, cls.PROCESSED]
