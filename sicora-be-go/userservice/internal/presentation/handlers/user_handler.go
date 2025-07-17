package handlers

import (
	"log"
	"net/http"
	"strconv"
	"time"

	"userservice/internal/application/dtos"
	"userservice/internal/application/usecases"
	"userservice/internal/domain/errors"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
	"github.com/google/uuid"
)

// UserHandler handles HTTP requests for user operations
type UserHandler struct {
	createUserUseCase          *usecases.CreateUserUseCase
	getUserUseCase             *usecases.GetUserUseCase
	listUsersUseCase           *usecases.ListUsersUseCase
	getProfileUseCase          *usecases.GetProfileUseCase
	updateProfileUseCase       *usecases.UpdateProfileUseCase
	updateUserUseCase          *usecases.UpdateUserUseCase
	deleteUserUseCase          *usecases.DeleteUserUseCase
	authenticateUserUseCase    *usecases.AuthenticateUserUseCase
	refreshTokenUseCase        *usecases.RefreshTokenUseCase
	logoutUseCase              *usecases.LogoutUseCase
	forgotPasswordUseCase      *usecases.ForgotPasswordUseCase
	resetPasswordUseCase       *usecases.ResetPasswordUseCase
	forceChangePasswordUseCase *usecases.ForceChangePasswordUseCase
	changePasswordUseCase      *usecases.ChangePasswordUseCase
	adminResetPasswordUseCase  *usecases.AdminResetPasswordUseCase
	toggleUserStatusUseCase    *usecases.ToggleUserStatusUseCase
	bulkUserUseCases           *usecases.BulkUserUseCases
	validator                  *validator.Validate
	logger                     *log.Logger
}

// NewUserHandler creates a new user handler
func NewUserHandler(
	createUserUseCase *usecases.CreateUserUseCase,
	getUserUseCase *usecases.GetUserUseCase,
	listUsersUseCase *usecases.ListUsersUseCase,
	getProfileUseCase *usecases.GetProfileUseCase,
	updateProfileUseCase *usecases.UpdateProfileUseCase,
	updateUserUseCase *usecases.UpdateUserUseCase,
	deleteUserUseCase *usecases.DeleteUserUseCase,
	authenticateUserUseCase *usecases.AuthenticateUserUseCase,
	refreshTokenUseCase *usecases.RefreshTokenUseCase,
	logoutUseCase *usecases.LogoutUseCase,
	forgotPasswordUseCase *usecases.ForgotPasswordUseCase,
	resetPasswordUseCase *usecases.ResetPasswordUseCase,
	forceChangePasswordUseCase *usecases.ForceChangePasswordUseCase,
	changePasswordUseCase *usecases.ChangePasswordUseCase,
	adminResetPasswordUseCase *usecases.AdminResetPasswordUseCase,
	toggleUserStatusUseCase *usecases.ToggleUserStatusUseCase,
	bulkUserUseCases *usecases.BulkUserUseCases,
	validator *validator.Validate,
	logger *log.Logger,
) *UserHandler {
	return &UserHandler{
		createUserUseCase:          createUserUseCase,
		getUserUseCase:             getUserUseCase,
		listUsersUseCase:           listUsersUseCase,
		getProfileUseCase:          getProfileUseCase,
		updateProfileUseCase:       updateProfileUseCase,
		updateUserUseCase:          updateUserUseCase,
		deleteUserUseCase:          deleteUserUseCase,
		authenticateUserUseCase:    authenticateUserUseCase,
		refreshTokenUseCase:        refreshTokenUseCase,
		logoutUseCase:              logoutUseCase,
		forgotPasswordUseCase:      forgotPasswordUseCase,
		resetPasswordUseCase:       resetPasswordUseCase,
		forceChangePasswordUseCase: forceChangePasswordUseCase,
		changePasswordUseCase:      changePasswordUseCase,
		adminResetPasswordUseCase:  adminResetPasswordUseCase,
		toggleUserStatusUseCase:    toggleUserStatusUseCase,
		bulkUserUseCases:           bulkUserUseCases,
		validator:                  validator,
		logger:                     logger,
	}
}

// CreateUser handles POST /api/v1/users
//
//	@Summary		Create new user
//	@Description	Create a new user with the provided information
//	@Tags			Users
//	@Accept			json
//	@Produce		json
//	@Param			user	body		dtos.CreateUserRequestDTO	true	"User creation data"
//	@Success		201		{object}	map[string]interface{}		"User created successfully"
//	@Failure		400		{object}	errors.ErrorResponse		"Invalid input data"
//	@Failure		409		{object}	errors.ErrorResponse		"Email already exists"
//	@Failure		500		{object}	errors.ErrorResponse		"Internal server error"
//	@Router			/users [post]
func (h *UserHandler) CreateUser(c *gin.Context) {
	var request dtos.CreateUserRequestDTO

	if err := c.ShouldBindJSON(&request); err != nil {
		h.logger.Printf("Error binding JSON: %v", err)
		panic(errors.NewInvalidInputError("request body"))
	}

	if err := h.validator.Struct(&request); err != nil {
		h.logger.Printf("Validation error: %v", err)
		panic(errors.NewInvalidInputError("validation"))
	}

	response, err := h.createUserUseCase.Execute(c.Request.Context(), request)
	if err != nil {
		h.logger.Printf("Error creating user: %v", err)
		panic(errors.NewInternalServerError(err.Error()))
	}

	c.JSON(http.StatusCreated, gin.H{"message": "Usuario creado exitosamente", "data": response})
}

