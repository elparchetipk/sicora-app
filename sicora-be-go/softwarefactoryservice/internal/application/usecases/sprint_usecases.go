package usecases

import (
	"context"
	"fmt"
	"time"

	"softwarefactoryservice/internal/application/dtos"
	"softwarefactoryservice/internal/domain/entities"
	"softwarefactoryservice/internal/domain/repositories"
)

// SprintUseCases handles business logic for sprints
type SprintUseCases struct {
	sprintRepo    repositories.SprintRepository
	projectRepo   repositories.ProjectRepository
	teamRepo      repositories.TeamRepository
	userStoryRepo repositories.UserStoryRepository
}

// NewSprintUseCases creates a new instance of SprintUseCases
func NewSprintUseCases(
	sprintRepo repositories.SprintRepository,
	projectRepo repositories.ProjectRepository,
	teamRepo repositories.TeamRepository,
	userStoryRepo repositories.UserStoryRepository,
) *SprintUseCases {
	return &SprintUseCases{
		sprintRepo:    sprintRepo,
		projectRepo:   projectRepo,
		teamRepo:      teamRepo,
		userStoryRepo: userStoryRepo,
	}
}

// CreateSprint creates a new sprint
func (uc *SprintUseCases) CreateSprint(ctx context.Context, req dtos.CreateSprintRequest) (*entities.Sprint, error) {
	// Validate dates
	if req.EndDate.Before(req.StartDate) {
		return nil, entities.NewValidationError("end_date", fmt.Errorf("end date must be after start date"))
	}

	// Verify project exists
	project, err := uc.projectRepo.GetByID(ctx, req.ProjectID.String())
	if err != nil {
		return nil, fmt.Errorf("failed to verify project: %w", err)
	}
	if project == nil {
		return nil, entities.NewNotFoundError("project", req.ProjectID.String())
	}

	// Verify team exists
	team, err := uc.teamRepo.GetByID(ctx, req.TeamID.String())
	if err != nil {
		return nil, fmt.Errorf("failed to verify team: %w", err)
	}
	if team == nil {
		return nil, entities.NewNotFoundError("team", req.TeamID.String())
	}

	// Check for overlapping sprints
	existingSprints, err := uc.sprintRepo.GetByProjectID(ctx, req.ProjectID.String())
	if err != nil {
		return nil, fmt.Errorf("failed to check existing sprints: %w", err)
	}

	for _, sprint := range existingSprints {
		if uc.sprintsOverlap(req.StartDate, req.EndDate, sprint.StartDate, sprint.EndDate) {
			return nil, entities.NewBusinessRuleError("sprint dates overlap with existing sprint")
		}
	}

	// Create sprint entity
	sprint := req.ToEntity()

	// Save sprint
	if err := uc.sprintRepo.Create(ctx, sprint); err != nil {
		return nil, fmt.Errorf("failed to create sprint: %w", err)
	}

	return sprint, nil
}

// UpdateSprint updates an existing sprint
func (uc *SprintUseCases) UpdateSprint(ctx context.Context, id string, req dtos.UpdateSprintRequest) (*entities.Sprint, error) {
	// Get existing sprint
	sprint, err := uc.sprintRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get sprint: %w", err)
	}

	// Update fields
	if req.SprintGoal != nil {
		sprint.SprintGoal = *req.SprintGoal
	}
	if req.LearningObjectives != nil {
		sprint.LearningObjectives = req.LearningObjectives
	}
	if req.Status != nil {
		sprint.Status = *req.Status
	}
	if req.VelocityPoints != nil {
		sprint.VelocityPoints = *req.VelocityPoints
	}

	// Save changes
	if err := uc.sprintRepo.Update(ctx, sprint); err != nil {
		return nil, fmt.Errorf("failed to update sprint: %w", err)
	}

	return sprint, nil
}

// GetSprintByID retrieves a sprint by ID
func (uc *SprintUseCases) GetSprintByID(ctx context.Context, id string) (*entities.Sprint, error) {
	sprint, err := uc.sprintRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get sprint: %w", err)
	}
	return sprint, nil
}

// DeleteSprint deletes a sprint
func (uc *SprintUseCases) DeleteSprint(ctx context.Context, id string) error {
	// Get sprint to verify it exists
	sprint, err := uc.sprintRepo.GetByID(ctx, id)
	if err != nil {
		return fmt.Errorf("failed to get sprint: %w", err)
	}

	// Check if sprint can be deleted (business rules)
	if sprint.Status == entities.SprintStatusActive {
		return entities.NewBusinessRuleError("cannot delete an active sprint")
	}

	// Delete sprint
	if err := uc.sprintRepo.Delete(ctx, id); err != nil {
		return fmt.Errorf("failed to delete sprint: %w", err)
	}

	return nil
}

