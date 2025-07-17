package entities

import (
	"errors"
	"time"

	"github.com/google/uuid"
)

type StakeholderRole string

const (
	StakeholderRoleCoordinator StakeholderRole = "coordinator"
	StakeholderRoleJuror       StakeholderRole = "juror"
	StakeholderRoleManager     StakeholderRole = "manager"
	StakeholderRoleExternal    StakeholderRole = "external"
	StakeholderRoleObserver    StakeholderRole = "observer"
)

type StakeholderType string

const (
	StakeholderTypeInternal StakeholderType = "internal"
	StakeholderTypeExternal StakeholderType = "external"
	StakeholderTypeIndustry StakeholderType = "industry"
	StakeholderTypeAcademic StakeholderType = "academic"
)

type StakeholderStatus string

const (
	StakeholderStatusActive   StakeholderStatus = "active"
	StakeholderStatusInactive StakeholderStatus = "inactive"
	StakeholderStatusPending  StakeholderStatus = "pending"
	StakeholderStatusBlocked  StakeholderStatus = "blocked"
)

type Stakeholder struct {
	ID           uuid.UUID         `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	ProjectID    uuid.UUID         `json:"project_id" gorm:"type:uuid;not null;index"`
	UserID       uuid.UUID         `json:"user_id" gorm:"type:uuid;not null;index"`
	Role         StakeholderRole   `json:"role" gorm:"type:varchar(50);not null"`
	Type         StakeholderType   `json:"type" gorm:"type:varchar(50);not null"`
	Status       StakeholderStatus `json:"status" gorm:"type:varchar(50);not null;default:'active'"`
	Organization string            `json:"organization" gorm:"type:varchar(255)"`
	Department   string            `json:"department" gorm:"type:varchar(255)"`
	Position     string            `json:"position" gorm:"type:varchar(255)"`
	Expertise    []string          `json:"expertise" gorm:"type:text[]"`
	ContactEmail string            `json:"contact_email" gorm:"type:varchar(255)"`
	ContactPhone string            `json:"contact_phone" gorm:"type:varchar(50)"`
	AccessLevel  int               `json:"access_level" gorm:"default:1"`
	CanEvaluate  bool              `json:"can_evaluate" gorm:"default:false"`
	CanReview    bool              `json:"can_review" gorm:"default:false"`
	CanApprove   bool              `json:"can_approve" gorm:"default:false"`
	Notes        string            `json:"notes" gorm:"type:text"`
	AssignedAt   time.Time         `json:"assigned_at" gorm:"default:CURRENT_TIMESTAMP"`
	LastActiveAt *time.Time        `json:"last_active_at"`
	CreatedAt    time.Time         `json:"created_at" gorm:"default:CURRENT_TIMESTAMP"`
	UpdatedAt    time.Time         `json:"updated_at" gorm:"default:CURRENT_TIMESTAMP"`

	// Relations
	Project *Project `json:"project,omitempty" gorm:"foreignKey:ProjectID"`
}

func NewStakeholder(projectID, userID uuid.UUID, role StakeholderRole, stakeholderType StakeholderType) *Stakeholder {
	return &Stakeholder{
		ID:          uuid.New(),
		ProjectID:   projectID,
		UserID:      userID,
		Role:        role,
		Type:        stakeholderType,
		Status:      StakeholderStatusActive,
		AccessLevel: 1,
		AssignedAt:  time.Now(),
		CreatedAt:   time.Now(),
		UpdatedAt:   time.Now(),
	}
}

func (s *Stakeholder) IsValid() error {
	if s.ProjectID == uuid.Nil {
		return errors.New("project ID is required")
	}
	if s.UserID == uuid.Nil {
		return errors.New("user ID is required")
	}
	if !s.IsValidRole(s.Role) {
		return errors.New("invalid stakeholder role")
	}
	if !s.IsValidType(s.Type) {
		return errors.New("invalid stakeholder type")
	}
	if !s.IsValidStatus(s.Status) {
		return errors.New("invalid stakeholder status")
	}
	if s.AccessLevel < 1 || s.AccessLevel > 5 {
		return errors.New("access level must be between 1 and 5")
	}
	return nil
}

func (s *Stakeholder) IsValidRole(role StakeholderRole) bool {
	validRoles := []StakeholderRole{
		StakeholderRoleCoordinator,
		StakeholderRoleJuror,
		StakeholderRoleManager,
		StakeholderRoleExternal,
		StakeholderRoleObserver,
	}
	for _, validRole := range validRoles {
		if role == validRole {
			return true
		}
	}
	return false
}

func (s *Stakeholder) IsValidType(stakeholderType StakeholderType) bool {
	validTypes := []StakeholderType{
		StakeholderTypeInternal,
		StakeholderTypeExternal,
		StakeholderTypeIndustry,
		StakeholderTypeAcademic,
	}
	for _, validType := range validTypes {
		if stakeholderType == validType {
			return true
		}
	}
	return false
}

func (s *Stakeholder) IsValidStatus(status StakeholderStatus) bool {
	validStatuses := []StakeholderStatus{
		StakeholderStatusActive,
		StakeholderStatusInactive,
		StakeholderStatusPending,
		StakeholderStatusBlocked,
	}
	for _, validStatus := range validStatuses {
		if status == validStatus {
			return true
		}
	}
	return false
}

func (s *Stakeholder) CanPerformAction(action string) bool {
	switch action {
	case "evaluate":
		return s.CanEvaluate && s.Status == StakeholderStatusActive
	case "review":
		return s.CanReview && s.Status == StakeholderStatusActive
	case "approve":
		return s.CanApprove && s.Status == StakeholderStatusActive
	default:
		return false
	}
}

func (s *Stakeholder) UpdateLastActive() {
	now := time.Now()
	s.LastActiveAt = &now
	s.UpdatedAt = now
}

func (s *Stakeholder) Activate() error {
	if s.Status == StakeholderStatusBlocked {
		return errors.New("cannot activate blocked stakeholder")
	}
	s.Status = StakeholderStatusActive
	s.UpdatedAt = time.Now()
	return nil
}

func (s *Stakeholder) Deactivate() {
	s.Status = StakeholderStatusInactive
	s.UpdatedAt = time.Now()
}

func (s *Stakeholder) Block(reason string) {
	s.Status = StakeholderStatusBlocked
	if reason != "" {
		s.Notes = reason
	}
	s.UpdatedAt = time.Now()
}

func (s *Stakeholder) HasHighAccessLevel() bool {
	return s.AccessLevel >= 4
}

func (s *Stakeholder) IsCoordinator() bool {
	return s.Role == StakeholderRoleCoordinator
}

func (s *Stakeholder) IsJuror() bool {
	return s.Role == StakeholderRoleJuror
}

func (s *Stakeholder) IsExternal() bool {
	return s.Type == StakeholderTypeExternal || s.Type == StakeholderTypeIndustry
}
