"""Evaluation repository implementation."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from ...domain.entities import Evaluation
from ...domain.repositories import EvaluationRepositoryInterface
from ...domain.value_objects import EvaluationStatus
from ..models import EvaluationModel


class EvaluationRepository(EvaluationRepositoryInterface):
    """
    Implementación SQLAlchemy del repositorio de evaluaciones.
    
    Responsabilidades:
    - Mapear entre entidades de dominio y modelos de SQLAlchemy
    - Implementar operaciones CRUD para evaluaciones
    - Mantener la persistencia de datos
    """
    
    def __init__(self, db_session: Session):
        self._db = db_session
    
    async def create(self, evaluation: Evaluation) -> Evaluation:
        """Crear nueva evaluación."""
        # Convertir responses a formato JSON para SQLAlchemy
        responses_json = [
            {
                "question_id": str(resp.question_id),
                "score": resp.score
            }
            for resp in evaluation.responses
        ]
        
        db_evaluation = EvaluationModel(
            id=evaluation.id,
            student_id=evaluation.student_id,
            instructor_id=evaluation.instructor_id,
            evaluation_period_id=evaluation.evaluation_period_id,
            status=evaluation.status,
            responses=responses_json,
            comments=evaluation.comments,
            submitted_at=evaluation.submitted_at,
            created_at=evaluation.created_at,
            updated_at=evaluation.updated_at
        )
        
        self._db.add(db_evaluation)
        self._db.commit()
        self._db.refresh(db_evaluation)
        
        return self._to_entity(db_evaluation)
    
    async def get_by_id(self, evaluation_id: UUID) -> Optional[Evaluation]:
        """Obtener evaluación por ID."""
        db_evaluation = self._db.query(EvaluationModel).filter(
            EvaluationModel.id == evaluation_id
        ).first()
        
        return self._to_entity(db_evaluation) if db_evaluation else None
    
    async def get_all(
        self,
        evaluation_period_id: Optional[UUID] = None,
        instructor_id: Optional[UUID] = None,
        student_id: Optional[UUID] = None,
        status: Optional[EvaluationStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Evaluation]:
        """Obtener evaluaciones con filtros."""
        query = self._db.query(EvaluationModel)
        
        if evaluation_period_id is not None:
            query = query.filter(EvaluationModel.evaluation_period_id == evaluation_period_id)
        
        if instructor_id is not None:
            query = query.filter(EvaluationModel.instructor_id == instructor_id)
        
        if student_id is not None:
            query = query.filter(EvaluationModel.student_id == student_id)
        
        if status is not None:
            query = query.filter(EvaluationModel.status == status)
        
        db_evaluations = query.offset(skip).limit(limit).all()
        
        return [self._to_entity(db_evaluation) for db_evaluation in db_evaluations]
    
    async def update(self, evaluation: Evaluation) -> Evaluation:
        """Actualizar evaluación existente."""
        db_evaluation = self._db.query(EvaluationModel).filter(
            EvaluationModel.id == evaluation.id
        ).first()
        
        if db_evaluation:
            # Convertir responses a formato JSON
            responses_json = [
                {
                    "question_id": str(resp.question_id),
                    "score": resp.score
                }
                for resp in evaluation.responses
            ]
            
            db_evaluation.status = evaluation.status
            db_evaluation.responses = responses_json
            db_evaluation.comments = evaluation.comments
            db_evaluation.submitted_at = evaluation.submitted_at
            db_evaluation.updated_at = evaluation.updated_at
            
            self._db.commit()
            self._db.refresh(db_evaluation)
        
        return self._to_entity(db_evaluation)
    
    async def delete(self, evaluation_id: UUID) -> bool:
        """Eliminar evaluación."""
        db_evaluation = self._db.query(EvaluationModel).filter(
            EvaluationModel.id == evaluation_id
        ).first()
        
        if db_evaluation:
            self._db.delete(db_evaluation)
            self._db.commit()
            return True
        
        return False
    
    async def get_by_period_and_student(
        self, 
        evaluation_period_id: UUID, 
        student_id: UUID
    ) -> Optional[Evaluation]:
        """Obtener evaluación específica de un estudiante en un período."""
        db_evaluation = self._db.query(EvaluationModel).filter(
            EvaluationModel.evaluation_period_id == evaluation_period_id,
            EvaluationModel.student_id == student_id
        ).first()
        
        return self._to_entity(db_evaluation) if db_evaluation else None
    
    async def get_by_instructor_and_period(
        self, 
        instructor_id: UUID, 
        evaluation_period_id: UUID
    ) -> List[Evaluation]:
        """Obtener todas las evaluaciones de un instructor en un período."""
        db_evaluations = self._db.query(EvaluationModel).filter(
            EvaluationModel.instructor_id == instructor_id,
            EvaluationModel.evaluation_period_id == evaluation_period_id
        ).all()
        
        return [self._to_entity(db_evaluation) for db_evaluation in db_evaluations]
    
    async def get_by_period(self, evaluation_period_id: UUID) -> List[Evaluation]:
        """Obtener todas las evaluaciones de un período."""
        db_evaluations = self._db.query(EvaluationModel).filter(
            EvaluationModel.evaluation_period_id == evaluation_period_id
        ).all()
        
        return [self._to_entity(db_evaluation) for db_evaluation in db_evaluations]
    
    def _to_entity(self, db_evaluation: EvaluationModel) -> Evaluation:
        """Convertir modelo SQLAlchemy a entidad de dominio."""
        if not db_evaluation:
            return None
        
        # Convertir responses de JSON a objetos de dominio
        from ...domain.entities.evaluation import QuestionResponse
        
        responses = []
        if db_evaluation.responses:
            for resp_data in db_evaluation.responses:
                responses.append(QuestionResponse(
                    question_id=UUID(resp_data["question_id"]),
                    score=resp_data["score"]
                ))
        
        return Evaluation(
            id=db_evaluation.id,
            student_id=db_evaluation.student_id,
            instructor_id=db_evaluation.instructor_id,
            evaluation_period_id=db_evaluation.evaluation_period_id,
            status=db_evaluation.status,
            responses=responses,
            comments=db_evaluation.comments,
            submitted_at=db_evaluation.submitted_at,
            created_at=db_evaluation.created_at,
            updated_at=db_evaluation.updated_at
        )
