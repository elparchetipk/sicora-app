package repositories

import (
	"context"
	"time"

	"softwarefactoryservice/internal/domain/entities"
)

// ProjectRepository defines the interface for project data operations
type ProjectRepository interface {
	// Create creates a new project
	Create(ctx context.Context, project *entities.Project) error
	
	// GetByID retrieves a project by its ID
	GetByID(ctx context.Context, id string) (*entities.Project, error)
	
	// GetByInstructorID retrieves projects by instructor ID
	GetByInstructorID(ctx context.Context, instructorID string) ([]*entities.Project, error)
	
	// GetByCourseID retrieves projects by course ID
	GetByCourseID(ctx context.Context, courseID string) ([]*entities.Project, error)
	
	// GetByStatus retrieves projects by status
	GetByStatus(ctx context.Context, status entities.ProjectStatus) ([]*entities.Project, error)
	
	// Update updates an existing project
	Update(ctx context.Context, project *entities.Project) error
	
	// Delete soft deletes a project
	Delete(ctx context.Context, id string) error
	
	// List retrieves projects with pagination and filters
	List(ctx context.Context, filters ProjectFilters) ([]*entities.Project, int64, error)
	
	// GetActiveProjectsByPeriod retrieves active projects in a date range
	GetActiveProjectsByPeriod(ctx context.Context, startDate, endDate time.Time) ([]*entities.Project, error)
}

// ProjectFilters defines filters for project listing
type ProjectFilters struct {
	InstructorID *string               `json:"instructor_id,omitempty"`
	CourseID     *string               `json:"course_id,omitempty"`
	Status       *entities.ProjectStatus `json:"status,omitempty"`
	StartDate    *time.Time            `json:"start_date,omitempty"`
	EndDate      *time.Time            `json:"end_date,omitempty"`
	Technology   *string               `json:"technology,omitempty"`
	Search       *string               `json:"search,omitempty"`
	Page         int                   `json:"page"`
	PageSize     int                   `json:"page_size"`
	SortBy       string                `json:"sort_by"`
	SortOrder    string                `json:"sort_order"`
}
