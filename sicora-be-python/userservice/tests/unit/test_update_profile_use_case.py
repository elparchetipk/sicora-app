import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from app.application.use_cases.user_use_cases import UpdateProfileUseCase
from app.application.dtos.user_dtos import UpdateProfileDTO
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
def update_profile_use_case(user_repository_mock):
    return UpdateProfileUseCase(user_repository_mock)

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

async def test_update_profile_success(update_profile_use_case, user_repository_mock, sample_user):
    # Arrange
    user_id = sample_user.id
    dto = UpdateProfileDTO(
        first_name="Jane",
        last_name="Smith",
        phone="9876543210"
    )

    # Configure mock to return our sample user when get_by_id is called
    user_repository_mock.get_by_id.return_value = sample_user

    # Configure mock to return updated user when update is called
    # Create a new user object with updated values
    updated_user = User(
        id=sample_user.id,
        first_name="Jane",
        last_name="Smith",
        email=sample_user.email,
        document_number=sample_user.document_number,
        role=sample_user.role,
        hashed_password=sample_user.hashed_password,
        is_active=sample_user.is_active,
        must_change_password=sample_user.must_change_password,
        created_at=sample_user.created_at,
        updated_at=sample_user.updated_at,
        last_login_at=sample_user.last_login_at,
        phone="9876543210"
    )
    user_repository_mock.update.return_value = updated_user

    # Act
    result = await update_profile_use_case.execute(user_id, dto)

    # Assert
    user_repository_mock.get_by_id.assert_called_once_with(user_id)
    user_repository_mock.update.assert_called_once()
    assert result.first_name == "Jane"
    assert result.last_name == "Smith"
    assert result.phone == "9876543210"
    # Verify other fields remain unchanged
    assert result.email == sample_user.email.value
    assert result.document_number == sample_user.document_number.value
    assert result.role == sample_user.role.value

async def test_update_profile_user_not_found(update_profile_use_case, user_repository_mock):
    # Arrange
    user_id = uuid4()
    dto = UpdateProfileDTO(
        first_name="Jane",
        last_name="Smith",
        phone="9876543210"
    )

    # Configure mock to raise UserNotFoundError
    user_repository_mock.get_by_id.side_effect = UserNotFoundError(f"User with ID {user_id} not found")

    # Act & Assert
    with pytest.raises(UserNotFoundError):
        await update_profile_use_case.execute(user_id, dto)

    user_repository_mock.get_by_id.assert_called_once_with(user_id)
    user_repository_mock.update.assert_not_called()

async def test_update_profile_partial_update(update_profile_use_case, user_repository_mock, sample_user):
    # Arrange
    user_id = sample_user.id
    # Only update first_name, leaving other fields unchanged
    dto = UpdateProfileDTO(
        first_name="Jane",
        last_name=None,
        phone=None
    )

    # Configure mock to return our sample user when get_by_id is called
    user_repository_mock.get_by_id.return_value = sample_user

    # Configure mock to return updated user when update is called
    # Create a new user object with updated values
    updated_user = User(
        id=sample_user.id,
        first_name="Jane",
        last_name=sample_user.last_name,
        email=sample_user.email,
        document_number=sample_user.document_number,
        role=sample_user.role,
        hashed_password=sample_user.hashed_password,
        is_active=sample_user.is_active,
        must_change_password=sample_user.must_change_password,
        created_at=sample_user.created_at,
        updated_at=sample_user.updated_at,
        last_login_at=sample_user.last_login_at,
        phone=sample_user.phone
    )
    user_repository_mock.update.return_value = updated_user

    # Act
    result = await update_profile_use_case.execute(user_id, dto)

    # Assert
    user_repository_mock.get_by_id.assert_called_once_with(user_id)
    user_repository_mock.update.assert_called_once()
    assert result.first_name == "Jane"
    assert result.last_name == sample_user.last_name  # Unchanged
    assert result.phone == sample_user.phone  # Unchanged
