"""Evaluation Period entity for evaluation system."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..value_objects.period_status import PeriodStatus
from ..exceptions.period_exceptions import (
    InvalidPeriodNameError,
    InvalidPeriodDatesError,
    PeriodOverlapError
)


@dataclass
class EvaluationPeriod:
    """
    Entidad EvaluationPeriod del dominio.
    Representa un período durante el cual se pueden realizar evaluaciones.
    """
    id: UUID
    name: str
    description: Optional[str]
    start_date: datetime
    end_date: datetime
    status: PeriodStatus
    questionnaire_id: Optional[UUID]  # Cuestionario asociado al período
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        name: str,
        start_date: datetime,
        end_date: datetime,
        description: Optional[str] = None,
        questionnaire_id: Optional[UUID] = None
    ) -> "EvaluationPeriod":
        """
        Factory method para crear un nuevo período de evaluación.
        Aplica todas las validaciones de dominio.
        """
        now = datetime.utcnow()
        
        # Validaciones de dominio
        if not name or len(name.strip()) < 3:
            raise InvalidPeriodNameError("El nombre del período debe tener al menos 3 caracteres")
        
        if len(name.strip()) > 100:
            raise InvalidPeriodNameError("El nombre del período no puede exceder 100 caracteres")
        
        if description and len(description.strip()) > 500:
            raise InvalidPeriodNameError("La descripción no puede exceder 500 caracteres")
        
        # Validar fechas
        if start_date >= end_date:
            raise InvalidPeriodDatesError("La fecha de inicio debe ser anterior a la fecha de fin")
        
        if end_date <= now:
            raise InvalidPeriodDatesError("La fecha de fin debe ser futura")
        
        # Determinar status inicial basado en fechas
        if start_date <= now <= end_date:
            initial_status = PeriodStatus.ACTIVE
        elif start_date > now:
            initial_status = PeriodStatus.SCHEDULED
        else:
            initial_status = PeriodStatus.EXPIRED
        
        return cls(
            id=uuid4(),
            name=name.strip(),
            description=description.strip() if description else None,
            start_date=start_date,
            end_date=end_date,
            status=initial_status,
            questionnaire_id=questionnaire_id,
            is_active=True,
            created_at=now,
            updated_at=now
        )
    
    def update_name(self, new_name: str) -> None:
        """Actualiza el nombre del período con validación."""
        if not new_name or len(new_name.strip()) < 3:
            raise InvalidPeriodNameError("El nombre del período debe tener al menos 3 caracteres")
        
        if len(new_name.strip()) > 100:
            raise InvalidPeriodNameError("El nombre del período no puede exceder 100 caracteres")
        
        self.name = new_name.strip()
        self.updated_at = datetime.utcnow()
    
    def update_description(self, new_description: Optional[str]) -> None:
        """Actualiza la descripción del período."""
        if new_description and len(new_description.strip()) > 500:
            raise InvalidPeriodNameError("La descripción no puede exceder 500 caracteres")
        
        self.description = new_description.strip() if new_description else None
        self.updated_at = datetime.utcnow()
    
    def update_dates(self, new_start_date: datetime, new_end_date: datetime) -> None:
        """Actualiza las fechas del período con validación."""
        if new_start_date >= new_end_date:
            raise InvalidPeriodDatesError("La fecha de inicio debe ser anterior a la fecha de fin")
        
        # No permitir cambiar fechas si el período ya está activo y tiene evaluaciones
        if self.status == PeriodStatus.ACTIVE:
            raise InvalidPeriodDatesError("No se pueden modificar las fechas de un período activo")
        
        self.start_date = new_start_date
        self.end_date = new_end_date
        self.updated_at = datetime.utcnow()
        
        # Actualizar status basado en las nuevas fechas
        self._update_status_by_dates()
    
    def assign_questionnaire(self, questionnaire_id: UUID) -> None:
        """Asigna un cuestionario al período."""
        self.questionnaire_id = questionnaire_id
        self.updated_at = datetime.utcnow()
    
    def remove_questionnaire(self) -> None:
        """Remueve el cuestionario asignado al período."""
        self.questionnaire_id = None
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activa el período de evaluación."""
        now = datetime.utcnow()
        
        # Validar que el período esté en fechas válidas
        if now < self.start_date:
            raise InvalidPeriodDatesError("No se puede activar un período antes de su fecha de inicio")
        
        if now > self.end_date:
            raise InvalidPeriodDatesError("No se puede activar un período después de su fecha de fin")
        
        self.status = PeriodStatus.ACTIVE
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Desactiva el período de evaluación."""
        self.status = PeriodStatus.INACTIVE
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def close(self) -> None:
        """Cierra el período de evaluación."""
        self.status = PeriodStatus.CLOSED
        self.updated_at = datetime.utcnow()
    
    def is_current(self) -> bool:
        """Verifica si el período está actualmente en vigor."""
        now = datetime.utcnow()
        return (
            self.status == PeriodStatus.ACTIVE and
            self.is_active and
            self.start_date <= now <= self.end_date
        )
    
    def is_upcoming(self) -> bool:
        """Verifica si el período está programado para el futuro."""
        now = datetime.utcnow()
        return self.status == PeriodStatus.SCHEDULED and now < self.start_date
    
    def is_expired(self) -> bool:
        """Verifica si el período ha expirado."""
        now = datetime.utcnow()
        return now > self.end_date or self.status == PeriodStatus.EXPIRED
    
    def get_remaining_days(self) -> int:
        """Retorna los días restantes del período (negativo si ya expiró)."""
        now = datetime.utcnow()
        if now > self.end_date:
            return -1
        return (self.end_date - now).days
    
    def get_duration_days(self) -> int:
        """Retorna la duración total del período en días."""
        return (self.end_date - self.start_date).days
    
    def _update_status_by_dates(self) -> None:
        """Actualiza el status basado en las fechas actuales."""
        now = datetime.utcnow()
        
        if now < self.start_date:
            self.status = PeriodStatus.SCHEDULED
        elif self.start_date <= now <= self.end_date:
            if self.is_active:
                self.status = PeriodStatus.ACTIVE
        else:
            self.status = PeriodStatus.EXPIRED
