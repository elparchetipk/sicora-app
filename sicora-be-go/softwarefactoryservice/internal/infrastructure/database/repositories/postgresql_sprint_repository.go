package repositories

import (
	"context"
	"fmt"
	"time"

	"softwarefactoryservice/internal/domain/entities"
	"softwarefactoryservice/internal/domain/repositories"

	"gorm.io/gorm"
)

// PostgreSQLSprintRepository implements the SprintRepository interface using PostgreSQL
type PostgreSQLSprintRepository struct {
	db *gorm.DB
}

// NewPostgreSQLSprintRepository creates a new PostgreSQL sprint repository
func NewPostgreSQLSprintRepository(db *gorm.DB) repositories.SprintRepository {
	return &PostgreSQLSprintRepository{
		db: db,
	}
}

// Create creates a new sprint
func (r *PostgreSQLSprintRepository) Create(ctx context.Context, sprint *entities.Sprint) error {
	if err := r.db.WithContext(ctx).Create(sprint).Error; err != nil {
		return fmt.Errorf("failed to create sprint: %w", err)
	}
	return nil
}

// GetByID retrieves a sprint by its ID
func (r *PostgreSQLSprintRepository) GetByID(ctx context.Context, id string) (*entities.Sprint, error) {
	var sprint entities.Sprint
	err := r.db.WithContext(ctx).
		Where("id = ?", id).
		First(&sprint).Error
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, fmt.Errorf("failed to get sprint by ID: %w", err)
	}
	return &sprint, nil
}

// GetByProjectID retrieves sprints by project ID
func (r *PostgreSQLSprintRepository) GetByProjectID(ctx context.Context, projectID string) ([]*entities.Sprint, error) {
	var sprints []*entities.Sprint
	err := r.db.WithContext(ctx).
		Where("project_id = ?", projectID).
		Order("start_date DESC").
		Find(&sprints).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get sprints by project ID: %w", err)
	}
	return sprints, nil
}

// GetCurrentSprint retrieves the current active sprint for a project
func (r *PostgreSQLSprintRepository) GetCurrentSprint(ctx context.Context, projectID string) (*entities.Sprint, error) {
	var sprint entities.Sprint
	err := r.db.WithContext(ctx).
		Where("project_id = ? AND status = ?", projectID, entities.SprintStatusActive).
		First(&sprint).Error
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, fmt.Errorf("failed to get current sprint: %w", err)
	}
	return &sprint, nil
}

// GetByDateRange retrieves sprints within a date range
func (r *PostgreSQLSprintRepository) GetByDateRange(ctx context.Context, startDate, endDate time.Time) ([]*entities.Sprint, error) {
	var sprints []*entities.Sprint
	err := r.db.WithContext(ctx).
		Where("(start_date BETWEEN ? AND ?) OR (end_date BETWEEN ? AND ?) OR (start_date <= ? AND end_date >= ?)",
			startDate, endDate, startDate, endDate, startDate, endDate).
		Find(&sprints).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get sprints by date range: %w", err)
	}
	return sprints, nil
}

// Update updates an existing sprint
func (r *PostgreSQLSprintRepository) Update(ctx context.Context, sprint *entities.Sprint) error {
	sprint.UpdatedAt = time.Now()
	if err := r.db.WithContext(ctx).Save(sprint).Error; err != nil {
		return fmt.Errorf("failed to update sprint: %w", err)
	}
	return nil
}

// Delete soft deletes a sprint
func (r *PostgreSQLSprintRepository) Delete(ctx context.Context, id string) error {
	if err := r.db.WithContext(ctx).Where("id = ?", id).Delete(&entities.Sprint{}).Error; err != nil {
		return fmt.Errorf("failed to delete sprint: %w", err)
	}
	return nil
}

