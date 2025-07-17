package usecases

import (
	"context"
	"fmt"
	"time"

	"softwarefactoryservice/internal/application/dtos"
	"softwarefactoryservice/internal/domain/entities"
	"softwarefactoryservice/internal/domain/repositories"
)

// TeamUseCases handles business logic for teams
type TeamUseCases struct {
	teamRepo       repositories.TeamRepository
	projectRepo    repositories.ProjectRepository
	userStoryRepo  repositories.UserStoryRepository
	sprintRepo     repositories.SprintRepository
}

// NewTeamUseCases creates a new instance of TeamUseCases
func NewTeamUseCases(
	teamRepo repositories.TeamRepository,
	projectRepo repositories.ProjectRepository,
	userStoryRepo repositories.UserStoryRepository,
	sprintRepo repositories.SprintRepository,
) *TeamUseCases {
	return &TeamUseCases{
		teamRepo:      teamRepo,
		projectRepo:   projectRepo,
		userStoryRepo: userStoryRepo,
		sprintRepo:    sprintRepo,
	}
}

// CreateTeam creates a new team for a project
func (uc *TeamUseCases) CreateTeam(ctx context.Context, req dtos.CreateTeamRequest) (*entities.Team, error) {
	// Validate request
	if err := req.Validate(); err != nil {
		return nil, entities.NewValidationError("invalid team data", err)
	}

	// Verify project exists
	project, err := uc.projectRepo.GetByID(ctx, req.ProjectID.String())
	if err != nil {
		return nil, fmt.Errorf("failed to verify project: %w", err)
	}
	if project == nil {
		return nil, entities.NewNotFoundError("project", req.ProjectID.String())
	}

	// Check if project is in a state that allows team creation
	if project.Status == entities.ProjectStatusCompleted || project.Status == entities.ProjectStatusCancelled {
		return nil, entities.NewBusinessRuleError("cannot create teams for completed or cancelled projects")
	}

	// Create team entity
	team := req.ToTeamEntity()

	// Save team
	if err := uc.teamRepo.Create(ctx, team); err != nil {
		return nil, fmt.Errorf("failed to create team: %w", err)
	}

	return team, nil
}

// GetTeam retrieves a team by ID
func (uc *TeamUseCases) GetTeam(ctx context.Context, id string) (*entities.Team, error) {
	if id == "" {
		return nil, entities.NewValidationError("team ID is required", nil)
	}

	team, err := uc.teamRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get team: %w", err)
	}

	if team == nil {
		return nil, entities.NewNotFoundError("team", id)
	}

	return team, nil
}

// UpdateTeam updates an existing team
func (uc *TeamUseCases) UpdateTeam(ctx context.Context, id string, req dtos.UpdateTeamRequest) (*entities.Team, error) {
	// Get existing team
	team, err := uc.GetTeam(ctx, id)
	if err != nil {
		return nil, err
	}

	// Validate update request
	if err := req.Validate(); err != nil {
		return nil, entities.NewValidationError("invalid update data", err)
	}

	// Update fields
	if req.Name != nil {
		team.Name = *req.Name
	}
	if req.TeamCapacity != nil {
		// Check if new capacity is compatible with current members
		currentMembersCount := len(team.Members)
		if *req.TeamCapacity < currentMembersCount {
			return nil, entities.NewBusinessRuleError(fmt.Sprintf("cannot reduce capacity below current members count (%d)", currentMembersCount))
		}
		team.TeamCapacity = *req.TeamCapacity
	}

	team.UpdatedAt = time.Now()

	// Save updated team
	if err := uc.teamRepo.Update(ctx, team); err != nil {
		return nil, fmt.Errorf("failed to update team: %w", err)
	}

	return team, nil
}

// DeleteTeam soft deletes a team
func (uc *TeamUseCases) DeleteTeam(ctx context.Context, id string) error {
	// Verify team exists
	team, err := uc.GetTeam(ctx, id)
	if err != nil {
		return err
	}

	// Check if team can be deleted (e.g., no active sprints)
	if team.ActiveSprintID != nil {
		return entities.NewBusinessRuleError("cannot delete team with active sprint")
	}

	// Check if team has members
	if len(team.Members) > 0 {
		return entities.NewBusinessRuleError("cannot delete team with active members")
	}

	// Delete team
	if err := uc.teamRepo.Delete(ctx, id); err != nil {
		return fmt.Errorf("failed to delete team: %w", err)
	}

	return nil
}

