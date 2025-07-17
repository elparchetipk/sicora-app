package repositories

import (
	"context"
	"fmt"

	"gorm.io/gorm"

	"softwarefactoryservice/internal/domain/entities"
	"softwarefactoryservice/internal/domain/repositories"
)

type PostgreSQLTechnologyRepository struct {
	db *gorm.DB
}

func NewPostgreSQLTechnologyRepository(db *gorm.DB) repositories.TechnologyRepository {
	return &PostgreSQLTechnologyRepository{db: db}
}

// Create creates a new technology in the database
func (r *PostgreSQLTechnologyRepository) Create(ctx context.Context, technology *entities.Technology) error {
	if err := r.db.WithContext(ctx).Create(technology).Error; err != nil {
		return fmt.Errorf("failed to create technology: %w", err)
	}
	return nil
}

// GetByID retrieves a technology by ID
func (r *PostgreSQLTechnologyRepository) GetByID(ctx context.Context, id string) (*entities.Technology, error) {
	var technology entities.Technology
	if err := r.db.WithContext(ctx).First(&technology, "id = ?", id).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, entities.NewNotFoundError("technology", id)
		}
		return nil, fmt.Errorf("failed to get technology: %w", err)
	}
	return &technology, nil
}

// GetByName retrieves a technology by name
func (r *PostgreSQLTechnologyRepository) GetByName(ctx context.Context, name string) (*entities.Technology, error) {
	var technology entities.Technology
	if err := r.db.WithContext(ctx).Where("name = ?", name).First(&technology).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, entities.NewNotFoundError("technology", name)
		}
		return nil, fmt.Errorf("failed to get technology by name: %w", err)
	}
	return &technology, nil
}

// GetByCategory retrieves technologies by category
func (r *PostgreSQLTechnologyRepository) GetByCategory(ctx context.Context, category entities.TechnologyCategory) ([]*entities.Technology, error) {
	var technologies []*entities.Technology
	if err := r.db.WithContext(ctx).Where("category = ? AND status = ?", category, entities.TechnologyActive).Find(&technologies).Error; err != nil {
		return nil, fmt.Errorf("failed to get technologies by category: %w", err)
	}
	return technologies, nil
}

// GetByLevel retrieves technologies by complexity level
func (r *PostgreSQLTechnologyRepository) GetByLevel(ctx context.Context, level entities.TechnologyLevel) ([]*entities.Technology, error) {
	var technologies []*entities.Technology
	if err := r.db.WithContext(ctx).Where("level = ? AND status = ?", level, entities.TechnologyActive).Find(&technologies).Error; err != nil {
		return nil, fmt.Errorf("failed to get technologies by level: %w", err)
	}
	return technologies, nil
}

// Update updates an existing technology
func (r *PostgreSQLTechnologyRepository) Update(ctx context.Context, technology *entities.Technology) error {
	if err := r.db.WithContext(ctx).Save(technology).Error; err != nil {
		return fmt.Errorf("failed to update technology: %w", err)
	}
	return nil
}

// Delete deletes a technology by ID
func (r *PostgreSQLTechnologyRepository) Delete(ctx context.Context, id string) error {
	result := r.db.WithContext(ctx).Delete(&entities.Technology{}, "id = ?", id)
	if result.Error != nil {
		return fmt.Errorf("failed to delete technology: %w", result.Error)
	}
	if result.RowsAffected == 0 {
		return entities.NewNotFoundError("technology", id)
	}
	return nil
}

// List retrieves technologies with pagination and filters
func (r *PostgreSQLTechnologyRepository) List(ctx context.Context, filters repositories.TechnologyFilters) ([]*entities.Technology, int64, error) {
	var technologies []*entities.Technology
	var total int64

	query := r.db.WithContext(ctx).Model(&entities.Technology{})

	// Apply filters
	if filters.Category != nil {
		query = query.Where("category = ?", *filters.Category)
	}
	if filters.Level != nil {
		query = query.Where("level = ?", *filters.Level)
	}
	if filters.IsActive != nil {
		if *filters.IsActive {
			query = query.Where("status = ?", entities.TechnologyActive)
		} else {
			query = query.Where("status != ?", entities.TechnologyActive)
		}
	}
	if filters.Search != nil {
		searchTerm := "%" + *filters.Search + "%"
		query = query.Where("name ILIKE ? OR description ILIKE ?", searchTerm, searchTerm)
	}

	// Count total
	if err := query.Count(&total).Error; err != nil {
		return nil, 0, fmt.Errorf("failed to count technologies: %w", err)
	}

	// Apply pagination
	offset := (filters.Page - 1) * filters.PageSize
	query = query.Offset(offset).Limit(filters.PageSize)

	// Apply sorting
	if filters.SortBy != "" {
		order := filters.SortBy
		if filters.SortOrder == "desc" {
			order += " desc"
		}
		query = query.Order(order)
	} else {
		query = query.Order("name asc")
	}

	if err := query.Find(&technologies).Error; err != nil {
		return nil, 0, fmt.Errorf("failed to list technologies: %w", err)
	}

	return technologies, total, nil
}

