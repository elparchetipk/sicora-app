"""AI Service domain exceptions."""


class AIServiceException(Exception):
    """Base exception for AI Service domain."""

    pass


class ConversationNotFoundError(AIServiceException):
    """Raised when a conversation is not found."""

    pass


class KnowledgeBaseError(AIServiceException):
    """Raised when there's an error with the knowledge base."""

    pass


class ModelNotAvailableError(AIServiceException):
    """Raised when an AI model is not available."""

    pass


class InvalidPromptError(AIServiceException):
    """Raised when a prompt is invalid or malformed."""

    pass


class TokenLimitExceededError(AIServiceException):
    """Raised when token limit is exceeded."""

    pass


class EmbeddingError(AIServiceException):
    """Raised when there's an error generating embeddings."""

    pass


class VectorStoreError(AIServiceException):
    """Raised when there's an error with vector store operations."""

    pass


class ConversationLimitExceededError(AIServiceException):
    """Raised when conversation limit is exceeded."""

    pass


class InvalidModelConfigurationError(AIServiceException):
    """Raised when model configuration is invalid."""

    pass


class AIProviderError(AIServiceException):
    """Raised when there's an error with AI provider operations."""

    pass


class ModelNotFoundError(AIServiceException):
    """Raised when a requested AI model is not found."""

    pass


class RateLimitError(AIServiceException):
    """Raised when API rate limit is exceeded."""

    pass


class InvalidInputError(AIServiceException):
    """Raised when input is invalid for AI operations."""

    pass


class CacheError(AIServiceException):
    """Raised when there's an error with cache operations."""

    pass


# Prediction related exceptions
class PredictionError(AIServiceException):
    """Base exception for prediction related errors."""

    pass


class PredictionNotFoundError(PredictionError):
    """Raised when a prediction is not found."""

    pass


class InvalidPredictionDataError(PredictionError):
    """Raised when prediction data is invalid."""

    pass


class PredictionModelError(PredictionError):
    """Raised when there's an error with prediction model."""

    pass


class InsufficientDataError(PredictionError):
    """Raised when there's insufficient data for prediction."""

    pass


# Alert related exceptions
class AlertError(AIServiceException):
    """Base exception for alert related errors."""

    pass


class AlertNotFoundError(AlertError):
    """Raised when an alert is not found."""

    pass


class InvalidAlertDataError(AlertError):
    """Raised when alert data is invalid."""

    pass


class AlertPermissionError(AlertError):
    """Raised when user doesn't have permission for alert operation."""

    pass


class AlertStatusError(AlertError):
    """Raised when alert status transition is invalid."""

    pass


class SearchError(AIServiceException):
    """Raised when there's an error during knowledge search."""
    pass


class KnowledgeBaseIntegrationError(AIServiceException):
    """Raised when there's an error integrating with KbService."""
    pass


class ContextGenerationError(AIServiceException):
    """Raised when there's an error generating chat context."""
    pass
