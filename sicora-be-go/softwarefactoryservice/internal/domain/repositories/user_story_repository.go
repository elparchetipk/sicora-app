package repositories

import (
	"context"

	"softwarefactoryservice/internal/domain/entities"
)

// UserStoryRepository defines the interface for user story data operations
type UserStoryRepository interface {
	// Create creates a new user story
	Create(ctx context.Context, userStory *entities.UserStory) error
	
	// GetByID retrieves a user story by its ID
	GetByID(ctx context.Context, id string) (*entities.UserStory, error)
	
	// GetBySprintID retrieves user stories by sprint ID
	GetBySprintID(ctx context.Context, sprintID string) ([]*entities.UserStory, error)
	
	// GetByProjectID retrieves user stories by project ID
	GetByProjectID(ctx context.Context, projectID string) ([]*entities.UserStory, error)
	
	// GetByAssigneeID retrieves user stories by assignee ID
	GetByAssigneeID(ctx context.Context, assigneeID string) ([]*entities.UserStory, error)
	
	// GetByStatus retrieves user stories by status
	GetByStatus(ctx context.Context, status entities.StoryStatus) ([]*entities.UserStory, error)
	
	// GetByPriority retrieves user stories by priority
	GetByPriority(ctx context.Context, priority int) ([]*entities.UserStory, error)
	
	// Update updates an existing user story
	Update(ctx context.Context, userStory *entities.UserStory) error
	
	// Delete soft deletes a user story
	Delete(ctx context.Context, id string) error
	
	// UpdateStatus updates the status of a user story
	UpdateStatus(ctx context.Context, id string, status entities.StoryStatus) error
	
	// AssignToSprint assigns a user story to a sprint
	AssignToSprint(ctx context.Context, userStoryID, sprintID string) error
	
	// UnassignFromSprint removes a user story from a sprint
	UnassignFromSprint(ctx context.Context, userStoryID string) error
	
	// List retrieves user stories with pagination and filters
	List(ctx context.Context, filters UserStoryFilters) ([]*entities.UserStory, int64, error)
	
	// GetBacklog retrieves the product backlog for a project
	GetBacklog(ctx context.Context, projectID string) ([]*entities.UserStory, error)
	
	// GetSprintBacklog retrieves the sprint backlog
	GetSprintBacklog(ctx context.Context, sprintID string) ([]*entities.UserStory, error)
}

// UserStoryFilters defines filters for user story listing
type UserStoryFilters struct {
	ProjectID  *string                      `json:"project_id,omitempty"`
	SprintID   *string                      `json:"sprint_id,omitempty"`
	AssigneeID *string                      `json:"assignee_id,omitempty"`
	Status     *entities.StoryStatus        `json:"status,omitempty"`
	Priority   *int                         `json:"priority,omitempty"`
	Points     *int                         `json:"points,omitempty"`
	Search     *string                      `json:"search,omitempty"`
	Page       int                          `json:"page"`
	PageSize   int                          `json:"page_size"`
	SortBy     string                       `json:"sort_by"`
	SortOrder  string                       `json:"sort_order"`
}
