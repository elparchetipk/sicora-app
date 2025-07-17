package usecases

import (
	"context"
	"fmt"
	"time"

	"softwarefactoryservice/internal/application/dtos"
	"softwarefactoryservice/internal/domain/entities"
	"softwarefactoryservice/internal/domain/repositories"
)

// ProjectUseCases handles business logic for projects
type ProjectUseCases struct {
	projectRepo    repositories.ProjectRepository
	teamRepo       repositories.TeamRepository
	userStoryRepo  repositories.UserStoryRepository
	sprintRepo     repositories.SprintRepository
	evaluationRepo repositories.EvaluationRepository
}

// NewProjectUseCases creates a new instance of ProjectUseCases
func NewProjectUseCases(
	projectRepo repositories.ProjectRepository,
	teamRepo repositories.TeamRepository,
	userStoryRepo repositories.UserStoryRepository,
	sprintRepo repositories.SprintRepository,
	evaluationRepo repositories.EvaluationRepository,
) *ProjectUseCases {
	return &ProjectUseCases{
		projectRepo:    projectRepo,
		teamRepo:       teamRepo,
		userStoryRepo:  userStoryRepo,
		sprintRepo:     sprintRepo,
		evaluationRepo: evaluationRepo,
	}
}

// CreateProject creates a new software factory project
func (uc *ProjectUseCases) CreateProject(ctx context.Context, req dtos.CreateProjectRequest) (*entities.Project, error) {
	// Validate request
	if err := req.Validate(); err != nil {
		return nil, entities.NewValidationError("invalid project data", err)
	}

	// Create project entity
	project := req.ToProjectEntity()

	// Save project
	if err := uc.projectRepo.Create(ctx, project); err != nil {
		return nil, fmt.Errorf("failed to create project: %w", err)
	}

	return project, nil
}

// GetProject retrieves a project by ID with validation
func (uc *ProjectUseCases) GetProject(ctx context.Context, id string) (*entities.Project, error) {
	if id == "" {
		return nil, entities.NewValidationError("project ID is required", nil)
	}

	project, err := uc.projectRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get project: %w", err)
	}

	if project == nil {
		return nil, entities.NewNotFoundError("project", id)
	}

	return project, nil
}

// UpdateProject updates an existing project
func (uc *ProjectUseCases) UpdateProject(ctx context.Context, id string, req dtos.UpdateProjectRequest) (*entities.Project, error) {
	// Get existing project
	project, err := uc.GetProject(ctx, id)
	if err != nil {
		return nil, err
	}

	// Validate update request
	if err := req.Validate(); err != nil {
		return nil, entities.NewValidationError("invalid update data", err)
	}

	// Update fields
	if req.Name != nil {
		project.Name = *req.Name
	}
	if req.Description != nil {
		project.Description = *req.Description
	}
	if req.Status != nil {
		project.Status = *req.Status
	}
	if req.StartDate != nil {
		project.StartDate = req.StartDate
	}
	if req.EndDate != nil {
		project.EndDate = req.EndDate
	}
	if req.EstimatedDurationWeeks != nil {
		project.EstimatedDurationWeeks = *req.EstimatedDurationWeeks
	}
	if req.LearningObjectives != nil {
		project.LearningObjectives = req.LearningObjectives
	}
	if req.TechStack != nil {
		project.TechStack = req.TechStack
	}
	if req.ComplexityLevel != nil {
		project.ComplexityLevel = *req.ComplexityLevel
	}
	if req.EvaluationCriteria != nil {
		project.EvaluationCriteria = req.EvaluationCriteria
	}
	if req.Deliverables != nil {
		project.Deliverables = req.Deliverables
	}
	if req.Milestones != nil {
		project.Milestones = req.Milestones
	}

	project.UpdatedAt = time.Now()

	// Save updated project
	if err := uc.projectRepo.Update(ctx, project); err != nil {
		return nil, fmt.Errorf("failed to update project: %w", err)
	}

	return project, nil
}

