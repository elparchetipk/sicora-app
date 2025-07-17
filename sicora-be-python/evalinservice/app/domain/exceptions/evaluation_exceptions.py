"""Evaluation-related domain exceptions."""


class EvaluationDomainError(Exception):
    """Base exception for evaluation domain errors."""
    pass


class InvalidEvaluationError(EvaluationDomainError):
    """Raised when evaluation data is invalid."""
    pass


class InvalidResponseError(EvaluationDomainError):
    """Raised when evaluation response is invalid."""
    pass


class InvalidQuestionResponseError(EvaluationDomainError):
    """Raised when question response is invalid."""
    pass


class EvaluationNotFoundError(EvaluationDomainError):
    """Raised when an evaluation is not found."""
    pass


class EvaluationAlreadyExistsError(EvaluationDomainError):
    """Raised when trying to create an evaluation that already exists."""
    pass


class DuplicateEvaluation(EvaluationDomainError):
    """Raised when trying to create a duplicate evaluation."""
    pass


class EvaluationPeriodNotActive(EvaluationDomainError):
    """Raised when evaluation period is not active."""
    pass


class InvalidEvaluationData(EvaluationDomainError):
    """Raised when evaluation data is invalid."""
    pass


class EvaluationNotInProgress(EvaluationDomainError):
    """Raised when evaluation is not in progress state."""
    pass


class EvaluationAlreadySubmittedError(EvaluationDomainError):
    """Raised when trying to modify a submitted evaluation."""
    pass


class IncompleteEvaluationError(EvaluationDomainError):
    """Raised when trying to submit an incomplete evaluation."""
    pass


class UnauthorizedEvaluationError(EvaluationDomainError):
    """Raised when user is not authorized to perform evaluation action."""
    pass


class InvalidInstructorError(EvaluationDomainError):
    """Raised when instructor is invalid for evaluation."""
    pass