// GetSprintsByProject retrieves all sprints for a project
func (uc *SprintUseCases) GetSprintsByProject(ctx context.Context, projectID string) ([]*entities.Sprint, error) {
	sprints, err := uc.sprintRepo.GetByProjectID(ctx, projectID)
	if err != nil {
		return nil, fmt.Errorf("failed to get sprints by project: %w", err)
	}
	return sprints, nil
}

// GetSprintsByTeam retrieves all sprints for a team
func (uc *SprintUseCases) GetSprintsByTeam(ctx context.Context, teamID string) ([]*entities.Sprint, error) {
	// Get all sprints and filter by team ID
	allSprints, _, err := uc.sprintRepo.List(ctx, repositories.SprintFilters{
		Page:     1,
		PageSize: 1000, // Large number to get all sprints
	})
	if err != nil {
		return nil, fmt.Errorf("failed to get sprints: %w", err)
	}

	var teamSprints []*entities.Sprint
	for _, sprint := range allSprints {
		if sprint.TeamID.String() == teamID {
			teamSprints = append(teamSprints, sprint)
		}
	}

	return teamSprints, nil
}

// StartSprint starts a sprint
func (uc *SprintUseCases) StartSprint(ctx context.Context, id string) (*entities.Sprint, error) {
	sprint, err := uc.sprintRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get sprint: %w", err)
	}

	// Validate business rules
	if sprint.Status != entities.SprintStatusPlanning {
		return nil, entities.NewBusinessRuleError("only sprints in planning status can be started")
	}

	if time.Now().Before(sprint.StartDate) {
		return nil, entities.NewBusinessRuleError("cannot start sprint before start date")
	}

	// Update status
	sprint.Status = entities.SprintStatusActive

	if err := uc.sprintRepo.Update(ctx, sprint); err != nil {
		return nil, fmt.Errorf("failed to start sprint: %w", err)
	}

	return sprint, nil
}

// CompleteSprint completes a sprint
func (uc *SprintUseCases) CompleteSprint(ctx context.Context, id string) (*entities.Sprint, error) {
	sprint, err := uc.sprintRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get sprint: %w", err)
	}

	// Validate business rules
	if sprint.Status != entities.SprintStatusActive {
		return nil, entities.NewBusinessRuleError("only active sprints can be completed")
	}

	// Update status
	sprint.Status = entities.SprintStatusCompleted

	// Calculate completed stories
	userStories, err := uc.userStoryRepo.GetBySprintID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get user stories: %w", err)
	}

	completedCount := 0
	for _, story := range userStories {
		if story.Status == entities.StoryStatusDone {
			completedCount++
		}
	}
	sprint.StoriesCompleted = completedCount

	if err := uc.sprintRepo.Update(ctx, sprint); err != nil {
		return nil, fmt.Errorf("failed to complete sprint: %w", err)
	}

	return sprint, nil
}

// GetSprintStatistics retrieves sprint statistics
func (uc *SprintUseCases) GetSprintStatistics(ctx context.Context, id string) (*dtos.SprintStatisticsDTO, error) {
	sprint, err := uc.sprintRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get sprint: %w", err)
	}

	// Get user stories for this sprint
	userStories, err := uc.userStoryRepo.GetBySprintID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get user stories: %w", err)
	}

	// Calculate statistics
	totalStories := len(userStories)
	completedStories := 0
	for _, story := range userStories {
		if story.Status == entities.StoryStatusDone {
			completedStories++
		}
	}

	var completionRate float64
	if totalStories > 0 {
		completionRate = float64(completedStories) / float64(totalStories) * 100
	}

	// Calculate days remaining
	daysRemaining := 0
	if time.Now().Before(sprint.EndDate) {
		daysRemaining = int(sprint.EndDate.Sub(time.Now()).Hours() / 24)
	}

	return &dtos.SprintStatisticsDTO{
		ID:               sprint.ID.String(),
		SprintNumber:     sprint.SprintNumber,
		Status:           string(sprint.Status),
		TotalStories:     totalStories,
		CompletedStories: completedStories,
		CompletionRate:   completionRate,
		VelocityPoints:   sprint.VelocityPoints,
		TeamEfficiency:   completionRate, // Simplified calculation
		LearningProgress: completionRate, // Simplified calculation
		DaysRemaining:    daysRemaining,
		StartDate:        sprint.StartDate,
		EndDate:          sprint.EndDate,
	}, nil
}

// Helper function to check if two sprint date ranges overlap
func (uc *SprintUseCases) sprintsOverlap(start1, end1, start2, end2 time.Time) bool {
	return start1.Before(end2) && end1.After(start2)
}
