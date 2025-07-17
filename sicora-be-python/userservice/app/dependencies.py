"""Dependency injection configuration for the application."""

from functools import lru_cache
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.config.database import get_db_session
from app.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.infrastructure.repositories.sqlalchemy_refresh_token_repository import SQLAlchemyRefreshTokenRepository  # PASO 6: Added
from app.infrastructure.adapters.bcrypt_password_service import BcryptPasswordService
from app.infrastructure.adapters.jwt_token_service import JWTTokenService
from app.infrastructure.adapters.smtp_email_service import SMTPEmailService

from app.application.interfaces.password_service_interface import PasswordServiceInterface
from app.application.interfaces.token_service_interface import TokenServiceInterface
from app.application.interfaces.email_service_interface import EmailServiceInterface
from app.domain.repositories.user_repository_interface import UserRepositoryInterface
from app.domain.repositories.refresh_token_repository_interface import RefreshTokenRepositoryInterface  # PASO 6: Added

from app.application.use_cases.auth_use_cases import (
    LoginUseCase,
    RegisterUserUseCase,  # PASO 7: Added
    RefreshTokenUseCase,  # PASO 6: Added
    LogoutUseCase,
    ForgotPasswordUseCase,
    ResetPasswordUseCase,
    ForceChangePasswordUseCase,
)
from app.application.use_cases.user_use_cases import (
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
    UpdateProfileUseCase,
)


# Repository dependencies
async def get_user_repository(
    session: AsyncSession = Depends(get_db_session)
) -> UserRepositoryInterface:
    """Get user repository instance."""
    return SQLAlchemyUserRepository(session)


# PASO 6: Refresh token repository dependency
async def get_refresh_token_repository(
    session: AsyncSession = Depends(get_db_session)
) -> RefreshTokenRepositoryInterface:
    """Get refresh token repository instance."""
    return SQLAlchemyRefreshTokenRepository(session)


# Service dependencies
@lru_cache()
def get_password_service() -> PasswordServiceInterface:
    """Get password service instance."""
    return BcryptPasswordService()


@lru_cache()
def get_token_service() -> TokenServiceInterface:
    """Get token service instance."""
    return JWTTokenService()


@lru_cache()
def get_email_service() -> EmailServiceInterface:
    """Get email service instance."""
    return SMTPEmailService()


# Use case dependencies - Authentication
def get_login_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    refresh_token_repository: RefreshTokenRepositoryInterface = Depends(get_refresh_token_repository),  # PASO 6: Added
    password_service: PasswordServiceInterface = Depends(get_password_service),
    token_service: TokenServiceInterface = Depends(get_token_service)
) -> LoginUseCase:
    """Get login use case instance."""
    return LoginUseCase(user_repository, refresh_token_repository, password_service, token_service)  # PASO 6: Updated


def get_refresh_token_use_case(  # PASO 6: Added
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    refresh_token_repository: RefreshTokenRepositoryInterface = Depends(get_refresh_token_repository),
    token_service: TokenServiceInterface = Depends(get_token_service)
) -> RefreshTokenUseCase:  # PASO 6: Added
    """Get refresh token use case instance."""
    return RefreshTokenUseCase(user_repository, refresh_token_repository, token_service)  # PASO 6: Added


def get_logout_use_case(
    token_service: TokenServiceInterface = Depends(get_token_service),
    refresh_token_repository: RefreshTokenRepositoryInterface = Depends(get_refresh_token_repository)
) -> LogoutUseCase:
    """Get logout use case instance."""
    return LogoutUseCase(token_service, refresh_token_repository)


# TODO: Implement ValidateTokenUseCase
# def get_validate_token_use_case(
#     token_service: TokenServiceInterface = Depends(get_token_service),
#     user_repository: UserRepositoryInterface = Depends(get_user_repository)
# ) -> ValidateTokenUseCase:
#     """Get validate token use case instance."""
#     return ValidateTokenUseCase(token_service, user_repository)


def get_change_password_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    password_service: PasswordServiceInterface = Depends(get_password_service),
    email_service: EmailServiceInterface = Depends(get_email_service)
) -> ChangePasswordUseCase:
    """Get change password use case instance."""
    return ChangePasswordUseCase(user_repository, password_service, email_service)


# Use case dependencies - User Management
def get_create_user_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    password_service: PasswordServiceInterface = Depends(get_password_service),
    email_service: EmailServiceInterface = Depends(get_email_service)
) -> CreateUserUseCase:
    """Get create user use case instance."""
    return CreateUserUseCase(user_repository, password_service, email_service)


def get_get_user_by_id_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> GetUserByIdUseCase:
    """Get get user by id use case instance."""
    return GetUserByIdUseCase(user_repository)


def get_update_user_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> UpdateUserUseCase:
    """Get update user use case instance."""
    return UpdateUserUseCase(user_repository)


