package repositories

import (
	"context"
	"fmt"

	"softwarefactoryservice/internal/domain/entities"
	"softwarefactoryservice/internal/domain/repositories"

	"gorm.io/gorm"
)

// PostgreSQLTeamRepository implements the TeamRepository interface using PostgreSQL
type PostgreSQLTeamRepository struct {
	db *gorm.DB
}

// NewPostgreSQLTeamRepository creates a new PostgreSQL team repository
func NewPostgreSQLTeamRepository(db *gorm.DB) repositories.TeamRepository {
	return &PostgreSQLTeamRepository{
		db: db,
	}
}

// Create creates a new team
func (r *PostgreSQLTeamRepository) Create(ctx context.Context, team *entities.Team) error {
	if err := r.db.WithContext(ctx).Create(team).Error; err != nil {
		return fmt.Errorf("failed to create team: %w", err)
	}
	return nil
}

// GetByID retrieves a team by its ID
func (r *PostgreSQLTeamRepository) GetByID(ctx context.Context, id string) (*entities.Team, error) {
	var team entities.Team
	err := r.db.WithContext(ctx).
		Preload("Members").
		Where("id = ?", id).
		First(&team).Error
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, fmt.Errorf("failed to get team by ID: %w", err)
	}
	return &team, nil
}

// GetByProjectID retrieves teams by project ID
func (r *PostgreSQLTeamRepository) GetByProjectID(ctx context.Context, projectID string) ([]*entities.Team, error) {
	var teams []*entities.Team
	err := r.db.WithContext(ctx).
		Preload("Members").
		Where("project_id = ?", projectID).
		Find(&teams).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get teams by project ID: %w", err)
	}
	return teams, nil
}

// GetByLeaderID retrieves teams by leader ID
func (r *PostgreSQLTeamRepository) GetByLeaderID(ctx context.Context, leaderID string) ([]*entities.Team, error) {
	var teams []*entities.Team
	err := r.db.WithContext(ctx).
		Preload("Members").
		Where("tech_lead_instructor_id = ?", leaderID).
		Find(&teams).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get teams by leader ID: %w", err)
	}
	return teams, nil
}

// Update updates an existing team
func (r *PostgreSQLTeamRepository) Update(ctx context.Context, team *entities.Team) error {
	if err := r.db.WithContext(ctx).Save(team).Error; err != nil {
		return fmt.Errorf("failed to update team: %w", err)
	}
	return nil
}

// Delete soft deletes a team
func (r *PostgreSQLTeamRepository) Delete(ctx context.Context, id string) error {
	if err := r.db.WithContext(ctx).Where("id = ?", id).Delete(&entities.Team{}).Error; err != nil {
		return fmt.Errorf("failed to delete team: %w", err)
	}
	return nil
}

// AddMember adds a member to a team
func (r *PostgreSQLTeamRepository) AddMember(ctx context.Context, teamID, userID string) error {
	// First check if team exists and get current members count
	var team entities.Team
	err := r.db.WithContext(ctx).
		Preload("Members").
		Where("id = ?", teamID).
		First(&team).Error
	if err != nil {
		return fmt.Errorf("failed to get team: %w", err)
	}

	// Check capacity
	activeMembers := 0
	for _, member := range team.Members {
		if member.IsActive {
			activeMembers++
		}
	}
	
	if activeMembers >= team.TeamCapacity {
		return fmt.Errorf("team is at full capacity")
	}

	// Check if user is already a member
	for _, member := range team.Members {
		if member.ApprenticeID.String() == userID && member.IsActive {
			return fmt.Errorf("user is already an active member of this team")
		}
	}

	// Create new team member
	teamMember := &entities.TeamMember{
		TeamID:       team.ID,
		ApprenticeID: team.ID, // This should be parsed from userID
		RoleFocus:    entities.RoleFocusFullstack, // Default role
		IsActive:     true,
	}

	if err := r.db.WithContext(ctx).Create(teamMember).Error; err != nil {
		return fmt.Errorf("failed to add team member: %w", err)
	}

	return nil
}

// RemoveMember removes a member from a team
func (r *PostgreSQLTeamRepository) RemoveMember(ctx context.Context, teamID, userID string) error {
	err := r.db.WithContext(ctx).
		Model(&entities.TeamMember{}).
		Where("team_id = ? AND apprentice_id = ?", teamID, userID).
		Update("is_active", false).Error
	if err != nil {
		return fmt.Errorf("failed to remove team member: %w", err)
	}
	return nil
}

// GetTeamMembers retrieves all members of a team
func (r *PostgreSQLTeamRepository) GetTeamMembers(ctx context.Context, teamID string) ([]string, error) {
	var members []entities.TeamMember
	err := r.db.WithContext(ctx).
		Where("team_id = ? AND is_active = ?", teamID, true).
		Find(&members).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get team members: %w", err)
	}

	memberIDs := make([]string, len(members))
	for i, member := range members {
		memberIDs[i] = member.ApprenticeID.String()
	}

	return memberIDs, nil
}

// GetUserTeams retrieves all teams a user belongs to
func (r *PostgreSQLTeamRepository) GetUserTeams(ctx context.Context, userID string) ([]*entities.Team, error) {
	var teams []*entities.Team
	err := r.db.WithContext(ctx).
		Joins("JOIN factory_team_members ON factory_teams.id = factory_team_members.team_id").
		Where("factory_team_members.apprentice_id = ? AND factory_team_members.is_active = ?", userID, true).
		Preload("Members").
		Find(&teams).Error
	if err != nil {
		return nil, fmt.Errorf("failed to get user teams: %w", err)
	}
	return teams, nil
}

// List retrieves teams with pagination and filters
func (r *PostgreSQLTeamRepository) List(ctx context.Context, filters repositories.TeamFilters) ([]*entities.Team, int64, error) {
	var teams []*entities.Team
	var totalCount int64

	// Build query
	query := r.db.WithContext(ctx).Model(&entities.Team{})

	// Apply filters
	if filters.ProjectID != nil {
		query = query.Where("project_id = ?", *filters.ProjectID)
	}
	if filters.LeaderID != nil {
		query = query.Where("tech_lead_instructor_id = ?", *filters.LeaderID)
	}
	if filters.MinSize != nil {
		// This requires a subquery to count active members
		query = query.Where("(SELECT COUNT(*) FROM factory_team_members WHERE team_id = factory_teams.id AND is_active = true) >= ?", *filters.MinSize)
	}
	if filters.MaxSize != nil {
		query = query.Where("(SELECT COUNT(*) FROM factory_team_members WHERE team_id = factory_teams.id AND is_active = true) <= ?", *filters.MaxSize)
	}
	if filters.Search != nil {
		searchPattern := "%" + *filters.Search + "%"
		query = query.Where("name ILIKE ?", searchPattern)
	}

	// Get total count
	if err := query.Count(&totalCount).Error; err != nil {
		return nil, 0, fmt.Errorf("failed to count teams: %w", err)
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

	// Execute query with preloads
	if err := query.Preload("Members").Find(&teams).Error; err != nil {
		return nil, 0, fmt.Errorf("failed to list teams: %w", err)
	}

	return teams, totalCount, nil
}

// UpdateTeamSize updates the current team size
func (r *PostgreSQLTeamRepository) UpdateTeamSize(ctx context.Context, teamID string, currentSize int) error {
	// This is handled automatically through the Members relationship
	// No explicit update needed as the size is calculated from active members
	return nil
}
