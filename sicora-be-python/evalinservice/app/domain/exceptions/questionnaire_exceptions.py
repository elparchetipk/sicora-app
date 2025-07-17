"""Questionnaire-related domain exceptions."""


class QuestionnaireDomainError(Exception):
    """Base exception for questionnaire domain errors."""
    pass


class InvalidQuestionnaireNameError(QuestionnaireDomainError):
    """Raised when questionnaire name is invalid."""
    pass


class QuestionnaireNotFoundError(QuestionnaireDomainError):
    """Raised when a questionnaire is not found."""
    pass


class QuestionnaireAlreadyExistsError(QuestionnaireDomainError):
    """Raised when trying to create a questionnaire that already exists."""
    pass


class QuestionNotFoundError(QuestionnaireDomainError):
    """Raised when a question is not found in questionnaire."""
    pass


class DuplicateQuestionError(QuestionnaireDomainError):
    """Raised when trying to add a question that's already in questionnaire."""
    pass


class QuestionNotInQuestionnaireError(QuestionnaireDomainError):
    """Raised when trying to remove a question that's not in questionnaire."""
    pass


class EmptyQuestionnaireError(QuestionnaireDomainError):
    """Raised when trying to use an empty questionnaire."""
    pass


class QuestionnaireInUseError(QuestionnaireDomainError):
    """Raised when trying to delete a questionnaire that is in use."""
    pass
