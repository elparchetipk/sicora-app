"""Domain exceptions for EvalinService."""

from .question_exceptions import (
    QuestionDomainError,
    InvalidQuestionTextError,
    InvalidQuestionTypeError,
    QuestionNotFoundError,
    QuestionAlreadyExistsError,
    InvalidQuestionOrderError,
    QuestionInUseError
)
from .questionnaire_exceptions import (
    QuestionnaireDomainError,
    InvalidQuestionnaireNameError,
    QuestionnaireNotFoundError,
    QuestionnaireAlreadyExistsError,
    DuplicateQuestionError,
    QuestionNotInQuestionnaireError,
    EmptyQuestionnaireError,
    QuestionnaireInUseError
)
from .period_exceptions import (
    PeriodDomainError,
    InvalidPeriodNameError,
    InvalidPeriodDatesError,
    PeriodNotFoundError,
    EvaluationPeriodNotFoundError,
    EvaluationPeriodNotFound,
    EvaluationPeriodInvalidStateError,
    PeriodOverlapError,
    EvaluationPeriodOverlapError,
    PeriodAlreadyActiveError,
    PeriodNotActiveError,
    EvaluationPeriodNotActiveError,
    PeriodExpiredError,
    PeriodInUseError
)
from .evaluation_exceptions import (
    EvaluationDomainError,
    InvalidEvaluationError,
    InvalidResponseError,
    InvalidQuestionResponseError,
    EvaluationNotFoundError,
    EvaluationAlreadyExistsError,
    DuplicateEvaluation,
    EvaluationPeriodNotActive,
    InvalidEvaluationData,
    EvaluationNotInProgress,
    EvaluationAlreadySubmittedError,
    IncompleteEvaluationError,
    UnauthorizedEvaluationError,
    InvalidInstructorError
)

__all__ = [
    # Question exceptions
    "QuestionDomainError",
    "InvalidQuestionTextError", 
    "InvalidQuestionTypeError",
    "QuestionNotFoundError",
    "QuestionAlreadyExistsError",
    "InvalidQuestionOrderError",
    "QuestionInUseError",
    
    # Questionnaire exceptions  
    "QuestionnaireDomainError",
    "InvalidQuestionnaireNameError",
    "QuestionnaireNotFoundError",
    "QuestionnaireAlreadyExistsError",
    "DuplicateQuestionError",
    "QuestionNotInQuestionnaireError",
    "EmptyQuestionnaireError", 
    "QuestionnaireInUseError",
    
    # Period exceptions
    "PeriodDomainError",
    "InvalidPeriodNameError",
    "InvalidPeriodDatesError", 
    "PeriodNotFoundError",
    "EvaluationPeriodNotFoundError",
    "EvaluationPeriodNotFound",
    "EvaluationPeriodInvalidStateError",
    "PeriodOverlapError",
    "EvaluationPeriodOverlapError",
    "PeriodAlreadyActiveError",
    "PeriodNotActiveError",
    "EvaluationPeriodNotActiveError",
    "PeriodExpiredError",
    "PeriodInUseError",
    
    # Evaluation exceptions
    "EvaluationDomainError",
    "InvalidEvaluationError",
    "InvalidResponseError",
    "EvaluationNotFoundError", 
    "EvaluationAlreadyExistsError",
    "DuplicateEvaluation",
    "EvaluationPeriodNotActive",
    "InvalidEvaluationData",
    "EvaluationNotInProgress",
    "EvaluationAlreadySubmittedError",
    "IncompleteEvaluationError",
    "UnauthorizedEvaluationError",
    "InvalidInstructorError"
]
