package repositories

import (
	"context"

	"softwarefactoryservice/internal/domain/entities"
)

// TeamRepository defines the interface for team data operations
type TeamRepository interface {
	// Create creates a new team
	Create(ctx context.Context, team *entities.Team) error
	
	// GetByID retrieves a team by its ID
	GetByID(ctx context.Context, id string) (*entities.Team, error)
	
	// GetByProjectID retrieves teams by project ID
	GetByProjectID(ctx context.Context, projectID string) ([]*entities.Team, error)
	
	// GetByLeaderID retrieves teams by leader ID
	GetByLeaderID(ctx context.Context, leaderID string) ([]*entities.Team, error)
	
	// Update updates an existing team
	Update(ctx context.Context, team *entities.Team) error
	
	// Delete soft deletes a team
	Delete(ctx context.Context, id string) error
	
	// AddMember adds a member to a team
	AddMember(ctx context.Context, teamID, userID string) error
	
	// RemoveMember removes a member from a team
	RemoveMember(ctx context.Context, teamID, userID string) error
	
	// GetTeamMembers retrieves all members of a team
	GetTeamMembers(ctx context.Context, teamID string) ([]string, error)
	
	// GetUserTeams retrieves all teams a user belongs to
	GetUserTeams(ctx context.Context, userID string) ([]*entities.Team, error)
	
	// List retrieves teams with pagination and filters
	List(ctx context.Context, filters TeamFilters) ([]*entities.Team, int64, error)
	
	// UpdateTeamSize updates the current team size
	UpdateTeamSize(ctx context.Context, teamID string, currentSize int) error
}

// TeamFilters defines filters for team listing
type TeamFilters struct {
	ProjectID    *string `json:"project_id,omitempty"`
	LeaderID     *string `json:"leader_id,omitempty"`
	MinSize      *int    `json:"min_size,omitempty"`
	MaxSize      *int    `json:"max_size,omitempty"`
	Search       *string `json:"search,omitempty"`
	Page         int     `json:"page"`
	PageSize     int     `json:"page_size"`
	SortBy       string  `json:"sort_by"`
	SortOrder    string  `json:"sort_order"`
}
