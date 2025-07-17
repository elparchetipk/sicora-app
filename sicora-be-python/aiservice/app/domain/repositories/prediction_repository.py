"""Prediction Result repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from app.domain.entities.prediction_result import (
    PredictionResult,
    PredictionType,
    PredictionStatus,
)


class PredictionResultRepositoryInterface(ABC):
    """Interface for prediction result repository operations."""

    @abstractmethod
    async def create(self, prediction: PredictionResult) -> PredictionResult:
        """Create a new prediction result."""
        pass

    @abstractmethod
    async def get_by_id(self, prediction_id: UUID) -> Optional[PredictionResult]:
        """Get prediction result by ID."""
        pass

    @abstractmethod
    async def get_by_subject_id(
        self,
        subject_id: UUID,
        prediction_type: Optional[PredictionType] = None,
        limit: int = 10,
    ) -> List[PredictionResult]:
        """Get predictions for a specific subject."""
        pass

    @abstractmethod
    async def get_by_type(
        self,
        prediction_type: PredictionType,
        status: Optional[PredictionStatus] = None,
        limit: int = 50,
    ) -> List[PredictionResult]:
        """Get predictions by type and optionally by status."""
        pass

    @abstractmethod
    async def get_active_predictions(
        self,
        subject_id: Optional[UUID] = None,
        prediction_type: Optional[PredictionType] = None,
    ) -> List[PredictionResult]:
        """Get active (non-expired) predictions."""
        pass

    @abstractmethod
    async def get_high_confidence_predictions(
        self,
        prediction_type: Optional[PredictionType] = None,
        confidence_threshold: float = 0.7,
    ) -> List[PredictionResult]:
        """Get high confidence predictions."""
        pass

    @abstractmethod
    async def update_status(
        self, prediction_id: UUID, status: PredictionStatus
    ) -> Optional[PredictionResult]:
        """Update prediction status."""
        pass

    @abstractmethod
    async def delete(self, prediction_id: UUID) -> bool:
        """Delete a prediction result."""
        pass

    @abstractmethod
    async def get_expired_predictions(self) -> List[PredictionResult]:
        """Get expired predictions for cleanup."""
        pass

    @abstractmethod
    async def get_predictions_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        prediction_type: Optional[PredictionType] = None,
    ) -> List[PredictionResult]:
        """Get predictions within a date range."""
        pass

    @abstractmethod
    async def get_predictions_statistics(
        self, prediction_type: Optional[PredictionType] = None, days: int = 30
    ) -> Dict[str, Any]:
        """Get prediction statistics for the last N days."""
        pass
