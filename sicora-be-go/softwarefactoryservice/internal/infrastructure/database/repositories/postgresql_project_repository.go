package repositories

import (
	"context"
	"fmt"
	"time"

	"softwarefactoryservice/internal/domain/entities"
	"softwarefactoryservice/internal/domain/repositories"

	"gorm.io/gorm"
)

// PostgreSQLProjectRepository implements the ProjectRepository interface using PostgreSQL
type PostgreSQLProjectRepository struct {
	db *gorm.DB
}

// NewPostgreSQLProjectRepository creates a new PostgreSQL project repository
func NewPostgreSQLProjectRepository(db *gorm.DB) repositories.ProjectRepository {
	return &PostgreSQLProjectRepository{
		db: db,
	}
}

// Create creates a new project
func (r *PostgreSQLProjectRepository) Create(ctx context.Context, project *entities.Project) error {
	if err := r.db.WithContext(ctx).Create(project).Error; err != nil {
		return fmt.Errorf("failed to create project: %w", err)
	}
	return nil
}

// GetByID retrieves a project by its ID
func (r *PostgreSQLProjectRepository) GetByID(ctx context.Context, id string) (*entities.Project, error) {
	var project entities.Project
	err := r.db.WithContext(ctx).Where("id = ?", id).First(&project).Error
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, fmt.Errorf("failed to get project by ID: %w", err)
	}
	return &project, nil
}

// GetByInstructorID retrieves projects by instructor ID
func (r *PostgreSQLProjectRepository) GetByInstructorID(ctx context.Context, instructorID string) ([]*entities.Project, error) {
	var projects []*entities.Project
	err := r.db.WithContext(ctx).
		Where("created_by = ?", instructorID).
		Find(&projects).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get projects by instructor ID: %w", err)
	}
	return projects, nil
}

// GetByCourseID retrieves projects by course ID
func (r *PostgreSQLProjectRepository) GetByCourseID(ctx context.Context, courseID string) ([]*entities.Project, error) {
	var projects []*entities.Project
	// Note: This assumes there's a course_id field in the project entity
	// For now, we'll use a placeholder implementation
	err := r.db.WithContext(ctx).
		Where("client_name = ?", courseID). // Placeholder until course integration
		Find(&projects).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get projects by course ID: %w", err)
	}
	return projects, nil
}

// GetByStatus retrieves projects by status
func (r *PostgreSQLProjectRepository) GetByStatus(ctx context.Context, status entities.ProjectStatus) ([]*entities.Project, error) {
	var projects []*entities.Project
	err := r.db.WithContext(ctx).
		Where("status = ?", status).
		Find(&projects).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get projects by status: %w", err)
	}
	return projects, nil
}

// Update updates an existing project
func (r *PostgreSQLProjectRepository) Update(ctx context.Context, project *entities.Project) error {
	project.UpdatedAt = time.Now()
	if err := r.db.WithContext(ctx).Save(project).Error; err != nil {
		return fmt.Errorf("failed to update project: %w", err)
	}
	return nil
}

// Delete soft deletes a project
func (r *PostgreSQLProjectRepository) Delete(ctx context.Context, id string) error {
	if err := r.db.WithContext(ctx).Where("id = ?", id).Delete(&entities.Project{}).Error; err != nil {
		return fmt.Errorf("failed to delete project: %w", err)
	}
	return nil
}

// List retrieves projects with pagination and filters
func (r *PostgreSQLProjectRepository) List(ctx context.Context, filters repositories.ProjectFilters) ([]*entities.Project, int64, error) {
	var projects []*entities.Project
	var totalCount int64

	// Build query
	query := r.db.WithContext(ctx).Model(&entities.Project{})

	// Apply filters
	if filters.InstructorID != nil {
		query = query.Where("created_by = ?", *filters.InstructorID)
	}
	if filters.CourseID != nil {
		// Placeholder implementation
		query = query.Where("client_name = ?", *filters.CourseID)
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
	if filters.Technology != nil {
		query = query.Where("? = ANY(tech_stack)", *filters.Technology)
	}
	if filters.Search != nil {
		searchPattern := "%" + *filters.Search + "%"
		query = query.Where("name ILIKE ? OR description ILIKE ?", searchPattern, searchPattern)
	}

	// Get total count
	if err := query.Count(&totalCount).Error; err != nil {
		return nil, 0, fmt.Errorf("failed to count projects: %w", err)
	}

	// Apply sorting
	sortBy := filters.SortBy
	if sortBy == "" {
		sortBy = "created_at"
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
	if err := query.Find(&projects).Error; err != nil {
		return nil, 0, fmt.Errorf("failed to list projects: %w", err)
	}

	return projects, totalCount, nil
}

// GetActiveProjectsByPeriod retrieves active projects in a date range
func (r *PostgreSQLProjectRepository) GetActiveProjectsByPeriod(ctx context.Context, startDate, endDate time.Time) ([]*entities.Project, error) {
	var projects []*entities.Project
	err := r.db.WithContext(ctx).
		Where("status = ? AND start_date <= ? AND (end_date IS NULL OR end_date >= ?)",
			entities.ProjectStatusActive, endDate, startDate).
		Find(&projects).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get active projects by period: %w", err)
	}
	return projects, nil
}
