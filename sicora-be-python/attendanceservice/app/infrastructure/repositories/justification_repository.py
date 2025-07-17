from datetime import date, datetime, timedelta
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc

from ...domain.entities import Justification
from ...domain.repositories import JustificationRepository
from ...domain.value_objects import JustificationStatus
from ..models import JustificationModel, JustificationStatusEnum


class SQLAlchemyJustificationRepository(JustificationRepository):
    """Implementación SQLAlchemy del repositorio de justificaciones."""

    def __init__(self, session: Session):
        self.session = session

    async def save(self, justification: Justification) -> Justification:
        """Guarda una justificación."""
        # Buscar si ya existe el registro
        existing_model = self.session.query(JustificationModel).filter(
            JustificationModel.id == justification.id
        ).first()

        if existing_model:
            # Actualizar registro existente
            self._update_model_from_entity(existing_model, justification)
        else:
            # Crear nuevo registro
            model = self._create_model_from_entity(justification)
            self.session.add(model)

        self.session.flush()
        return justification

    async def get_by_id(self, justification_id: UUID) -> Optional[Justification]:
        """Obtiene una justificación por ID."""
        model = self.session.query(JustificationModel).filter(
            JustificationModel.id == justification_id
        ).first()

        return self._create_entity_from_model(model) if model else None

    async def get_by_student(self, student_id: UUID) -> List[Justification]:
        """Obtiene todas las justificaciones de un estudiante."""
        models = self.session.query(JustificationModel).filter(
            JustificationModel.student_id == student_id
        ).order_by(desc(JustificationModel.submitted_at)).all()

        return [self._create_entity_from_model(model) for model in models]

    async def get_by_attendance_record(
        self, 
        attendance_record_id: UUID
    ) -> Optional[Justification]:
        """Obtiene una justificación por registro de asistencia."""
        model = self.session.query(JustificationModel).filter(
            JustificationModel.attendance_record_id == attendance_record_id
        ).first()

        return self._create_entity_from_model(model) if model else None

    async def get_pending_for_instructor(
        self,
        instructor_id: UUID
    ) -> List[Justification]:
        """Obtiene justificaciones pendientes que puede revisar un instructor."""
        # Nota: Esta implementación requiere join con attendance_records
        # para filtrar por instructor_id. Por simplicidad, por ahora retornamos
        # todas las pendientes y el filtrado se hará en el caso de uso
        models = self.session.query(JustificationModel).filter(
            JustificationModel.status == JustificationStatusEnum.PENDING
        ).order_by(JustificationModel.submitted_at).all()

        return [self._create_entity_from_model(model) for model in models]

    async def get_by_status(
        self,
        status: JustificationStatus,
        student_id: Optional[UUID] = None,
        instructor_id: Optional[UUID] = None
    ) -> List[Justification]:
        """Obtiene justificaciones por estado con filtros opcionales."""
        query = self.session.query(JustificationModel).filter(
            JustificationModel.status == self._domain_status_to_enum(status)
        )

        if student_id:
            query = query.filter(JustificationModel.student_id == student_id)

        # Para filtrar por instructor, necesitaríamos hacer join con attendance_records
        # Por ahora omitimos este filtro y se aplicará en el caso de uso

        models = query.order_by(desc(JustificationModel.submitted_at)).all()
        return [self._create_entity_from_model(model) for model in models]

    async def get_overdue_justifications(
        self,
        days_threshold: int = 7
    ) -> List[Justification]:
        """Obtiene justificaciones que llevan mucho tiempo pendientes."""
        cutoff_date = datetime.now() - timedelta(days=days_threshold)
        
        models = self.session.query(JustificationModel).filter(
            and_(
                JustificationModel.status == JustificationStatusEnum.PENDING,
                JustificationModel.submitted_at <= cutoff_date
            )
        ).order_by(JustificationModel.submitted_at).all()

        return [self._create_entity_from_model(model) for model in models]

    async def count_by_student_and_period(
        self,
        student_id: UUID,
        start_date: date,
        end_date: date,
        status: Optional[JustificationStatus] = None
    ) -> int:
        """Cuenta las justificaciones de un estudiante en un período."""
        query = self.session.query(JustificationModel).filter(
            and_(
                JustificationModel.student_id == student_id,
                func.date(JustificationModel.submitted_at) >= start_date,
                func.date(JustificationModel.submitted_at) <= end_date
            )
        )

        if status:
            query = query.filter(
                JustificationModel.status == self._domain_status_to_enum(status)
            )

        return query.count()

    async def delete(self, justification_id: UUID) -> bool:
        """Elimina una justificación."""
        result = self.session.query(JustificationModel).filter(
            JustificationModel.id == justification_id
        ).delete()
        
        return result > 0

    async def exists_for_attendance(
        self,
        attendance_record_id: UUID
    ) -> bool:
        """Verifica si existe una justificación para un registro de asistencia."""
        count = self.session.query(JustificationModel).filter(
            JustificationModel.attendance_record_id == attendance_record_id
        ).count()

        return count > 0

    def _create_model_from_entity(self, entity: Justification) -> JustificationModel:
        """Convierte una entidad de dominio a modelo SQLAlchemy."""
        return JustificationModel(
            id=entity.id,
            student_id=entity.student_id,
            attendance_record_id=entity.attendance_record_id,
            reason=entity.reason,
            file_path=entity.file_path,
            status=self._domain_status_to_enum(entity.status),
            submitted_at=entity.submitted_at,
            reviewed_at=entity.reviewed_at,
            reviewed_by=entity.reviewed_by,
            review_comments=entity.review_comments,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def _update_model_from_entity(
        self, 
        model: JustificationModel, 
        entity: Justification
    ) -> None:
        """Actualiza un modelo SQLAlchemy desde una entidad de dominio."""
        model.student_id = entity.student_id
        model.attendance_record_id = entity.attendance_record_id
        model.reason = entity.reason
        model.file_path = entity.file_path
        model.status = self._domain_status_to_enum(entity.status)
        model.submitted_at = entity.submitted_at
        model.reviewed_at = entity.reviewed_at
        model.reviewed_by = entity.reviewed_by
        model.review_comments = entity.review_comments
        model.updated_at = entity.updated_at

    def _create_entity_from_model(self, model: JustificationModel) -> Justification:
        """Convierte un modelo SQLAlchemy a entidad de dominio."""
        return Justification(
            id=model.id,
            student_id=model.student_id,
            attendance_record_id=model.attendance_record_id,
            reason=model.reason,
            file_path=model.file_path,
            status=self._enum_to_domain_status(model.status),
            submitted_at=model.submitted_at,
            reviewed_at=model.reviewed_at,
            reviewed_by=model.reviewed_by,
            review_comments=model.review_comments,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _domain_status_to_enum(self, status: JustificationStatus) -> JustificationStatusEnum:
        """Convierte estado del dominio a enum de SQLAlchemy."""
        mapping = {
            JustificationStatus.PENDING: JustificationStatusEnum.PENDING,
            JustificationStatus.APPROVED: JustificationStatusEnum.APPROVED,
            JustificationStatus.REJECTED: JustificationStatusEnum.REJECTED,
        }
        return mapping[status]

    def _enum_to_domain_status(self, enum_status: JustificationStatusEnum) -> JustificationStatus:
        """Convierte enum de SQLAlchemy a estado del dominio."""
        mapping = {
            JustificationStatusEnum.PENDING: JustificationStatus.PENDING,
            JustificationStatusEnum.APPROVED: JustificationStatus.APPROVED,
            JustificationStatusEnum.REJECTED: JustificationStatus.REJECTED,
        }
        return mapping[enum_status]
