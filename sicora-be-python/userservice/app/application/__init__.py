"""Application layer for user service."""

from .dtos import (
    CreateUserDTO,
    UpdateUserDTO,
    ChangePasswordDTO,
    UserResponseDTO,
    LoginDTO,
    TokenResponseDTO,
    UserListDTO,
    UserFilterDTO,
)

from .interfaces import (
    PasswordServiceInterface,
    TokenServiceInterface,
    EmailServiceInterface,
)

from .use_cases import (
    LoginUseCase,
    LogoutUseCase,
    RegisterUserUseCase,
    RefreshTokenUseCase,
    CreateUserUseCase,
    GetUserByIdUseCase,
    UpdateUserUseCase,
    ChangePasswordUseCase,
    ActivateUserUseCase,
    DeactivateUserUseCase,
    ListUsersUseCase,
    GetUserDetailUseCase,
    AdminUpdateUserUseCase,
    DeleteUserUseCase,
    BulkUploadUsersUseCase,
)

__all__ = [
    # DTOs
    "CreateUserDTO",
    "UpdateUserDTO",
    "ChangePasswordDTO",
    "UserResponseDTO",
    "LoginDTO",
    "TokenResponseDTO",
    "UserListDTO",
    "UserFilterDTO",
    # Interfaces
    "PasswordServiceInterface",
    "TokenServiceInterface",
    "EmailServiceInterface",
    # Use Cases
    "LoginUseCase",
    "LogoutUseCase",
    "RegisterUserUseCase",
    "RefreshTokenUseCase",
    "CreateUserUseCase",
    "GetUserByIdUseCase",
    "UpdateUserUseCase",
    "ChangePasswordUseCase",
    "ActivateUserUseCase",
    "DeactivateUserUseCase",
    "ListUsersUseCase",
    "GetUserDetailUseCase",
    "AdminUpdateUserUseCase",
    "DeleteUserUseCase",
    "BulkUploadUsersUseCase",
]
