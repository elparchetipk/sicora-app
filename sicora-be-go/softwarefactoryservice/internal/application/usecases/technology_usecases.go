package usecases

import (
	"context"
	"fmt"
	"time"

	"softwarefactoryservice/internal/application/dtos"
	"softwarefactoryservice/internal/domain/entities"
	"softwarefactoryservice/internal/domain/repositories"
)

// TechnologyUseCases handles business logic for technologies
type TechnologyUseCases struct {
	technologyRepo repositories.TechnologyRepository
	projectRepo    repositories.ProjectRepository
}

// NewTechnologyUseCases creates a new TechnologyUseCases instance
func NewTechnologyUseCases(
	technologyRepo repositories.TechnologyRepository,
	projectRepo repositories.ProjectRepository,
) *TechnologyUseCases {
	return &TechnologyUseCases{
		technologyRepo: technologyRepo,
		projectRepo:    projectRepo,
	}
}

// CreateTechnology creates a new technology
func (t *TechnologyUseCases) CreateTechnology(ctx context.Context, req *dtos.CreateTechnologyRequest) (*dtos.TechnologyResponse, error) {
	// Convert request to entity
	technology, err := req.ToEntity()
	if err != nil {
		return nil, fmt.Errorf("failed to convert request to entity: %w", err)
	}

	// Check if technology with same name already exists
	if existingTech, err := t.technologyRepo.GetByName(ctx, req.Name); err == nil && existingTech != nil {
		return nil, fmt.Errorf("technology with name '%s' already exists", req.Name)
	}

	// Validate the technology
	if err := technology.Validate(); err != nil {
		return nil, err
	}

	// Create the technology
	if err := t.technologyRepo.Create(ctx, technology); err != nil {
		return nil, err
	}

	// Convert to response
	response := &dtos.TechnologyResponse{}
	response.FromEntity(technology)
	return response, nil
}

// GetTechnology retrieves a technology by ID
func (t *TechnologyUseCases) GetTechnology(ctx context.Context, id string) (*dtos.TechnologyResponse, error) {
	technology, err := t.technologyRepo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	response := &dtos.TechnologyResponse{}
	response.FromEntity(technology)
	return response, nil
}

// ListTechnologies retrieves technologies with filtering and pagination
func (t *TechnologyUseCases) ListTechnologies(ctx context.Context, req *dtos.TechnologyFilterRequest) (*dtos.TechnologyListResponse, error) {
	filters := repositories.TechnologyFilters{
		Page:     req.Page,
		PageSize: req.PageSize,
		Search:   req.Search,
	}

	// Convert category and level from string to enums
	if req.Category != nil {
		category := entities.TechnologyCategory(*req.Category)
		filters.Category = &category
	}
	if req.Level != nil {
		level := entities.TechnologyLevel(*req.Level)
		filters.Level = &level
	}

	// Set defaults
	if filters.Page <= 0 {
		filters.Page = 1
	}
	if filters.PageSize <= 0 {
		filters.PageSize = 20
	}

	technologies, total, err := t.technologyRepo.List(ctx, filters)
	if err != nil {
		return nil, err
	}

	// Convert to slice of entities (dereferenced)
	var technologyEntities []entities.Technology
	for _, tech := range technologies {
		technologyEntities = append(technologyEntities, *tech)
	}

	response := &dtos.TechnologyListResponse{}
	response.FromEntityList(technologyEntities, total, filters.Page, filters.PageSize)
	return response, nil
}

// GetTechnologiesByCategory retrieves technologies for a specific category
func (t *TechnologyUseCases) GetTechnologiesByCategory(ctx context.Context, category entities.TechnologyCategory) (*dtos.TechnologyListResponse, error) {
	technologies, err := t.technologyRepo.GetByCategory(ctx, category)
	if err != nil {
		return nil, err
	}

	// Convert to slice of entities (dereferenced)
	var technologyEntities []entities.Technology
	for _, tech := range technologies {
		technologyEntities = append(technologyEntities, *tech)
	}

	response := &dtos.TechnologyListResponse{}
	response.FromEntityList(technologyEntities, int64(len(technologyEntities)), 1, len(technologyEntities))
	return response, nil
}

