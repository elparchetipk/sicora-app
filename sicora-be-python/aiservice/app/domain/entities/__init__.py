"""Domain entities package for AI Service."""

from .conversation import Conversation
from .knowledge_entry import KnowledgeEntry
from .ai_model import AIModel, ModelType, ModelStatus
from .prediction_result import (
    PredictionResult,
    PredictionType,
    PredictionStatus,
    ConfidenceLevel,
)
from .alert import Alert, AlertType, AlertSeverity, AlertStatus

__all__ = [
    "Conversation",
    "KnowledgeEntry",
    "AIModel",
    "ModelType",
    "ModelStatus",
    "PredictionResult",
    "PredictionType",
    "PredictionStatus",
    "ConfidenceLevel",
    "Alert",
    "AlertType",
    "AlertSeverity",
    "AlertStatus",
]
