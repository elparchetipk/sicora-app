package external

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/google/uuid"
)

// ScheduleServiceAdapter representa el adaptador para el servicio de horarios
type ScheduleServiceAdapter struct {
	baseURL    string
	httpClient *http.Client
	apiKey     string
}

// FichaInfo representa la información de una ficha
type FichaInfo struct {
	ID           string      `json:"id"`
	Number       string      `json:"number"`
	Name         string      `json:"name"`
	Program      string      `json:"program"`
	StartDate    time.Time   `json:"start_date"`
	EndDate      time.Time   `json:"end_date"`
	IsActive     bool        `json:"is_active"`
	InstructorID uuid.UUID   `json:"instructor_id"`
	StudentIDs   []uuid.UUID `json:"student_ids"`
}

// ScheduleInfo representa información de horarios
type ScheduleInfo struct {
	ID           uuid.UUID `json:"id"`
	FichaID      string    `json:"ficha_id"`
	InstructorID uuid.UUID `json:"instructor_id"`
	Subject      string    `json:"subject"`
	StartTime    time.Time `json:"start_time"`
	EndTime      time.Time `json:"end_time"`
	DayOfWeek    int       `json:"day_of_week"`
	IsActive     bool      `json:"is_active"`
}

// InstructorAssignment representa la asignación de un instructor
type InstructorAssignment struct {
	InstructorID uuid.UUID `json:"instructor_id"`
	FichaID      string    `json:"ficha_id"`
	Subject      string    `json:"subject"`
	Hours        int       `json:"hours"`
	StartDate    time.Time `json:"start_date"`
	EndDate      time.Time `json:"end_date"`
}

// FichaResponse representa la respuesta del servicio para una ficha
type FichaResponse struct {
	Data    *FichaInfo `json:"data"`
	Message string     `json:"message"`
	Success bool       `json:"success"`
}

// FichasResponse representa la respuesta para múltiples fichas
type FichasResponse struct {
	Data    []*FichaInfo `json:"data"`
	Message string       `json:"message"`
	Success bool         `json:"success"`
}

// SchedulesResponse representa la respuesta para horarios
type SchedulesResponse struct {
	Data    []*ScheduleInfo `json:"data"`
	Message string          `json:"message"`
	Success bool            `json:"success"`
}

// AssignmentsResponse representa la respuesta para asignaciones
type AssignmentsResponse struct {
	Data    []*InstructorAssignment `json:"data"`
	Message string                  `json:"message"`
	Success bool                    `json:"success"`
}

// NewScheduleServiceAdapter crea un nuevo adaptador para el servicio de horarios
func NewScheduleServiceAdapter(baseURL, apiKey string) *ScheduleServiceAdapter {
	return &ScheduleServiceAdapter{
		baseURL: baseURL,
		apiKey:  apiKey,
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

// GetFichaByID obtiene una ficha por su ID
func (a *ScheduleServiceAdapter) GetFichaByID(ctx context.Context, fichaID string) (*FichaInfo, error) {
	url := fmt.Sprintf("%s/api/v1/fichas/%s", a.baseURL, fichaID)

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
		return nil, fmt.Errorf("schedule service returned status %d", resp.StatusCode)
	}

	var response FichaResponse
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	if !response.Success {
		return nil, fmt.Errorf("schedule service error: %s", response.Message)
	}

	return response.Data, nil
}

// GetActiveFichas obtiene todas las fichas activas
func (a *ScheduleServiceAdapter) GetActiveFichas(ctx context.Context) ([]*FichaInfo, error) {
	url := fmt.Sprintf("%s/api/v1/fichas?active=true", a.baseURL)

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
		return nil, fmt.Errorf("schedule service returned status %d", resp.StatusCode)
	}

	var response FichasResponse
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	if !response.Success {
		return nil, fmt.Errorf("schedule service error: %s", response.Message)
	}

	return response.Data, nil
}

// GetInstructorAssignments obtiene las asignaciones de un instructor
func (a *ScheduleServiceAdapter) GetInstructorAssignments(ctx context.Context, instructorID uuid.UUID) ([]*InstructorAssignment, error) {
	url := fmt.Sprintf("%s/api/v1/assignments/instructor/%s", a.baseURL, instructorID.String())

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
		return nil, fmt.Errorf("schedule service returned status %d", resp.StatusCode)
	}

	var response AssignmentsResponse
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	if !response.Success {
		return nil, fmt.Errorf("schedule service error: %s", response.Message)
	}

	return response.Data, nil
}

// GetStudentsByFicha obtiene los estudiantes de una ficha
func (a *ScheduleServiceAdapter) GetStudentsByFicha(ctx context.Context, fichaID string) ([]uuid.UUID, error) {
	ficha, err := a.GetFichaByID(ctx, fichaID)
	if err != nil {
		return nil, err
	}

	return ficha.StudentIDs, nil
}

// ValidateFichaExists valida si una ficha existe y está activa
func (a *ScheduleServiceAdapter) ValidateFichaExists(ctx context.Context, fichaID string) (bool, error) {
	ficha, err := a.GetFichaByID(ctx, fichaID)
	if err != nil {
		return false, err
	}

	return ficha != nil && ficha.IsActive, nil
}

// GetInstructorsByFicha obtiene los instructores asignados a una ficha
func (a *ScheduleServiceAdapter) GetInstructorsByFicha(ctx context.Context, fichaID string) ([]uuid.UUID, error) {
	url := fmt.Sprintf("%s/api/v1/assignments/ficha/%s", a.baseURL, fichaID)

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
		return nil, fmt.Errorf("schedule service returned status %d", resp.StatusCode)
	}

	var response AssignmentsResponse
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	if !response.Success {
		return nil, fmt.Errorf("schedule service error: %s", response.Message)
	}

	instructorIDs := make([]uuid.UUID, 0, len(response.Data))
	seen := make(map[uuid.UUID]bool)

	for _, assignment := range response.Data {
		if !seen[assignment.InstructorID] {
			instructorIDs = append(instructorIDs, assignment.InstructorID)
			seen[assignment.InstructorID] = true
		}
	}

	return instructorIDs, nil
}
