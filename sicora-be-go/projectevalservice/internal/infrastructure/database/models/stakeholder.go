package models

import (
	"time"

	"projectevalservice/internal/domain/entities"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Stakeholder struct {
	ID           uuid.UUID                  `gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	ProjectID    uuid.UUID                  `gorm:"type:uuid;not null;index"`
	UserID       uuid.UUID                  `gorm:"type:uuid;not null;index"`
	Role         entities.StakeholderRole   `gorm:"type:varchar(50);not null"`
	Type         entities.StakeholderType   `gorm:"type:varchar(50);not null"`
	Status       entities.StakeholderStatus `gorm:"type:varchar(50);not null;default:'active'"`
	Organization string                     `gorm:"type:varchar(255)"`
	Department   string                     `gorm:"type:varchar(255)"`
	Position     string                     `gorm:"type:varchar(255)"`
	Expertise    StringArray                `gorm:"type:text[]"`
	ContactEmail string                     `gorm:"type:varchar(255)"`
	ContactPhone string                     `gorm:"type:varchar(50)"`
	AccessLevel  int                        `gorm:"default:1"`
	CanEvaluate  bool                       `gorm:"default:false"`
	CanReview    bool                       `gorm:"default:false"`
	CanApprove   bool                       `gorm:"default:false"`
	Notes        string                     `gorm:"type:text"`
	AssignedAt   time.Time                  `gorm:"default:CURRENT_TIMESTAMP"`
	LastActiveAt *time.Time
	CreatedAt    time.Time `gorm:"default:CURRENT_TIMESTAMP"`
	UpdatedAt    time.Time `gorm:"default:CURRENT_TIMESTAMP"`

	// Relations
	Project *Project `gorm:"foreignKey:ProjectID"`
}

func (s *Stakeholder) TableName() string {
	return "stakeholders"
}

func (s *Stakeholder) BeforeCreate(tx *gorm.DB) error {
	if s.ID == uuid.Nil {
		s.ID = uuid.New()
	}
	s.CreatedAt = time.Now()
	s.UpdatedAt = time.Now()
	s.AssignedAt = time.Now()
	return nil
}

func (s *Stakeholder) BeforeUpdate(tx *gorm.DB) error {
	s.UpdatedAt = time.Now()
	return nil
}

// Convert from domain entity to GORM model
func StakeholderFromEntity(entity *entities.Stakeholder) *Stakeholder {
	model := &Stakeholder{
		ID:           entity.ID,
		ProjectID:    entity.ProjectID,
		UserID:       entity.UserID,
		Role:         entity.Role,
		Type:         entity.Type,
		Status:       entity.Status,
		Organization: entity.Organization,
		Department:   entity.Department,
		Position:     entity.Position,
		Expertise:    StringArray(entity.Expertise),
		ContactEmail: entity.ContactEmail,
		ContactPhone: entity.ContactPhone,
		AccessLevel:  entity.AccessLevel,
		CanEvaluate:  entity.CanEvaluate,
		CanReview:    entity.CanReview,
		CanApprove:   entity.CanApprove,
		Notes:        entity.Notes,
		AssignedAt:   entity.AssignedAt,
		LastActiveAt: entity.LastActiveAt,
		CreatedAt:    entity.CreatedAt,
		UpdatedAt:    entity.UpdatedAt,
	}
	return model
}

// Convert from GORM model to domain entity
func (s *Stakeholder) ToEntity() *entities.Stakeholder {
	entity := &entities.Stakeholder{
		ID:           s.ID,
		ProjectID:    s.ProjectID,
		UserID:       s.UserID,
		Role:         s.Role,
		Type:         s.Type,
		Status:       s.Status,
		Organization: s.Organization,
		Department:   s.Department,
		Position:     s.Position,
		Expertise:    []string(s.Expertise),
		ContactEmail: s.ContactEmail,
		ContactPhone: s.ContactPhone,
		AccessLevel:  s.AccessLevel,
		CanEvaluate:  s.CanEvaluate,
		CanReview:    s.CanReview,
		CanApprove:   s.CanApprove,
		Notes:        s.Notes,
		AssignedAt:   s.AssignedAt,
		LastActiveAt: s.LastActiveAt,
		CreatedAt:    s.CreatedAt,
		UpdatedAt:    s.UpdatedAt,
	}
	return entity
}