// GetUser handles GET /api/v1/users/:id
//
//	@Summary		Get user by ID
//	@Description	Retrieve a specific user by their unique identifier
//	@Tags			Users
//	@Accept			json
//	@Produce		json
//	@Param			id	path		string	true	"User ID (UUID)"
//	@Success		200	{object}	map[string]interface{}	"User retrieved successfully"
//	@Failure		400	{object}	errors.ErrorResponse	"Invalid UUID format"
//	@Failure		404	{object}	errors.ErrorResponse	"User not found"
//	@Failure		500	{object}	errors.ErrorResponse	"Internal server error"
//	@Router			/users/{id} [get]
func (h *UserHandler) GetUser(c *gin.Context) {
	idParam := c.Param("id")
	userID, err := uuid.Parse(idParam)
	if err != nil {
		panic(errors.NewInvalidUUIDError(idParam))
	}

	request := dtos.GetUserRequest{ID: userID}

	response, err := h.getUserUseCase.Execute(c.Request.Context(), request)
	if err != nil {
		h.logger.Printf("Error getting user: %v", err)
		panic(errors.NewUserNotFoundError(idParam))
	}

	c.JSON(http.StatusOK, gin.H{"data": response})
}

// ListUsers handles GET /api/v1/users
func (h *UserHandler) ListUsers(c *gin.Context) {
	var request dtos.ListUsersRequest // Usar el DTO de request para ListUsers (alias de UserListRequestDTO)

	// Parse query parameters y asignarlos a 'request'
	if pageStr := c.Query("page"); pageStr != "" {
		if page, err := strconv.Atoi(pageStr); err == nil && page > 0 {
			request.Page = page
		} else {
			request.Page = 1 // Default page
		}
	} else {
		request.Page = 1 // Default page
	}

	if pageSizeStr := c.Query("page_size"); pageSizeStr != "" {
		if pageSize, err := strconv.Atoi(pageSizeStr); err == nil && pageSize > 0 && pageSize <= 100 {
			request.PageSize = pageSize
		} else {
			request.PageSize = 10 // Default page size
		}
	} else {
		request.PageSize = 10 // Default page size
	}

	// Asignar strings directamente, el caso de uso se encargará de la lógica de punteros si es necesario
	// o ajustar los DTOs para que los campos opcionales sean punteros consistentemente.
	rolQuery := c.Query("rol")
	if rolQuery != "" {
		request.Rol = &rolQuery
	}
	fichaIDQuery := c.Query("ficha_id")
	if fichaIDQuery != "" {
		request.FichaID = &fichaIDQuery
	}
	searchQuery := c.Query("search")
	if searchQuery != "" {
		request.Search = &searchQuery
	}

	request.SortBy = c.Query("sort_by")
	request.SortDirection = c.Query("sort_direction")

	if activeStr := c.Query("is_active"); activeStr != "" {
		if active, err := strconv.ParseBool(activeStr); err == nil {
			request.IsActive = &active
		}
	}

	if err := h.validator.Struct(&request); err != nil {
		h.logger.Printf("Validation error for ListUsers query: %v", err)
		panic(errors.NewInvalidInputError("query parameters"))
	}

	response, err := h.listUsersUseCase.Execute(c.Request.Context(), request)
	if err != nil {
		h.logger.Printf("Error listing users: %v", err)
		panic(errors.NewInternalServerError(err.Error()))
	}

	c.JSON(http.StatusOK, response)
}

