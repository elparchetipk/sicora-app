package external

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/google/uuid"
)

// UserServiceAdapter representa el adaptador para el servicio de usuarios
type UserServiceAdapter struct {
	baseURL    string
	httpClient *http.Client
	apiKey     string
}

// UserInfo representa la información básica de un usuario
type UserInfo struct {
	ID        uuid.UUID `json:"id"`
	Email     string    `json:"email"`
	FirstName string    `json:"first_name"`
	LastName  string    `json:"last_name"`
	Role      string    `json:"role"`
	IsActive  bool      `json:"is_active"`
}

// UserResponse representa la respuesta del servicio de usuarios
type UserResponse struct {
	Data    *UserInfo `json:"data"`
	Message string    `json:"message"`
	Success bool      `json:"success"`
}

// UsersResponse representa la respuesta para múltiples usuarios
type UsersResponse struct {
	Data    []*UserInfo `json:"data"`
	Message string      `json:"message"`
	Success bool        `json:"success"`
}

// NewUserServiceAdapter crea un nuevo adaptador para el servicio de usuarios
func NewUserServiceAdapter(baseURL, apiKey string) *UserServiceAdapter {
	return &UserServiceAdapter{
		baseURL: baseURL,
		apiKey:  apiKey,
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

// GetUserByID obtiene un usuario por su ID
func (a *UserServiceAdapter) GetUserByID(ctx context.Context, userID uuid.UUID) (*UserInfo, error) {
	url := fmt.Sprintf("%s/api/v1/users/%s", a.baseURL, userID.String())

	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Authorization", "Bearer "+a.apiKey)
	req.Header.Set("Content-Type", "application/json")

	resp, err := a.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to make request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("user service returned status %d", resp.StatusCode)
	}

	var response UserResponse
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	if !response.Success {
		return nil, fmt.Errorf("user service error: %s", response.Message)
	}

	return response.Data, nil
}

// GetUsersByRole obtiene usuarios por rol
func (a *UserServiceAdapter) GetUsersByRole(ctx context.Context, role string) ([]*UserInfo, error) {
	url := fmt.Sprintf("%s/api/v1/users?role=%s", a.baseURL, role)

	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Authorization", "Bearer "+a.apiKey)
	req.Header.Set("Content-Type", "application/json")

	resp, err := a.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to make request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("user service returned status %d", resp.StatusCode)
	}

	var response UsersResponse
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	if !response.Success {
		return nil, fmt.Errorf("user service error: %s", response.Message)
	}

	return response.Data, nil
}

// ValidateUser valida si un usuario existe y está activo
func (a *UserServiceAdapter) ValidateUser(ctx context.Context, userID uuid.UUID) (bool, error) {
	user, err := a.GetUserByID(ctx, userID)
	if err != nil {
		return false, err
	}

	return user != nil && user.IsActive, nil
}

// GetInstructors obtiene todos los instructores
func (a *UserServiceAdapter) GetInstructors(ctx context.Context) ([]*UserInfo, error) {
	return a.GetUsersByRole(ctx, "instructor")
}

// GetStudents obtiene todos los estudiantes
func (a *UserServiceAdapter) GetStudents(ctx context.Context) ([]*UserInfo, error) {
	return a.GetUsersByRole(ctx, "student")
}

// GetAdministrators obtiene todos los administradores
func (a *UserServiceAdapter) GetAdministrators(ctx context.Context) ([]*UserInfo, error) {
	return a.GetUsersByRole(ctx, "admin")
}
