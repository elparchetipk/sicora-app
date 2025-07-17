package models

import (
	"time"

	"projectevalservice/internal/domain/entities"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Submission struct {
	ID                     uuid.UUID `gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	ProjectID              uuid.UUID `gorm:"type:uuid;not null"`
	StudentID              uuid.UUID `gorm:"type:uuid;not null"`
	RepositoryURL          string    `gorm:"not null;size:500"`
	DeploymentURL          string    `gorm:"size:500"`
	Description            string    `gorm:"type:text"`
	TechnicalDocumentation string    `gorm:"type:text"`
	Status                 string    `gorm:"type:varchar(20);not null;default:'submitted'"`
	SubmittedAt            time.Time `gorm:"autoCreateTime"`
	UpdatedAt              time.Time `gorm:"autoUpdateTime"`

	Project     Project      `gorm:"foreignKey:ProjectID"`
	Evaluations []Evaluation `gorm:"foreignKey:SubmissionID;constraint:OnDelete:CASCADE"`
}

func (s *Submission) ToEntity() *entities.Submission {
	return &entities.Submission{
		ID:                     s.ID,
		ProjectID:              s.ProjectID,
		StudentID:              s.StudentID,
		RepositoryURL:          s.RepositoryURL,
		DeploymentURL:          s.DeploymentURL,
		Description:            s.Description,
		TechnicalDocumentation: s.TechnicalDocumentation,
		Status:                 entities.SubmissionStatus(s.Status),
		SubmittedAt:            s.SubmittedAt,
		UpdatedAt:              s.UpdatedAt,
	}
}

func (s *Submission) FromEntity(entity *entities.Submission) {
	s.ID = entity.ID
	s.ProjectID = entity.ProjectID
	s.StudentID = entity.StudentID
	s.RepositoryURL = entity.RepositoryURL
	s.DeploymentURL = entity.DeploymentURL
	s.Description = entity.Description
	s.TechnicalDocumentation = entity.TechnicalDocumentation
	s.Status = string(entity.Status)
	s.SubmittedAt = entity.SubmittedAt
	s.UpdatedAt = entity.UpdatedAt
}

func (s *Submission) BeforeCreate(tx *gorm.DB) error {
	if s.ID == uuid.Nil {
		s.ID = uuid.New()
	}
	return nil
}
