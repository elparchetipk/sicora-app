"""Period-related domain exceptions."""


class PeriodDomainError(Exception):
    """Base exception for period domain errors."""
    pass


class InvalidPeriodNameError(PeriodDomainError):
    """Raised when period name is invalid."""
    pass


class InvalidPeriodDatesError(PeriodDomainError):
    """Raised when period dates are invalid."""
    pass


class PeriodNotFoundError(PeriodDomainError):
    """Raised when a period is not found."""
    pass


class EvaluationPeriodNotFoundError(PeriodDomainError):
    """Raised when an evaluation period is not found."""
    pass


class EvaluationPeriodNotFound(PeriodDomainError):
    """Raised when an evaluation period is not found."""
    pass


class EvaluationPeriodInvalidStateError(PeriodDomainError):
    """Raised when evaluation period is in invalid state."""
    pass


class PeriodOverlapError(PeriodDomainError):
    """Raised when periods overlap inappropriately."""
    pass


class EvaluationPeriodOverlapError(PeriodDomainError):
    """Raised when evaluation periods overlap inappropriately."""
    pass


class PeriodAlreadyActiveError(PeriodDomainError):
    """Raised when trying to activate an already active period."""
    pass


class PeriodNotActiveError(PeriodDomainError):
    """Raised when trying to perform actions on inactive period."""
    pass


class EvaluationPeriodNotActiveError(PeriodDomainError):
    """Raised when trying to perform actions on inactive evaluation period."""
    pass


class PeriodExpiredError(PeriodDomainError):
    """Raised when trying to perform actions on expired period."""
    pass


class PeriodInUseError(PeriodDomainError):
    """Raised when trying to delete a period that has evaluations."""
    pass
