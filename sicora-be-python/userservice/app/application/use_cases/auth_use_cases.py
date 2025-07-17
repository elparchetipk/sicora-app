"""Authentication use cases for user service."""

import secrets
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from ...domain import (
    UserRepositoryInterface, 
    RefreshTokenRepositoryInterface,
    User, 
    RefreshToken,
    Email,
    DocumentNumber,
    DocumentType,
    UserRole,
    AuthenticationError,
    UserNotFoundError,
    UserAlreadyExistsError,
    UserInactiveError,
    InvalidPasswordError,
    WeakPasswordError,
    InvalidTokenError,
)
from ..interfaces import PasswordServiceInterface, TokenServiceInterface, EmailServiceInterface
from ..dtos import (
    LoginDTO, 
    TokenResponseDTO, 
    RefreshTokenDTO,
    RefreshTokenResponseDTO,
    CreateUserDTO,  # PASO 7: Added for registration
    UserResponseDTO,
    ForgotPasswordDTO,
    ResetPasswordDTO,
    ForceChangePasswordDTO,
)


class LoginUseCase:
    """Use case for user authentication."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        refresh_token_repository: RefreshTokenRepositoryInterface,  # PASO 6: Added
        password_service: PasswordServiceInterface,
        token_service: TokenServiceInterface,
    ):
        self._user_repository = user_repository
        self._refresh_token_repository = refresh_token_repository  # PASO 6: Added
        self._password_service = password_service
        self._token_service = token_service
    
    async def execute(self, login_data: LoginDTO) -> TokenResponseDTO:
        """Execute user login."""
        # Validate email format
        try:
            email = Email(login_data.email)
        except Exception as e:
            raise AuthenticationError("Invalid email format") from e
        
        # Get user by email
        user = await self._user_repository.get_by_email(email.value)
        if not user:
            raise AuthenticationError("Invalid credentials")
        
        # Check if user is active
        if not user.is_active:
            raise UserInactiveError(str(user.id))
        
        # Verify password
        if not self._password_service.verify_password(login_data.password, user.hashed_password):
            raise AuthenticationError("Invalid credentials")
        
        # Record login
        user.record_login()
        await self._user_repository.update(user)
        
        # Create tokens
        access_token = self._token_service.create_access_token(
            user_id=user.id,
            role=user.role.value
        )
        
        # PASO 6: Create and save refresh token
        refresh_token = RefreshToken.create_for_user(user.id)
        await self._refresh_token_repository.save(refresh_token)
        
        # Create user response DTO
        user_response = UserResponseDTO(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email.value,
            document_number=user.document_number.value,
            document_type=user.document_number.document_type.value,
            role=user.role.value,
            is_active=user.is_active,
            must_change_password=user.must_change_password,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login_at=user.last_login_at,
        )
        
        return TokenResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token.token,  # PASO 6: Added
            token_type="bearer",
            expires_in=3600,  # 1 hour
            user=user_response,
        )


# PASO 6: Refresh Token Use Case for HU-BE-003

class RefreshTokenUseCase:
    """Use case for refreshing access tokens (HU-BE-003)."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        refresh_token_repository: RefreshTokenRepositoryInterface,
        token_service: TokenServiceInterface,
    ):
        self._user_repository = user_repository
        self._refresh_token_repository = refresh_token_repository
        self._token_service = token_service
    
    async def execute(self, refresh_data: RefreshTokenDTO) -> RefreshTokenResponseDTO:
        """Refresh access token using valid refresh token."""
        # Get refresh token from repository
        refresh_token = await self._refresh_token_repository.get_by_token(refresh_data.refresh_token)
        if not refresh_token:
            raise InvalidTokenError("Invalid refresh token")
        
        # Validate refresh token
        try:
            refresh_token.validate_for_refresh()
        except InvalidTokenError:
            # Clean up invalid token
            await self._refresh_token_repository.delete(refresh_token.id)
            raise
        
        # Get user
        user = await self._user_repository.get_by_id(refresh_token.user_id)
        if not user:
            raise UserNotFoundError(f"User not found: {refresh_token.user_id}")
        
        # Check if user is still active
        if not user.is_active:
            # Revoke all tokens for inactive user
            await self._refresh_token_repository.revoke_all_user_tokens(user.id)
            raise UserInactiveError(f"User account is inactive: {user.id}")
        
        # Mark token as used
        refresh_token.mark_as_used()
        
        # Create new access token
        access_token = self._token_service.create_access_token(
            user_id=user.id,
            role=user.role.value,
            expires_delta=3600  # 1 hour
        )
        
        # Rotate refresh token (create new one and revoke old one)
        new_refresh_token = refresh_token.rotate()
        await self._refresh_token_repository.save(new_refresh_token)
        
        # Update the used token in repository
        await self._refresh_token_repository.update(refresh_token)
        
        return RefreshTokenResponseDTO(
            access_token=access_token,
            refresh_token=new_refresh_token.token,
            token_type="bearer",
            expires_in=3600,  # 1 hour
        )