// UpdateUser handles PUT /api/v1/users/:id
//
//	@Summary		Update user (Admin only)
//	@Description	Update a user's information. Admin-only endpoint.
//	@Tags			Admin
//	@Accept			json
//	@Produce		json
//	@Security		BearerAuth
//	@Param			id		path		string						true	"User ID (UUID)"
//	@Param			user	body		dtos.UpdateUserRequestDTO	true	"User update data"
//	@Success		200		{object}	map[string]interface{}		"User updated successfully"
//	@Failure		400		{object}	errors.ErrorResponse		"Invalid input data"
//	@Failure		403		{object}	errors.ErrorResponse		"Forbidden - Admin only"
//	@Failure		404		{object}	errors.ErrorResponse		"User not found"
//	@Failure		500		{object}	errors.ErrorResponse		"Internal server error"
//	@Router			/users/{id} [put]
func (h *UserHandler) UpdateUser(c *gin.Context) {
	idParam := c.Param("id")
	userID, err := uuid.Parse(idParam)
	if err != nil {
		panic(errors.NewInvalidUUIDError(idParam))
	}

	var request dtos.UpdateUserRequestDTO
	if err := c.ShouldBindJSON(&request); err != nil {
		h.logger.Printf("Error binding JSON: %v", err)
		panic(errors.NewInvalidInputError("request body"))
	}

	if err := h.validator.Struct(&request); err != nil {
		h.logger.Printf("Validation error: %v", err)
		panic(errors.NewInvalidInputError("validation"))
	}

	// Note: Admin authentication will be handled by middleware
	response, err := h.updateUserUseCase.Execute(c.Request.Context(), userID, request)
	if err != nil {
		h.logger.Printf("Error updating user: %v", err)
		panic(errors.NewInternalServerError(err.Error()))
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Usuario actualizado exitosamente",
		"data":    response,
	})
}

// DeleteUser handles DELETE /api/v1/users/:id
//
//	@Summary		Delete user (Admin only)
//	@Description	Soft delete a user. Admin-only endpoint.
//	@Tags			Admin
//	@Accept			json
//	@Produce		json
//	@Security		BearerAuth
//	@Param			id	path		string					true	"User ID (UUID)"
//	@Success		200	{object}	map[string]interface{}	"User deleted successfully"
//	@Failure		400	{object}	errors.ErrorResponse	"Invalid UUID format"
//	@Failure		403	{object}	errors.ErrorResponse	"Forbidden - Admin only"
//	@Failure		404	{object}	errors.ErrorResponse	"User not found"
//	@Failure		500	{object}	errors.ErrorResponse	"Internal server error"
//	@Router			/users/{id} [delete]
func (h *UserHandler) DeleteUser(c *gin.Context) {
	idParam := c.Param("id")
	userID, err := uuid.Parse(idParam)
	if err != nil {
		panic(errors.NewInvalidUUIDError(idParam))
	}

	// Note: Admin authentication will be handled by middleware
	err = h.deleteUserUseCase.Execute(c.Request.Context(), userID)
	if err != nil {
		h.logger.Printf("Error deleting user: %v", err)
		panic(errors.NewInternalServerError(err.Error()))
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Usuario eliminado exitosamente",
	})
}

// AuthenticateUser handles POST /api/v1/auth/login
//
//	@Summary		Authenticate user
//	@Description	Authenticate a user with email and password
//	@Tags			Auth
//	@Accept			json
//	@Produce		json
//	@Param			credentials	body		dtos.AuthenticateUserRequest	true	"User credentials"
//	@Success		200			{object}	dtos.AuthResponseDTO			"Authentication successful"
//	@Failure		400			{object}	errors.ErrorResponse			"Invalid input data"
//	@Failure		401			{object}	errors.ErrorResponse			"Invalid credentials"
//	@Failure		500			{object}	errors.ErrorResponse			"Internal server error"
//	@Router			/auth/login [post]
func (h *UserHandler) AuthenticateUser(c *gin.Context) {
	var request dtos.AuthenticateUserRequest

	if err := c.ShouldBindJSON(&request); err != nil {
		h.logger.Printf("Error binding JSON: %v", err)
		panic(errors.NewInvalidInputError("request body"))
	}

	if err := h.validator.Struct(&request); err != nil {
		h.logger.Printf("Validation error: %v", err)
		panic(errors.NewInvalidInputError("validation"))
	}

	response, err := h.authenticateUserUseCase.Execute(c.Request.Context(), request)
	if err != nil {
		h.logger.Printf("Error authenticating user: %v", err)
		panic(errors.NewUnauthorizedError("credenciales inválidas"))
	}

	c.JSON(http.StatusOK, response)
}

// RefreshToken handles POST /api/v1/auth/refresh
//
//	@Summary		Refresh token
//	@Description	Refresh an access token using a refresh token
//	@Tags			Auth
//	@Accept			json
//	@Produce		json
//	@Param			refresh_token	body		string					true	"Refresh token"
//	@Success		200				{object}	dtos.AuthResponseDTO	"Token refreshed successfully"
//	@Failure		400				{object}	errors.ErrorResponse	"Invalid input data"
//	@Failure		401				{object}	errors.ErrorResponse	"Invalid refresh token"
//	@Failure		500				{object}	errors.ErrorResponse	"Internal server error"
//	@Router			/auth/refresh [post]
func (h *UserHandler) RefreshToken(c *gin.Context) {
	var request struct {
		RefreshToken string `json:"refresh_token" validate:"required"`
	}

	if err := c.ShouldBindJSON(&request); err != nil {
		h.logger.Printf("Error binding JSON: %v", err)
		panic(errors.NewInvalidInputError("request body"))
	}

	if err := h.validator.Struct(&request); err != nil {
		h.logger.Printf("Validation error: %v", err)
		panic(errors.NewInvalidInputError("validation"))
	}

	response, err := h.refreshTokenUseCase.Execute(c.Request.Context(), request.RefreshToken)
	if err != nil {
		h.logger.Printf("Error refreshing token: %v", err)
		panic(errors.NewUnauthorizedError("token inválido"))
	}

	c.JSON(http.StatusOK, response)
}

