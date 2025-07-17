"""Prediction use cases for AI Service."""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta

from app.domain.entities.prediction_result import (
    PredictionResult,
    PredictionType,
    PredictionStatus,
    ConfidenceLevel,
)
from app.domain.repositories.prediction_repository import (
    PredictionResultRepositoryInterface,
)
from app.domain.exceptions import (
    PredictionNotFoundError,
    InvalidPredictionDataError,
    InsufficientDataError,
)


class CreatePredictionUseCase:
    """Use case for creating predictions."""

    def __init__(self, prediction_repository: PredictionResultRepositoryInterface):
        self.prediction_repository = prediction_repository

    async def execute(
        self,
        prediction_type: PredictionType,
        subject_id: UUID,
        subject_type: str = "user",
        prediction_data: Dict[str, Any] = None,
        model_used: str = "default",
        created_by: Optional[UUID] = None,
    ) -> PredictionResult:
        """Create a new prediction."""

        if not prediction_data:
            raise InvalidPredictionDataError("Prediction data is required")

        # Calculate confidence based on data quality and type
        confidence = self._calculate_confidence(prediction_type, prediction_data)

        # Set expiration based on prediction type
        expires_at = self._calculate_expiration(prediction_type)

        prediction = PredictionResult(
            prediction_type=prediction_type,
            subject_id=subject_id,
            subject_type=subject_type,
            confidence=confidence,
            prediction_data=prediction_data,
            model_used=model_used,
            status=PredictionStatus.COMPLETED,
            created_by=created_by,
            expires_at=expires_at,
        )

        return await self.prediction_repository.create(prediction)

    def _calculate_confidence(
        self, prediction_type: PredictionType, data: Dict[str, Any]
    ) -> float:
        """Calculate confidence score based on data quality."""
        # Basic confidence calculation - can be enhanced with ML models
        base_confidence = 0.5

        if prediction_type == PredictionType.ATTENDANCE:
            # Higher confidence for attendance prediction if we have historical data
            if data.get("historical_attendance_count", 0) > 10:
                base_confidence += 0.3
            if data.get("recent_attendance_rate", 0) > 0.8:
                base_confidence += 0.2
        elif prediction_type == PredictionType.DROPOUT:
            # Dropout prediction confidence based on multiple factors
            if data.get("academic_performance_score", 0) < 0.3:
                base_confidence += 0.3
            if data.get("attendance_rate", 1) < 0.6:
                base_confidence += 0.2

        return min(base_confidence, 0.95)  # Cap at 95%

    def _calculate_expiration(self, prediction_type: PredictionType) -> datetime:
        """Calculate expiration date based on prediction type."""
        now = datetime.utcnow()

        if prediction_type == PredictionType.ATTENDANCE:
            return now + timedelta(days=7)  # Attendance predictions valid for 1 week
        elif prediction_type == PredictionType.DROPOUT:
            return now + timedelta(days=30)  # Dropout predictions valid for 1 month
        else:
            return now + timedelta(days=14)  # Default 2 weeks


class GetPredictionByIdUseCase:
    """Use case for getting prediction by ID."""

    def __init__(self, prediction_repository: PredictionResultRepositoryInterface):
        self.prediction_repository = prediction_repository

    async def execute(self, prediction_id: UUID) -> PredictionResult:
        """Get prediction by ID."""
        prediction = await self.prediction_repository.get_by_id(prediction_id)
        if not prediction:
            raise PredictionNotFoundError(
                f"Prediction with ID {prediction_id} not found"
            )
        return prediction


class GetPredictionsBySubjectUseCase:
    """Use case for getting predictions by subject."""

    def __init__(self, prediction_repository: PredictionResultRepositoryInterface):
        self.prediction_repository = prediction_repository

    async def execute(
        self,
        subject_id: UUID,
        prediction_type: Optional[PredictionType] = None,
        limit: int = 10,
    ) -> List[PredictionResult]:
        """Get predictions for a specific subject."""
        return await self.prediction_repository.get_by_subject_id(
            subject_id, prediction_type, limit
        )