# PASO 7: Register User Use Case for HU-BE-001

class RegisterUserUseCase:
    """Use case for user registration (HU-BE-001)."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        refresh_token_repository: RefreshTokenRepositoryInterface,
        password_service: PasswordServiceInterface,
        token_service: TokenServiceInterface,
        email_service: EmailServiceInterface,
    ):
        self._user_repository = user_repository
        self._refresh_token_repository = refresh_token_repository
        self._password_service = password_service
        self._token_service = token_service
        self._email_service = email_service
    
    async def execute(self, user_data: CreateUserDTO) -> TokenResponseDTO:
        """Register a new user and return authentication tokens."""
        # Check if email already exists
        existing_user = await self._user_repository.get_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsError("email", user_data.email)
        
        # Check if document number already exists  
        existing_doc = await self._user_repository.get_by_document_number(user_data.document_number)
        if existing_doc:
            raise UserAlreadyExistsError("document_number", user_data.document_number)
        
        # Validate password strength (assume basic validation for now)
        if len(user_data.password) < 8:
            raise WeakPasswordError("Password must be at least 8 characters")
        
        # Hash password
        hashed_password = self._password_service.hash_password(user_data.password)
        
        # Create user entity
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=Email(user_data.email),
            document_number=DocumentNumber(user_data.document_number, user_data.document_type),
            hashed_password=hashed_password,
            role=user_data.role,
            must_change_password=False  # Public registration doesn't require password change
        )
        
        # Save user
        created_user = await self._user_repository.create(user)
        
        # Create access token
        access_token = self._token_service.create_access_token(
            user_id=created_user.id,
            role=created_user.role.value
        )
        
        # Create and save refresh token
        refresh_token = RefreshToken.create_for_user(created_user.id)
        await self._refresh_token_repository.save(refresh_token)
        
        # Send welcome email (optional)
        try:
            await self._email_service.send_welcome_email(
                to_email=created_user.email.value,
                user_name=created_user.first_name,
                temporary_password=""  # No temporary password for registration
            )
        except Exception:
            # Don't fail registration if email fails
            pass
        
        # Create user response
        user_response = UserResponseDTO(
            id=created_user.id,
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            email=created_user.email.value,
            document_number=created_user.document_number.value,
            document_type=created_user.document_number.document_type.value,
            role=created_user.role.value,
            is_active=created_user.is_active,
            must_change_password=created_user.must_change_password,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at,
            last_login_at=created_user.last_login_at,
            phone=created_user.phone,
        )
        
        return TokenResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token.token,
            token_type="bearer",
            expires_in=3600,  # 1 hour
            user=user_response,
        )


# PASO 7: Logout Use Case for HU-BE-004

class LogoutUseCase:
    """Use case for user logout with refresh token management (HU-BE-004)."""
    
    def __init__(
        self,
        token_service: TokenServiceInterface,
        refresh_token_repository: RefreshTokenRepositoryInterface,
    ):
        self._token_service = token_service
        self._refresh_token_repository = refresh_token_repository
    
    async def execute(self, access_token: str, refresh_token: Optional[str] = None) -> None:
        """Execute user logout by revoking tokens."""
        # Revoke access token (add to blacklist)
        self._token_service.revoke_token(access_token)
        
        # If refresh token provided, revoke it specifically
        if refresh_token:
            await self._refresh_token_repository.revoke_token(refresh_token)
        else:
            # If no specific refresh token, get user from access token and revoke all
            try:
                token_data = self._token_service.decode_token(access_token)
                user_id = token_data.get("sub")
                if user_id:
                    # Revoke all refresh tokens for the user
                    await self._refresh_token_repository.revoke_all_user_tokens(UUID(user_id))
            except Exception:
                # If token is invalid or expired, still continue
                pass


# PASO FINAL: Password Management Use Cases

class ForgotPasswordUseCase:
    """Use case for handling password reset requests."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        token_service: TokenServiceInterface,
        email_service: EmailServiceInterface
    ):
        self._user_repository = user_repository
        self._token_service = token_service
        self._email_service = email_service
    
    async def execute(self, forgot_data: ForgotPasswordDTO) -> None:
        """Send password reset email if user exists."""
        # Find user by email
        user = await self._user_repository.get_by_email(forgot_data.email)
        
        # For security, don't reveal if email exists or not
        if user and user.is_active:
            # Create password reset token
            reset_token = self._token_service.create_password_reset_token(user.id)
            
            # Send password reset email
            try:
                await self._email_service.send_password_reset_email(
                    to_email=user.email.value,
                    user_name=user.first_name,
                    reset_token=reset_token
                )
            except Exception:
                # Log error but don't fail the request
                pass
        
        # Always return success for security (don't reveal if email exists)