// Logout handles POST /api/v1/auth/logout
//
//	@Summary		Logout user
//	@Description	Invalidate a refresh token
//	@Tags			Auth
//	@Accept			json
//	@Produce		json
//	@Param			refresh_token	body		string				true	"Refresh token"
//	@Success		200				{object}	map[string]string	"Logout successful"
//	@Failure		400				{object}	errors.ErrorResponse	"Invalid input data"
//	@Failure		401				{object}	errors.ErrorResponse	"Invalid refresh token"
//	@Failure		500				{object}	errors.ErrorResponse	"Internal server error"
//	@Router			/auth/logout [post]
func (h *UserHandler) Logout(c *gin.Context) {
	var request struct {
		RefreshToken string `json:"refresh_token" validate:"required"`
	}

	if err := c.ShouldBindJSON(&request); err != nil {
		h.logger.Printf("Error binding JSON: %v", err)
		panic(errors.NewInvalidInputError("request body"))
	}

	if err := h.validator.Struct(&request); err != nil {
		h.logger.Printf("Validation error: %v", err)
		panic(errors.NewInvalidInputError("validation"))
	}

	// Obtener el user_id del token de acceso
	// En una implementación real, se extraería del token JWT
	userID := uuid.New()

	err := h.logoutUseCase.Execute(c.Request.Context(), userID, request.RefreshToken)
	if err != nil {
		h.logger.Printf("Error logging out: %v", err)
		panic(errors.NewInternalServerError(err.Error()))
	}

	c.JSON(http.StatusOK, gin.H{"message": "Sesión cerrada exitosamente"})
}

// ForgotPassword handles POST /api/v1/auth/forgot-password
//
//	@Summary		Request password reset
//	@Description	Request a password reset link to be sent to the user's email
//	@Tags			Auth
//	@Accept			json
//	@Produce		json
//	@Param			email	body		string				true	"User email"
//	@Success		200		{object}	map[string]string	"Reset link sent"
//	@Failure		400		{object}	errors.ErrorResponse	"Invalid input data"
//	@Failure		500		{object}	errors.ErrorResponse	"Internal server error"
//	@Router			/auth/forgot-password [post]
func (h *UserHandler) ForgotPassword(c *gin.Context) {
	var request struct {
		Email string `json:"email" validate:"required,email"`
	}

	if err := c.ShouldBindJSON(&request); err != nil {
		h.logger.Printf("Error binding JSON: %v", err)
		panic(errors.NewInvalidInputError("request body"))
	}

	if err := h.validator.Struct(&request); err != nil {
		h.logger.Printf("Validation error: %v", err)
		panic(errors.NewInvalidInputError("validation"))
	}

	err := h.forgotPasswordUseCase.Execute(c.Request.Context(), request.Email)
	if err != nil {
		h.logger.Printf("Error processing forgot password request: %v", err)
		panic(errors.NewInternalServerError(err.Error()))
	}

	// Por seguridad, siempre devolvemos el mismo mensaje, incluso si el email no existe
	c.JSON(http.StatusOK, gin.H{
		"message": "Si el email existe en nuestro sistema, recibirás un enlace para restablecer tu contraseña",
	})
}

// ResetPassword handles POST /api/v1/auth/reset-password
//
//	@Summary		Reset password
//	@Description	Reset a user's password using a valid reset token
//	@Tags			Auth
//	@Accept			json
//	@Produce		json
//	@Param			reset_data	body		object				true	"Reset token and new password"
//	@Success		200			{object}	map[string]string	"Password reset successful"
//	@Failure		400			{object}	errors.ErrorResponse	"Invalid input data"
//	@Failure		401			{object}	errors.ErrorResponse	"Invalid or expired token"
//	@Failure		500			{object}	errors.ErrorResponse	"Internal server error"
//	@Router			/auth/reset-password [post]
func (h *UserHandler) ResetPassword(c *gin.Context) {
	var request struct {
		Token           string `json:"token" validate:"required"`
		NewPassword     string `json:"new_password" validate:"required,min=10"`
		ConfirmPassword string `json:"confirm_password" validate:"required,eqfield=NewPassword"`
	}

	if err := c.ShouldBindJSON(&request); err != nil {
		h.logger.Printf("Error binding JSON: %v", err)
		panic(errors.NewInvalidInputError("request body"))
	}

	if err := h.validator.Struct(&request); err != nil {
		h.logger.Printf("Validation error: %v", err)
		panic(errors.NewInvalidInputError("validation"))
	}

	err := h.resetPasswordUseCase.Execute(c.Request.Context(), request.Token, request.NewPassword)
	if err != nil {
		h.logger.Printf("Error resetting password: %v", err)
		panic(errors.NewUnauthorizedError("token inválido o expirado"))
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Contraseña restablecida exitosamente",
	})
}

