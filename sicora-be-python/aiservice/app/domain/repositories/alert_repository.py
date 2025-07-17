"""Alert repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from app.domain.entities.alert import Alert, AlertType, AlertSeverity, AlertStatus


class AlertRepositoryInterface(ABC):
    """Interface for alert repository operations."""

    @abstractmethod
    async def create(self, alert: Alert) -> Alert:
        """Create a new alert."""
        pass

    @abstractmethod
    async def get_by_id(self, alert_id: UUID) -> Optional[Alert]:
        """Get alert by ID."""
        pass

    @abstractmethod
    async def get_by_subject_id(
        self,
        subject_id: UUID,
        alert_type: Optional[AlertType] = None,
        status: Optional[AlertStatus] = None,
        limit: int = 50,
    ) -> List[Alert]:
        """Get alerts for a specific subject."""
        pass

    @abstractmethod
    async def get_by_assigned_user(
        self, user_id: UUID, status: Optional[AlertStatus] = None, limit: int = 50
    ) -> List[Alert]:
        """Get alerts assigned to a specific user."""
        pass

    @abstractmethod
    async def get_active_alerts(
        self,
        alert_type: Optional[AlertType] = None,
        severity: Optional[AlertSeverity] = None,
        limit: int = 100,
    ) -> List[Alert]:
        """Get active alerts."""
        pass

    @abstractmethod
    async def get_critical_alerts(self, limit: int = 50) -> List[Alert]:
        """Get critical severity alerts."""
        pass

    @abstractmethod
    async def update_status(
        self, alert_id: UUID, status: AlertStatus, updated_by: UUID
    ) -> Optional[Alert]:
        """Update alert status."""
        pass

    @abstractmethod
    async def acknowledge_alert(
        self, alert_id: UUID, acknowledged_by: UUID
    ) -> Optional[Alert]:
        """Acknowledge an alert."""
        pass

    @abstractmethod
    async def resolve_alert(
        self, alert_id: UUID, resolved_by: UUID, resolution_notes: Optional[str] = None
    ) -> Optional[Alert]:
        """Resolve an alert."""
        pass

    @abstractmethod
    async def dismiss_alert(
        self, alert_id: UUID, dismissed_by: UUID, reason: Optional[str] = None
    ) -> Optional[Alert]:
        """Dismiss an alert."""
        pass

    @abstractmethod
    async def assign_alert(self, alert_id: UUID, assigned_to: UUID) -> Optional[Alert]:
        """Assign alert to a user."""
        pass

    @abstractmethod
    async def get_expired_alerts(self) -> List[Alert]:
        """Get expired alerts for cleanup."""
        pass

    @abstractmethod
    async def get_alerts_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        alert_type: Optional[AlertType] = None,
        status: Optional[AlertStatus] = None,
    ) -> List[Alert]:
        """Get alerts within a date range."""
        pass

    @abstractmethod
    async def get_alert_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Get alert statistics for the last N days."""
        pass

    @abstractmethod
    async def get_alerts_by_severity(
        self,
        severity: AlertSeverity,
        status: Optional[AlertStatus] = None,
        limit: int = 50,
    ) -> List[Alert]:
        """Get alerts by severity level."""
        pass

    @abstractmethod
    async def delete_old_alerts(
        self, days_old: int = 90, status: Optional[AlertStatus] = AlertStatus.RESOLVED
    ) -> int:
        """Delete old alerts and return count of deleted alerts."""
        pass
