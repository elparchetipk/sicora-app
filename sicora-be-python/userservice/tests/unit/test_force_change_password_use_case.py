import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from app.application.use_cases.auth_use_cases import ForceChangePasswordUseCase
from app.application.dtos.user_dtos import ForceChangePasswordDTO
from app.domain.entities.user_entity import User
from app.domain.value_objects.email import Email
from app.domain.value_objects.document_number import DocumentNumber
from app.domain.value_objects.document_type import DocumentType
from app.domain.value_objects.user_role import UserRole
from app.domain.exceptions.user_exceptions import (
    UserNotFoundError,
    WeakPasswordError,
    UserInactiveError
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
def force_change_password_use_case(user_repository_mock, password_service_mock, token_service_mock, email_service_mock):
    return ForceChangePasswordUseCase(user_repository_mock, password_service_mock, token_service_mock, email_service_mock)

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
        must_change_password=True,  # User must change password
        phone="1234567890"
    )

async def test_force_change_password_success(force_change_password_use_case, user_repository_mock, password_service_mock, token_service_mock, email_service_mock, sample_user):
    # Arrange
    user_id = sample_user.id
    new_password = "NewStrongPass123!"
    dto = ForceChangePasswordDTO(user_id=user_id, new_password=new_password)

    # Configure mocks
    user_repository_mock.get_by_id.return_value = sample_user
    password_service_mock.is_strong_password.return_value = True
    password_service_mock.hash_password.return_value = "new_hashed_password"

    # Act
    await force_change_password_use_case.execute(dto)

    # Assert
    user_repository_mock.get_by_id.assert_called_once_with(user_id)
    password_service_mock.is_strong_password.assert_called_once_with(new_password)
    password_service_mock.hash_password.assert_called_once_with(new_password)

    # Verify user was updated with new password and must_change_password=False
    user_repository_mock.update.assert_called_once()
    updated_user = user_repository_mock.update.call_args[0][0]
    assert updated_user.hashed_password == "new_hashed_password"
    assert updated_user.must_change_password is False

    # Verify tokens were revoked
    token_service_mock.revoke_all_refresh_tokens_for_user.assert_called_once_with(str(user_id))

    # Verify notification was sent
    email_service_mock.send_password_changed_notification.assert_called_once_with(
        email=sample_user.email.value,
        first_name=sample_user.first_name
    )

async def test_force_change_password_user_not_found(force_change_password_use_case, user_repository_mock):
    # Arrange
    user_id = uuid4()
    new_password = "NewStrongPass123!"
    dto = ForceChangePasswordDTO(user_id=user_id, new_password=new_password)

    # Configure mock to raise UserNotFoundError
    user_repository_mock.get_by_id.side_effect = UserNotFoundError(f"User with ID {user_id} not found")

    # Act & Assert
    with pytest.raises(UserNotFoundError):
        await force_change_password_use_case.execute(dto)

    user_repository_mock.get_by_id.assert_called_once_with(user_id)

async def test_force_change_password_weak_password(force_change_password_use_case, user_repository_mock, password_service_mock, sample_user):
    # Arrange
    user_id = sample_user.id
    weak_password = "weak"
    dto = ForceChangePasswordDTO(user_id=user_id, new_password=weak_password)

    # Configure mocks
    user_repository_mock.get_by_id.return_value = sample_user
    password_service_mock.is_strong_password.return_value = False

    # Act & Assert
    with pytest.raises(WeakPasswordError):
        await force_change_password_use_case.execute(dto)

    user_repository_mock.get_by_id.assert_called_once_with(user_id)
    password_service_mock.is_strong_password.assert_called_once_with(weak_password)
    password_service_mock.hash_password.assert_not_called()
    user_repository_mock.update.assert_not_called()

async def test_force_change_password_inactive_user(force_change_password_use_case, user_repository_mock, sample_user):
    # Arrange
    user_id = sample_user.id
    new_password = "NewStrongPass123!"
    dto = ForceChangePasswordDTO(user_id=user_id, new_password=new_password)

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

    # Configure mock to return inactive user
    user_repository_mock.get_by_id.return_value = inactive_user

    # Act & Assert
    with pytest.raises(UserInactiveError):
        await force_change_password_use_case.execute(dto)

    user_repository_mock.get_by_id.assert_called_once_with(user_id)

async def test_force_change_password_not_required(force_change_password_use_case, user_repository_mock, sample_user):
    # Arrange
    user_id = sample_user.id
    new_password = "NewStrongPass123!"
    dto = ForceChangePasswordDTO(user_id=user_id, new_password=new_password)

    # Create user that doesn't need to change password
    user_no_change_required = User(
        id=sample_user.id,
        first_name=sample_user.first_name,
        last_name=sample_user.last_name,
        email=sample_user.email,
        document_number=sample_user.document_number,
        role=sample_user.role,
        hashed_password=sample_user.hashed_password,
        is_active=sample_user.is_active,
        must_change_password=False,  # No need to change password
        created_at=sample_user.created_at,
        updated_at=sample_user.updated_at,
        last_login_at=sample_user.last_login_at,
        phone=sample_user.phone
    )

    # Configure mock to return user that doesn't need to change password
    user_repository_mock.get_by_id.return_value = user_no_change_required

    # Act
    await force_change_password_use_case.execute(dto)

    # Assert - should still work even if not required
    user_repository_mock.get_by_id.assert_called_once_with(user_id)
    user_repository_mock.update.assert_called_once()
