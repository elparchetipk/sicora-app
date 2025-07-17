package repositories

import (
	"context"
	"fmt"

	"softwarefactoryservice/internal/domain/entities"
	"softwarefactoryservice/internal/domain/repositories"

	"gorm.io/gorm"
)

// PostgreSQLUserStoryRepository implements the UserStoryRepository interface using PostgreSQL
type PostgreSQLUserStoryRepository struct {
	db *gorm.DB
}

// NewPostgreSQLUserStoryRepository creates a new PostgreSQL user story repository
func NewPostgreSQLUserStoryRepository(db *gorm.DB) repositories.UserStoryRepository {
	return &PostgreSQLUserStoryRepository{
		db: db,
	}
}

// Create creates a new user story
func (r *PostgreSQLUserStoryRepository) Create(ctx context.Context, userStory *entities.UserStory) error {
	if err := r.db.WithContext(ctx).Create(userStory).Error; err != nil {
		return fmt.Errorf("failed to create user story: %w", err)
	}
	return nil
}

// GetByID retrieves a user story by its ID
func (r *PostgreSQLUserStoryRepository) GetByID(ctx context.Context, id string) (*entities.UserStory, error) {
	var userStory entities.UserStory
	err := r.db.WithContext(ctx).
		Where("id = ?", id).
		First(&userStory).Error
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, fmt.Errorf("failed to get user story by ID: %w", err)
	}
	return &userStory, nil
}

// GetBySprintID retrieves user stories by sprint ID
func (r *PostgreSQLUserStoryRepository) GetBySprintID(ctx context.Context, sprintID string) ([]*entities.UserStory, error) {
	var userStories []*entities.UserStory
	err := r.db.WithContext(ctx).
		Where("sprint_id = ?", sprintID).
		Order("priority ASC, created_at ASC").
		Find(&userStories).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get user stories by sprint ID: %w", err)
	}
	return userStories, nil
}

// GetByProjectID retrieves user stories by project ID
func (r *PostgreSQLUserStoryRepository) GetByProjectID(ctx context.Context, projectID string) ([]*entities.UserStory, error) {
	var userStories []*entities.UserStory
	err := r.db.WithContext(ctx).
		Where("project_id = ?", projectID).
		Order("priority ASC, created_at ASC").
		Find(&userStories).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get user stories by project ID: %w", err)
	}
	return userStories, nil
}

// GetByAssigneeID retrieves user stories by assignee ID
func (r *PostgreSQLUserStoryRepository) GetByAssigneeID(ctx context.Context, assigneeID string) ([]*entities.UserStory, error) {
	var userStories []*entities.UserStory
	err := r.db.WithContext(ctx).
		Where("assigned_to = ?", assigneeID).
		Order("priority ASC, created_at ASC").
		Find(&userStories).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get user stories by assignee ID: %w", err)
	}
	return userStories, nil
}

// GetByStatus retrieves user stories by status
func (r *PostgreSQLUserStoryRepository) GetByStatus(ctx context.Context, status entities.StoryStatus) ([]*entities.UserStory, error) {
	var userStories []*entities.UserStory
	err := r.db.WithContext(ctx).
		Where("status = ?", status).
		Order("priority ASC, created_at ASC").
		Find(&userStories).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get user stories by status: %w", err)
	}
	return userStories, nil
}

// GetByPriority retrieves user stories by priority
func (r *PostgreSQLUserStoryRepository) GetByPriority(ctx context.Context, priority int) ([]*entities.UserStory, error) {
	var userStories []*entities.UserStory
	err := r.db.WithContext(ctx).
		Where("priority = ?", priority).
		Order("created_at ASC").
		Find(&userStories).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get user stories by priority: %w", err)
	}
	return userStories, nil
}

// Update updates an existing user story
func (r *PostgreSQLUserStoryRepository) Update(ctx context.Context, userStory *entities.UserStory) error {
	if err := r.db.WithContext(ctx).Save(userStory).Error; err != nil {
		return fmt.Errorf("failed to update user story: %w", err)
	}
	return nil
}

// Delete soft deletes a user story
func (r *PostgreSQLUserStoryRepository) Delete(ctx context.Context, id string) error {
	if err := r.db.WithContext(ctx).Where("id = ?", id).Delete(&entities.UserStory{}).Error; err != nil {
		return fmt.Errorf("failed to delete user story: %w", err)
	}
	return nil
}

