"""Question type value object."""

from enum import Enum


class QuestionType(Enum):
    """
    Value object que define los tipos de pregunta disponibles.
    """
    SCALE_1_5 = "scale_1_5"  # Escala del 1 al 5
    SCALE_1_10 = "scale_1_10"  # Escala del 1 al 10
    YES_NO = "yes_no"  # Sí/No
    MULTIPLE_CHOICE = "multiple_choice"  # Opción múltiple
    TEXT = "text"  # Texto libre
    RATING = "rating"  # Rating con estrellas
    
    @classmethod
    def get_display_name(cls, question_type: "QuestionType") -> str:
        """Retorna el nombre para mostrar del tipo de pregunta."""
        display_names = {
            cls.SCALE_1_5: "Escala 1-5",
            cls.SCALE_1_10: "Escala 1-10",
            cls.YES_NO: "Sí/No",
            cls.MULTIPLE_CHOICE: "Opción múltiple",
            cls.TEXT: "Texto libre",
            cls.RATING: "Calificación con estrellas"
        }
        return display_names.get(question_type, question_type.value)
    
    @classmethod
    def get_valid_response_values(cls, question_type: "QuestionType") -> list:
        """Retorna los valores válidos de respuesta para cada tipo de pregunta."""
        valid_values = {
            cls.SCALE_1_5: ["1", "2", "3", "4", "5"],
            cls.SCALE_1_10: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            cls.YES_NO: ["yes", "no"],
            cls.RATING: ["1", "2", "3", "4", "5"],
            cls.MULTIPLE_CHOICE: [],  # Depende de las opciones específicas
            cls.TEXT: []  # Cualquier texto
        }
        return valid_values.get(question_type, [])
    
    @classmethod
    def requires_options(cls, question_type: "QuestionType") -> bool:
        """Verifica si el tipo de pregunta requiere opciones predefinidas."""
        return question_type == cls.MULTIPLE_CHOICE
    
    @classmethod
    def allows_comments(cls, question_type: "QuestionType") -> bool:
        """Verifica si el tipo de pregunta permite comentarios adicionales."""
        # Todos los tipos excepto TEXT permiten comentarios adicionales
        return question_type != cls.TEXT
