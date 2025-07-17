"""Questionnaire repository implementation."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from ...domain.entities import Questionnaire
from ...domain.repositories import QuestionnaireRepositoryInterface
from ..models import QuestionnaireModel


class QuestionnaireRepository(QuestionnaireRepositoryInterface):
    """
    Implementación SQLAlchemy del repositorio de cuestionarios.
    
    Responsabilidades:
    - Mapear entre entidades de dominio y modelos de SQLAlchemy
    - Implementar operaciones CRUD para cuestionarios
    - Mantener la persistencia de datos
    """
    
    def __init__(self, db_session: Session):
        self._db = db_session
    
    async def create(self, questionnaire: Questionnaire) -> Questionnaire:
        """Crear nuevo cuestionario."""
        db_questionnaire = QuestionnaireModel(
            id=questionnaire.id,
            name=questionnaire.name,
            description=questionnaire.description,
            is_active=questionnaire.is_active,
            question_ids=questionnaire.question_ids,
            created_at=questionnaire.created_at,
            updated_at=questionnaire.updated_at
        )
        
        self._db.add(db_questionnaire)
        self._db.commit()
        self._db.refresh(db_questionnaire)
        
        return self._to_entity(db_questionnaire)
    
    async def get_by_id(self, questionnaire_id: UUID) -> Optional[Questionnaire]:
        """Obtener cuestionario por ID."""
        db_questionnaire = self._db.query(QuestionnaireModel).filter(
            QuestionnaireModel.id == questionnaire_id
        ).first()
        
        return self._to_entity(db_questionnaire) if db_questionnaire else None
    
    async def get_all(
        self,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Questionnaire]:
        """Obtener cuestionarios con filtros."""
        query = self._db.query(QuestionnaireModel)
        
        if is_active is not None:
            query = query.filter(QuestionnaireModel.is_active == is_active)
        
        db_questionnaires = query.offset(skip).limit(limit).all()
        
        return [self._to_entity(db_questionnaire) for db_questionnaire in db_questionnaires]
    
    async def update(self, questionnaire: Questionnaire) -> Questionnaire:
        """Actualizar cuestionario existente."""
        db_questionnaire = self._db.query(QuestionnaireModel).filter(
            QuestionnaireModel.id == questionnaire.id
        ).first()
        
        if db_questionnaire:
            db_questionnaire.name = questionnaire.name
            db_questionnaire.description = questionnaire.description
            db_questionnaire.is_active = questionnaire.is_active
            db_questionnaire.question_ids = questionnaire.question_ids
            db_questionnaire.updated_at = questionnaire.updated_at
            
            self._db.commit()
            self._db.refresh(db_questionnaire)
        
        return self._to_entity(db_questionnaire)
    
    async def delete(self, questionnaire_id: UUID) -> bool:
        """Eliminar cuestionario."""
        db_questionnaire = self._db.query(QuestionnaireModel).filter(
            QuestionnaireModel.id == questionnaire_id
        ).first()
        
        if db_questionnaire:
            self._db.delete(db_questionnaire)
            self._db.commit()
            return True
        
        return False
    
    async def exists_by_name(self, name: str) -> bool:
        """Verificar si existe un cuestionario con el nombre dado."""
        return self._db.query(QuestionnaireModel).filter(
            QuestionnaireModel.name == name
        ).first() is not None
    
    def _to_entity(self, db_questionnaire: QuestionnaireModel) -> Questionnaire:
        """Convertir modelo SQLAlchemy a entidad de dominio."""
        if not db_questionnaire:
            return None
            
        return Questionnaire(
            id=db_questionnaire.id,
            name=db_questionnaire.name,
            description=db_questionnaire.description,
            is_active=db_questionnaire.is_active,
            question_ids=db_questionnaire.question_ids or [],
            created_at=db_questionnaire.created_at,
            updated_at=db_questionnaire.updated_at
        )
