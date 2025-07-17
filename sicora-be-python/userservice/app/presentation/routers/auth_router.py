from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Optional
from uuid import UUID

from app.dependencies import (
    get_login_use_case,
    get_register_user_use_case,  # PASO 7: Added
    get_refresh_token_use_case,  # PASO 6: Added
    get_logout_use_case,
    # get_validate_token_use_case,  # PASO FINAL: Added - COMMENTED: Use case not implemented
    get_change_password_use_case,  # PASO FINAL: Added
    get_update_profile_use_case,  # PASO FINAL: Added
    get_forgot_password_use_case,  # PASO FINAL: Added
    get_reset_password_use_case,  # PASO FINAL: Added
    get_force_change_password_use_case,  # PASO FINAL: Added
)
from app.application.use_cases.auth_use_cases import (
    LoginUseCase,
    RegisterUserUseCase,  # PASO 7: Added
    RefreshTokenUseCase,  # PASO 6: Added
    LogoutUseCase,
    # ValidateTokenUseCase,  # PASO FINAL: Added - COMMENTED: Use case not implemented
    ForgotPasswordUseCase,  # PASO FINAL: Added
    ResetPasswordUseCase,  # PASO FINAL: Added
    ForceChangePasswordUseCase,  # PASO FINAL: Added
)
from app.application.use_cases.user_use_cases import (
    ChangePasswordUseCase,  # PASO FINAL: Added
    UpdateProfileUseCase,  # PASO FINAL: Added
)
from app.application.dtos.user_dtos import (
    LoginDTO,
    TokenResponseDTO,
    RefreshTokenDTO,  # PASO 6: Added
    CreateUserDTO,  # PASO 7: Added
    UserResponseDTO,  # PASO 7: Added
    ChangePasswordDTO,  # PASO FINAL: Added
    UpdateProfileDTO,  # PASO FINAL: Added
    ForgotPasswordDTO,
    ResetPasswordDTO,
    ForceChangePasswordDTO,
)
from app.presentation.schemas.user_schemas import (
    LoginRequest,
    LoginResponse,
    CreateUserRequest,  # PASO 7: Added
    LogoutRequest,  # PASO 7: Added
    ChangePasswordRequest,  # PASO FINAL: Added
    UpdateProfileRequest,  # PASO FINAL: Added
    RefreshTokenRequest,  # PASO 6: Added
    RefreshTokenResponse,  # PASO 6: Added
    MessageResponse,
    UserResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ForceChangePasswordRequest,
)
from app.presentation.dependencies.auth import get_current_user, get_current_active_user
from app.domain.entities.user_entity import User
from app.domain.exceptions.user_exceptions import (
    AuthenticationError,
    UserNotFoundError,
    UserAlreadyExistsError,  # PASO 7: Added
    InvalidTokenError,
    WeakPasswordError,
    UserInactiveError,
    InvalidPasswordError,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
async def login(
    login_request: LoginRequest,
    login_use_case: Annotated[LoginUseCase, Depends(get_login_use_case)]
):
    """
    Autenticar usuario y obtener tokens de acceso.

    - **email**: Email del usuario
    - **password**: Contraseña del usuario
    """
    try:
        login_dto = LoginDTO(
            email=login_request.email,
            password=login_request.password
        )
        result = await login_use_case.execute(login_dto)

        return LoginResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,  # PASO 6: Added
            token_type=result.token_type,
            expires_in=result.expires_in,
            user=UserResponse(
                id=result.user.id,
                first_name=result.user.first_name,
                last_name=result.user.last_name,
                email=result.user.email,
                document_number=result.user.document_number,
                document_type=result.user.document_type,
                role=result.user.role,
                is_active=result.user.is_active,
                must_change_password=result.user.must_change_password,
                created_at=result.user.created_at,
                updated_at=result.user.updated_at,
                last_login_at=result.user.last_login_at,
                phone=result.user.phone,
            )
        )
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )


