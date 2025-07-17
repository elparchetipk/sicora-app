from datetime import date, datetime, timedelta
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc

from ...domain.entities import AttendanceAlert
from ...domain.repositories import AttendanceAlertRepository
from ...domain.value_objects import AlertLevel, AlertType
from ..models import AttendanceAlertModel, AlertLevelEnum, AlertTypeEnum


class SQLAlchemyAttendanceAlertRepository(AttendanceAlertRepository):
    """Implementación SQLAlchemy del repositorio de alertas de asistencia."""

    def __init__(self, session: Session):
        self.session = session

    async def save(self, alert: AttendanceAlert) -> AttendanceAlert:
        """Guarda una alerta."""
        # Buscar si ya existe el registro
        existing_model = self.session.query(AttendanceAlertModel).filter(
            AttendanceAlertModel.id == alert.id
        ).first()

        if existing_model:
            # Actualizar registro existente
            self._update_model_from_entity(existing_model, alert)
        else:
            # Crear nuevo registro
            model = self._create_model_from_entity(alert)
            self.session.add(model)

        self.session.flush()
        return alert

    async def get_by_id(self, alert_id: UUID) -> Optional[AttendanceAlert]:
        """Obtiene una alerta por ID."""
        model = self.session.query(AttendanceAlertModel).filter(
            AttendanceAlertModel.id == alert_id
        ).first()

        return self._create_entity_from_model(model) if model else None

    async def get_active_alerts(
        self,
        student_id: Optional[UUID] = None,
        ficha_id: Optional[UUID] = None,
        instructor_id: Optional[UUID] = None,
        level: Optional[AlertLevel] = None,
        alert_type: Optional[AlertType] = None
    ) -> List[AttendanceAlert]:
        """Obtiene alertas activas con filtros opcionales."""
        query = self.session.query(AttendanceAlertModel).filter(
            AttendanceAlertModel.is_active == True
        )

        if student_id:
            query = query.filter(AttendanceAlertModel.student_id == student_id)
        
        if ficha_id:
            query = query.filter(AttendanceAlertModel.ficha_id == ficha_id)
        
        if level:
            query = query.filter(
                AttendanceAlertModel.level == self._domain_level_to_enum(level)
            )
        
        if alert_type:
            query = query.filter(
                AttendanceAlertModel.alert_type == self._domain_type_to_enum(alert_type)
            )

        # Para filtrar por instructor, necesitaríamos información adicional
        # sobre qué fichas maneja el instructor. Por ahora se omite.

        models = query.order_by(
            AttendanceAlertModel.level,
            desc(AttendanceAlertModel.created_at)
        ).all()

        return [self._create_entity_from_model(model) for model in models]

    async def get_by_student(
        self,
        student_id: UUID,
        include_inactive: bool = False
    ) -> List[AttendanceAlert]:
        """Obtiene todas las alertas de un estudiante."""
        query = self.session.query(AttendanceAlertModel).filter(
            AttendanceAlertModel.student_id == student_id
        )

        if not include_inactive:
            query = query.filter(AttendanceAlertModel.is_active == True)

        models = query.order_by(desc(AttendanceAlertModel.created_at)).all()
        return [self._create_entity_from_model(model) for model in models]

    async def get_by_ficha(
        self,
        ficha_id: UUID,
        include_inactive: bool = False
    ) -> List[AttendanceAlert]:
        """Obtiene todas las alertas de una ficha."""
        query = self.session.query(AttendanceAlertModel).filter(
            AttendanceAlertModel.ficha_id == ficha_id
        )

        if not include_inactive:
            query = query.filter(AttendanceAlertModel.is_active == True)

        models = query.order_by(
            AttendanceAlertModel.level,
            desc(AttendanceAlertModel.created_at)
        ).all()

        return [self._create_entity_from_model(model) for model in models]

    async def get_critical_alerts(self) -> List[AttendanceAlert]:
        """Obtiene todas las alertas críticas activas."""
        models = self.session.query(AttendanceAlertModel).filter(
            and_(
                AttendanceAlertModel.is_active == True,
                AttendanceAlertModel.level == AlertLevelEnum.CRITICAL
            )
        ).order_by(AttendanceAlertModel.created_at).all()

        return [self._create_entity_from_model(model) for model in models]

    async def get_unacknowledged_alerts(
        self,
        instructor_id: Optional[UUID] = None,
        max_days: int = 7
    ) -> List[AttendanceAlert]:
        """Obtiene alertas sin reconocer que superen el tiempo límite."""
        cutoff_date = datetime.now() - timedelta(days=max_days)
        
        query = self.session.query(AttendanceAlertModel).filter(
            and_(
                AttendanceAlertModel.is_active == True,
                AttendanceAlertModel.acknowledged == False,
                AttendanceAlertModel.created_at <= cutoff_date
            )
        )

        # Para filtrar por instructor, necesitaríamos información adicional
        # sobre qué fichas maneja. Por ahora se omite.

        models = query.order_by(AttendanceAlertModel.created_at).all()
        return [self._create_entity_from_model(model) for model in models]

    async def get_alerts_by_type(
        self,
        alert_type: AlertType,
        include_inactive: bool = False
    ) -> List[AttendanceAlert]:
        """Obtiene alertas por tipo específico."""
        query = self.session.query(AttendanceAlertModel).filter(
            AttendanceAlertModel.alert_type == self._domain_type_to_enum(alert_type)
        )

        if not include_inactive:
            query = query.filter(AttendanceAlertModel.is_active == True)

        models = query.order_by(desc(AttendanceAlertModel.created_at)).all()
        return [self._create_entity_from_model(model) for model in models]

    async def deactivate_resolved_alerts(
        self,
        student_id: UUID,
        alert_type: AlertType
    ) -> int:
        """Desactiva alertas resueltas de un estudiante y tipo específico."""
        result = self.session.query(AttendanceAlertModel).filter(
            and_(
                AttendanceAlertModel.student_id == student_id,
                AttendanceAlertModel.alert_type == self._domain_type_to_enum(alert_type),
                AttendanceAlertModel.is_active == True
            )
        ).update({"is_active": False, "updated_at": datetime.now()})

        return result

    async def get_alert_statistics(
        self,
        start_date: date,
        end_date: date,
        ficha_id: Optional[UUID] = None
    ) -> dict:
        """Obtiene estadísticas de alertas en un período."""
        query = self.session.query(AttendanceAlertModel).filter(
            and_(
                func.date(AttendanceAlertModel.created_at) >= start_date,
                func.date(AttendanceAlertModel.created_at) <= end_date
            )
        )

        if ficha_id:
            query = query.filter(AttendanceAlertModel.ficha_id == ficha_id)

        alerts = query.all()

        # Calcular estadísticas
        total_alerts = len(alerts)
        by_level = {}
        by_type = {}
        resolved_count = 0

        for alert in alerts:
            # Contar por nivel
            level_key = alert.level.value
            by_level[level_key] = by_level.get(level_key, 0) + 1

            # Contar por tipo
            type_key = alert.alert_type.value
            by_type[type_key] = by_type.get(type_key, 0) + 1

            # Contar resueltas (reconocidas o inactivas)
            if alert.acknowledged or not alert.is_active:
                resolved_count += 1

        resolution_rate = (resolved_count / total_alerts * 100) if total_alerts > 0 else 0

        return {
            "total_alerts": total_alerts,
            "by_level": by_level,
            "by_type": by_type,
            "resolution_rate": resolution_rate,
            "resolved_count": resolved_count
        }

    async def exists_active_alert(
        self,
        student_id: UUID,
        alert_type: AlertType
    ) -> bool:
        """Verifica si existe una alerta activa del tipo especificado para un estudiante."""
        count = self.session.query(AttendanceAlertModel).filter(
            and_(
                AttendanceAlertModel.student_id == student_id,
                AttendanceAlertModel.alert_type == self._domain_type_to_enum(alert_type),
                AttendanceAlertModel.is_active == True
            )
        ).count()

        return count > 0

    async def delete(self, alert_id: UUID) -> bool:
        """Elimina una alerta."""
        result = self.session.query(AttendanceAlertModel).filter(
            AttendanceAlertModel.id == alert_id
        ).delete()
        
        return result > 0

    def _create_model_from_entity(self, entity: AttendanceAlert) -> AttendanceAlertModel:
        """Convierte una entidad de dominio a modelo SQLAlchemy."""
        return AttendanceAlertModel(
            id=entity.id,
            student_id=entity.student_id,
            ficha_id=entity.ficha_id,
            alert_type=self._domain_type_to_enum(entity.alert_type),
            level=self._domain_level_to_enum(entity.level),
            message=entity.message,
            data=entity.data,
            is_active=entity.is_active,
            acknowledged=entity.acknowledged,
            acknowledged_by=entity.acknowledged_by,
            acknowledged_at=entity.acknowledged_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def _update_model_from_entity(
        self, 
        model: AttendanceAlertModel, 
        entity: AttendanceAlert
    ) -> None:
        """Actualiza un modelo SQLAlchemy desde una entidad de dominio."""
        model.student_id = entity.student_id
        model.ficha_id = entity.ficha_id
        model.alert_type = self._domain_type_to_enum(entity.alert_type)
        model.level = self._domain_level_to_enum(entity.level)
        model.message = entity.message
        model.data = entity.data
        model.is_active = entity.is_active
        model.acknowledged = entity.acknowledged
        model.acknowledged_by = entity.acknowledged_by
        model.acknowledged_at = entity.acknowledged_at
        model.updated_at = entity.updated_at

    def _create_entity_from_model(self, model: AttendanceAlertModel) -> AttendanceAlert:
        """Convierte un modelo SQLAlchemy a entidad de dominio."""
        return AttendanceAlert(
            id=model.id,
            student_id=model.student_id,
            ficha_id=model.ficha_id,
            alert_type=self._enum_to_domain_type(model.alert_type),
            level=self._enum_to_domain_level(model.level),
            message=model.message,
            data=model.data,
            is_active=model.is_active,
            acknowledged=model.acknowledged,
            acknowledged_by=model.acknowledged_by,
            acknowledged_at=model.acknowledged_at,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _domain_level_to_enum(self, level: AlertLevel) -> AlertLevelEnum:
        """Convierte nivel del dominio a enum de SQLAlchemy."""
        mapping = {
            AlertLevel.LOW: AlertLevelEnum.LOW,
            AlertLevel.MEDIUM: AlertLevelEnum.MEDIUM,
            AlertLevel.HIGH: AlertLevelEnum.HIGH,
            AlertLevel.CRITICAL: AlertLevelEnum.CRITICAL,
        }
        return mapping[level]

    def _enum_to_domain_level(self, enum_level: AlertLevelEnum) -> AlertLevel:
        """Convierte enum de SQLAlchemy a nivel del dominio."""
        mapping = {
            AlertLevelEnum.LOW: AlertLevel.LOW,
            AlertLevelEnum.MEDIUM: AlertLevel.MEDIUM,
            AlertLevelEnum.HIGH: AlertLevel.HIGH,
            AlertLevelEnum.CRITICAL: AlertLevel.CRITICAL,
        }
        return mapping[enum_level]

    def _domain_type_to_enum(self, alert_type: AlertType) -> AlertTypeEnum:
        """Convierte tipo del dominio a enum de SQLAlchemy."""
        mapping = {
            AlertType.CONSECUTIVE_ABSENCES: AlertTypeEnum.CONSECUTIVE_ABSENCES,
            AlertType.LOW_ATTENDANCE: AlertTypeEnum.LOW_ATTENDANCE,
            AlertType.DESERTION_RISK: AlertTypeEnum.DESERTION_RISK,
            AlertType.PATTERN_ANOMALY: AlertTypeEnum.PATTERN_ANOMALY,
            AlertType.INSTRUCTOR_NO_RECORD: AlertTypeEnum.INSTRUCTOR_NO_RECORD,
        }
        return mapping[alert_type]

    def _enum_to_domain_type(self, enum_type: AlertTypeEnum) -> AlertType:
        """Convierte enum de SQLAlchemy a tipo del dominio."""
        mapping = {
            AlertTypeEnum.CONSECUTIVE_ABSENCES: AlertType.CONSECUTIVE_ABSENCES,
            AlertTypeEnum.LOW_ATTENDANCE: AlertType.LOW_ATTENDANCE,
            AlertTypeEnum.DESERTION_RISK: AlertType.DESERTION_RISK,
            AlertTypeEnum.PATTERN_ANOMALY: AlertType.PATTERN_ANOMALY,
            AlertTypeEnum.INSTRUCTOR_NO_RECORD: AlertType.INSTRUCTOR_NO_RECORD,
        }
        return mapping[enum_type]
