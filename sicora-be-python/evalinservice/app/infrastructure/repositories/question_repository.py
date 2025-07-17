"""Question repository implementation."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ...domain.entities import Question
from ...domain.repositories import QuestionRepositoryInterface
from ...domain.value_objects import QuestionType
from ..models import QuestionModel


class QuestionRepository(QuestionRepositoryInterface):
    """
    Implementación SQLAlchemy del repositorio de preguntas.
    
    Responsabilidades:
    - Mapear entre entidades de dominio y modelos de SQLAlchemy
    - Implementar operaciones CRUD para preguntas
    - Mantener la persistencia de datos
    """
    
    def __init__(self, db_session: Session):
        self._db = db_session
    
    async def create(self, question: Question) -> Question:
        """Crear nueva pregunta."""
        db_question = QuestionModel(
            id=question.id,
            text=question.text,
            question_type=question.question_type,
            category=question.category,
            is_active=question.is_active,
            created_at=question.created_at,
            updated_at=question.updated_at
        )
        
        self._db.add(db_question)
        self._db.commit()
        self._db.refresh(db_question)
        
        return self._to_entity(db_question)
    
    async def get_by_id(self, question_id: UUID) -> Optional[Question]:
        """Obtener pregunta por ID."""
        db_question = self._db.query(QuestionModel).filter(
            QuestionModel.id == question_id
        ).first()
        
        return self._to_entity(db_question) if db_question else None
    
    async def get_all(
        self, 
        question_type: Optional[QuestionType] = None,
        category: Optional[str] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Question]:
        """Obtener preguntas con filtros."""
        query = self._db.query(QuestionModel)
        
        if question_type is not None:
            query = query.filter(QuestionModel.question_type == question_type)
        
        if category is not None:
            query = query.filter(QuestionModel.category == category)
        
        if is_active is not None:
            query = query.filter(QuestionModel.is_active == is_active)
        
        db_questions = query.offset(skip).limit(limit).all()
        
        return [self._to_entity(db_question) for db_question in db_questions]
    
    async def update(self, question: Question) -> Question:
        """Actualizar pregunta existente."""
        db_question = self._db.query(QuestionModel).filter(
            QuestionModel.id == question.id
        ).first()
        
        if db_question:
            db_question.text = question.text
            db_question.question_type = question.question_type
            db_question.category = question.category
            db_question.is_active = question.is_active
            db_question.updated_at = question.updated_at
            
            self._db.commit()
            self._db.refresh(db_question)
        
        return self._to_entity(db_question)
    
    async def delete(self, question_id: UUID) -> bool:
        """Eliminar pregunta."""
        db_question = self._db.query(QuestionModel).filter(
            QuestionModel.id == question_id
        ).first()
        
        if db_question:
            self._db.delete(db_question)
            self._db.commit()
            return True
        
        return False
    
    async def get_by_questionnaire_id(self, questionnaire_id: UUID) -> List[Question]:
        """Obtener preguntas de un cuestionario específico."""
        # Esta implementación requiere acceso al QuestionnaireModel
        # Se implementará cuando se tenga la referencia completa
        # Por ahora, retornamos lista vacía
        return []
    
    async def bulk_create(self, questions: List[Question]) -> List[Question]:
        """Crear múltiples preguntas."""
        db_questions = []
        
        for question in questions:
            db_question = QuestionModel(
                id=question.id,
                text=question.text,
                question_type=question.question_type,
                category=question.category,
                is_active=question.is_active,
                created_at=question.created_at,
                updated_at=question.updated_at
            )
            db_questions.append(db_question)
        
        self._db.add_all(db_questions)
        self._db.commit()
        
        for db_question in db_questions:
            self._db.refresh(db_question)
        
        return [self._to_entity(db_question) for db_question in db_questions]
    
    def _to_entity(self, db_question: QuestionModel) -> Question:
        """Convertir modelo SQLAlchemy a entidad de dominio."""
        if not db_question:
            return None
            
        return Question(
            id=db_question.id,
            text=db_question.text,
            question_type=db_question.question_type,
            category=db_question.category,
            is_active=db_question.is_active,
            created_at=db_question.created_at,
            updated_at=db_question.updated_at
        )