// AddTeamMember adds a new member to a team
func (uc *TeamUseCases) AddTeamMember(ctx context.Context, teamID string, req dtos.AddTeamMemberRequest) error {
	// Validate request
	if err := req.Validate(); err != nil {
		return entities.NewValidationError("invalid member data", err)
	}

	// Get team
	team, err := uc.GetTeam(ctx, teamID)
	if err != nil {
		return err
	}

	// Check team capacity
	currentSize := len(team.Members)
	if currentSize >= team.TeamCapacity {
		return entities.NewBusinessRuleError("team is at full capacity")
	}

	// Check if apprentice is already in the team
	for _, member := range team.Members {
		if member.ApprenticeID == req.ApprenticeID && member.IsActive {
			return entities.NewBusinessRuleError("apprentice is already an active member of this team")
		}
	}

	// Add member to team
	if err := uc.teamRepo.AddMember(ctx, teamID, req.ApprenticeID.String()); err != nil {
		return fmt.Errorf("failed to add team member: %w", err)
	}

	return nil
}

// RemoveTeamMember removes a member from a team
func (uc *TeamUseCases) RemoveTeamMember(ctx context.Context, teamID, apprenticeID string) error {
	// Get team to verify it exists
	_, err := uc.GetTeam(ctx, teamID)
	if err != nil {
		return err
	}

	// Remove member from team
	if err := uc.teamRepo.RemoveMember(ctx, teamID, apprenticeID); err != nil {
		return fmt.Errorf("failed to remove team member: %w", err)
	}

	return nil
}

// GetProjectTeams retrieves all teams for a project
func (uc *TeamUseCases) GetProjectTeams(ctx context.Context, projectID string) ([]*entities.Team, error) {
	if projectID == "" {
		return nil, entities.NewValidationError("project ID is required", nil)
	}

	return uc.teamRepo.GetByProjectID(ctx, projectID)
}

// GetTeamMembers retrieves all members of a team
func (uc *TeamUseCases) GetTeamMembers(ctx context.Context, teamID string) ([]string, error) {
	if teamID == "" {
		return nil, entities.NewValidationError("team ID is required", nil)
	}

	return uc.teamRepo.GetTeamMembers(ctx, teamID)
}

// GetUserTeams retrieves all teams a user belongs to
func (uc *TeamUseCases) GetUserTeams(ctx context.Context, userID string) ([]*entities.Team, error) {
	if userID == "" {
		return nil, entities.NewValidationError("user ID is required", nil)
	}

	return uc.teamRepo.GetUserTeams(ctx, userID)
}

// ListTeams retrieves teams with filters and pagination
func (uc *TeamUseCases) ListTeams(ctx context.Context, filters repositories.TeamFilters) ([]*entities.Team, int64, error) {
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

	return uc.teamRepo.List(ctx, filters)
}

// GetTeamStats retrieves team statistics
func (uc *TeamUseCases) GetTeamStats(ctx context.Context, teamID string) (*dtos.TeamStats, error) {
	team, err := uc.GetTeam(ctx, teamID)
	if err != nil {
		return nil, err
	}

	// Count active members
	activeMembersCount := 0
	for _, member := range team.Members {
		if member.IsActive {
			activeMembersCount++
		}
	}

	// Get sprints stats
	sprints, err := uc.sprintRepo.GetByProjectID(ctx, team.ProjectID.String())
	if err != nil {
		return nil, fmt.Errorf("failed to get team sprints: %w", err)
	}

	// Calculate completed sprints for this team
	completedSprints := 0
	var currentSprintID *string
	
	for _, sprint := range sprints {
		// Note: This assumes sprints have team association
		// In practice, you might need to check if the sprint belongs to this team
		if sprint.Status == entities.SprintStatusCompleted {
			completedSprints++
		}
		if sprint.Status == entities.SprintStatusActive {
			sprintIDStr := sprint.ID.String()
			currentSprintID = &sprintIDStr
		}
	}

	// Calculate team velocity and completion rate
	// This would require more complex logic based on user stories completed
	averageVelocity := 0.0
	completionRate := 0.0

	// Count rotations due (members with rotation dates in the past)
	rotationsDue := 0
	now := time.Now()
	for _, member := range team.Members {
		if member.IsActive && member.RotationSchedule.NextRotationDate != nil && 
		   member.RotationSchedule.NextRotationDate.Before(now) {
			rotationsDue++
		}
	}

	stats := &dtos.TeamStats{
		TeamID:             teamID,
		MembersCount:       len(team.Members),
		ActiveMembersCount: activeMembersCount,
		CompletedSprints:   completedSprints,
		CurrentSprintID:    currentSprintID,
		AverageVelocity:    averageVelocity,
		CompletionRate:     completionRate,
		RotationsDue:       rotationsDue,
	}

	return stats, nil
}
