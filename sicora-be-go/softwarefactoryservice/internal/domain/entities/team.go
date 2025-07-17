package entities

import (
	"time"

	"github.com/google/uuid"
)

// RoleFocus representa el área de especialización de un aprendiz
type RoleFocus string

const (
	RoleFocusFrontend  RoleFocus = "frontend"
	RoleFocusBackend   RoleFocus = "backend"
	RoleFocusQA        RoleFocus = "qa"
	RoleFocusDevOps    RoleFocus = "devops"
	RoleFocusFullstack RoleFocus = "fullstack"
)

// Team representa un equipo de desarrollo en la fábrica
type Team struct {
	ID                   uuid.UUID       `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	Name                 string          `json:"name" gorm:"not null;size:255" validate:"required,min=3,max=100"`
	ProjectID            uuid.UUID       `json:"project_id" gorm:"type:uuid;not null"`
	TechLeadInstructorID uuid.UUID       `json:"tech_lead_instructor_id" gorm:"type:uuid;not null"`
	TeamCapacity         int             `json:"team_capacity" gorm:"not null;default:6" validate:"min=4,max=6"`
	ActiveSprintID       *uuid.UUID      `json:"active_sprint_id,omitempty" gorm:"type:uuid"`
	CreatedAt            time.Time       `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt            time.Time       `json:"updated_at" gorm:"autoUpdateTime"`
	
	// Relationships
	Project              Project         `json:"project,omitempty" gorm:"foreignKey:ProjectID"`
	Members              []TeamMember    `json:"members,omitempty" gorm:"foreignKey:TeamID"`
	Sprints              []Sprint        `json:"sprints,omitempty" gorm:"foreignKey:TeamID"`
}

// TeamMember representa un miembro del equipo (aprendiz)
type TeamMember struct {
	ID               uuid.UUID      `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	TeamID           uuid.UUID      `json:"team_id" gorm:"type:uuid;not null"`
	ApprenticeID     uuid.UUID      `json:"apprentice_id" gorm:"type:uuid;not null"`
	RoleFocus        RoleFocus      `json:"role_focus" gorm:"type:varchar(20)" validate:"required"`
	JoinDate         time.Time      `json:"join_date" gorm:"not null"`
	LeaveDate        *time.Time     `json:"leave_date,omitempty"`
	IsActive         bool           `json:"is_active" gorm:"default:true"`
	RotationSchedule RotationSchedule `json:"rotation_schedule" gorm:"embedded;embeddedPrefix:rotation_"`
	CreatedAt        time.Time      `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt        time.Time      `json:"updated_at" gorm:"autoUpdateTime"`
	
	// Relationships
	Team             Team           `json:"team,omitempty" gorm:"foreignKey:TeamID"`
	Evaluations      []Evaluation   `json:"evaluations,omitempty" gorm:"foreignKey:ApprenticeID"`
}

// RotationSchedule representa el cronograma de rotación de un aprendiz
type RotationSchedule struct {
	NextRotationDate   *time.Time `json:"next_rotation_date,omitempty" gorm:"column:rotation_next_rotation_date"`
	RotationFrequency  int        `json:"rotation_frequency" gorm:"column:rotation_frequency;default:8"` // weeks
	CanRotateEarly     bool       `json:"can_rotate_early" gorm:"column:rotation_can_rotate_early;default:false"`
	PreferredNextTeam  *uuid.UUID `json:"preferred_next_team,omitempty" gorm:"column:rotation_preferred_next_team;type:uuid"`
}

// TableName especifica el nombre de la tabla para GORM
func (Team) TableName() string {
	return "factory_teams"
}

// TableName especifica el nombre de la tabla para GORM
func (TeamMember) TableName() string {
	return "factory_team_members"
}

// Validate valida las reglas de negocio del equipo
func (t *Team) Validate() error {
	if t.TeamCapacity < 4 || t.TeamCapacity > 6 {
		return &ValidationError{Field: "team_capacity", Message: "team capacity must be between 4 and 6 members"}
	}
	
	return nil
}

// IsFull verifica si el equipo está completo
func (t *Team) IsFull() bool {
	activeMembers := 0
	for _, member := range t.Members {
		if member.IsActive {
			activeMembers++
		}
	}
	return activeMembers >= t.TeamCapacity
}

// GetActiveMembersCount retorna el número de miembros activos
func (t *Team) GetActiveMembersCount() int {
	activeMembers := 0
	for _, member := range t.Members {
		if member.IsActive {
			activeMembers++
		}
	}
	return activeMembers
}

// HasMember verifica si un aprendiz específico es miembro del equipo
func (t *Team) HasMember(apprenticeID uuid.UUID) bool {
	for _, member := range t.Members {
		if member.ApprenticeID == apprenticeID && member.IsActive {
			return true
		}
	}
	return false
}

// GetMembersByRole retorna miembros filtrados por rol
func (t *Team) GetMembersByRole(role RoleFocus) []TeamMember {
	var members []TeamMember
	for _, member := range t.Members {
		if member.RoleFocus == role && member.IsActive {
			members = append(members, member)
		}
	}
	return members
}

// Validate valida las reglas de negocio del miembro del equipo
func (tm *TeamMember) Validate() error {
	if tm.JoinDate.After(time.Now()) {
		return &ValidationError{Field: "join_date", Message: "join date cannot be in the future"}
	}
	
	if tm.LeaveDate != nil && tm.LeaveDate.Before(tm.JoinDate) {
		return &ValidationError{Field: "leave_date", Message: "leave date cannot be before join date"}
	}
	
	return nil
}

// IsEligibleForRotation verifica si el miembro es elegible para rotación
func (tm *TeamMember) IsEligibleForRotation() bool {
	if !tm.IsActive {
		return false
	}
	
	if tm.RotationSchedule.NextRotationDate == nil {
		return false
	}
	
	return time.Now().After(*tm.RotationSchedule.NextRotationDate) || tm.RotationSchedule.CanRotateEarly
}

// CalculateNextRotationDate calcula la próxima fecha de rotación
func (tm *TeamMember) CalculateNextRotationDate() time.Time {
	weeks := tm.RotationSchedule.RotationFrequency
	if weeks == 0 {
		weeks = 8 // Default 8 weeks
	}
	return tm.JoinDate.AddDate(0, 0, weeks*7)
}
