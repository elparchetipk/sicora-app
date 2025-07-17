package dtos

import (
	"time"

	"github.com/google/uuid"

	"softwarefactoryservice/internal/domain/entities"
)

// CreateSprintRequest representa la solicitud para crear un sprint
type CreateSprintRequest struct {
	ProjectID          uuid.UUID `json:"project_id" validate:"required"`
	TeamID             uuid.UUID `json:"team_id" validate:"required"`
	SprintNumber       int       `json:"sprint_number" validate:"required,min=1"`
	StartDate          time.Time `json:"start_date" validate:"required"`
	EndDate            time.Time `json:"end_date" validate:"required"`
	SprintGoal         string    `json:"sprint_goal" validate:"required,min=10"`
	LearningObjectives []string  `json:"learning_objectives" validate:"required,min=1"`
}

// UpdateSprintRequest representa la solicitud para actualizar un sprint
type UpdateSprintRequest struct {
	SprintGoal         *string   `json:"sprint_goal,omitempty" validate:"omitempty,min=10"`
	LearningObjectives []string  `json:"learning_objectives,omitempty"`
	Status             *entities.SprintStatus `json:"status,omitempty"`
	VelocityPoints     *int      `json:"velocity_points,omitempty" validate:"omitempty,min=0"`
}

// SprintResponse representa la respuesta de un sprint
type SprintResponse struct {
	ID                 uuid.UUID              `json:"id"`
	ProjectID          uuid.UUID              `json:"project_id"`
	TeamID             uuid.UUID              `json:"team_id"`
	SprintNumber       int                    `json:"sprint_number"`
	StartDate          time.Time              `json:"start_date"`
	EndDate            time.Time              `json:"end_date"`
	SprintGoal         string                 `json:"sprint_goal"`
	LearningObjectives []string               `json:"learning_objectives"`
	Status             entities.SprintStatus  `json:"status"`
	VelocityPoints     int                    `json:"velocity_points"`
	StoriesCompleted   int                    `json:"stories_completed"`
	CreatedAt          time.Time              `json:"created_at"`
	UpdatedAt          time.Time              `json:"updated_at"`
}

// SprintListResponse represents the response for sprint listing
type SprintListResponse struct {
	Sprints    []SprintResponse `json:"sprints"`
	TotalCount int64            `json:"total_count"`
	Page       int              `json:"page"`
	PageSize   int              `json:"page_size"`
	TotalPages int              `json:"total_pages"`
}

// SprintStatisticsDTO representa las estadísticas del sprint con datos de progreso
type SprintStatisticsDTO struct {
	ID                  string    `json:"id"`
	SprintNumber        int       `json:"sprint_number"`
	Status              string    `json:"status"`
	TotalStories        int       `json:"total_stories"`
	CompletedStories    int       `json:"completed_stories"`
	CompletionRate      float64   `json:"completion_rate"`
	VelocityPoints      int       `json:"velocity_points"`
	TeamEfficiency      float64   `json:"team_efficiency"`
	LearningProgress    float64   `json:"learning_progress"`
	DaysRemaining       int       `json:"days_remaining"`
	StartDate           time.Time `json:"start_date"`
	EndDate             time.Time `json:"end_date"`
}

// ToEntity converts CreateSprintRequest to Sprint entity
func (r *CreateSprintRequest) ToEntity() *entities.Sprint {
	return &entities.Sprint{
		ID:                 uuid.New(),
		ProjectID:          r.ProjectID,
		TeamID:             r.TeamID,
		SprintNumber:       r.SprintNumber,
		StartDate:          r.StartDate,
		EndDate:            r.EndDate,
		SprintGoal:         r.SprintGoal,
		LearningObjectives: r.LearningObjectives,
		Status:             entities.SprintStatusPlanning,
		VelocityPoints:     0,
		StoriesCompleted:   0,
	}
}

// ToResponse converts Sprint entity to SprintResponse
func ToSprintResponse(sprint *entities.Sprint) *SprintResponse {
	if sprint == nil {
		return nil
	}

	return &SprintResponse{
		ID:                 sprint.ID,
		ProjectID:          sprint.ProjectID,
		TeamID:             sprint.TeamID,
		SprintNumber:       sprint.SprintNumber,
		StartDate:          sprint.StartDate,
		EndDate:            sprint.EndDate,
		SprintGoal:         sprint.SprintGoal,
		LearningObjectives: sprint.LearningObjectives,
		Status:             sprint.Status,
		VelocityPoints:     sprint.VelocityPoints,
		StoriesCompleted:   sprint.StoriesCompleted,
		CreatedAt:          sprint.CreatedAt,
		UpdatedAt:          sprint.UpdatedAt,
	}
}

// ToSprintListResponse converts slice of Sprint entities to SprintListResponse
func ToSprintListResponse(sprints []*entities.Sprint, totalCount int64, page, pageSize int) *SprintListResponse {
	responses := make([]SprintResponse, len(sprints))
	for i, sprint := range sprints {
		responses[i] = *ToSprintResponse(sprint)
	}

	totalPages := int((totalCount + int64(pageSize) - 1) / int64(pageSize))

	return &SprintListResponse{
		Sprints:    responses,
		TotalCount: totalCount,
		Page:       page,
		PageSize:   pageSize,
		TotalPages: totalPages,
	}
}
