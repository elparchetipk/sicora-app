"""Question entity for evaluation system."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..value_objects.question_type import QuestionType
from ..exceptions.question_exceptions import (
    InvalidQuestionTextError,
    InvalidQuestionTypeError
)


@dataclass
class Question:
    """
    Entidad Question del dominio.
    Representa una pregunta de evaluación que puede ser utilizada en cuestionarios.
    """
    id: UUID
    text: str
    question_type: QuestionType
    category: str
    is_required: bool
    order_index: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    options: Optional[str] = None  # JSON string for multiple choice options

    @classmethod
    def create(
        cls,
        text: str,
        question_type: QuestionType,
        category: str,
        is_required: bool = True,
        order_index: int = 0,
        options: Optional[str] = None
    ) -> "Question":
        """
        Factory method para crear una nueva pregunta.
        Aplica todas las validaciones de dominio.
        """
        now = datetime.utcnow()
        
        # Validaciones de dominio
        if not text or len(text.strip()) < 10:
            raise InvalidQuestionTextError("El texto de la pregunta debe tener al menos 10 caracteres")
        
        if len(text.strip()) > 500:
            raise InvalidQuestionTextError("El texto de la pregunta no puede exceder 500 caracteres")
        
        if not isinstance(question_type, QuestionType):
            raise InvalidQuestionTypeError("El tipo de pregunta debe ser válido")
        
        # Para preguntas de opción múltiple, debe tener opciones
        if question_type == QuestionType.MULTIPLE_CHOICE and not options:
            raise InvalidQuestionTypeError("Las preguntas de opción múltiple deben tener opciones definidas")
        
        if not category or len(category.strip()) < 2:
            raise InvalidQuestionTextError("La categoría debe tener al menos 2 caracteres")
        
        return cls(
            id=uuid4(),
            text=text.strip(),
            question_type=question_type,
            category=category.strip(),
            is_required=is_required,
            order_index=order_index,
            is_active=True,
            options=options,
            created_at=now,
            updated_at=now
        )
    
    def update_text(self, new_text: str) -> None:
        """Actualiza el texto de la pregunta con validación."""
        if not new_text or len(new_text.strip()) < 10:
            raise InvalidQuestionTextError("El texto de la pregunta debe tener al menos 10 caracteres")
        
        if len(new_text.strip()) > 500:
            raise InvalidQuestionTextError("El texto de la pregunta no puede exceder 500 caracteres")
        
        self.text = new_text.strip()
        self.updated_at = datetime.utcnow()
    
    def update_category(self, new_category: str) -> None:
        """Actualiza la categoría de la pregunta."""
        if not new_category or len(new_category.strip()) < 2:
            raise InvalidQuestionTextError("La categoría debe tener al menos 2 caracteres")
        
        self.category = new_category.strip()
        self.updated_at = datetime.utcnow()
    
    def set_options(self, options: str) -> None:
        """Establece las opciones para preguntas de opción múltiple."""
        if self.question_type == QuestionType.MULTIPLE_CHOICE and not options:
            raise InvalidQuestionTypeError("Las preguntas de opción múltiple deben tener opciones definidas")
        
        self.options = options
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Desactiva la pregunta."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activa la pregunta."""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def set_order(self, new_order: int) -> None:
        """Establece el orden de la pregunta."""
        if new_order < 0:
            raise ValueError("El orden no puede ser negativo")
        
        self.order_index = new_order
        self.updated_at = datetime.utcnow()
    
    def toggle_required(self) -> None:
        """Cambia el estado requerido de la pregunta."""
        self.is_required = not self.is_required
        self.updated_at = datetime.utcnow()
