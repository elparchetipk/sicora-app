from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .connection import Base
from ...domain.entities import StakeholderStatus, StakeholderType


class StakeholderModel(Base):
    __tablename__ = "stakeholders"
    __table_args__ = {'schema': 'projectevalservice_schema'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    stakeholder_type = Column(SQLEnum(StakeholderType), nullable=False)
    status = Column(
        SQLEnum(StakeholderStatus), nullable=False, default=StakeholderStatus.ACTIVE
    )

    # Contact information
    contact_person = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)

    # Organization details
    organization_size = Column(String(50), nullable=True)
    sector = Column(String(100), nullable=True)
    website = Column(String(500), nullable=True)

    # SENA collaboration
    previous_collaborations = Column(Integer, default=0)
    expectations_documented = Column(Boolean, default=False)
    limitations_acknowledged = Column(Boolean, default=False)
    communication_channel_established = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    created_by = Column(UUID(as_uuid=True), nullable=False)

    # Governance and limitations
    scope_change_requests = Column(Integer, default=0)
    scope_changes_approved = Column(Integer, default=0)
    scope_changes_rejected = Column(Integer, default=0)
    last_interaction_date = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = {"schema": "projectevalservice_schema"}
