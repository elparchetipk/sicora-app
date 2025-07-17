package repositories

import (
	"context"
	"time"

	"softwarefactoryservice/internal/domain/entities"
)

// SprintRepository defines the interface for sprint data operations
type SprintRepository interface {
	// Create creates a new sprint
	Create(ctx context.Context, sprint *entities.Sprint) error
	
	// GetByID retrieves a sprint by its ID
	GetByID(ctx context.Context, id string) (*entities.Sprint, error)
	
	// GetByProjectID retrieves sprints by project ID
	GetByProjectID(ctx context.Context, projectID string) ([]*entities.Sprint, error)
	
	// GetCurrentSprint retrieves the current active sprint for a project
	GetCurrentSprint(ctx context.Context, projectID string) (*entities.Sprint, error)
	
	// GetByDateRange retrieves sprints within a date range
	GetByDateRange(ctx context.Context, startDate, endDate time.Time) ([]*entities.Sprint, error)
	
	// Update updates an existing sprint
	Update(ctx context.Context, sprint *entities.Sprint) error
	
	// Delete soft deletes a sprint
	Delete(ctx context.Context, id string) error
	
	// List retrieves sprints with pagination and filters
	List(ctx context.Context, filters SprintFilters) ([]*entities.Sprint, int64, error)
	
	// GetSprintStats retrieves statistics for a sprint
	GetSprintStats(ctx context.Context, sprintID string) (*SprintStats, error)
	
	// UpdateProgress updates sprint progress
	UpdateProgress(ctx context.Context, sprintID string, completedStories, totalStories int) error
}

// SprintFilters defines filters for sprint listing
type SprintFilters struct {
	ProjectID   *string                 `json:"project_id,omitempty"`
	Status      *entities.SprintStatus  `json:"status,omitempty"`
	StartDate   *time.Time             `json:"start_date,omitempty"`
	EndDate     *time.Time             `json:"end_date,omitempty"`
	Search      *string                `json:"search,omitempty"`
	Page        int                    `json:"page"`
	PageSize    int                    `json:"page_size"`
	SortBy      string                 `json:"sort_by"`
	SortOrder   string                 `json:"sort_order"`
}

// SprintStats represents sprint statistics
type SprintStats struct {
	TotalStories     int     `json:"total_stories"`
	CompletedStories int     `json:"completed_stories"`
	InProgressStories int    `json:"in_progress_stories"`
	PendingStories   int     `json:"pending_stories"`
	CompletionRate   float64 `json:"completion_rate"`
	VelocityPoints   int     `json:"velocity_points"`
}