# PASO 7: Updated logout endpoint for HU-BE-004
@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user: Annotated[User, Depends(get_current_user)],
    logout_use_case: Annotated[LogoutUseCase, Depends(get_logout_use_case)],
    request: Optional[LogoutRequest] = None  # Optional request body
):
    """
    Log out the current user and revoke tokens.

    Optionally accepts:
    - **refresh_token**: Specific refresh token to revoke (optional)

    If no refresh token provided, all user's refresh tokens will be revoked.
    """
    try:
        # Get the access token from the Authorization header
        # This would normally be extracted from the bearer token used for authentication
        access_token = getattr(current_user, '_access_token', None)
        refresh_token = request.refresh_token if request else None

        await logout_use_case.execute(
            access_token=access_token or "placeholder", 
            refresh_token=refresh_token
        )

        return MessageResponse(message="Successfully logged out")

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during logout"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Obtener el perfil del usuario autenticado.
    """
    from app.application.dtos.user_dtos import UserResponseDTO

    return UserResponseDTO(
        id=current_user.id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email.value,
        document_number=current_user.document_number.value,
        document_type=current_user.document_number.document_type.value,
        role=current_user.role.value,
        is_active=current_user.is_active,
        must_change_password=current_user.must_change_password,
        phone=current_user.phone,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        last_login_at=current_user.last_login_at
    )


# COMMENTED: ValidateTokenUseCase not implemented
# @router.post("/validate", response_model=UserResponse)
# async def validate_token(
#     validate_use_case: Annotated[ValidateTokenUseCase, Depends(get_validate_token_use_case)],
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     """
#     Validar token y obtener información del usuario.
#     """
#     return UserResponseDTO(
#         id=current_user.id,
#         first_name=current_user.first_name,
#         last_name=current_user.last_name,
#         email=current_user.email.value,
#         document_number=current_user.document_number.value,
#         document_type=current_user.document_number.document_type.value,
#         role=current_user.role.value,
#         is_active=current_user.is_active,
#         must_change_password=current_user.must_change_password,
#         phone=current_user.phone,
#         created_at=current_user.created_at,
#         updated_at=current_user.updated_at,
#         last_login_at=current_user.last_login_at
#     )


# PASO 6: Refresh token endpoint for HU-BE-003
@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    refresh_token_use_case: Annotated[RefreshTokenUseCase, Depends(get_refresh_token_use_case)]
):
    """
    Refresh access token using valid refresh token.

    - **refresh_token**: Valid refresh token to exchange for new access token
    """
    try:
        refresh_dto = RefreshTokenDTO(
            refresh_token=request.refresh_token
        )
        result = await refresh_token_use_case.execute(refresh_dto)

        return RefreshTokenResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            token_type=result.token_type,
            expires_in=result.expires_in
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except UserInactiveError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )


# PASO 7: Register endpoint for HU-BE-001
@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: CreateUserRequest,
    register_use_case: Annotated[RegisterUserUseCase, Depends(get_register_user_use_case)]
):
    """
    Register a new user account.

    - **first_name**: User's first name (2-100 characters)
    - **last_name**: User's last name (2-100 characters)
    - **email**: User's email address (must be unique)
    - **document_number**: User's document number (must be unique)
    - **document_type**: Type of document (CC, TI, etc.)
    - **password**: User's password (minimum 8 characters)
    - **role**: User's role in the system
    - **phone**: User's phone number (optional)
    """
    try:
        create_dto = CreateUserDTO(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            document_number=request.document_number,
            document_type=request.document_type,
            password=request.password,
            role=request.role,
            phone=getattr(request, 'phone', None)  # Use getattr to handle optional phone
        )

        result = await register_use_case.execute(create_dto)

        return LoginResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            token_type=result.token_type,
            expires_in=result.expires_in,
            user=UserResponse(
                id=result.user.id,
                first_name=result.user.first_name,
                last_name=result.user.last_name,
                email=result.user.email,
                document_number=result.user.document_number,
                document_type=result.user.document_type,
                role=result.user.role,
                is_active=result.user.is_active,
                must_change_password=result.user.must_change_password,
                created_at=result.user.created_at,
                updated_at=result.user.updated_at,
                last_login_at=result.user.last_login_at,
                phone=result.user.phone,
            )
        )

    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except WeakPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


