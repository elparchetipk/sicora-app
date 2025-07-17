import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from app.application.use_cases.auth_use_cases import ResetPasswordUseCase
from app.application.dtos.user_dtos import ResetPasswordDTO
from app.domain.entities.user_entity import User
from app.domain.value_objects.email import Email
from app.domain.value_objects.document_number import DocumentNumber
from app.domain.value_objects.document_type import DocumentType
from app.domain.value_objects.user_role import UserRole
from app.domain.exceptions.user_exceptions import (
    UserNotFoundError,
    InvalidTokenError,
    WeakPasswordError
)

@pytest.fixture
def user_repository_mock():
    repository = AsyncMock()
    return repository

@pytest.fixture
def password_service_mock():
    service = AsyncMock()
    return service

@pytest.fixture
def token_service_mock():
    service = AsyncMock()
    return service

@pytest.fixture
def email_service_mock():
    service = AsyncMock()
    return service

@pytest.fixture
def reset_password_use_case(user_repository_mock, password_service_mock, token_service_mock, email_service_mock):
    return ResetPasswordUseCase(user_repository_mock, password_service_mock, token_service_mock, email_service_mock)

@pytest.fixture
def sample_user():
    return User(
        id=uuid4(),
        first_name="John",
        last_name="Doe",
        email=Email("john.doe@example.com"),
        document_number=DocumentNumber("12345678", DocumentType.CC),
        role=UserRole.APPRENTICE,
        hashed_password="hashed_password",
        is_active=True,
        must_change_password=False,
        phone="1234567890"
    )

async def test_reset_password_success(reset_password_use_case, user_repository_mock, password_service_mock, token_service_mock, email_service_mock, sample_user):
    # Arrange
    token = "valid_reset_token"
    new_password = "NewStrongPass123!"
    dto = ResetPasswordDTO(token=token, new_password=new_password)

    # Configure mocks
    token_service_mock.validate_password_reset_token.return_value = str(sample_user.id)
    user_repository_mock.get_by_id.return_value = sample_user
    password_service_mock.is_strong_password.return_value = True
    password_service_mock.hash_password.return_value = "new_hashed_password"

    # Act
    await reset_password_use_case.execute(dto)

    # Assert
    token_service_mock.validate_password_reset_token.assert_called_once_with(token)
    user_repository_mock.get_by_id.assert_called_once_with(sample_user.id)
    password_service_mock.is_strong_password.assert_called_once_with(new_password)
    password_service_mock.hash_password.assert_called_once_with(new_password)
    user_repository_mock.update.assert_called_once()
    token_service_mock.invalidate_password_reset_token.assert_called_once_with(token)
    email_service_mock.send_password_changed_notification.assert_called_once_with(
        email=sample_user.email.value,
        first_name=sample_user.first_name
    )

async def test_reset_password_invalid_token(reset_password_use_case, token_service_mock):
    # Arrange
    token = "invalid_token"
    new_password = "NewStrongPass123!"
    dto = ResetPasswordDTO(token=token, new_password=new_password)

    # Configure mock to raise InvalidTokenError
    token_service_mock.validate_password_reset_token.side_effect = InvalidTokenError("Invalid or expired token")

    # Act & Assert
    with pytest.raises(InvalidTokenError):
        await reset_password_use_case.execute(dto)

    token_service_mock.validate_password_reset_token.assert_called_once_with(token)

async def test_reset_password_user_not_found(reset_password_use_case, user_repository_mock, token_service_mock, sample_user):
    # Arrange
    token = "valid_token"
    new_password = "NewStrongPass123!"
    dto = ResetPasswordDTO(token=token, new_password=new_password)

    # Configure mocks
    token_service_mock.validate_password_reset_token.return_value = str(sample_user.id)
    user_repository_mock.get_by_id.side_effect = UserNotFoundError(f"User with ID {sample_user.id} not found")

    # Act & Assert
    with pytest.raises(UserNotFoundError):
        await reset_password_use_case.execute(dto)

    token_service_mock.validate_password_reset_token.assert_called_once_with(token)
    user_repository_mock.get_by_id.assert_called_once_with(sample_user.id)

async def test_reset_password_weak_password(reset_password_use_case, user_repository_mock, password_service_mock, token_service_mock, sample_user):
    # Arrange
    token = "valid_token"
    weak_password = "weak"
    dto = ResetPasswordDTO(token=token, new_password=weak_password)

    # Configure mocks
    token_service_mock.validate_password_reset_token.return_value = str(sample_user.id)
    user_repository_mock.get_by_id.return_value = sample_user
    password_service_mock.is_strong_password.return_value = False

    # Act & Assert
    with pytest.raises(WeakPasswordError):
        await reset_password_use_case.execute(dto)

    token_service_mock.validate_password_reset_token.assert_called_once_with(token)
    user_repository_mock.get_by_id.assert_called_once_with(sample_user.id)
    password_service_mock.is_strong_password.assert_called_once_with(weak_password)
    password_service_mock.hash_password.assert_not_called()
    user_repository_mock.update.assert_not_called()

async def test_reset_password_inactive_user(reset_password_use_case, user_repository_mock, password_service_mock, token_service_mock, sample_user):
    # Arrange
    token = "valid_token"
    new_password = "NewStrongPass123!"
    dto = ResetPasswordDTO(token=token, new_password=new_password)

    # Create inactive user
    inactive_user = User(
        id=sample_user.id,
        first_name=sample_user.first_name,
        last_name=sample_user.last_name,
        email=sample_user.email,
        document_number=sample_user.document_number,
        role=sample_user.role,
        hashed_password=sample_user.hashed_password,
        is_active=False,  # Inactive user
        must_change_password=sample_user.must_change_password,
        created_at=sample_user.created_at,
        updated_at=sample_user.updated_at,
        last_login_at=sample_user.last_login_at,
        phone=sample_user.phone
    )

    # Configure mocks
    token_service_mock.validate_password_reset_token.return_value = str(inactive_user.id)
    user_repository_mock.get_by_id.return_value = inactive_user
    password_service_mock.is_strong_password.return_value = True

    # Act
    await reset_password_use_case.execute(dto)

    # Assert - should still work for inactive users
    token_service_mock.validate_password_reset_token.assert_called_once_with(token)
    user_repository_mock.get_by_id.assert_called_once_with(inactive_user.id)
    password_service_mock.is_strong_password.assert_called_once_with(new_password)
    password_service_mock.hash_password.assert_called_once()
    user_repository_mock.update.assert_called_once()