// GetRecommendedTechnologies retrieves recommended technologies for a project
func (r *PostgreSQLTechnologyRepository) GetRecommendedTechnologies(ctx context.Context, category entities.TechnologyCategory, level entities.TechnologyLevel) ([]*entities.Technology, error) {
	var technologies []*entities.Technology
	
	query := r.db.WithContext(ctx).Where("category = ? AND level = ? AND status = ?", 
		category, level, entities.TechnologyActive).
		Order("popularity_score desc").
		Limit(10)

	if err := query.Find(&technologies).Error; err != nil {
		return nil, fmt.Errorf("failed to get recommended technologies: %w", err)
	}

	return technologies, nil
}

// GetProjectTechnologies retrieves technologies used in projects
func (r *PostgreSQLTechnologyRepository) GetProjectTechnologies(ctx context.Context, projectID string) ([]*entities.Technology, error) {
	var technologies []*entities.Technology
	
	// This assumes a join table exists - for simplicity, we'll implement it directly
	if err := r.db.WithContext(ctx).Table("factory_technologies t").
		Select("t.*").
		Joins("JOIN factory_project_technologies pt ON t.id = pt.technology_id").
		Where("pt.project_id = ? AND t.status = ?", projectID, entities.TechnologyActive).
		Find(&technologies).Error; err != nil {
		return nil, fmt.Errorf("failed to get project technologies: %w", err)
	}

	return technologies, nil
}

// AddProjectTechnology associates a technology with a project
func (r *PostgreSQLTechnologyRepository) AddProjectTechnology(ctx context.Context, projectID, technologyID string) error {
	// Insert into join table
	if err := r.db.WithContext(ctx).Exec(
		"INSERT INTO factory_project_technologies (project_id, technology_id) VALUES (?, ?) ON CONFLICT DO NOTHING",
		projectID, technologyID).Error; err != nil {
		return fmt.Errorf("failed to add project technology: %w", err)
	}
	return nil
}

// RemoveProjectTechnology removes technology association from a project
func (r *PostgreSQLTechnologyRepository) RemoveProjectTechnology(ctx context.Context, projectID, technologyID string) error {
	if err := r.db.WithContext(ctx).Exec(
		"DELETE FROM factory_project_technologies WHERE project_id = ? AND technology_id = ?",
		projectID, technologyID).Error; err != nil {
		return fmt.Errorf("failed to remove project technology: %w", err)
	}
	return nil
}

// GetPopularTechnologies retrieves most used technologies
func (r *PostgreSQLTechnologyRepository) GetPopularTechnologies(ctx context.Context, limit int) ([]*repositories.TechnologyUsageStats, error) {
	var results []struct {
		TechnologyID string `json:"technology_id"`
		UsageCount   int    `json:"usage_count"`
		ProjectCount int    `json:"project_count"`
	}

	query := `
		SELECT 
			t.id as technology_id,
			COALESCE(pt.usage_count, 0) as usage_count,
			COALESCE(pt.project_count, 0) as project_count
		FROM factory_technologies t
		LEFT JOIN (
			SELECT 
				technology_id,
				COUNT(*) as usage_count,
				COUNT(DISTINCT project_id) as project_count
			FROM factory_project_technologies
			GROUP BY technology_id
		) pt ON t.id = pt.technology_id
		WHERE t.status = ?
		ORDER BY pt.usage_count DESC, pt.project_count DESC
		LIMIT ?
	`

	if err := r.db.WithContext(ctx).Raw(query, entities.TechnologyActive, limit).Scan(&results).Error; err != nil {
		return nil, fmt.Errorf("failed to get popular technologies: %w", err)
	}

	var stats []*repositories.TechnologyUsageStats
	for _, result := range results {
		technology, err := r.GetByID(ctx, result.TechnologyID)
		if err != nil {
			continue // Skip if technology not found
		}

		stats = append(stats, &repositories.TechnologyUsageStats{
			Technology:   technology,
			UsageCount:   result.UsageCount,
			ProjectCount: result.ProjectCount,
		})
	}

	return stats, nil
}
