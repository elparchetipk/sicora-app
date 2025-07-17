package dtos

import (
	"errors"
	"time"

	"softwarefactoryservice/internal/domain/entities"

	"github.com/google/uuid"
)

// CreateTeamRequest represents the request to create a new team
type CreateTeamRequest struct {
	Name                 string    `json:"name" validate:"required,min=3,max=100"`
	ProjectID            uuid.UUID `json:"project_id" validate:"required"`
	TechLeadInstructorID uuid.UUID `json:"tech_lead_instructor_id" validate:"required"`
	TeamCapacity         int       `json:"team_capacity" validate:"min=4,max=6"`
}

// Validate validates the create team request
func (r CreateTeamRequest) Validate() error {
	if r.Name == "" {
		return errors.New("name is required")
	}
	if len(r.Name) < 3 || len(r.Name) > 100 {
		return errors.New("name must be between 3 and 100 characters")
	}
	if r.TeamCapacity < 4 || r.TeamCapacity > 6 {
		return errors.New("team capacity must be between 4 and 6 members")
	}
	return nil
}

// UpdateTeamRequest represents the request to update a team
type UpdateTeamRequest struct {
	Name         *string    `json:"name,omitempty"`
	TeamCapacity *int       `json:"team_capacity,omitempty"`
}

// Validate validates the update team request
func (r UpdateTeamRequest) Validate() error {
	if r.Name != nil {
		if len(*r.Name) < 3 || len(*r.Name) > 100 {
			return errors.New("name must be between 3 and 100 characters")
		}
	}
	if r.TeamCapacity != nil {
		if *r.TeamCapacity < 4 || *r.TeamCapacity > 6 {
			return errors.New("team capacity must be between 4 and 6 members")
		}
	}
	return nil
}

// AddTeamMemberRequest represents the request to add a member to a team
type AddTeamMemberRequest struct {
	ApprenticeID  uuid.UUID               `json:"apprentice_id" validate:"required"`
	RoleFocus     entities.RoleFocus      `json:"role_focus" validate:"required"`
	JoinDate      time.Time               `json:"join_date"`
	RotationPlan  *entities.RotationSchedule `json:"rotation_plan,omitempty"`
}

// Validate validates the add team member request
func (r AddTeamMemberRequest) Validate() error {
	if r.ApprenticeID == uuid.Nil {
		return errors.New("apprentice ID is required")
	}
	if r.RoleFocus == "" {
		return errors.New("role focus is required")
	}
	if r.JoinDate.IsZero() {
		r.JoinDate = time.Now()
	}
	return nil
}

// TeamResponse represents the response for team operations
type TeamResponse struct {
	ID                   uuid.UUID              `json:"id"`
	Name                 string                 `json:"name"`
	ProjectID            uuid.UUID              `json:"project_id"`
	TechLeadInstructorID uuid.UUID              `json:"tech_lead_instructor_id"`
	TeamCapacity         int                    `json:"team_capacity"`
	ActiveSprintID       *uuid.UUID             `json:"active_sprint_id,omitempty"`
	CreatedAt            time.Time              `json:"created_at"`
	UpdatedAt            time.Time              `json:"updated_at"`
	CurrentSize          int                    `json:"current_size"`
	Members              []TeamMemberResponse   `json:"members,omitempty"`
}

// TeamMemberResponse represents a team member in responses
type TeamMemberResponse struct {
	ID               uuid.UUID                  `json:"id"`
	TeamID           uuid.UUID                  `json:"team_id"`
	ApprenticeID     uuid.UUID                  `json:"apprentice_id"`
	RoleFocus        entities.RoleFocus         `json:"role_focus"`
	JoinDate         time.Time                  `json:"join_date"`
	LeaveDate        *time.Time                 `json:"leave_date,omitempty"`
	IsActive         bool                       `json:"is_active"`
	RotationSchedule entities.RotationSchedule `json:"rotation_schedule"`
	CreatedAt        time.Time                  `json:"created_at"`
	UpdatedAt        time.Time                  `json:"updated_at"`
}

// TeamListResponse represents the response for team listing
type TeamListResponse struct {
	Teams      []TeamResponse `json:"teams"`
	TotalCount int64          `json:"total_count"`
	Page       int            `json:"page"`
	PageSize   int            `json:"page_size"`
	TotalPages int            `json:"total_pages"`
}

// TeamStats represents team statistics
type TeamStats struct {
	TeamID              string  `json:"team_id"`
	MembersCount        int     `json:"members_count"`
	ActiveMembersCount  int     `json:"active_members_count"`
	CompletedSprints    int     `json:"completed_sprints"`
	CurrentSprintID     *string `json:"current_sprint_id,omitempty"`
	AverageVelocity     float64 `json:"average_velocity"`
	CompletionRate      float64 `json:"completion_rate"`
	RotationsDue        int     `json:"rotations_due"`
}

// ToTeamEntity converts CreateTeamRequest to Team entity
func (r CreateTeamRequest) ToTeamEntity() *entities.Team {
	return &entities.Team{
		ID:                   uuid.New(),
		Name:                 r.Name,
		ProjectID:            r.ProjectID,
		TechLeadInstructorID: r.TechLeadInstructorID,
		TeamCapacity:         r.TeamCapacity,
		CreatedAt:            time.Now(),
		UpdatedAt:            time.Now(),
	}
}

// FromTeamEntity converts Team entity to TeamResponse
func FromTeamEntity(team *entities.Team) TeamResponse {
	response := TeamResponse{
		ID:                   team.ID,
		Name:                 team.Name,
		ProjectID:            team.ProjectID,
		TechLeadInstructorID: team.TechLeadInstructorID,
		TeamCapacity:         team.TeamCapacity,
		ActiveSprintID:       team.ActiveSprintID,
		CreatedAt:            team.CreatedAt,
		UpdatedAt:            team.UpdatedAt,
		CurrentSize:          len(team.Members),
	}

	// Convert members if they exist
	if team.Members != nil {
		response.Members = make([]TeamMemberResponse, len(team.Members))
		for i, member := range team.Members {
			response.Members[i] = TeamMemberResponse{
				ID:               member.ID,
				TeamID:           member.TeamID,
				ApprenticeID:     member.ApprenticeID,
				RoleFocus:        member.RoleFocus,
				JoinDate:         member.JoinDate,
				LeaveDate:        member.LeaveDate,
				IsActive:         member.IsActive,
				RotationSchedule: member.RotationSchedule,
				CreatedAt:        member.CreatedAt,
				UpdatedAt:        member.UpdatedAt,
			}
		}
	}

	return response
}