// List retrieves sprints with pagination and filters
func (r *PostgreSQLSprintRepository) List(ctx context.Context, filters repositories.SprintFilters) ([]*entities.Sprint, int64, error) {
	var sprints []*entities.Sprint
	var totalCount int64

	// Build query
	query := r.db.WithContext(ctx).Model(&entities.Sprint{})

	// Apply filters
	if filters.ProjectID != nil {
		query = query.Where("project_id = ?", *filters.ProjectID)
	}
	if filters.Status != nil {
		query = query.Where("status = ?", *filters.Status)
	}
	if filters.StartDate != nil {
		query = query.Where("start_date >= ?", *filters.StartDate)
	}
	if filters.EndDate != nil {
		query = query.Where("end_date <= ?", *filters.EndDate)
	}
	if filters.Search != nil {
		searchPattern := "%" + *filters.Search + "%"
		query = query.Where("name ILIKE ? OR goal ILIKE ?", searchPattern, searchPattern)
	}

	// Get total count
	if err := query.Count(&totalCount).Error; err != nil {
		return nil, 0, fmt.Errorf("failed to count sprints: %w", err)
	}

	// Apply sorting
	sortBy := filters.SortBy
	if sortBy == "" {
		sortBy = "start_date"
	}
	sortOrder := filters.SortOrder
	if sortOrder == "" {
		sortOrder = "desc"
	}
	query = query.Order(fmt.Sprintf("%s %s", sortBy, sortOrder))

	// Apply pagination
	offset := (filters.Page - 1) * filters.PageSize
	query = query.Offset(offset).Limit(filters.PageSize)

	// Execute query
	if err := query.Find(&sprints).Error; err != nil {
		return nil, 0, fmt.Errorf("failed to list sprints: %w", err)
	}

	return sprints, totalCount, nil
}

// GetSprintStats retrieves statistics for a sprint
func (r *PostgreSQLSprintRepository) GetSprintStats(ctx context.Context, sprintID string) (*repositories.SprintStats, error) {
	var stats repositories.SprintStats
	
	// Get basic sprint info
	var sprint entities.Sprint
	if err := r.db.WithContext(ctx).Where("id = ?", sprintID).First(&sprint).Error; err != nil {
		return nil, fmt.Errorf("failed to get sprint: %w", err)
	}

	// Count user stories by status
	var totalStories, completedStories, inProgressStories, pendingStories int64
	
	r.db.WithContext(ctx).Model(&entities.UserStory{}).
		Where("sprint_id = ?", sprintID).
		Count(&totalStories)
	
	r.db.WithContext(ctx).Model(&entities.UserStory{}).
		Where("sprint_id = ? AND status = ?", sprintID, entities.StoryStatusDone).
		Count(&completedStories)
	
	r.db.WithContext(ctx).Model(&entities.UserStory{}).
		Where("sprint_id = ? AND status = ?", sprintID, entities.StoryStatusInProgress).
		Count(&inProgressStories)
	
	r.db.WithContext(ctx).Model(&entities.UserStory{}).
		Where("sprint_id = ? AND status IN ?", sprintID, []entities.StoryStatus{
			entities.StoryStatusBacklog, entities.StoryStatusTodo,
		}).Count(&pendingStories)

	// Calculate completion rate
	completionRate := 0.0
	if totalStories > 0 {
		completionRate = float64(completedStories) / float64(totalStories) * 100
	}

	// Calculate velocity points (sum of completed story points)
	var velocityPoints int
	r.db.WithContext(ctx).Model(&entities.UserStory{}).
		Where("sprint_id = ? AND status = ?", sprintID, entities.StoryStatusDone).
		Select("COALESCE(SUM(story_points), 0)").
		Scan(&velocityPoints)

	stats = repositories.SprintStats{
		TotalStories:      int(totalStories),
		CompletedStories:  int(completedStories),
		InProgressStories: int(inProgressStories),
		PendingStories:    int(pendingStories),
		CompletionRate:    completionRate,
		VelocityPoints:    velocityPoints,
	}

	return &stats, nil
}

// UpdateProgress updates sprint progress
func (r *PostgreSQLSprintRepository) UpdateProgress(ctx context.Context, sprintID string, completedStories, totalStories int) error {
	err := r.db.WithContext(ctx).
		Model(&entities.Sprint{}).
		Where("id = ?", sprintID).
		Updates(map[string]interface{}{
			"completed_stories": completedStories,
			"total_stories":     totalStories,
			"updated_at":        time.Now(),
		}).Error
	
	if err != nil {
		return fmt.Errorf("failed to update sprint progress: %w", err)
	}
	return nil
}
