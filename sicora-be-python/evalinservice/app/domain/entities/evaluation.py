"""Evaluation entity for evaluation system."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from ..value_objects.evaluation_status import EvaluationStatus
from ..exceptions.evaluation_exceptions import (
    InvalidEvaluationError,
    InvalidResponseError,
    EvaluationAlreadySubmittedError
)


@dataclass
class EvaluationResponse:
    """
    Value object que representa una respuesta individual a una pregunta.
    """
    question_id: UUID
    response_value: str  # Valor de la respuesta (escala 1-5, texto, etc.)
    comment: Optional[str] = None

    def __post_init__(self):
        """Validaciones post-inicialización."""
        if not self.response_value or not self.response_value.strip():
            raise InvalidResponseError("La respuesta no puede estar vacía")
        
        if self.comment and len(self.comment.strip()) > 1000:
            raise InvalidResponseError("El comentario no puede exceder 1000 caracteres")


@dataclass
class Evaluation:
    """
    Entidad Evaluation del dominio.
    Representa una evaluación completada por un aprendiz hacia un instructor.
    """
    id: UUID
    student_id: UUID  # ID del aprendiz que evalúa
    instructor_id: UUID  # ID del instructor evaluado
    period_id: UUID  # ID del período de evaluación
    questionnaire_id: UUID  # ID del cuestionario utilizado
    responses: List[EvaluationResponse]
    status: EvaluationStatus
    general_comment: Optional[str]
    submitted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        student_id: UUID,
        instructor_id: UUID,
        period_id: UUID,
        questionnaire_id: UUID
    ) -> "Evaluation":
        """
        Factory method para crear una nueva evaluación.
        Aplica todas las validaciones de dominio.
        """
        now = datetime.utcnow()
        
        # Validaciones de dominio
        if student_id == instructor_id:
            raise InvalidEvaluationError("Un usuario no puede evaluarse a sí mismo")
        
        return cls(
            id=uuid4(),
            student_id=student_id,
            instructor_id=instructor_id,
            period_id=period_id,
            questionnaire_id=questionnaire_id,
            responses=[],
            status=EvaluationStatus.DRAFT,
            general_comment=None,
            submitted_at=None,
            created_at=now,
            updated_at=now
        )
    
    def add_response(self, question_id: UUID, response_value: str, comment: Optional[str] = None) -> None:
        """Agrega o actualiza una respuesta a la evaluación."""
        if self.status == EvaluationStatus.SUBMITTED:
            raise EvaluationAlreadySubmittedError("No se pueden modificar evaluaciones ya enviadas")
        
        # Validar que la respuesta no esté vacía
        if not response_value or not response_value.strip():
            raise InvalidResponseError("La respuesta no puede estar vacía")
        
        # Buscar si ya existe una respuesta para esta pregunta
        existing_response = None
        for i, response in enumerate(self.responses):
            if response.question_id == question_id:
                existing_response = i
                break
        
        new_response = EvaluationResponse(
            question_id=question_id,
            response_value=response_value.strip(),
            comment=comment.strip() if comment else None
        )
        
        if existing_response is not None:
            # Actualizar respuesta existente
            self.responses[existing_response] = new_response
        else:
            # Agregar nueva respuesta
            self.responses.append(new_response)
        
        self.updated_at = datetime.utcnow()
    
    def remove_response(self, question_id: UUID) -> None:
        """Remueve una respuesta de la evaluación."""
        if self.status == EvaluationStatus.SUBMITTED:
            raise EvaluationAlreadySubmittedError("No se pueden modificar evaluaciones ya enviadas")
        
        self.responses = [r for r in self.responses if r.question_id != question_id]
        self.updated_at = datetime.utcnow()
    
    def set_general_comment(self, comment: str) -> None:
        """Establece el comentario general de la evaluación."""
        if self.status == EvaluationStatus.SUBMITTED:
            raise EvaluationAlreadySubmittedError("No se pueden modificar evaluaciones ya enviadas")
        
        if comment and len(comment.strip()) > 2000:
            raise InvalidResponseError("El comentario general no puede exceder 2000 caracteres")
        
        self.general_comment = comment.strip() if comment else None
        self.updated_at = datetime.utcnow()
    
    def submit(self, required_question_ids: List[UUID]) -> None:
        """
        Envía la evaluación para procesamiento.
        Valida que todas las preguntas requeridas hayan sido respondidas.
        """
        if self.status == EvaluationStatus.SUBMITTED:
            raise EvaluationAlreadySubmittedError("La evaluación ya ha sido enviada")
        
        # Validar que todas las preguntas requeridas tengan respuesta
        response_question_ids = {r.question_id for r in self.responses}
        missing_questions = set(required_question_ids) - response_question_ids
        
        if missing_questions:
            raise InvalidEvaluationError(
                f"Faltan respuestas para las preguntas requeridas: {missing_questions}"
            )
        
        # Validar que todas las respuestas tengan valor
        for response in self.responses:
            if not response.response_value or not response.response_value.strip():
                raise InvalidResponseError(f"La respuesta para la pregunta {response.question_id} está vacía")
        
        self.status = EvaluationStatus.SUBMITTED
        self.submitted_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def get_response_for_question(self, question_id: UUID) -> Optional[EvaluationResponse]:
        """Obtiene la respuesta para una pregunta específica."""
        for response in self.responses:
            if response.question_id == question_id:
                return response
        return None
    
    def get_response_count(self) -> int:
        """Retorna el número de respuestas en la evaluación."""
        return len(self.responses)
    
    def is_complete(self, required_question_ids: List[UUID]) -> bool:
        """Verifica si la evaluación está completa (todas las preguntas requeridas respondidas)."""
        response_question_ids = {r.question_id for r in self.responses}
        return set(required_question_ids).issubset(response_question_ids)
    
    def get_completion_percentage(self, total_questions: int) -> float:
        """Retorna el porcentaje de completitud de la evaluación."""
        if total_questions == 0:
            return 100.0
        return (len(self.responses) / total_questions) * 100.0
    
    def can_be_modified(self) -> bool:
        """Verifica si la evaluación puede ser modificada."""
        return self.status != EvaluationStatus.SUBMITTED