// ForceChangePassword handles POST /api/v1/auth/force-change-password
//
//	@Summary		Force change password
//	@Description	Change password for users with must_change_password flag
//	@Tags			Auth
//	@Accept			json
//	@Produce		json
//	@Param			password_data	body		object				true	"New password data"
//	@Success		200				{object}	dtos.AuthResponseDTO	"Password changed successfully"
//	@Failure		400				{object}	errors.ErrorResponse	"Invalid input data"
//	@Failure		401				{object}	errors.ErrorResponse	"User doesn't need to change password"
//	@Failure		500				{object}	errors.ErrorResponse	"Internal server error"
//	@Router			/auth/force-change-password [post]
func (h *UserHandler) ForceChangePassword(c *gin.Context) {
	var request struct {
		NewPassword     string `json:"new_password" validate:"required,min=10"`
		ConfirmPassword string `json:"confirm_password" validate:"required,eqfield=NewPassword"`
	}

	if err := c.ShouldBindJSON(&request); err != nil {
		h.logger.Printf("Error binding JSON: %v", err)
		panic(errors.NewInvalidInputError("request body"))
	}

	if err := h.validator.Struct(&request); err != nil {
		h.logger.Printf("Validation error: %v", err)
		panic(errors.NewInvalidInputError("validation"))
	}

	// Obtener el user_id del token de acceso
	// En una implementación real, se extraería del token JWT
	userID := uuid.New()

	response, err := h.forceChangePasswordUseCase.Execute(c.Request.Context(), userID, request.NewPassword)
	if err != nil {
		h.logger.Printf("Error forcing password change: %v", err)
		panic(errors.NewUnauthorizedError("no se puede cambiar la contraseña"))
	}

	c.JSON(http.StatusOK, response)
}

// GetProfile handles GET /api/v1/users/profile
//
//	@Summary		Get user profile
//	@Description	Retrieve the profile of the authenticated user
//	@Tags			Users
//	@Accept			json
//	@Produce		json
//	@Security		BearerAuth
//	@Success		200	{object}	dtos.UserDTO	"User profile retrieved successfully"
//	@Failure		401	{object}	errors.ErrorResponse	"Unauthorized"
//	@Failure		404	{object}	errors.ErrorResponse	"User not found"
//	@Failure		500	{object}	errors.ErrorResponse	"Internal server error"
//	@Router			/users/profile [get]
func (h *UserHandler) GetProfile(c *gin.Context) {
	// En una implementación real, el ID del usuario se extraería del token JWT
	// que se validó en el middleware de autenticación
	// Por simplicidad, simulamos la extracción del ID del usuario
	userID := uuid.New()

	// Crear la solicitud para el caso de uso
	request := dtos.GetProfileRequest{UserID: userID}

	// Ejecutar el caso de uso
	response, err := h.getProfileUseCase.Execute(c.Request.Context(), request)
	if err != nil {
		h.logger.Printf("Error getting user profile: %v", err)
		panic(errors.NewUserNotFoundError(userID.String()))
	}

	// Devolver la respuesta
	c.JSON(http.StatusOK, gin.H{"data": response})
}

