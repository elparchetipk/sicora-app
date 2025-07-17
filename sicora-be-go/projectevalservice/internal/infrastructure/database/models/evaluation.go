package models

import (
	"time"

	"projectevalservice/internal/domain/entities"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Evaluation struct {
	ID           uuid.UUID `gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	SubmissionID uuid.UUID `gorm:"type:uuid;not null"`
	EvaluatorID  uuid.UUID `gorm:"type:uuid;not null"`

	FunctionalityScore float64 `gorm:"not null;default:0"`
	CodeQualityScore   float64 `gorm:"not null;default:0"`
	ArchitectureScore  float64 `gorm:"not null;default:0"`
	DocumentationScore float64 `gorm:"not null;default:0"`
	TestingScore       float64 `gorm:"not null;default:0"`
	DeploymentScore    float64 `gorm:"not null;default:0"`
	SecurityScore      float64 `gorm:"not null;default:0"`
	PerformanceScore   float64 `gorm:"not null;default:0"`

	TotalScore float64 `gorm:"not null;default:0"`
	Grade      string  `gorm:"type:varchar(10)"`

	GeneralComments       string `gorm:"type:text"`
	FunctionalityComments string `gorm:"type:text"`
	CodeQualityComments   string `gorm:"type:text"`
	ArchitectureComments  string `gorm:"type:text"`
	DocumentationComments string `gorm:"type:text"`
	TestingComments       string `gorm:"type:text"`
	DeploymentComments    string `gorm:"type:text"`
	SecurityComments      string `gorm:"type:text"`
	PerformanceComments   string `gorm:"type:text"`

	Recommendations string `gorm:"type:text"`

	Status      string     `gorm:"type:varchar(20);not null;default:'draft'"`
	EvaluatedAt *time.Time `gorm:"type:timestamp"`
	CreatedAt   time.Time  `gorm:"autoCreateTime"`
	UpdatedAt   time.Time  `gorm:"autoUpdateTime"`

	Submission Submission `gorm:"foreignKey:SubmissionID"`
}

func (e *Evaluation) ToEntity() *entities.Evaluation {
	return &entities.Evaluation{
		ID:                    e.ID,
		SubmissionID:          e.SubmissionID,
		EvaluatorID:           e.EvaluatorID,
		FunctionalityScore:    e.FunctionalityScore,
		CodeQualityScore:      e.CodeQualityScore,
		ArchitectureScore:     e.ArchitectureScore,
		DocumentationScore:    e.DocumentationScore,
		TestingScore:          e.TestingScore,
		DeploymentScore:       e.DeploymentScore,
		SecurityScore:         e.SecurityScore,
		PerformanceScore:      e.PerformanceScore,
		TotalScore:            e.TotalScore,
		Grade:                 e.Grade,
		GeneralComments:       e.GeneralComments,
		FunctionalityComments: e.FunctionalityComments,
		CodeQualityComments:   e.CodeQualityComments,
		ArchitectureComments:  e.ArchitectureComments,
		DocumentationComments: e.DocumentationComments,
		TestingComments:       e.TestingComments,
		DeploymentComments:    e.DeploymentComments,
		SecurityComments:      e.SecurityComments,
		PerformanceComments:   e.PerformanceComments,
		Recommendations:       e.Recommendations,
		Status:                entities.EvaluationStatus(e.Status),
		EvaluatedAt:           e.EvaluatedAt,
		CreatedAt:             e.CreatedAt,
		UpdatedAt:             e.UpdatedAt,
	}
}

func (e *Evaluation) FromEntity(entity *entities.Evaluation) {
	e.ID = entity.ID
	e.SubmissionID = entity.SubmissionID
	e.EvaluatorID = entity.EvaluatorID
	e.FunctionalityScore = entity.FunctionalityScore
	e.CodeQualityScore = entity.CodeQualityScore
	e.ArchitectureScore = entity.ArchitectureScore
	e.DocumentationScore = entity.DocumentationScore
	e.TestingScore = entity.TestingScore
	e.DeploymentScore = entity.DeploymentScore
	e.SecurityScore = entity.SecurityScore
	e.PerformanceScore = entity.PerformanceScore
	e.TotalScore = entity.TotalScore
	e.Grade = entity.Grade
	e.GeneralComments = entity.GeneralComments
	e.FunctionalityComments = entity.FunctionalityComments
	e.CodeQualityComments = entity.CodeQualityComments
	e.ArchitectureComments = entity.ArchitectureComments
	e.DocumentationComments = entity.DocumentationComments
	e.TestingComments = entity.TestingComments
	e.DeploymentComments = entity.DeploymentComments
	e.SecurityComments = entity.SecurityComments
	e.PerformanceComments = entity.PerformanceComments
	e.Recommendations = entity.Recommendations
	e.Status = string(entity.Status)
	e.EvaluatedAt = entity.EvaluatedAt
	e.CreatedAt = entity.CreatedAt
	e.UpdatedAt = entity.UpdatedAt
}

func (e *Evaluation) BeforeCreate(tx *gorm.DB) error {
	if e.ID == uuid.Nil {
		e.ID = uuid.New()
	}
	return nil
}
