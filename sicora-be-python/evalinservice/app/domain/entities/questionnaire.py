"""Questionnaire entity for evaluation system."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from .question import Question
from ..exceptions.questionnaire_exceptions import (
    InvalidQuestionnaireNameError,
    QuestionNotFoundError,
    DuplicateQuestionError
)


@dataclass
class Questionnaire:
    """
    Entidad Questionnaire del dominio.
    Representa un cuestionario que agrupa preguntas para evaluar instructores.
    """
    id: UUID
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    question_ids: List[UUID] = field(default_factory=list)  # Referencias a preguntas

    @classmethod
    def create(
        cls,
        name: str,
        description: Optional[str] = None
    ) -> "Questionnaire":
        """
        Factory method para crear un nuevo cuestionario.
        Aplica todas las validaciones de dominio.
        """
        now = datetime.utcnow()
        
        # Validaciones de dominio
        if not name or len(name.strip()) < 3:
            raise InvalidQuestionnaireNameError("El nombre del cuestionario debe tener al menos 3 caracteres")
        
        if len(name.strip()) > 100:
            raise InvalidQuestionnaireNameError("El nombre del cuestionario no puede exceder 100 caracteres")
        
        if description and len(description.strip()) > 500:
            raise InvalidQuestionnaireNameError("La descripción no puede exceder 500 caracteres")
        
        return cls(
            id=uuid4(),
            name=name.strip(),
            description=description.strip() if description else None,
            is_active=True,
            created_at=now,
            updated_at=now,
            question_ids=[]
        )
    
    def update_name(self, new_name: str) -> None:
        """Actualiza el nombre del cuestionario con validación."""
        if not new_name or len(new_name.strip()) < 3:
            raise InvalidQuestionnaireNameError("El nombre del cuestionario debe tener al menos 3 caracteres")
        
        if len(new_name.strip()) > 100:
            raise InvalidQuestionnaireNameError("El nombre del cuestionario no puede exceder 100 caracteres")
        
        self.name = new_name.strip()
        self.updated_at = datetime.utcnow()
    
    def update_description(self, new_description: Optional[str]) -> None:
        """Actualiza la descripción del cuestionario."""
        if new_description and len(new_description.strip()) > 500:
            raise InvalidQuestionnaireNameError("La descripción no puede exceder 500 caracteres")
        
        self.description = new_description.strip() if new_description else None
        self.updated_at = datetime.utcnow()
    
    def add_question(self, question_id: UUID) -> None:
        """Agrega una pregunta al cuestionario."""
        if question_id in self.question_ids:
            raise DuplicateQuestionError(f"La pregunta {question_id} ya está en el cuestionario")
        
        self.question_ids.append(question_id)
        self.updated_at = datetime.utcnow()
    
    def remove_question(self, question_id: UUID) -> None:
        """Remueve una pregunta del cuestionario."""
        if question_id not in self.question_ids:
            raise QuestionNotFoundError(f"La pregunta {question_id} no está en el cuestionario")
        
        self.question_ids.remove(question_id)
        self.updated_at = datetime.utcnow()
    
    def reorder_questions(self, ordered_question_ids: List[UUID]) -> None:
        """Reordena las preguntas del cuestionario."""
        # Validar que todas las preguntas existan en el cuestionario
        for question_id in ordered_question_ids:
            if question_id not in self.question_ids:
                raise QuestionNotFoundError(f"La pregunta {question_id} no está en el cuestionario")
        
        # Validar que no falten preguntas
        if set(ordered_question_ids) != set(self.question_ids):
            raise ValueError("La lista de preguntas debe contener exactamente las mismas preguntas")
        
        self.question_ids = ordered_question_ids
        self.updated_at = datetime.utcnow()
    
    def get_question_count(self) -> int:
        """Retorna el número de preguntas en el cuestionario."""
        return len(self.question_ids)
    
    def has_questions(self) -> bool:
        """Verifica si el cuestionario tiene preguntas."""
        return len(self.question_ids) > 0
    
    def deactivate(self) -> None:
        """Desactiva el cuestionario."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activa el cuestionario."""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def clear_questions(self) -> None:
        """Remueve todas las preguntas del cuestionario."""
        self.question_ids.clear()
        self.updated_at = datetime.utcnow()
