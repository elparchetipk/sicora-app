"""Question-related domain exceptions."""


class QuestionDomainError(Exception):
    """Base exception for question domain errors."""
    pass


class InvalidQuestionTextError(QuestionDomainError):
    """Raised when question text is invalid."""
    pass


class InvalidQuestionTypeError(QuestionDomainError):
    """Raised when question type is invalid."""
    pass


class QuestionNotFoundError(QuestionDomainError):
    """Raised when a question is not found."""
    pass


class QuestionAlreadyExistsError(QuestionDomainError):
    """Raised when trying to create a question that already exists."""
    pass


class InvalidQuestionOrderError(QuestionDomainError):
    """Raised when question order is invalid."""
    pass


class QuestionInUseError(QuestionDomainError):
    """Raised when trying to delete a question that is in use."""
    pass
