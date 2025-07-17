"""Domain repository interfaces for EvalinService."""

from .question_repository_interface import QuestionRepositoryInterface
from .questionnaire_repository_interface import QuestionnaireRepositoryInterface
from .evaluation_period_repository_interface import EvaluationPeriodRepositoryInterface
from .evaluation_repository_interface import EvaluationRepositoryInterface

__all__ = [
    "QuestionRepositoryInterface",
    "QuestionnaireRepositoryInterface",
    "EvaluationPeriodRepositoryInterface", 
    "EvaluationRepositoryInterface"
]
