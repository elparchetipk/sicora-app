"""Tests unitarios básicos para Question Use Cases."""

import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from app.domain.entities.question import Question
from app.domain.value_objects import QuestionType
from app.domain.exceptions.question_exceptions import (
    QuestionNotFoundError,
    QuestionAlreadyExistsError,
    InvalidQuestionTextError
)
from app.application.dtos.question_dtos import (
    CreateQuestionRequest,
    UpdateQuestionRequest
)


class TestCreateQuestionUseCase:
    """Tests básicos para CreateQuestionUseCase."""

    @pytest.fixture
    def mock_repository(self):
        repository = Mock()
        repository.exists_by_text = AsyncMock()
        repository.get_max_order_index = AsyncMock()
        repository.create = AsyncMock()
        return repository

    @pytest.fixture
    def use_case(self, mock_repository):
        from app.application.use_cases.create_question_use_case import CreateQuestionUseCase
        return CreateQuestionUseCase(mock_repository)

    @pytest.mark.asyncio
    async def test_create_question_success(self, use_case, mock_repository):
        """Test creación exitosa de pregunta."""
        # Arrange
        request = CreateQuestionRequest(
            text="¿El instructor explica claramente?",
            question_type=QuestionType.SCALE_1_5,
            category="comunicacion"
        )
        mock_repository.exists_by_text.return_value = False
        mock_repository.get_max_order_index.return_value = 0
        
        expected_question = Question.create(
            text=request.text,
            question_type=request.question_type,
            category=request.category
        )
        mock_repository.save.return_value = expected_question

        # Act
        result = await use_case.execute(request)

        # Assert
        assert result.text == request.text
        assert result.question_type == request.question_type
        assert result.category == request.category
        mock_repository.exists_by_text.assert_called_once_with(request.text)
        mock_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_question_duplicate_text(self, use_case, mock_repository):
        """Test fallo por texto duplicado."""
        # Arrange
        request = CreateQuestionRequest(
            text="Pregunta existente con texto suficientemente largo",
            question_type=QuestionType.SCALE_1_5,
            category="test"
        )
        mock_repository.exists_by_text.return_value = True

        # Act & Assert
        with pytest.raises(QuestionAlreadyExistsError):
            await use_case.execute(request)


class TestGetQuestionByIdUseCase:
    """Tests básicos para GetQuestionByIdUseCase."""

    @pytest.fixture
    def mock_repository(self):
        repository = Mock()
        repository.get_by_id = AsyncMock()
        return repository

    @pytest.fixture
    def use_case(self, mock_repository):
        from app.application.use_cases.get_question_by_id_use_case import GetQuestionByIdUseCase
        return GetQuestionByIdUseCase(mock_repository)

    @pytest.mark.asyncio
    async def test_get_question_by_id_success(self, use_case, mock_repository):
        """Test obtención exitosa de pregunta por ID."""
        # Arrange
        question_id = uuid4()
        expected_question = Question.create(
            text="Pregunta test con texto suficientemente largo",
            question_type=QuestionType.SCALE_1_5,
            category="test"
        )
        expected_question.id = question_id
        mock_repository.get_by_id.return_value = expected_question

        # Act
        result = await use_case.execute(question_id)

        # Assert
        assert result.id == question_id
        assert "Pregunta test" in result.text
        mock_repository.get_by_id.assert_called_once_with(question_id)

    @pytest.mark.asyncio
    async def test_get_question_by_id_not_found(self, use_case, mock_repository):
        """Test fallo por pregunta no encontrada."""
        # Arrange
        question_id = uuid4()
        mock_repository.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(QuestionNotFoundError):
            await use_case.execute(question_id)


class TestUpdateQuestionUseCase:
    """Tests básicos para UpdateQuestionUseCase."""

    @pytest.fixture
    def mock_repository(self):
        repository = Mock()
        repository.get_by_id = AsyncMock()
        repository.get_by_text = AsyncMock()
        repository.save = AsyncMock()
        return repository

    @pytest.fixture
    def use_case(self, mock_repository):
        from app.application.use_cases.update_question_use_case import UpdateQuestionUseCase
        return UpdateQuestionUseCase(mock_repository)

    @pytest.mark.asyncio
    async def test_update_question_success(self, use_case, mock_repository):
        """Test actualización exitosa de pregunta."""
        # Arrange
        question_id = uuid4()
        existing_question = Question.create(
            text="Texto original con suficiente longitud para ser válido",
            question_type=QuestionType.SCALE_1_5,
            category="original"
        )
        existing_question.id = question_id
        
        request = UpdateQuestionRequest(
            text="Texto actualizado con suficiente longitud para ser válido",
            category="nueva_categoria"
        )
        
        mock_repository.get_by_id.return_value = existing_question
        mock_repository.get_by_text.return_value = None
        mock_repository.save.return_value = existing_question

        # Act
        result = await use_case.execute(question_id, request)

        # Assert
        assert result is not None
        mock_repository.get_by_id.assert_called_once_with(question_id)
        mock_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_question_not_found(self, use_case, mock_repository):
        """Test fallo por pregunta no encontrada."""
        # Arrange
        question_id = uuid4()
        request = UpdateQuestionRequest(text="Nuevo texto con suficiente longitud")
        mock_repository.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(QuestionNotFoundError):
            await use_case.execute(question_id, request)


class TestDeleteQuestionUseCase:
    """Tests básicos para DeleteQuestionUseCase."""

    @pytest.fixture
    def mock_repository(self):
        repository = Mock()
        repository.get_by_id = AsyncMock()
        repository.delete = AsyncMock()
        return repository

    @pytest.fixture
    def use_case(self, mock_repository):
        from app.application.use_cases.delete_question_use_case import DeleteQuestionUseCase
        return DeleteQuestionUseCase(mock_repository)

    @pytest.mark.asyncio
    async def test_delete_question_success(self, use_case, mock_repository):
        """Test eliminación exitosa de pregunta."""
        # Arrange
        question_id = uuid4()
        existing_question = Question.create(
            text="Pregunta a eliminar con texto suficientemente largo",
            question_type=QuestionType.SCALE_1_5,
            category="test"
        )
        existing_question.id = question_id
        mock_repository.get_by_id.return_value = existing_question
        mock_repository.delete.return_value = True

        # Act
        result = await use_case.execute(question_id)

        # Assert
        assert result is True
        mock_repository.get_by_id.assert_called_once_with(question_id)
        mock_repository.delete.assert_called_once_with(question_id)

    @pytest.mark.asyncio
    async def test_delete_question_not_found(self, use_case, mock_repository):
        """Test fallo por pregunta no encontrada."""
        # Arrange
        question_id = uuid4()
        mock_repository.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(QuestionNotFoundError):
            await use_case.execute(question_id)