# PASO FINAL: Complete password management endpoints

@router.put("/change-password", response_model=MessageResponse)
async def change_password(
    request: ChangePasswordRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    change_password_use_case: Annotated[ChangePasswordUseCase, Depends(get_change_password_use_case)]
):
    """
    Change user's password (HU-BE-006).

    - **current_password**: Current password for verification
    - **new_password**: New password (minimum 8 characters)
    """
    try:
        dto = ChangePasswordDTO(
            user_id=current_user.id,
            current_password=request.current_password,
            new_password=request.new_password
        )
        await change_password_use_case.execute(dto)
        return MessageResponse(message="Password changed successfully")
    except InvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except WeakPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    request: UpdateProfileRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    update_profile_use_case: Annotated[UpdateProfileUseCase, Depends(get_update_profile_use_case)]
):
    """
    Update user profile (non-sensitive information).

    - **first_name**: Updated first name (optional)
    - **last_name**: Updated last name (optional)
    - **phone**: Updated phone number (optional)
    """
    try:
        dto = UpdateProfileDTO(
            user_id=current_user.id,
            first_name=request.first_name,
            last_name=request.last_name,
            phone=request.phone
        )
        updated_user = await update_profile_use_case.execute(dto)

        return UserResponse(
            id=updated_user.id,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            email=updated_user.email,
            document_number=updated_user.document_number,
            document_type=updated_user.document_type,
            role=updated_user.role,
            is_active=updated_user.is_active,
            must_change_password=updated_user.must_change_password,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
            last_login_at=updated_user.last_login_at,
            phone=updated_user.phone,
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    request: ForgotPasswordRequest,
    forgot_password_use_case: Annotated[ForgotPasswordUseCase, Depends(get_forgot_password_use_case)]
):
    """
    Request password reset (HU-BE-005).

    - **email**: User's email to send reset instructions
    """
    try:
        dto = ForgotPasswordDTO(email=request.email)
        await forgot_password_use_case.execute(dto)
        return MessageResponse(
            message="If the email exists in our system, you will receive password reset instructions"
        )
    except Exception:
        # For security, always return the same message
        return MessageResponse(
            message="If the email exists in our system, you will receive password reset instructions"
        )


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    request: ResetPasswordRequest,
    reset_password_use_case: Annotated[ResetPasswordUseCase, Depends(get_reset_password_use_case)]
):
    """
    Reset password using reset token (HU-BE-006).

    - **token**: Password reset token from email
    - **new_password**: New password (minimum 8 characters)
    """
    try:
        dto = ResetPasswordDTO(
            token=request.token,
            new_password=request.new_password
        )
        await reset_password_use_case.execute(dto)
        return MessageResponse(message="Password reset successfully")
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    except WeakPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during password reset"
        )


@router.post("/force-change-password", response_model=MessageResponse)
async def force_change_password(
    request: ForceChangePasswordRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    force_change_password_use_case: Annotated[ForceChangePasswordUseCase, Depends(get_force_change_password_use_case)]
):
    """
    Force password change for users who must change password (HU-BE-007).

    - **new_password**: New password (minimum 8 characters)
    """
    try:
        if not current_user.must_change_password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Password change not required for this user"
            )

        dto = ForceChangePasswordDTO(
            user_id=current_user.id,
            new_password=request.new_password
        )
        await force_change_password_use_case.execute(dto)
        return MessageResponse(message="Password changed successfully")
    except WeakPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during password change"
        )