// UpdateProfile handles PUT /api/v1/users/profile
//
//	@Summary		Update user profile
//	@Description	Update the profile of the authenticated user
//	@Tags			Users
//	@Accept			json
//	@Produce		json
//	@Security		BearerAuth
//	@Param			profile	body		dtos.UpdateProfileRequestDTO	true	"User profile data to update"
//	@Success		200		{object}	dtos.UserDTO					"User profile updated successfully"
//	@Failure		400		{object}	errors.ErrorResponse			"Invalid input data"
//	@Failure		401		{object}	errors.ErrorResponse			"Unauthorized"
//	@Failure		404		{object}	errors.ErrorResponse			"User not found"
//	@Failure		409		{object}	errors.ErrorResponse			"Email already exists"
//	@Failure		500		{object}	errors.ErrorResponse			"Internal server error"
//	@Router			/users/profile [put]
func (h *UserHandler) UpdateProfile(c *gin.Context) {
	// En una implementación real, el ID del usuario se extraería del token JWT
	// que se validó en el middleware de autenticación
	// Por simplicidad, simulamos la extracción del ID del usuario
	userID := uuid.New()

	// Parsear el cuerpo de la solicitud
	var requestBody struct {
		Nombre            *string `json:"nombre,omitempty" validate:"omitempty,min=2,max=50"`
		Apellido          *string `json:"apellido,omitempty" validate:"omitempty,min=2,max=50"`
		Email             *string `json:"email,omitempty" validate:"omitempty,email"`
		ProgramaFormacion *string `json:"programa_formacion,omitempty" validate:"omitempty,max=100"`
	}

	if err := c.ShouldBindJSON(&requestBody); err != nil {
		h.logger.Printf("Error binding JSON: %v", err)
		panic(errors.NewInvalidInputError("request body"))
	}

	if err := h.validator.Struct(&requestBody); err != nil {
		h.logger.Printf("Validation error: %v", err)
		panic(errors.NewInvalidInputError("validation"))
	}

	// Crear la solicitud para el caso de uso
	request := dtos.UpdateProfileRequestDTO{
		UserID:            userID,
		Nombre:            requestBody.Nombre,
		Apellido:          requestBody.Apellido,
		Email:             requestBody.Email,
		ProgramaFormacion: requestBody.ProgramaFormacion,
	}

	// Ejecutar el caso de uso
	response, err := h.updateProfileUseCase.Execute(c.Request.Context(), request)
	if err != nil {
		h.logger.Printf("Error updating user profile: %v", err)
		// Manejar diferentes tipos de errores
		if err.Error() == "ya existe un usuario con este email" {
			panic(errors.NewConflictError(err.Error()))
		} else if err.Error() == "usuario no encontrado" {
			panic(errors.NewUserNotFoundError(userID.String()))
		} else {
			panic(errors.NewInternalServerError(err.Error()))
		}
	}

	// Devolver la respuesta
	c.JSON(http.StatusOK, gin.H{
		"message": "Perfil actualizado exitosamente",
		"data":    response,
	})
}

// ChangePassword handles PUT /api/v1/users/profile/change-password
//
//	@Summary		Change user password
//	@Description	Change the password of the authenticated user
//	@Tags			Profile
//	@Accept			json
//	@Produce		json
//	@Security		BearerAuth
//	@Param			password	body		dtos.ChangePasswordRequestDTO	true	"Password change data"
//	@Success		200			{object}	map[string]interface{}			"Password changed successfully"
//	@Failure		400			{object}	errors.ErrorResponse			"Invalid input data"
//	@Failure		401			{object}	errors.ErrorResponse			"Unauthorized"
//	@Failure		403			{object}	errors.ErrorResponse			"Invalid current password"
//	@Failure		500			{object}	errors.ErrorResponse			"Internal server error"
//	@Router			/users/profile/change-password [put]
func (h *UserHandler) ChangePassword(c *gin.Context) {
	// TODO: Extract user ID from JWT token when auth middleware is implemented
	// For now, simulate user ID extraction
	userID := uuid.New()

	var request dtos.ChangePasswordRequestDTO
	if err := c.ShouldBindJSON(&request); err != nil {
		h.logger.Printf("Error binding JSON: %v", err)
		panic(errors.NewInvalidInputError("request body"))
	}

	if err := h.validator.Struct(&request); err != nil {
		h.logger.Printf("Validation error: %v", err)
		panic(errors.NewInvalidInputError("validation"))
	}

	err := h.changePasswordUseCase.Execute(c.Request.Context(), userID, request)
	if err != nil {
		h.logger.Printf("Error changing password: %v", err)
		panic(errors.NewInternalServerError(err.Error()))
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Contraseña cambiada exitosamente",
	})
}

// AdminResetPassword handles POST /api/v1/users/:id/reset-password
//
//	@Summary		Reset user password (Admin only)
//	@Description	Reset a user's password and optionally set a new one. Admin-only endpoint.
//	@Tags			Admin
//	@Accept			json
//	@Produce		json
//	@Security		BearerAuth
//	@Param			id			path		string								true	"User ID (UUID)"
//	@Param			password	body		dtos.AdminResetPasswordRequestDTO	true	"Password reset data"
//	@Success		200			{object}	dtos.AdminResetPasswordResponseDTO	"Password reset successfully"
//	@Failure		400			{object}	errors.ErrorResponse				"Invalid input data"
//	@Failure		403			{object}	errors.ErrorResponse				"Forbidden - Admin only"
//	@Failure		404			{object}	errors.ErrorResponse				"User not found"
//	@Failure		500			{object}	errors.ErrorResponse				"Internal server error"
//	@Router			/users/{id}/reset-password [post]
func (h *UserHandler) AdminResetPassword(c *gin.Context) {
	idParam := c.Param("id")
	userID, err := uuid.Parse(idParam)
	if err != nil {
		panic(errors.NewInvalidUUIDError(idParam))
	}

	var request dtos.AdminResetPasswordRequestDTO
	if err := c.ShouldBindJSON(&request); err != nil {
		h.logger.Printf("Error binding JSON: %v", err)
		panic(errors.NewInvalidInputError("request body"))
	}

	if err := h.validator.Struct(&request); err != nil {
		h.logger.Printf("Validation error: %v", err)
		panic(errors.NewInvalidInputError("validation"))
	}

	response, err := h.adminResetPasswordUseCase.Execute(c.Request.Context(), userID, request)
	if err != nil {
		h.logger.Printf("Error resetting password: %v", err)
		panic(errors.NewInternalServerError(err.Error()))
	}

	c.JSON(http.StatusOK, response)
}

