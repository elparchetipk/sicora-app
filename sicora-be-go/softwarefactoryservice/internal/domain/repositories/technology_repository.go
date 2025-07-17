package repositories

import (
	"context"

	"softwarefactoryservice/internal/domain/entities"
)

// TechnologyRepository defines the interface for technology data operations
type TechnologyRepository interface {
	// Create creates a new technology
	Create(ctx context.Context, technology *entities.Technology) error
	
	// GetByID retrieves a technology by its ID
	GetByID(ctx context.Context, id string) (*entities.Technology, error)
	
	// GetByName retrieves a technology by its name
	GetByName(ctx context.Context, name string) (*entities.Technology, error)
	
	// GetByCategory retrieves technologies by category
	GetByCategory(ctx context.Context, category entities.TechnologyCategory) ([]*entities.Technology, error)
	
	// GetByLevel retrieves technologies by complexity level
	GetByLevel(ctx context.Context, level entities.TechnologyLevel) ([]*entities.Technology, error)
	
	// Update updates an existing technology
	Update(ctx context.Context, technology *entities.Technology) error
	
	// Delete soft deletes a technology
	Delete(ctx context.Context, id string) error
	
	// List retrieves technologies with pagination and filters
	List(ctx context.Context, filters TechnologyFilters) ([]*entities.Technology, int64, error)
	
	// GetRecommendedTechnologies retrieves recommended technologies for a project
	GetRecommendedTechnologies(ctx context.Context, category entities.TechnologyCategory, level entities.TechnologyLevel) ([]*entities.Technology, error)
	
	// GetProjectTechnologies retrieves technologies used in projects
	GetProjectTechnologies(ctx context.Context, projectID string) ([]*entities.Technology, error)
	
	// AddProjectTechnology associates a technology with a project
	AddProjectTechnology(ctx context.Context, projectID, technologyID string) error
	
	// RemoveProjectTechnology removes technology association from a project
	RemoveProjectTechnology(ctx context.Context, projectID, technologyID string) error
	
	// GetPopularTechnologies retrieves most used technologies
	GetPopularTechnologies(ctx context.Context, limit int) ([]*TechnologyUsageStats, error)
}

// TechnologyFilters defines filters for technology listing
type TechnologyFilters struct {
	Category    *entities.TechnologyCategory `json:"category,omitempty"`
	Level       *entities.TechnologyLevel   `json:"level,omitempty"`
	IsActive    *bool                       `json:"is_active,omitempty"`
	Search      *string                     `json:"search,omitempty"`
	Page        int                         `json:"page"`
	PageSize    int                         `json:"page_size"`
	SortBy      string                      `json:"sort_by"`
	SortOrder   string                      `json:"sort_order"`
}

// TechnologyUsageStats represents technology usage statistics
type TechnologyUsageStats struct {
	Technology   *entities.Technology `json:"technology"`
	UsageCount   int                  `json:"usage_count"`
	ProjectCount int                  `json:"project_count"`
}
