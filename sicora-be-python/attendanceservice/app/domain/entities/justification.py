from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..value_objects import JustificationStatus


@dataclass
class Justification:
    """
    Entidad de dominio que representa una justificación de inasistencia.
    
    Una justificación permite a un aprendiz documentar las razones de su ausencia
    mediante la subida de un archivo PDF. Los instructores pueden aprobar o rechazar
    estas justificaciones.
    """
    
    student_id: UUID
    attendance_record_id: UUID
    reason: str
    file_path: str
    id: UUID = field(default_factory=uuid4)
    status: JustificationStatus = field(default=JustificationStatus.PENDING)
    submitted_at: datetime = field(default_factory=datetime.now)
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[UUID] = None
    review_comments: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def approve(self, reviewed_by: UUID, comments: Optional[str] = None) -> None:
        """
        Aprueba la justificación.
        
        Args:
            reviewed_by: ID del instructor que aprueba
            comments: Comentarios opcionales del revisor
            
        Raises:
            ValueError: Si la justificación ya fue procesada
        """
        if self.status != JustificationStatus.PENDING:
            raise ValueError(f"Cannot approve justification with status {self.status.value}")
            
        self.status = JustificationStatus.APPROVED
        self.reviewed_at = datetime.now()
        self.reviewed_by = reviewed_by
        self.review_comments = comments
        self.updated_at = datetime.now()

    def reject(self, reviewed_by: UUID, comments: str) -> None:
        """
        Rechaza la justificación.
        
        Args:
            reviewed_by: ID del instructor que rechaza
            comments: Comentarios obligatorios explicando el rechazo
            
        Raises:
            ValueError: Si la justificación ya fue procesada o no se proporcionan comentarios
        """
        if self.status != JustificationStatus.PENDING:
            raise ValueError(f"Cannot reject justification with status {self.status.value}")
            
        if not comments or not comments.strip():
            raise ValueError("Comments are required when rejecting a justification")
            
        self.status = JustificationStatus.REJECTED
        self.reviewed_at = datetime.now()
        self.reviewed_by = reviewed_by
        self.review_comments = comments.strip()
        self.updated_at = datetime.now()

    def is_pending(self) -> bool:
        """Verifica si la justificación está pendiente de revisión."""
        return self.status == JustificationStatus.PENDING

    def is_approved(self) -> bool:
        """Verifica si la justificación fue aprobada."""
        return self.status == JustificationStatus.APPROVED

    def is_rejected(self) -> bool:
        """Verifica si la justificación fue rechazada."""
        return self.status == JustificationStatus.REJECTED

    def days_since_submission(self) -> int:
        """Calcula los días transcurridos desde la presentación."""
        return (datetime.now() - self.submitted_at).days

    def __eq__(self, other) -> bool:
        if not isinstance(other, Justification):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self) -> str:
        return f"Justification(id={self.id}, student_id={self.student_id}, status={self.status.value})"