// DeleteProject soft deletes a project
func (uc *ProjectUseCases) DeleteProject(ctx context.Context, id string) error {
	// Verify project exists
	_, err := uc.GetProject(ctx, id)
	if err != nil {
		return err
	}

	// Check if project can be deleted (e.g., no active teams or sprints)
	teams, err := uc.teamRepo.GetByProjectID(ctx, id)
	if err != nil {
		return fmt.Errorf("failed to check project teams: %w", err)
	}

	if len(teams) > 0 {
		return entities.NewBusinessRuleError("cannot delete project with active teams")
	}

	// Delete project
	if err := uc.projectRepo.Delete(ctx, id); err != nil {
		return fmt.Errorf("failed to delete project: %w", err)
	}

	return nil
}

// ListProjects retrieves projects with filters and pagination
func (uc *ProjectUseCases) ListProjects(ctx context.Context, filters repositories.ProjectFilters) ([]*entities.Project, int64, error) {
	// Set default pagination if not provided
	if filters.Page <= 0 {
		filters.Page = 1
	}
	if filters.PageSize <= 0 {
		filters.PageSize = 20
	}
	if filters.PageSize > 100 {
		filters.PageSize = 100
	}

	// Set default sorting
	if filters.SortBy == "" {
		filters.SortBy = "created_at"
	}
	if filters.SortOrder == "" {
		filters.SortOrder = "desc"
	}

	return uc.projectRepo.List(ctx, filters)
}

// GetProjectStats retrieves project statistics
func (uc *ProjectUseCases) GetProjectStats(ctx context.Context, projectID string) (*dtos.ProjectStats, error) {
	project, err := uc.GetProject(ctx, projectID)
	if err != nil {
		return nil, err
	}

	// Get teams count
	teams, err := uc.teamRepo.GetByProjectID(ctx, projectID)
	if err != nil {
		return nil, fmt.Errorf("failed to get project teams: %w", err)
	}

	// Get user stories stats
	userStories, err := uc.userStoryRepo.GetByProjectID(ctx, projectID)
	if err != nil {
		return nil, fmt.Errorf("failed to get project user stories: %w", err)
	}

	// Get sprints stats
	sprints, err := uc.sprintRepo.GetByProjectID(ctx, projectID)
	if err != nil {
		return nil, fmt.Errorf("failed to get project sprints: %w", err)
	}

	// Calculate statistics
	stats := &dtos.ProjectStats{
		ProjectID:         projectID,
		TeamsCount:        len(teams),
		TotalStudents:     calculateTotalStudents(teams),
		UserStoriesCount:  len(userStories),
		CompletedStories:  countStoriesByStatus(userStories, entities.StoryStatusDone),
		InProgressStories: countStoriesByStatus(userStories, entities.StoryStatusInProgress),
		SprintsCount:      len(sprints),
		ActiveSprints:     countSprintsByStatus(sprints, entities.SprintStatusActive),
		CompletionRate:    calculateCompletionRate(userStories),
		ProjectStatus:     project.Status,
	}

	return stats, nil
}

// Helper functions
func calculateTotalStudents(teams []*entities.Team) int {
	total := 0
	for _, team := range teams {
		// Count active team members
		activeMembers := 0
		for _, member := range team.Members {
			if member.IsActive {
				activeMembers++
			}
		}
		total += activeMembers
	}
	return total
}

func countStoriesByStatus(stories []*entities.UserStory, status entities.StoryStatus) int {
	count := 0
	for _, story := range stories {
		if story.Status == status {
			count++
		}
	}
	return count
}

func countSprintsByStatus(sprints []*entities.Sprint, status entities.SprintStatus) int {
	count := 0
	for _, sprint := range sprints {
		if sprint.Status == status {
			count++
		}
	}
	return count
}

func calculateCompletionRate(stories []*entities.UserStory) float64 {
	if len(stories) == 0 {
		return 0.0
	}

	completed := countStoriesByStatus(stories, entities.StoryStatusDone)
	return float64(completed) / float64(len(stories)) * 100
}
