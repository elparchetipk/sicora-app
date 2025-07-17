package models

import (
	"time"

	"projectevalservice/internal/domain/entities"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Project struct {
	ID              uuid.UUID `gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	Name            string    `gorm:"not null;size:200"`
	Description     string    `gorm:"type:text"`
	TechnologyStack string    `gorm:"not null;size:100"`
	Requirements    string    `gorm:"type:text"`
	DeliveryDate    time.Time `gorm:"not null"`
	MaxScore        float64   `gorm:"not null;default:100"`
	Status          string    `gorm:"type:varchar(20);not null;default:'active'"`
	InstructorID    uuid.UUID `gorm:"type:uuid;not null"`
	CreatedAt       time.Time `gorm:"autoCreateTime"`
	UpdatedAt       time.Time `gorm:"autoUpdateTime"`

	// Submissions      []Submission `gorm:"foreignKey:ProjectID;constraint:OnDelete:CASCADE"`
}

func (p *Project) ToEntity() *entities.Project {
	return &entities.Project{
		ID:              p.ID,
		Name:            p.Name,
		Description:     p.Description,
		TechnologyStack: p.TechnologyStack,
		Requirements:    p.Requirements,
		DeliveryDate:    p.DeliveryDate,
		MaxScore:        p.MaxScore,
		Status:          entities.ProjectStatus(p.Status),
		InstructorID:    p.InstructorID,
		CreatedAt:       p.CreatedAt,
		UpdatedAt:       p.UpdatedAt,
	}
}

func (p *Project) FromEntity(entity *entities.Project) {
	p.ID = entity.ID
	p.Name = entity.Name
	p.Description = entity.Description
	p.TechnologyStack = entity.TechnologyStack
	p.Requirements = entity.Requirements
	p.DeliveryDate = entity.DeliveryDate
	p.MaxScore = entity.MaxScore
	p.Status = string(entity.Status)
	p.InstructorID = entity.InstructorID
	p.CreatedAt = entity.CreatedAt
	p.UpdatedAt = entity.UpdatedAt
}

func (p *Project) BeforeCreate(tx *gorm.DB) error {
	if p.ID == uuid.Nil {
		p.ID = uuid.New()
	}
	return nil
}
