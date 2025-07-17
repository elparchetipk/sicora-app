import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from app.application.use_cases.auth_use_cases import ForgotPasswordUseCase
from app.application.dtos.user_dtos import ForgotPasswordDTO
from app.domain.entities.user_entity import User
from app.domain.value_objects.email import Email
from app.domain.value_objects.document_number import DocumentNumber
from app.domain.value_objects.document_type import DocumentType
from app.domain.value_objects.user_role import UserRole
from app.domain.exceptions.user_exceptions import UserNotFoundError

@pytest.fixture
def user_repository_mock():
    repository = AsyncMock()
    return repository

@pytest.fixture
def token_service_mock():
    service = AsyncMock()
    return service

@pytest.fixture
def email_service_mock():
    service = AsyncMock()
    return service

@pytest.fixture
def forgot_password_use_case(user_repository_mock, token_service_mock, email_service_mock):
    return ForgotPasswordUseCase(user_repository_mock, token_service_mock, email_service_mock)

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

async def test_forgot_password_success(forgot_password_use_case, user_repository_mock, token_service_mock, email_service_mock, sample_user):
    # Arrange
    email = "john.doe@example.com"
    dto = ForgotPasswordDTO(email=email)

    # Configure mocks
    user_repository_mock.get_by_email.return_value = sample_user
    token_service_mock.generate_password_reset_token.return_value = "reset_token_123"

    # Act
    await forgot_password_use_case.execute(dto)

    # Assert
    user_repository_mock.get_by_email.assert_called_once_with(email)
    token_service_mock.generate_password_reset_token.assert_called_once_with(str(sample_user.id))
    email_service_mock.send_password_reset_email.assert_called_once_with(
        email=email,
        first_name=sample_user.first_name,
        reset_token="reset_token_123"
    )

async def test_forgot_password_user_not_found(forgot_password_use_case, user_repository_mock, token_service_mock, email_service_mock):
    # Arrange
    email = "nonexistent@example.com"
    dto = ForgotPasswordDTO(email=email)

    # Configure mock to return None (user not found)
    user_repository_mock.get_by_email.return_value = None

    # Act
    await forgot_password_use_case.execute(dto)

    # Assert
    user_repository_mock.get_by_email.assert_called_once_with(email)
    # No token should be generated and no email should be sent
    token_service_mock.generate_password_reset_token.assert_not_called()
    email_service_mock.send_password_reset_email.assert_not_called()

async def test_forgot_password_inactive_user(forgot_password_use_case, user_repository_mock, token_service_mock, email_service_mock, sample_user):
    # Arrange
    email = "inactive@example.com"
    dto = ForgotPasswordDTO(email=email)

    # Create inactive user
    inactive_user = User(
        id=sample_user.id,
        first_name=sample_user.first_name,
        last_name=sample_user.last_name,
        email=Email(email),
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

    # Configure mock to return inactive user
    user_repository_mock.get_by_email.return_value = inactive_user

    # Act
    await forgot_password_use_case.execute(dto)

    # Assert
    user_repository_mock.get_by_email.assert_called_once_with(email)
    # No token should be generated and no email should be sent for inactive users
    token_service_mock.generate_password_reset_token.assert_not_called()
    email_service_mock.send_password_reset_email.assert_not_called()

async def test_forgot_password_email_service_failure(forgot_password_use_case, user_repository_mock, token_service_mock, email_service_mock, sample_user):
    # Arrange
    email = "john.doe@example.com"
    dto = ForgotPasswordDTO(email=email)

    # Configure mocks
    user_repository_mock.get_by_email.return_value = sample_user
    token_service_mock.generate_password_reset_token.return_value = "reset_token_123"
    email_service_mock.send_password_reset_email.side_effect = Exception("Email service failure")

    # Act & Assert
    # The use case should handle email service failures gracefully
    # It should not raise an exception to the caller
    await forgot_password_use_case.execute(dto)

    # Verify that the token was generated but email sending failed
    user_repository_mock.get_by_email.assert_called_once_with(email)
    token_service_mock.generate_password_reset_token.assert_called_once_with(str(sample_user.id))
    email_service_mock.send_password_reset_email.assert_called_once()
