from datetime import date, datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc

from ...domain.entities import AttendanceRecord
from ...domain.repositories import AttendanceRecordRepository
from ...domain.value_objects import AttendanceStatus
from ..models import AttendanceRecordModel, AttendanceStatusEnum


class SQLAlchemyAttendanceRecordRepository(AttendanceRecordRepository):
    """Implementación SQLAlchemy del repositorio de registros de asistencia."""

    def __init__(self, session: Session):
        self.session = session

    async def save(self, attendance_record: AttendanceRecord) -> AttendanceRecord:
        """Guarda un registro de asistencia."""
        # Buscar si ya existe el registro
        existing_model = self.session.query(AttendanceRecordModel).filter(
            AttendanceRecordModel.id == attendance_record.id
        ).first()

        if existing_model:
            # Actualizar registro existente
            self._update_model_from_entity(existing_model, attendance_record)
        else:
            # Crear nuevo registro
            model = self._create_model_from_entity(attendance_record)
            self.session.add(model)

        self.session.flush()
        return attendance_record

    async def get_by_id(self, attendance_id: UUID) -> Optional[AttendanceRecord]:
        """Obtiene un registro de asistencia por ID."""
        model = self.session.query(AttendanceRecordModel).filter(
            AttendanceRecordModel.id == attendance_id
        ).first()

        return self._create_entity_from_model(model) if model else None

    async def get_by_student_and_date(
        self, 
        student_id: UUID, 
        date: date,
        block_identifier: str
    ) -> Optional[AttendanceRecord]:
        """Obtiene un registro de asistencia por estudiante, fecha y bloque."""
        model = self.session.query(AttendanceRecordModel).filter(
            and_(
                AttendanceRecordModel.student_id == student_id,
                func.date(AttendanceRecordModel.date) == date,
                AttendanceRecordModel.block_identifier == block_identifier
            )
        ).first()

        return self._create_entity_from_model(model) if model else None

    async def get_by_student_and_period(
        self,
        student_id: UUID,
        start_date: date,
        end_date: date
    ) -> List[AttendanceRecord]:
        """Obtiene registros de asistencia de un estudiante en un período."""
        models = self.session.query(AttendanceRecordModel).filter(
            and_(
                AttendanceRecordModel.student_id == student_id,
                func.date(AttendanceRecordModel.date) >= start_date,
                func.date(AttendanceRecordModel.date) <= end_date
            )
        ).order_by(desc(AttendanceRecordModel.date)).all()

        return [self._create_entity_from_model(model) for model in models]

    async def get_by_ficha_and_date(
        self,
        ficha_id: UUID,
        date: date
    ) -> List[AttendanceRecord]:
        """Obtiene todos los registros de asistencia de una ficha en una fecha."""
        # Nota: Esto requiere integración con UserService para obtener estudiantes de la ficha
        # Por ahora retornamos lista vacía y se implementará en la integración
        return []

    async def get_by_instructor_and_period(
        self,
        instructor_id: UUID,
        start_date: date,
        end_date: date
    ) -> List[AttendanceRecord]:
        """Obtiene registros de asistencia de un instructor en un período."""
        models = self.session.query(AttendanceRecordModel).filter(
            and_(
                AttendanceRecordModel.instructor_id == instructor_id,
                func.date(AttendanceRecordModel.date) >= start_date,
                func.date(AttendanceRecordModel.date) <= end_date
            )
        ).order_by(desc(AttendanceRecordModel.date)).all()

        return [self._create_entity_from_model(model) for model in models]

    async def get_consecutive_absences(
        self,
        student_id: UUID,
        ficha_id: UUID,
        end_date: date,
        max_days: int = 30
    ) -> int:
        """Calcula las inasistencias consecutivas de un estudiante."""
        # Obtener registros recientes del estudiante
        records = self.session.query(AttendanceRecordModel).filter(
            and_(
                AttendanceRecordModel.student_id == student_id,
                func.date(AttendanceRecordModel.date) <= end_date,
                func.date(AttendanceRecordModel.date) >= end_date - datetime.timedelta(days=max_days)
            )
        ).order_by(desc(AttendanceRecordModel.date)).all()

        # Contar inasistencias consecutivas desde la fecha más reciente
        consecutive_count = 0
        for record in records:
            if record.status == AttendanceStatusEnum.ABSENT:
                consecutive_count += 1
            else:
                break

        return consecutive_count

    async def get_attendance_percentage(
        self,
        student_id: UUID,
        start_date: date,
        end_date: date
    ) -> float:
        """Calcula el porcentaje de asistencia de un estudiante en un período."""
        total_records = self.session.query(AttendanceRecordModel).filter(
            and_(
                AttendanceRecordModel.student_id == student_id,
                func.date(AttendanceRecordModel.date) >= start_date,
                func.date(AttendanceRecordModel.date) <= end_date
            )
        ).count()

        if total_records == 0:
            return 0.0

        present_records = self.session.query(AttendanceRecordModel).filter(
            and_(
                AttendanceRecordModel.student_id == student_id,
                func.date(AttendanceRecordModel.date) >= start_date,
                func.date(AttendanceRecordModel.date) <= end_date,
                AttendanceRecordModel.status.in_([
                    AttendanceStatusEnum.PRESENT,
                    AttendanceStatusEnum.JUSTIFIED
                ])
            )
        ).count()

        return (present_records / total_records) * 100.0

    async def get_attendance_summary(
        self,
        student_id: Optional[UUID] = None,
        ficha_id: Optional[UUID] = None,
        instructor_id: Optional[UUID] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> dict:
        """Obtiene un resumen estadístico de asistencia con filtros opcionales."""
        query = self.session.query(AttendanceRecordModel)

        # Aplicar filtros
        if student_id:
            query = query.filter(AttendanceRecordModel.student_id == student_id)
        if instructor_id:
            query = query.filter(AttendanceRecordModel.instructor_id == instructor_id)
        if start_date:
            query = query.filter(func.date(AttendanceRecordModel.date) >= start_date)
        if end_date:
            query = query.filter(func.date(AttendanceRecordModel.date) <= end_date)

        records = query.all()

        # Calcular estadísticas
        total_sessions = len(records)
        present_count = sum(1 for r in records if r.status == AttendanceStatusEnum.PRESENT)
        absent_count = sum(1 for r in records if r.status == AttendanceStatusEnum.ABSENT)
        justified_count = sum(1 for r in records if r.status == AttendanceStatusEnum.JUSTIFIED)

        attendance_percentage = 0.0
        if total_sessions > 0:
            attendance_percentage = ((present_count + justified_count) / total_sessions) * 100.0

        return {
            "total_sessions": total_sessions,
            "present_count": present_count,
            "absent_count": absent_count,
            "justified_count": justified_count,
            "attendance_percentage": attendance_percentage,
            "detailed_records": records
        }

    async def delete(self, attendance_id: UUID) -> bool:
        """Elimina un registro de asistencia."""
        result = self.session.query(AttendanceRecordModel).filter(
            AttendanceRecordModel.id == attendance_id
        ).delete()
        
        return result > 0

    async def exists(
        self,
        student_id: UUID,
        date: date,
        block_identifier: str
    ) -> bool:
        """Verifica si existe un registro de asistencia."""
        count = self.session.query(AttendanceRecordModel).filter(
            and_(
                AttendanceRecordModel.student_id == student_id,
                func.date(AttendanceRecordModel.date) == date,
                AttendanceRecordModel.block_identifier == block_identifier
            )
        ).count()

        return count > 0

    def _create_model_from_entity(self, entity: AttendanceRecord) -> AttendanceRecordModel:
        """Convierte una entidad de dominio a modelo SQLAlchemy."""
        return AttendanceRecordModel(
            id=entity.id,
            student_id=entity.student_id,
            schedule_id=entity.schedule_id,
            instructor_id=entity.instructor_id,
            date=entity.date,
            block_identifier=entity.block_identifier,
            venue_id=entity.venue_id,
            status=self._domain_status_to_enum(entity.status),
            qr_code_used=entity.qr_code_used,
            notes=entity.notes,
            recorded_at=entity.recorded_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def _update_model_from_entity(
        self, 
        model: AttendanceRecordModel, 
        entity: AttendanceRecord
    ) -> None:
        """Actualiza un modelo SQLAlchemy desde una entidad de dominio."""
        model.student_id = entity.student_id
        model.schedule_id = entity.schedule_id
        model.instructor_id = entity.instructor_id
        model.date = entity.date
        model.block_identifier = entity.block_identifier
        model.venue_id = entity.venue_id
        model.status = self._domain_status_to_enum(entity.status)
        model.qr_code_used = entity.qr_code_used
        model.notes = entity.notes
        model.recorded_at = entity.recorded_at
        model.updated_at = entity.updated_at

    def _create_entity_from_model(self, model: AttendanceRecordModel) -> AttendanceRecord:
        """Convierte un modelo SQLAlchemy a entidad de dominio."""
        return AttendanceRecord(
            id=model.id,
            student_id=model.student_id,
            schedule_id=model.schedule_id,
            instructor_id=model.instructor_id,
            date=model.date,
            block_identifier=model.block_identifier,
            venue_id=model.venue_id,
            status=self._enum_to_domain_status(model.status),
            qr_code_used=model.qr_code_used,
            notes=model.notes,
            recorded_at=model.recorded_at,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _domain_status_to_enum(self, status: AttendanceStatus) -> AttendanceStatusEnum:
        """Convierte estado del dominio a enum de SQLAlchemy."""
        mapping = {
            AttendanceStatus.PRESENT: AttendanceStatusEnum.PRESENT,
            AttendanceStatus.ABSENT: AttendanceStatusEnum.ABSENT,
            AttendanceStatus.JUSTIFIED: AttendanceStatusEnum.JUSTIFIED,
            AttendanceStatus.LATE: AttendanceStatusEnum.LATE,
        }
        return mapping[status]

    def _enum_to_domain_status(self, enum_status: AttendanceStatusEnum) -> AttendanceStatus:
        """Convierte enum de SQLAlchemy a estado del dominio."""
        mapping = {
            AttendanceStatusEnum.PRESENT: AttendanceStatus.PRESENT,
            AttendanceStatusEnum.ABSENT: AttendanceStatus.ABSENT,
            AttendanceStatusEnum.JUSTIFIED: AttendanceStatus.JUSTIFIED,
            AttendanceStatusEnum.LATE: AttendanceStatus.LATE,
        }
        return mapping[enum_status]
