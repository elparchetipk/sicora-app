package usecases

import (
	"context"
	"fmt"
	"time"

	"softwarefactoryservice/internal/application/dtos"
	"softwarefactoryservice/internal/domain/entities"
	"softwarefactoryservice/internal/domain/repositories"
)

// UserStoryUseCases handles business logic for user stories
type UserStoryUseCases struct {
	userStoryRepo repositories.UserStoryRepository
	projectRepo   repositories.ProjectRepository
	sprintRepo    repositories.SprintRepository
}

// NewUserStoryUseCases creates a new UserStoryUseCases instance
func NewUserStoryUseCases(
	userStoryRepo repositories.UserStoryRepository,
	projectRepo repositories.ProjectRepository,
	sprintRepo repositories.SprintRepository,
) *UserStoryUseCases {
	return &UserStoryUseCases{
		userStoryRepo: userStoryRepo,
		projectRepo:   projectRepo,
		sprintRepo:    sprintRepo,
	}
}

// CreateUserStory creates a new user story
func (u *UserStoryUseCases) CreateUserStory(ctx context.Context, req *dtos.CreateUserStoryRequest) (*dtos.UserStoryResponse, error) {
	// Convert request to entity
	userStory, err := req.ToEntity()
	if err != nil {
		return nil, fmt.Errorf("failed to convert request to entity: %w", err)
	}

	// Validate relationships
	if _, err := u.projectRepo.GetByID(ctx, req.ProjectID); err != nil {
		return nil, fmt.Errorf("project with ID %s not found: %w", req.ProjectID, err)
	}

	if req.SprintID != nil && *req.SprintID != "" {
		if _, err := u.sprintRepo.GetByID(ctx, *req.SprintID); err != nil {
			return nil, fmt.Errorf("sprint with ID %s not found: %w", *req.SprintID, err)
		}
	}

	// Validate the user story
	if err := userStory.Validate(); err != nil {
		return nil, err
	}

	// Create the user story
	if err := u.userStoryRepo.Create(ctx, userStory); err != nil {
		return nil, err
	}

	// Convert to response
	response := &dtos.UserStoryResponse{}
	response.FromEntity(userStory)
	return response, nil
}

// GetUserStory retrieves a user story by ID
func (u *UserStoryUseCases) GetUserStory(ctx context.Context, id string) (*dtos.UserStoryResponse, error) {
	userStory, err := u.userStoryRepo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	response := &dtos.UserStoryResponse{}
	response.FromEntity(userStory)
	return response, nil
}

// ListUserStories retrieves user stories with filtering and pagination
func (u *UserStoryUseCases) ListUserStories(ctx context.Context, req *dtos.UserStoryFilterRequest) (*dtos.UserStoryListResponse, error) {
	filters := repositories.UserStoryFilters{
		ProjectID:  req.ProjectID,
		SprintID:   req.SprintID,
		AssigneeID: req.AssignedTo,
		Page:       req.Page,
		PageSize:   req.PageSize,
	}

	// Set defaults
	if filters.Page <= 0 {
		filters.Page = 1
	}
	if filters.PageSize <= 0 {
		filters.PageSize = 20
	}

	userStories, total, err := u.userStoryRepo.List(ctx, filters)
	if err != nil {
		return nil, err
	}

	// Convert to slice of entities (dereferenced)
	var userStoryEntities []entities.UserStory
	for _, story := range userStories {
		userStoryEntities = append(userStoryEntities, *story)
	}

	response := &dtos.UserStoryListResponse{}
	response.FromEntityList(userStoryEntities, total, filters.Page, filters.PageSize)
	return response, nil
}

// UpdateUserStory updates an existing user story
func (u *UserStoryUseCases) UpdateUserStory(ctx context.Context, id string, req *dtos.UpdateUserStoryRequest) (*dtos.UserStoryResponse, error) {
	// Get existing user story
	userStory, err := u.userStoryRepo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	// Apply updates
	if err := req.ApplyToEntity(userStory); err != nil {
		return nil, err
	}

	userStory.UpdatedAt = time.Now()

	// Validate the updated user story
	if err := userStory.Validate(); err != nil {
		return nil, err
	}

	// Update in repository
	if err := u.userStoryRepo.Update(ctx, userStory); err != nil {
		return nil, err
	}

	response := &dtos.UserStoryResponse{}
	response.FromEntity(userStory)
	return response, nil
}

// DeleteUserStory soft deletes a user story
func (u *UserStoryUseCases) DeleteUserStory(ctx context.Context, id string) error {
	return u.userStoryRepo.Delete(ctx, id)
}