// ToggleUserStatus handles PATCH /api/v1/users/:id/status
//
//	@Summary		Toggle user status (Admin only)
//	@Description	Activate or deactivate a user. Admin-only endpoint.
//	@Tags			Admin
//	@Accept			json
//	@Produce		json
//	@Security		BearerAuth
//	@Param			id	path		string					true	"User ID (UUID)"
//	@Success		200	{object}	map[string]interface{}	"User status updated successfully"
//	@Failure		400	{object}	errors.ErrorResponse	"Invalid UUID format"
//	@Failure		403	{object}	errors.ErrorResponse	"Forbidden - Admin only"
//	@Failure		404	{object}	errors.ErrorResponse	"User not found"
//	@Failure		500	{object}	errors.ErrorResponse	"Internal server error"
//	@Router			/users/{id}/status [patch]
func (h *UserHandler) ToggleUserStatus(c *gin.Context) {
	idParam := c.Param("id")
	userID, err := uuid.Parse(idParam)
	if err != nil {
		panic(errors.NewInvalidUUIDError(idParam))
	}

	response, err := h.toggleUserStatusUseCase.Execute(c.Request.Context(), userID)
	if err != nil {
		h.logger.Printf("Error toggling user status: %v", err)
		panic(errors.NewInternalServerError(err.Error()))
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Estado del usuario actualizado exitosamente",
		"data":    response,
	})
}

// HealthCheck handles GET /health
func (h *UserHandler) HealthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status":    "healthy",
		"service":   "userservice-go",
		"timestamp": time.Now().UTC(),
		"version":   "0.1.0",
		// Podrías añadir un chequeo real a la BD aquí si es necesario
		// "database_status": h.checkDatabaseStatus(),
	})
}

// BulkCreateUsers handles POST /api/v1/users/bulk
//
//	@Summary		Bulk create users
//	@Description	Create multiple users in a single operation
//	@Tags			Users
//	@Accept			json
//	@Produce		json
//	@Param			request	body		dtos.BulkCreateUserRequest	true	"Bulk user creation data"
//	@Success		200		{object}	dtos.BulkOperationResponse	"Bulk operation completed"
//	@Failure		400		{object}	errors.ErrorResponse		"Invalid input data"
//	@Failure		500		{object}	errors.ErrorResponse		"Internal server error"
//	@Router			/users/bulk [post]
//	@Security		BearerAuth
func (h *UserHandler) BulkCreateUsers(c *gin.Context) {
	var request dtos.BulkCreateUserRequest

	if err := c.ShouldBindJSON(&request); err != nil {
		h.logger.Printf("Error binding JSON for bulk create: %v", err)
		c.JSON(http.StatusBadRequest, errors.NewErrorResponse(
			"INVALID_INPUT",
			"Invalid request format",
			map[string]interface{}{"details": err.Error()},
		))
		return
	}

	response, err := h.bulkUserUseCases.BulkCreateUsers(c.Request.Context(), &request)
	if err != nil {
		h.logger.Printf("Error in bulk create users: %v", err)
		c.JSON(http.StatusInternalServerError, errors.NewErrorResponse(
			"BULK_CREATE_FAILED",
			"Failed to create users in bulk",
			map[string]interface{}{"details": err.Error()},
		))
		return
	}

	statusCode := http.StatusOK
	if response.FailureCount > 0 && response.SuccessCount == 0 {
		statusCode = http.StatusBadRequest
	} else if response.FailureCount > 0 {
		statusCode = http.StatusMultiStatus
	}

	c.JSON(statusCode, response)
}