// UpdateStatus updates the status of a user story
func (r *PostgreSQLUserStoryRepository) UpdateStatus(ctx context.Context, id string, status entities.StoryStatus) error {
	err := r.db.WithContext(ctx).
		Model(&entities.UserStory{}).
		Where("id = ?", id).
		Update("status", status).Error
	if err != nil {
		return fmt.Errorf("failed to update user story status: %w", err)
	}
	return nil
}

// AssignToSprint assigns a user story to a sprint
func (r *PostgreSQLUserStoryRepository) AssignToSprint(ctx context.Context, userStoryID, sprintID string) error {
	err := r.db.WithContext(ctx).
		Model(&entities.UserStory{}).
		Where("id = ?", userStoryID).
		Update("sprint_id", sprintID).Error
	if err != nil {
		return fmt.Errorf("failed to assign user story to sprint: %w", err)
	}
	return nil
}

// UnassignFromSprint removes a user story from a sprint
func (r *PostgreSQLUserStoryRepository) UnassignFromSprint(ctx context.Context, userStoryID string) error {
	err := r.db.WithContext(ctx).
		Model(&entities.UserStory{}).
		Where("id = ?", userStoryID).
		Update("sprint_id", nil).Error
	if err != nil {
		return fmt.Errorf("failed to unassign user story from sprint: %w", err)
	}
	return nil
}

// List retrieves user stories with pagination and filters
func (r *PostgreSQLUserStoryRepository) List(ctx context.Context, filters repositories.UserStoryFilters) ([]*entities.UserStory, int64, error) {
	var userStories []*entities.UserStory
	var totalCount int64

	// Build query
	query := r.db.WithContext(ctx).Model(&entities.UserStory{})

	// Apply filters
	if filters.ProjectID != nil {
		query = query.Where("project_id = ?", *filters.ProjectID)
	}
	if filters.SprintID != nil {
		query = query.Where("sprint_id = ?", *filters.SprintID)
	}
	if filters.AssigneeID != nil {
		query = query.Where("assigned_to = ?", *filters.AssigneeID)
	}
	if filters.Status != nil {
		query = query.Where("status = ?", *filters.Status)
	}
	if filters.Priority != nil {
		query = query.Where("priority = ?", *filters.Priority)
	}
	if filters.Points != nil {
		query = query.Where("story_points = ?", *filters.Points)
	}
	if filters.Search != nil {
		searchPattern := "%" + *filters.Search + "%"
		query = query.Where("title ILIKE ? OR description ILIKE ?", searchPattern, searchPattern)
	}

	// Get total count
	if err := query.Count(&totalCount).Error; err != nil {
		return nil, 0, fmt.Errorf("failed to count user stories: %w", err)
	}

	// Apply sorting
	sortBy := filters.SortBy
	if sortBy == "" {
		sortBy = "priority"
	}
	sortOrder := filters.SortOrder
	if sortOrder == "" {
		sortOrder = "asc"
	}
	query = query.Order(fmt.Sprintf("%s %s", sortBy, sortOrder))

	// Apply pagination
	offset := (filters.Page - 1) * filters.PageSize
	query = query.Offset(offset).Limit(filters.PageSize)

	// Execute query
	if err := query.Find(&userStories).Error; err != nil {
		return nil, 0, fmt.Errorf("failed to list user stories: %w", err)
	}

	return userStories, totalCount, nil
}

// GetBacklog retrieves the product backlog for a project
func (r *PostgreSQLUserStoryRepository) GetBacklog(ctx context.Context, projectID string) ([]*entities.UserStory, error) {
	var userStories []*entities.UserStory
	err := r.db.WithContext(ctx).
		Where("project_id = ? AND (sprint_id IS NULL OR status = ?)", projectID, entities.StoryStatusBacklog).
		Order("priority ASC, created_at ASC").
		Find(&userStories).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get project backlog: %w", err)
	}
	return userStories, nil
}

// GetSprintBacklog retrieves the sprint backlog
func (r *PostgreSQLUserStoryRepository) GetSprintBacklog(ctx context.Context, sprintID string) ([]*entities.UserStory, error) {
	var userStories []*entities.UserStory
	err := r.db.WithContext(ctx).
		Where("sprint_id = ?", sprintID).
		Order("priority ASC, created_at ASC").
		Find(&userStories).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get sprint backlog: %w", err)
	}
	return userStories, nil
}