class ResetPasswordUseCase:
    """Use case for resetting password with reset token."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        password_service: PasswordServiceInterface,
        token_service: TokenServiceInterface,
        email_service: EmailServiceInterface
    ):
        self._user_repository = user_repository
        self._password_service = password_service
        self._token_service = token_service
        self._email_service = email_service
    
    async def execute(self, reset_data: ResetPasswordDTO) -> None:
        """Reset user password using valid reset token."""
        # Validate reset token
        if not self._token_service.validate_password_reset_token(reset_data.token):
            raise InvalidTokenError("Invalid or expired reset token")
        
        # Get user ID from token
        try:
            user_id_str = self._token_service.get_user_id_from_reset_token(reset_data.token)
            user_id = UUID(user_id_str)
        except (ValueError, TypeError):
            raise InvalidTokenError("Invalid token format")
        
        # Get user
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("id", str(user_id))
        
        if not user.is_active:
            raise UserInactiveError(str(user_id))
        
        # Validate new password strength
        if len(reset_data.new_password) < 8:
            raise WeakPasswordError("Password must be at least 8 characters")
        
        # Hash new password and update user
        hashed_password = self._password_service.hash_password(reset_data.new_password)
        user.change_password(hashed_password)
        
        # Save user
        await self._user_repository.update(user)
        
        # Send confirmation email
        try:
            await self._email_service.send_password_changed_notification(
                to_email=user.email.value,
                user_name=user.first_name
            )
        except Exception:
            # Don't fail if email sending fails
            pass


class ForceChangePasswordUseCase:
    """Use case for forced password changes."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        password_service: PasswordServiceInterface,
        token_service: TokenServiceInterface,
        email_service: EmailServiceInterface
    ):
        self._user_repository = user_repository
        self._password_service = password_service
        self._token_service = token_service
        self._email_service = email_service
    
    async def execute(self, force_change_data: ForceChangePasswordDTO) -> None:
        """Force change password for users who must change password."""
        # Get user
        user = await self._user_repository.get_by_id(force_change_data.user_id)
        if not user:
            raise UserNotFoundError("id", str(force_change_data.user_id))
        
        if not user.is_active:
            raise UserInactiveError(str(force_change_data.user_id))
        
        if not user.must_change_password:
            raise InvalidPasswordError("Password change not required for this user")
        
        # Validate new password strength
        if len(force_change_data.new_password) < 8:
            raise WeakPasswordError("Password must be at least 8 characters")
        
        # Hash new password and update user
        hashed_password = self._password_service.hash_password(force_change_data.new_password)
        user.change_password(hashed_password)
        user.clear_must_change_password()  # Clear the forced change flag
        
        # Save user
        await self._user_repository.update(user)
        
        # Revoke all existing tokens for security
        self._token_service.revoke_all_user_tokens(user.id)
        
        # Send notification email
        try:
            await self._email_service.send_password_changed_notification(
                to_email=user.email.value,
                user_name=user.first_name
            )
        except Exception:
            # Don't fail if email sending fails
            pass


# PASO FINAL: Token Validation Use Case

class ValidateTokenUseCase:
    """Use case for validating JWT tokens."""
    
    def __init__(
        self,
        token_service: TokenServiceInterface,
        user_repository: UserRepositoryInterface
    ):
        self._token_service = token_service
        self._user_repository = user_repository
    
    async def execute(self, token: str) -> UserResponseDTO:
        """Validate token and return user information."""
        try:
            # Decode and validate token
            payload = self._token_service.decode_token(token)
            user_id = UUID(payload.get("sub"))
            
            # Check if token is revoked
            if self._token_service.is_token_revoked(token):
                raise InvalidTokenError("Token has been revoked")
            
            # Get user from database
            user = await self._user_repository.get_by_id(user_id)
            if not user:
                raise UserNotFoundError("id", str(user_id))
            
            if not user.is_active:
                raise UserInactiveError(str(user_id))
            
            # Return user information
            return UserResponseDTO(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email.value,
                document_number=user.document_number.value,
                document_type=user.document_number.document_type.value,
                role=user.role.value,
                is_active=user.is_active,
                must_change_password=user.must_change_password,
                created_at=user.created_at,
                updated_at=user.updated_at,
                last_login_at=user.last_login_at,
                phone=user.phone,
            )
            
        except (ValueError, KeyError) as e:
            raise InvalidTokenError(f"Invalid token format: {e}")
        except Exception as e:
            raise InvalidTokenError(f"Token validation failed: {e}")
