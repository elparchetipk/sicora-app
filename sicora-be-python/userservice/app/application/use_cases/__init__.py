"""Use cases module for application layer."""

from .auth_use_cases import (
    LoginUseCase,
    RegisterUserUseCase,  # PASO 7: Added
    RefreshTokenUseCase,  # PASO 6: Added
    LogoutUseCase,
    # PASO 5: Critical auth use cases - commented out as not implemented
    # ForgotPasswordUseCase,
    # ResetPasswordUseCase,
    # ForceChangePasswordUseCase,
)

from .user_use_cases import (
    CreateUserUseCase,
    GetUserByIdUseCase,
    UpdateUserUseCase,
    ChangePasswordUseCase,
    ActivateUserUseCase,
    DeactivateUserUseCase,
    ListUsersUseCase,
    # PASO 4: Nuevos casos de uso para administración avanzada
    GetUserDetailUseCase,
    AdminUpdateUserUseCase,
    DeleteUserUseCase,
    BulkUploadUsersUseCase,
)

__all__ = [
    # Auth use cases
    "LoginUseCase",
    "RegisterUserUseCase",  # PASO 7: Added
    "RefreshTokenUseCase",  # PASO 6: Added
    "LogoutUseCase",
    # "ValidateTokenUseCase",  # Not implemented yet
    # PASO 5: Critical auth use cases - commented out as not implemented
    # "ForgotPasswordUseCase",
    # "ResetPasswordUseCase",
    # "ForceChangePasswordUseCase",
    # User use cases
    "CreateUserUseCase",
    "GetUserByIdUseCase",
    "UpdateUserUseCase",
    "ChangePasswordUseCase",
    "ActivateUserUseCase",
    "DeactivateUserUseCase",
    "ListUsersUseCase",
    # PASO 4: Casos de uso de administración avanzada
    "GetUserDetailUseCase",
    "AdminUpdateUserUseCase",
    "DeleteUserUseCase",
    "BulkUploadUsersUseCase",
]
