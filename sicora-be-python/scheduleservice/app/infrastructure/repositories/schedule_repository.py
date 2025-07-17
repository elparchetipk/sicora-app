"""SQLAlchemy implementation of the Schedule Repository."""

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, exists

from ...domain.entities.schedule_entity import Schedule
from ...domain.repositories.schedule_repository_interface import ScheduleRepositoryInterface
from ...domain.value_objects.time_slot import TimeSlot
from ...domain.value_objects.schedule_status import ScheduleStatus
from ..config.models import ScheduleModel, AcademicGroupModel, VenueModel


class ScheduleRepositorySQLAlchemy(ScheduleRepositoryInterface):
    """SQLAlchemy implementation of the schedule repository."""

    def __init__(self, db_session: Session):
        self._db = db_session

    async def create(self, schedule: Schedule) -> Schedule:
        """Create a new schedule."""
        schedule_model = ScheduleModel(
            id=schedule.id,
            start_date=schedule.start_date,
            end_date=schedule.end_date,
            start_time=schedule.time_slot.start_time,
            end_time=schedule.time_slot.end_time,
            instructor_id=schedule.instructor_id,
            group_id=schedule.group_id,
            venue_id=schedule.venue_id,
            subject=schedule.subject,
            status=schedule.status.value,
            notes=schedule.notes,
            created_at=schedule.created_at,
            updated_at=schedule.updated_at,
        )
        self._db.add(schedule_model)
        self._db.commit()
        self._db.refresh(schedule_model)
        return self._map_to_entity(schedule_model)

    async def get_by_id(self, schedule_id: UUID) -> Optional[Schedule]:
        """Get schedule by ID."""
        stmt = select(ScheduleModel).where(ScheduleModel.id == schedule_id)
        schedule_model = self._db.execute(stmt).scalar_one_or_none()
        return self._map_to_entity(schedule_model) if schedule_model else None

    async def update(self, schedule: Schedule) -> Schedule:
        """Update an existing schedule."""
        stmt = select(ScheduleModel).where(ScheduleModel.id == schedule.id)
        schedule_model = self._db.execute(stmt).scalar_one_or_none()

        if not schedule_model:
            return None # Or raise an exception

        schedule_model.start_date = schedule.start_date
        schedule_model.end_date = schedule.end_date
        schedule_model.start_time = schedule.time_slot.start_time
        schedule_model.end_time = schedule.time_slot.end_time
        schedule_model.instructor_id = schedule.instructor_id
        schedule_model.group_id = schedule.group_id
        schedule_model.venue_id = schedule.venue_id
        schedule_model.subject = schedule.subject
        schedule_model.status = schedule.status.value
        schedule_model.notes = schedule.notes
        schedule_model.updated_at = datetime.now() # Ensure updated_at is set

        self._db.commit()
        self._db.refresh(schedule_model)
        return self._map_to_entity(schedule_model)

    async def delete(self, schedule_id: UUID) -> bool:
        """Delete a schedule."""
        stmt = select(ScheduleModel).where(ScheduleModel.id == schedule_id)
        schedule_model = self._db.execute(stmt).scalar_one_or_none()
        if schedule_model:
            self._db.delete(schedule_model)
            self._db.commit()
            return True
        return False

    async def get_by_date_range(self, start_date: date, end_date: date) -> List[Schedule]:
        """Get schedules by date range."""
        stmt = select(ScheduleModel).where(
            and_(ScheduleModel.start_date >= start_date, ScheduleModel.end_date <= end_date)
        ).order_by(ScheduleModel.start_date, ScheduleModel.start_time)
        schedule_models = self._db.execute(stmt).scalars().all()
        return [self._map_to_entity(sm) for sm in schedule_models]

    async def get_by_instructor(self, instructor_id: UUID) -> List[Schedule]:
        """Get schedules by instructor."""
        stmt = select(ScheduleModel).where(ScheduleModel.instructor_id == instructor_id).order_by(ScheduleModel.start_date, ScheduleModel.start_time)
        schedule_models = self._db.execute(stmt).scalars().all()
        return [self._map_to_entity(sm) for sm in schedule_models]

    async def get_by_group(self, group_id: UUID) -> List[Schedule]:
        """Get schedules by group."""
        stmt = select(ScheduleModel).where(ScheduleModel.group_id == group_id).order_by(ScheduleModel.start_date, ScheduleModel.start_time)
        schedule_models = self._db.execute(stmt).scalars().all()
        return [self._map_to_entity(sm) for sm in schedule_models]

    async def get_by_venue(self, venue_id: UUID) -> List[Schedule]:
        """Get schedules by venue."""
        stmt = select(ScheduleModel).where(ScheduleModel.venue_id == venue_id).order_by(ScheduleModel.start_date, ScheduleModel.start_time)
        schedule_models = self._db.execute(stmt).scalars().all()
        return [self._map_to_entity(sm) for sm in schedule_models]

    async def get_active_schedules(self) -> List[Schedule]:
        """Get all active schedules."""
        stmt = select(ScheduleModel).where(ScheduleModel.status == ScheduleStatus.ACTIVE.value).order_by(ScheduleModel.start_date, ScheduleModel.start_time)
        schedule_models = self._db.execute(stmt).scalars().all()
        return [self._map_to_entity(sm) for sm in schedule_models]

    async def check_instructor_conflict(
        self,
        instructor_id: UUID,
        start_date: date,
        end_date: date,
        start_time: time, # Added start_time
        end_time: time,   # Added end_time
        exclude_schedule_id: Optional[UUID] = None
    ) -> bool:
        """Check if instructor has scheduling conflicts within the given date and time range."""
        query = select(exists().where(
            and_(
                ScheduleModel.instructor_id == instructor_id,
                ScheduleModel.start_date <= end_date,   # Overlaps if schedule starts before or on new end_date
                ScheduleModel.end_date >= start_date,     # And ends after or on new start_date
                ScheduleModel.start_time < end_time,    # And starts before new end_time
                ScheduleModel.end_time > start_time,      # And ends after new start_time
                ScheduleModel.status != ScheduleStatus.CANCELLED.value # Ignore cancelled schedules
            )
        ))
        if exclude_schedule_id:
            query = query.where(ScheduleModel.id != exclude_schedule_id)
        
        return self._db.execute(query).scalar()

    async def check_venue_conflict(
        self,
        venue_id: UUID,
        start_date: date,
        end_date: date,
        start_time: time, # Added start_time
        end_time: time,   # Added end_time
        exclude_schedule_id: Optional[UUID] = None
    ) -> bool:
        """Check if venue has scheduling conflicts within the given date and time range."""
        query = select(exists().where(
            and_(
                ScheduleModel.venue_id == venue_id,
                ScheduleModel.start_date <= end_date,
                ScheduleModel.end_date >= start_date,
                ScheduleModel.start_time < end_time,
                ScheduleModel.end_time > start_time,
                ScheduleModel.status != ScheduleStatus.CANCELLED.value
            )
        ))
        if exclude_schedule_id:
            query = query.where(ScheduleModel.id != exclude_schedule_id)
            
        return self._db.execute(query).scalar()

    def _map_to_entity(self, model: ScheduleModel) -> Schedule:
        """Map SQLAlchemy model to domain entity."""
        if not model:
            return None
        return Schedule(
            id=model.id,
            start_date=model.start_date,
            end_date=model.end_date,
            time_slot=TimeSlot(model.start_time, model.end_time),
            instructor_id=model.instructor_id,
            group_id=model.group_id,
            venue_id=model.venue_id,
            subject=model.subject,
            status=ScheduleStatus(model.status),
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