class PredictAttendanceRiskUseCase:
    """Use case for predicting attendance risk."""

    def __init__(self, prediction_repository: PredictionResultRepositoryInterface):
        self.prediction_repository = prediction_repository

    async def execute(
        self,
        user_id: UUID,
        attendance_data: Dict[str, Any],
        created_by: Optional[UUID] = None,
    ) -> PredictionResult:
        """Predict attendance risk for a user."""

        if (
            not attendance_data.get("total_classes")
            or attendance_data["total_classes"] < 5
        ):
            raise InsufficientDataError("Insufficient attendance data for prediction")

        # Calculate attendance rate
        attended = attendance_data.get("attended_classes", 0)
        total = attendance_data.get("total_classes", 1)
        attendance_rate = attended / total

        # Predict risk level
        risk_score = 1 - attendance_rate  # Higher score = higher risk

        prediction_data = {
            "attendance_rate": attendance_rate,
            "risk_score": risk_score,
            "total_classes": total,
            "attended_classes": attended,
            "recent_absences": attendance_data.get("recent_absences", 0),
            "consecutive_absences": attendance_data.get("consecutive_absences", 0),
            "prediction_date": datetime.utcnow().isoformat(),
        }

        create_usecase = CreatePredictionUseCase(self.prediction_repository)
        return await create_usecase.execute(
            prediction_type=PredictionType.ATTENDANCE,
            subject_id=user_id,
            subject_type="user",
            prediction_data=prediction_data,
            model_used="attendance_risk_v1",
            created_by=created_by,
        )


class PredictDropoutRiskUseCase:
    """Use case for predicting dropout risk."""

    def __init__(self, prediction_repository: PredictionResultRepositoryInterface):
        self.prediction_repository = prediction_repository

    async def execute(
        self,
        user_id: UUID,
        academic_data: Dict[str, Any],
        created_by: Optional[UUID] = None,
    ) -> PredictionResult:
        """Predict dropout risk for a user."""

        required_fields = ["attendance_rate", "academic_performance"]
        missing_fields = [
            field for field in required_fields if field not in academic_data
        ]

        if missing_fields:
            raise InsufficientDataError(f"Missing required fields: {missing_fields}")

        attendance_rate = academic_data.get("attendance_rate", 1.0)
        academic_performance = academic_data.get("academic_performance", 1.0)

        # Simple dropout risk calculation
        # Lower attendance and performance = higher dropout risk
        risk_factors = []
        risk_score = 0.0

        if attendance_rate < 0.7:
            risk_score += 0.4
            risk_factors.append("low_attendance")

        if academic_performance < 0.6:
            risk_score += 0.3
            risk_factors.append("poor_performance")

        if academic_data.get("disciplinary_issues", 0) > 0:
            risk_score += 0.2
            risk_factors.append("disciplinary_issues")

        if academic_data.get("financial_difficulties", False):
            risk_score += 0.1
            risk_factors.append("financial_difficulties")

        prediction_data = {
            "risk_score": min(risk_score, 1.0),
            "risk_factors": risk_factors,
            "attendance_rate": attendance_rate,
            "academic_performance": academic_performance,
            "disciplinary_issues": academic_data.get("disciplinary_issues", 0),
            "financial_difficulties": academic_data.get(
                "financial_difficulties", False
            ),
            "prediction_date": datetime.utcnow().isoformat(),
        }

        create_usecase = CreatePredictionUseCase(self.prediction_repository)
        return await create_usecase.execute(
            prediction_type=PredictionType.DROPOUT,
            subject_id=user_id,
            subject_type="user",
            prediction_data=prediction_data,
            model_used="dropout_risk_v1",
            created_by=created_by,
        )


class GetHighRiskPredictionsUseCase:
    """Use case for getting high risk predictions."""

    def __init__(self, prediction_repository: PredictionResultRepositoryInterface):
        self.prediction_repository = prediction_repository

    async def execute(
        self,
        prediction_type: Optional[PredictionType] = None,
        confidence_threshold: float = 0.7,
    ) -> List[PredictionResult]:
        """Get high confidence/risk predictions."""
        return await self.prediction_repository.get_high_confidence_predictions(
            prediction_type, confidence_threshold
        )


class GetPredictionStatisticsUseCase:
    """Use case for getting prediction statistics."""

    def __init__(self, prediction_repository: PredictionResultRepositoryInterface):
        self.prediction_repository = prediction_repository

    async def execute(
        self, prediction_type: Optional[PredictionType] = None, days: int = 30
    ) -> Dict[str, Any]:
        """Get prediction statistics."""
        stats = await self.prediction_repository.get_predictions_statistics(
            prediction_type, days
        )

        # Add additional calculated metrics
        total_predictions = stats.get("total_predictions", 0)
        high_confidence = stats.get("high_confidence_predictions", 0)

        if total_predictions > 0:
            stats["high_confidence_rate"] = high_confidence / total_predictions
        else:
            stats["high_confidence_rate"] = 0.0

        return stats