def get_activate_user_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> ActivateUserUseCase:
    """Get activate user use case instance."""
    return ActivateUserUseCase(user_repository)


def get_deactivate_user_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    email_service: EmailServiceInterface = Depends(get_email_service)
) -> DeactivateUserUseCase:
    """Get deactivate user use case instance."""
    return DeactivateUserUseCase(user_repository, email_service)


def get_list_users_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> ListUsersUseCase:
    """Get list users use case instance."""
    return ListUsersUseCase(user_repository)


# PASO 4: Dependencias para casos de uso de administración avanzada

def get_get_user_detail_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> GetUserDetailUseCase:
    """Get user detail use case instance."""
    return GetUserDetailUseCase(user_repository)


def get_admin_update_user_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    password_service: PasswordServiceInterface = Depends(get_password_service),
    email_service: EmailServiceInterface = Depends(get_email_service)
) -> AdminUpdateUserUseCase:
    """Get admin update user use case instance."""
    return AdminUpdateUserUseCase(user_repository, password_service, email_service)


def get_delete_user_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    email_service: EmailServiceInterface = Depends(get_email_service)
) -> DeleteUserUseCase:
    """Get delete user use case instance."""
    return DeleteUserUseCase(user_repository, email_service)


def get_bulk_upload_users_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    password_service: PasswordServiceInterface = Depends(get_password_service),
    email_service: EmailServiceInterface = Depends(get_email_service)
) -> BulkUploadUsersUseCase:
    """Get bulk upload users use case instance."""
    return BulkUploadUsersUseCase(user_repository, password_service, email_service)


# PASO 5: Dependencias para funcionalidades de autenticación críticas - Comentadas (casos de uso no implementados)

# def get_forgot_password_use_case(
#     user_repository: UserRepositoryInterface = Depends(get_user_repository),
#     email_service: EmailServiceInterface = Depends(get_email_service)
# ) -> ForgotPasswordUseCase:
#     """Get forgot password use case instance."""
#     return ForgotPasswordUseCase(user_repository, email_service)


# def get_reset_password_use_case(
#     user_repository: UserRepositoryInterface = Depends(get_user_repository),
#     password_service: PasswordServiceInterface = Depends(get_password_service),
#     token_service: TokenServiceInterface = Depends(get_token_service),
#     email_service: EmailServiceInterface = Depends(get_email_service)
# ) -> ResetPasswordUseCase:
#     """Get reset password use case instance."""
#     return ResetPasswordUseCase(user_repository, password_service, token_service, email_service)


# def get_force_change_password_use_case(
#     user_repository: UserRepositoryInterface = Depends(get_user_repository),
#     password_service: PasswordServiceInterface = Depends(get_password_service),
#     token_service: TokenServiceInterface = Depends(get_token_service),
#     email_service: EmailServiceInterface = Depends(get_email_service)
# ) -> ForceChangePasswordUseCase:
#     """Get force change password use case instance."""
#     return ForceChangePasswordUseCase(user_repository, password_service, token_service, email_service)


# PASO 7: Register User Use Case dependency
def get_register_user_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    refresh_token_repository: RefreshTokenRepositoryInterface = Depends(get_refresh_token_repository),
    password_service: PasswordServiceInterface = Depends(get_password_service),
    token_service: TokenServiceInterface = Depends(get_token_service),
    email_service: EmailServiceInterface = Depends(get_email_service)
) -> RegisterUserUseCase:
    """Get register user use case instance."""
    return RegisterUserUseCase(
        user_repository, 
        refresh_token_repository, 
        password_service, 
        token_service, 
        email_service
    )


# PASO FINAL: Additional dependencies for complete auth functionality

def get_update_profile_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> UpdateProfileUseCase:
    """Get update profile use case instance."""
    return UpdateProfileUseCase(user_repository)

def get_forgot_password_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    token_service: TokenServiceInterface = Depends(get_token_service),
    email_service: EmailServiceInterface = Depends(get_email_service)
) -> ForgotPasswordUseCase:
    """Get forgot password use case instance."""
    return ForgotPasswordUseCase(user_repository, token_service, email_service)

def get_reset_password_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    password_service: PasswordServiceInterface = Depends(get_password_service),
    token_service: TokenServiceInterface = Depends(get_token_service),
    email_service: EmailServiceInterface = Depends(get_email_service)
) -> ResetPasswordUseCase:
    """Get reset password use case instance."""
    return ResetPasswordUseCase(user_repository, password_service, token_service, email_service)

def get_force_change_password_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    password_service: PasswordServiceInterface = Depends(get_password_service),
    token_service: TokenServiceInterface = Depends(get_token_service),
    email_service: EmailServiceInterface = Depends(get_email_service)
) -> ForceChangePasswordUseCase:
    """Get force change password use case instance."""
    return ForceChangePasswordUseCase(user_repository, password_service, token_service, email_service)