// GetTechnologiesByLevel retrieves technologies for a specific level
func (t *TechnologyUseCases) GetTechnologiesByLevel(ctx context.Context, level entities.TechnologyLevel) (*dtos.TechnologyListResponse, error) {
	technologies, err := t.technologyRepo.GetByLevel(ctx, level)
	if err != nil {
		return nil, err
	}

	// Convert to slice of entities (dereferenced)
	var technologyEntities []entities.Technology
	for _, tech := range technologies {
		technologyEntities = append(technologyEntities, *tech)
	}

	response := &dtos.TechnologyListResponse{}
	response.FromEntityList(technologyEntities, int64(len(technologyEntities)), 1, len(technologyEntities))
	return response, nil
}

// UpdateTechnology updates an existing technology
func (t *TechnologyUseCases) UpdateTechnology(ctx context.Context, id string, req *dtos.UpdateTechnologyRequest) (*dtos.TechnologyResponse, error) {
	// Get existing technology
	technology, err := t.technologyRepo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	// Check if another technology with same name exists (if name is being updated)
	if req.Name != nil && *req.Name != technology.Name {
		if existingTech, err := t.technologyRepo.GetByName(ctx, *req.Name); err == nil && existingTech != nil && existingTech.ID != technology.ID {
			return nil, fmt.Errorf("technology with name '%s' already exists", *req.Name)
		}
	}

	// Apply updates
	if err := req.ApplyToEntity(technology); err != nil {
		return nil, err
	}

	technology.UpdatedAt = time.Now()

	// Validate the updated technology
	if err := technology.Validate(); err != nil {
		return nil, err
	}

	// Update in repository
	if err := t.technologyRepo.Update(ctx, technology); err != nil {
		return nil, err
	}

	response := &dtos.TechnologyResponse{}
	response.FromEntity(technology)
	return response, nil
}

// DeleteTechnology soft deletes a technology
func (t *TechnologyUseCases) DeleteTechnology(ctx context.Context, id string) error {
	return t.technologyRepo.Delete(ctx, id)
}

// GetRecommendedTechnologies retrieves recommended technologies for a project
func (t *TechnologyUseCases) GetRecommendedTechnologies(ctx context.Context, category entities.TechnologyCategory, level entities.TechnologyLevel) (*dtos.TechnologyListResponse, error) {
	technologies, err := t.technologyRepo.GetRecommendedTechnologies(ctx, category, level)
	if err != nil {
		return nil, err
	}

	// Convert to slice of entities (dereferenced)
	var technologyEntities []entities.Technology
	for _, tech := range technologies {
		technologyEntities = append(technologyEntities, *tech)
	}

	response := &dtos.TechnologyListResponse{}
	response.FromEntityList(technologyEntities, int64(len(technologyEntities)), 1, len(technologyEntities))
	return response, nil
}

// GetProjectTechnologies retrieves technologies used in a project
func (t *TechnologyUseCases) GetProjectTechnologies(ctx context.Context, projectID string) (*dtos.TechnologyListResponse, error) {
	// Verify project exists
	if _, err := t.projectRepo.GetByID(ctx, projectID); err != nil {
		return nil, fmt.Errorf("project with ID %s not found: %w", projectID, err)
	}

	technologies, err := t.technologyRepo.GetProjectTechnologies(ctx, projectID)
	if err != nil {
		return nil, err
	}

	// Convert to slice of entities (dereferenced)
	var technologyEntities []entities.Technology
	for _, tech := range technologies {
		technologyEntities = append(technologyEntities, *tech)
	}

	response := &dtos.TechnologyListResponse{}
	response.FromEntityList(technologyEntities, int64(len(technologyEntities)), 1, len(technologyEntities))
	return response, nil
}

// AddProjectTechnology associates a technology with a project
func (t *TechnologyUseCases) AddProjectTechnology(ctx context.Context, projectID, technologyID string) error {
	// Verify project exists
	if _, err := t.projectRepo.GetByID(ctx, projectID); err != nil {
		return fmt.Errorf("project with ID %s not found: %w", projectID, err)
	}

	// Verify technology exists
	if _, err := t.technologyRepo.GetByID(ctx, technologyID); err != nil {
		return fmt.Errorf("technology with ID %s not found: %w", technologyID, err)
	}

	return t.technologyRepo.AddProjectTechnology(ctx, projectID, technologyID)
}

