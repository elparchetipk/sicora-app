"""Tests unitarios básicos para verificar la funcionalidad principal del dominio."""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from app.domain.value_objects import QuestionType, PeriodStatus, EvaluationStatus


class TestQuestionEntity:
    """Tests básicos para la entidad Question."""

    def test_create_question_valid(self):
        """Test creación de pregunta válida usando factory method."""
        from app.domain.entities.question import Question
        
        question = Question.create(
            text="¿El instructor explica claramente los conceptos?",
            question_type=QuestionType.SCALE_1_5,
            category="comunicacion"
        )
        
        assert question.text == "¿El instructor explica claramente los conceptos?"
        assert question.question_type == QuestionType.SCALE_1_5
        assert question.category == "comunicacion"
        assert question.is_active is True
        assert question.id is not None

    def test_create_question_invalid_short_text(self):
        """Test fallo con texto muy corto."""
        from app.domain.entities.question import Question
        from app.domain.exceptions.question_exceptions import InvalidQuestionTextError
        
        with pytest.raises(InvalidQuestionTextError):
            Question.create(
                text="Corto",
                question_type=QuestionType.SCALE_1_5,
                category="test"
            )


class TestValueObjects:
    """Tests básicos para value objects."""

    def test_question_type_enum(self):
        """Test enum QuestionType."""
        assert QuestionType.SCALE_1_5.value == "scale_1_5"
        assert QuestionType.TEXT.value == "text"
        assert QuestionType.YES_NO.value == "yes_no"

    def test_period_status_enum(self):
        """Test enum PeriodStatus."""
        assert PeriodStatus.SCHEDULED.value == "scheduled"
        assert PeriodStatus.ACTIVE.value == "active"
        assert PeriodStatus.CLOSED.value == "closed"

    def test_evaluation_status_enum(self):
        """Test enum EvaluationStatus."""
        assert EvaluationStatus.DRAFT.value == "draft"
        assert EvaluationStatus.SUBMITTED.value == "submitted"
        assert EvaluationStatus.PROCESSED.value == "processed"


class TestDomainBasics:
    """Tests básicos para verificar que las entidades se pueden importar y crear."""

    def test_import_entities(self):
        """Test que todas las entidades se pueden importar correctamente."""
        from app.domain.entities.question import Question
        from app.domain.entities.questionnaire import Questionnaire
        from app.domain.entities.evaluation_period import EvaluationPeriod
        from app.domain.entities.evaluation import Evaluation
        
        # Si llegamos aquí, las importaciones funcionan
        assert Question is not None
        assert Questionnaire is not None
        assert EvaluationPeriod is not None
        assert Evaluation is not None

    def test_basic_question_creation(self):
        """Test creación básica de pregunta."""
        from app.domain.entities.question import Question
        
        question = Question.create(
            text="Esta es una pregunta de prueba válida con suficiente texto",
            question_type=QuestionType.SCALE_1_5,
            category="test"
        )
        
        assert isinstance(question.id, type(uuid4()))
        assert len(question.text) >= 10
        assert question.is_active

    def test_basic_period_creation(self):
        """Test creación básica de período."""
        from app.domain.entities.evaluation_period import EvaluationPeriod
        
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)
        
        period = EvaluationPeriod.create(
            name="Período de Prueba",
            start_date=start_date,
            end_date=end_date
        )
        
        assert period.name == "Período de Prueba"
        assert period.start_date == start_date
        assert period.end_date == end_date
        assert isinstance(period.status, PeriodStatus)

    def test_basic_evaluation_creation(self):
        """Test creación básica de evaluación."""
        from app.domain.entities.evaluation import Evaluation
        
        evaluation = Evaluation.create(
            period_id=uuid4(),
            student_id=uuid4(),
            instructor_id=uuid4(),
            questionnaire_id=uuid4()
        )
        
        assert isinstance(evaluation.id, type(uuid4()))
        assert isinstance(evaluation.period_id, type(uuid4()))
        assert isinstance(evaluation.student_id, type(uuid4()))
        assert isinstance(evaluation.instructor_id, type(uuid4()))
        assert isinstance(evaluation.questionnaire_id, type(uuid4()))
        assert isinstance(evaluation.status, EvaluationStatus)
