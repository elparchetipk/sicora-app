"""Evaluation Period repository implementation."""

from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ...domain.entities import EvaluationPeriod
from ...domain.repositories import EvaluationPeriodRepositoryInterface
from ...domain.value_objects import PeriodStatus
from ..models import EvaluationPeriodModel


class EvaluationPeriodRepository(EvaluationPeriodRepositoryInterface):
    """
    Implementación SQLAlchemy del repositorio de períodos de evaluación.
    
    Responsabilidades:
    - Mapear entre entidades de dominio y modelos de SQLAlchemy
    - Implementar operaciones CRUD para períodos de evaluación
    - Mantener la persistencia de datos
    """
    
    def __init__(self, db_session: Session):
        self._db = db_session
    
    async def create(self, period: EvaluationPeriod) -> EvaluationPeriod:
        """Crear nuevo período de evaluación."""
        db_period = EvaluationPeriodModel(
            id=period.id,
            name=period.name,
            description=period.description,
            start_date=period.start_date,
            end_date=period.end_date,
            status=period.status,
            questionnaire_id=period.questionnaire_id,
            target_groups=period.target_groups,
            is_anonymous=period.is_anonymous,
            created_at=period.created_at,
            updated_at=period.updated_at
        )
        
        self._db.add(db_period)
        self._db.commit()
        self._db.refresh(db_period)
        
        return self._to_entity(db_period)
    
    async def get_by_id(self, period_id: UUID) -> Optional[EvaluationPeriod]:
        """Obtener período por ID."""
        db_period = self._db.query(EvaluationPeriodModel).filter(
            EvaluationPeriodModel.id == period_id
        ).first()
        
        return self._to_entity(db_period) if db_period else None
    
    async def get_all(
        self,
        status: Optional[PeriodStatus] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[EvaluationPeriod]:
        """Obtener períodos con filtros."""
        query = self._db.query(EvaluationPeriodModel)
        
        if status is not None:
            query = query.filter(EvaluationPeriodModel.status == status)
        
        if start_date is not None:
            query = query.filter(EvaluationPeriodModel.start_date >= start_date)
        
        if end_date is not None:
            query = query.filter(EvaluationPeriodModel.end_date <= end_date)
        
        db_periods = query.offset(skip).limit(limit).all()
        
        return [self._to_entity(db_period) for db_period in db_periods]
    
    async def update(self, period: EvaluationPeriod) -> EvaluationPeriod:
        """Actualizar período existente."""
        db_period = self._db.query(EvaluationPeriodModel).filter(
            EvaluationPeriodModel.id == period.id
        ).first()
        
        if db_period:
            db_period.name = period.name
            db_period.description = period.description
            db_period.start_date = period.start_date
            db_period.end_date = period.end_date
            db_period.status = period.status
            db_period.questionnaire_id = period.questionnaire_id
            db_period.target_groups = period.target_groups
            db_period.is_anonymous = period.is_anonymous
            db_period.updated_at = period.updated_at
            
            self._db.commit()
            self._db.refresh(db_period)
        
        return self._to_entity(db_period)
    
    async def delete(self, period_id: UUID) -> bool:
        """Eliminar período."""
        db_period = self._db.query(EvaluationPeriodModel).filter(
            EvaluationPeriodModel.id == period_id
        ).first()
        
        if db_period:
            self._db.delete(db_period)
            self._db.commit()
            return True
        
        return False
    
    async def get_overlapping_periods(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[EvaluationPeriod]:
        """Obtener períodos que se solapan con las fechas dadas."""
        db_periods = self._db.query(EvaluationPeriodModel).filter(
            or_(
                and_(
                    EvaluationPeriodModel.start_date <= start_date,
                    EvaluationPeriodModel.end_date >= start_date
                ),
                and_(
                    EvaluationPeriodModel.start_date <= end_date,
                    EvaluationPeriodModel.end_date >= end_date
                ),
                and_(
                    EvaluationPeriodModel.start_date >= start_date,
                    EvaluationPeriodModel.end_date <= end_date
                )
            )
        ).all()
        
        return [self._to_entity(db_period) for db_period in db_periods]
    
    async def get_by_questionnaire_id(self, questionnaire_id: UUID) -> List[EvaluationPeriod]:
        """Obtener períodos que usan un cuestionario específico."""
        db_periods = self._db.query(EvaluationPeriodModel).filter(
            EvaluationPeriodModel.questionnaire_id == questionnaire_id
        ).all()
        
        return [self._to_entity(db_period) for db_period in db_periods]
    
    def _to_entity(self, db_period: EvaluationPeriodModel) -> EvaluationPeriod:
        """Convertir modelo SQLAlchemy a entidad de dominio."""
        if not db_period:
            return None
            
        return EvaluationPeriod(
            id=db_period.id,
            name=db_period.name,
            description=db_period.description,
            start_date=db_period.start_date,
            end_date=db_period.end_date,
            status=db_period.status,
            questionnaire_id=db_period.questionnaire_id,
            target_groups=db_period.target_groups or [],
            is_anonymous=db_period.is_anonymous,
            created_at=db_period.created_at,
            updated_at=db_period.updated_at
        )