// RemoveProjectTechnology removes technology association from a project
func (t *TechnologyUseCases) RemoveProjectTechnology(ctx context.Context, projectID, technologyID string) error {
	// Verify project exists
	if _, err := t.projectRepo.GetByID(ctx, projectID); err != nil {
		return fmt.Errorf("project with ID %s not found: %w", projectID, err)
	}

	return t.technologyRepo.RemoveProjectTechnology(ctx, projectID, technologyID)
}

// GetPopularTechnologies retrieves most used technologies
func (t *TechnologyUseCases) GetPopularTechnologies(ctx context.Context, limit int) ([]*repositories.TechnologyUsageStats, error) {
	if limit <= 0 {
		limit = 10
	}

	return t.technologyRepo.GetPopularTechnologies(ctx, limit)
}

// GetTechnologyByName retrieves a technology by name
func (t *TechnologyUseCases) GetTechnologyByName(ctx context.Context, name string) (*dtos.TechnologyResponse, error) {
	technology, err := t.technologyRepo.GetByName(ctx, name)
	if err != nil {
		return nil, err
	}

	response := &dtos.TechnologyResponse{}
	response.FromEntity(technology)
	return response, nil
}

// ActivateTechnology activates a technology
func (t *TechnologyUseCases) ActivateTechnology(ctx context.Context, id string) (*dtos.TechnologyResponse, error) {
	technology, err := t.technologyRepo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	technology.Status = entities.TechnologyActive
	technology.UpdatedAt = time.Now()

	if err := t.technologyRepo.Update(ctx, technology); err != nil {
		return nil, err
	}

	response := &dtos.TechnologyResponse{}
	response.FromEntity(technology)
	return response, nil
}

// DeactivateTechnology deactivates a technology
func (t *TechnologyUseCases) DeactivateTechnology(ctx context.Context, id string) (*dtos.TechnologyResponse, error) {
	technology, err := t.technologyRepo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	technology.Status = entities.TechnologyDeprecated
	technology.UpdatedAt = time.Now()

	if err := t.technologyRepo.Update(ctx, technology); err != nil {
		return nil, err
	}

	response := &dtos.TechnologyResponse{}
	response.FromEntity(technology)
	return response, nil
}

// GetTechnologyStats provides statistics about technologies
func (t *TechnologyUseCases) GetTechnologyStats(ctx context.Context) (*dtos.TechnologyStatsResponse, error) {
	filters := repositories.TechnologyFilters{
		Page:     1,
		PageSize: 1000, // Get all for stats
	}

	technologies, total, err := t.technologyRepo.List(ctx, filters)
	if err != nil {
		return nil, err
	}

	stats := &dtos.TechnologyStatsResponse{
		TotalTechnologies:      total,
		TechnologiesByCategory: make(map[string]int64),
		TechnologiesByLevel:    make(map[string]int64),
		TechnologiesByStatus:   make(map[string]int64),
		TechnologiesByLicense:  make(map[string]int64),
	}

	var activeTechnologies int64
	for _, tech := range technologies {
		stats.TechnologiesByCategory[string(tech.Category)]++
		stats.TechnologiesByLevel[string(tech.Level)]++
		stats.TechnologiesByStatus[string(tech.Status)]++
		stats.TechnologiesByLicense[string(tech.LicenseType)]++
		if tech.Status == entities.TechnologyActive {
			activeTechnologies++
		}
	}

	// Note: Since the DTO doesn't have ActiveTechnologies and DeprecatedTechnologies fields,
	// we'll just calculate them but not set them in the response
	_ = activeTechnologies
	_ = total - activeTechnologies

	return stats, nil
}

// ValidateTechnologyData validates technology data
func (t *TechnologyUseCases) ValidateTechnologyData(name, description string, category entities.TechnologyCategory, level entities.TechnologyLevel) error {
	if name == "" {
		return fmt.Errorf("technology name cannot be empty")
	}
	if description == "" {
		return fmt.Errorf("technology description cannot be empty")
	}
	// Category and level validation is handled by the entity's Validate method
	return nil
}