// GetUserStoriesByProject retrieves user stories for a specific project
func (u *UserStoryUseCases) GetUserStoriesByProject(ctx context.Context, projectID string) (*dtos.UserStoryListResponse, error) {
	userStories, err := u.userStoryRepo.GetByProjectID(ctx, projectID)
	if err != nil {
		return nil, err
	}

	// Convert to slice of entities (dereferenced)
	var userStoryEntities []entities.UserStory
	for _, story := range userStories {
		userStoryEntities = append(userStoryEntities, *story)
	}

	response := &dtos.UserStoryListResponse{}
	response.FromEntityList(userStoryEntities, int64(len(userStoryEntities)), 1, len(userStoryEntities))
	return response, nil
}

// GetUserStoriesBySprint retrieves user stories for a specific sprint
func (u *UserStoryUseCases) GetUserStoriesBySprint(ctx context.Context, sprintID string) (*dtos.UserStoryListResponse, error) {
	userStories, err := u.userStoryRepo.GetBySprintID(ctx, sprintID)
	if err != nil {
		return nil, err
	}

	// Convert to slice of entities (dereferenced)
	var userStoryEntities []entities.UserStory
	for _, story := range userStories {
		userStoryEntities = append(userStoryEntities, *story)
	}

	response := &dtos.UserStoryListResponse{}
	response.FromEntityList(userStoryEntities, int64(len(userStoryEntities)), 1, len(userStoryEntities))
	return response, nil
}

// AssignToSprint assigns a user story to a sprint
func (u *UserStoryUseCases) AssignToSprint(ctx context.Context, userStoryID, sprintID string) (*dtos.UserStoryResponse, error) {
	// Verify sprint exists
	if _, err := u.sprintRepo.GetByID(ctx, sprintID); err != nil {
		return nil, fmt.Errorf("sprint with ID %s not found: %w", sprintID, err)
	}

	// Assign to sprint
	if err := u.userStoryRepo.AssignToSprint(ctx, userStoryID, sprintID); err != nil {
		return nil, err
	}

	// Return updated user story
	return u.GetUserStory(ctx, userStoryID)
}

// UnassignFromSprint removes a user story from a sprint
func (u *UserStoryUseCases) UnassignFromSprint(ctx context.Context, userStoryID string) (*dtos.UserStoryResponse, error) {
	// Unassign from sprint
	if err := u.userStoryRepo.UnassignFromSprint(ctx, userStoryID); err != nil {
		return nil, err
	}

	// Return updated user story
	return u.GetUserStory(ctx, userStoryID)
}

// UpdateStatus updates the status of a user story
func (u *UserStoryUseCases) UpdateStatus(ctx context.Context, id string, status entities.StoryStatus) (*dtos.UserStoryResponse, error) {
	// Update status
	if err := u.userStoryRepo.UpdateStatus(ctx, id, status); err != nil {
		return nil, err
	}

	// Return updated user story
	return u.GetUserStory(ctx, id)
}

// GetBacklog retrieves the product backlog for a project
func (u *UserStoryUseCases) GetBacklog(ctx context.Context, projectID string) (*dtos.UserStoryListResponse, error) {
	// Verify project exists
	if _, err := u.projectRepo.GetByID(ctx, projectID); err != nil {
		return nil, fmt.Errorf("project with ID %s not found: %w", projectID, err)
	}

	userStories, err := u.userStoryRepo.GetBacklog(ctx, projectID)
	if err != nil {
		return nil, err
	}

	// Convert to slice of entities (dereferenced)
	var userStoryEntities []entities.UserStory
	for _, story := range userStories {
		userStoryEntities = append(userStoryEntities, *story)
	}

	response := &dtos.UserStoryListResponse{}
	response.FromEntityList(userStoryEntities, int64(len(userStoryEntities)), 1, len(userStoryEntities))
	return response, nil
}

// GetSprintBacklog retrieves the sprint backlog
func (u *UserStoryUseCases) GetSprintBacklog(ctx context.Context, sprintID string) (*dtos.UserStoryListResponse, error) {
	// Verify sprint exists
	if _, err := u.sprintRepo.GetByID(ctx, sprintID); err != nil {
		return nil, fmt.Errorf("sprint with ID %s not found: %w", sprintID, err)
	}

	userStories, err := u.userStoryRepo.GetSprintBacklog(ctx, sprintID)
	if err != nil {
		return nil, err
	}

	// Convert to slice of entities (dereferenced)
	var userStoryEntities []entities.UserStory
	for _, story := range userStories {
		userStoryEntities = append(userStoryEntities, *story)
	}

	response := &dtos.UserStoryListResponse{}
	response.FromEntityList(userStoryEntities, int64(len(userStoryEntities)), 1, len(userStoryEntities))
	return response, nil
}