// BulkUpdateUsers handles PUT /api/v1/users/bulk
//
//	@Summary		Bulk update users
//	@Description	Update multiple users in a single operation
//	@Tags			Users
//	@Accept			json
//	@Produce		json
//	@Param			request	body		dtos.BulkUpdateUserRequest	true	"Bulk user update data"
//	@Success		200		{object}	dtos.BulkOperationResponse	"Bulk operation completed"
//	@Failure		400		{object}	errors.ErrorResponse		"Invalid input data"
//	@Failure		500		{object}	errors.ErrorResponse		"Internal server error"
//	@Router			/users/bulk [put]
//	@Security		BearerAuth
func (h *UserHandler) BulkUpdateUsers(c *gin.Context) {
	var request dtos.BulkUpdateUserRequest

	if err := c.ShouldBindJSON(&request); err != nil {
		h.logger.Printf("Error binding JSON for bulk update: %v", err)
		c.JSON(http.StatusBadRequest, errors.NewErrorResponse(
			"INVALID_INPUT",
			"Invalid request format",
			map[string]interface{}{"details": err.Error()},
		))
		return
	}

	response, err := h.bulkUserUseCases.BulkUpdateUsers(c.Request.Context(), &request)
	if err != nil {
		h.logger.Printf("Error in bulk update users: %v", err)
		c.JSON(http.StatusInternalServerError, errors.NewErrorResponse(
			"BULK_UPDATE_FAILED",
			"Failed to update users in bulk",
			map[string]interface{}{"details": err.Error()},
		))
		return
	}

	statusCode := http.StatusOK
	if response.FailureCount > 0 && response.SuccessCount == 0 {
		statusCode = http.StatusBadRequest
	} else if response.FailureCount > 0 {
		statusCode = http.StatusMultiStatus
	}

	c.JSON(statusCode, response)
}

// BulkDeleteUsers handles DELETE /api/v1/users/bulk
//
//	@Summary		Bulk delete users
//	@Description	Delete multiple users in a single operation
//	@Tags			Users
//	@Accept			json
//	@Produce		json
//	@Param			request	body		dtos.BulkDeleteRequest		true	"Bulk user deletion data"
//	@Success		200		{object}	dtos.BulkOperationResponse	"Bulk operation completed"
//	@Failure		400		{object}	errors.ErrorResponse		"Invalid input data"
//	@Failure		500		{object}	errors.ErrorResponse		"Internal server error"
//	@Router			/users/bulk [delete]
//	@Security		BearerAuth
func (h *UserHandler) BulkDeleteUsers(c *gin.Context) {
	var request dtos.BulkDeleteRequest

	if err := c.ShouldBindJSON(&request); err != nil {
		h.logger.Printf("Error binding JSON for bulk delete: %v", err)
		c.JSON(http.StatusBadRequest, errors.NewErrorResponse(
			"INVALID_INPUT",
			"Invalid request format",
			map[string]interface{}{"details": err.Error()},
		))
		return
	}

	response, err := h.bulkUserUseCases.BulkDeleteUsers(c.Request.Context(), &request)
	if err != nil {
		h.logger.Printf("Error in bulk delete users: %v", err)
		c.JSON(http.StatusInternalServerError, errors.NewErrorResponse(
			"BULK_DELETE_FAILED",
			"Failed to delete users in bulk",
			map[string]interface{}{"details": err.Error()},
		))
		return
	}

	statusCode := http.StatusOK
	if response.FailureCount > 0 && response.SuccessCount == 0 {
		statusCode = http.StatusBadRequest
	} else if response.FailureCount > 0 {
		statusCode = http.StatusMultiStatus
	}

	c.JSON(statusCode, response)
}

// BulkChangeStatus handles PATCH /api/v1/users/bulk/status
//
//	@Summary		Bulk change user status
//	@Description	Change status of multiple users in a single operation
//	@Tags			Users
//	@Accept			json
//	@Produce		json
//	@Param			request	body		dtos.BulkStatusRequest		true	"Bulk status change data"
//	@Success		200		{object}	dtos.BulkOperationResponse	"Bulk operation completed"
//	@Failure		400		{object}	errors.ErrorResponse		"Invalid input data"
//	@Failure		500		{object}	errors.ErrorResponse		"Internal server error"
//	@Router			/users/bulk/status [patch]
//	@Security		BearerAuth
func (h *UserHandler) BulkChangeStatus(c *gin.Context) {
	var request dtos.BulkStatusRequest

	if err := c.ShouldBindJSON(&request); err != nil {
		h.logger.Printf("Error binding JSON for bulk status change: %v", err)
		c.JSON(http.StatusBadRequest, errors.NewErrorResponse(
			"INVALID_INPUT",
			"Invalid request format",
			map[string]interface{}{"details": err.Error()},
		))
		return
	}

	response, err := h.bulkUserUseCases.BulkChangeStatus(c.Request.Context(), &request)
	if err != nil {
		h.logger.Printf("Error in bulk status change: %v", err)
		c.JSON(http.StatusInternalServerError, errors.NewErrorResponse(
			"BULK_STATUS_CHANGE_FAILED",
			"Failed to change user status in bulk",
			map[string]interface{}{"details": err.Error()},
		))
		return
	}

	statusCode := http.StatusOK
	if response.FailureCount > 0 && response.SuccessCount == 0 {
		statusCode = http.StatusBadRequest
	} else if response.FailureCount > 0 {
		statusCode = http.StatusMultiStatus
	}

	c.JSON(statusCode, response)
}
