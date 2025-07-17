package models

import (
	"time"

	"projectevalservice/internal/domain/entities"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type ProjectDocument struct {
	ID             uuid.UUID                   `gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	ProjectID      uuid.UUID                   `gorm:"type:uuid;not null;index"`
	UploadedByID   uuid.UUID                   `gorm:"type:uuid;not null"`
	Title          string                      `gorm:"not null"`
	Description    string                      `gorm:"type:text"`
	Type           entities.DocumentType       `gorm:"type:varchar(50);not null"`
	Status         entities.DocumentStatus     `gorm:"type:varchar(50);not null;default:'draft'"`
	Visibility     entities.DocumentVisibility `gorm:"type:varchar(50);not null;default:'private'"`
	FileName       string                      `gorm:"not null"`
	FilePath       string                      `gorm:"not null"`
	FileSize       int64                       `gorm:"not null"`
	MimeType       string                      `gorm:"type:varchar(255)"`
	Version        string                      `gorm:"type:varchar(50);default:'1.0'"`
	Tags           StringArray                 `gorm:"type:text[]"`
	IsRequired     bool                        `gorm:"default:false"`
	IsTemplate     bool                        `gorm:"default:false"`
	DownloadCount  int                         `gorm:"default:0"`
	LastAccessedAt *time.Time
	ReviewedByID   *uuid.UUID `gorm:"type:uuid"`
	ReviewedAt     *time.Time
	ReviewComments string     `gorm:"type:text"`
	ApprovedByID   *uuid.UUID `gorm:"type:uuid"`
	ApprovedAt     *time.Time
	CreatedAt      time.Time `gorm:"default:CURRENT_TIMESTAMP"`
	UpdatedAt      time.Time `gorm:"default:CURRENT_TIMESTAMP"`

	// Relations
	Project    *Project     `gorm:"foreignKey:ProjectID"`
	UploadedBy *Stakeholder `gorm:"foreignKey:UploadedByID"`
	ReviewedBy *Stakeholder `gorm:"foreignKey:ReviewedByID"`
	ApprovedBy *Stakeholder `gorm:"foreignKey:ApprovedByID"`
}

func (pd *ProjectDocument) TableName() string {
	return "project_documents"
}

func (pd *ProjectDocument) BeforeCreate(tx *gorm.DB) error {
	if pd.ID == uuid.Nil {
		pd.ID = uuid.New()
	}
	pd.CreatedAt = time.Now()
	pd.UpdatedAt = time.Now()
	return nil
}

func (pd *ProjectDocument) BeforeUpdate(tx *gorm.DB) error {
	pd.UpdatedAt = time.Now()
	return nil
}

// Convert from domain entity to GORM model
func ProjectDocumentFromEntity(entity *entities.ProjectDocument) *ProjectDocument {
	model := &ProjectDocument{
		ID:             entity.ID,
		ProjectID:      entity.ProjectID,
		UploadedByID:   entity.UploadedByID,
		Title:          entity.Title,
		Description:    entity.Description,
		Type:           entity.Type,
		Status:         entity.Status,
		Visibility:     entity.Visibility,
		FileName:       entity.FileName,
		FilePath:       entity.FilePath,
		FileSize:       entity.FileSize,
		MimeType:       entity.MimeType,
		Version:        entity.Version,
		Tags:           StringArray(entity.Tags),
		IsRequired:     entity.IsRequired,
		IsTemplate:     entity.IsTemplate,
		DownloadCount:  entity.DownloadCount,
		LastAccessedAt: entity.LastAccessedAt,
		ReviewedByID:   entity.ReviewedByID,
		ReviewedAt:     entity.ReviewedAt,
		ReviewComments: entity.ReviewComments,
		ApprovedByID:   entity.ApprovedByID,
		ApprovedAt:     entity.ApprovedAt,
		CreatedAt:      entity.CreatedAt,
		UpdatedAt:      entity.UpdatedAt,
	}
	return model
}

// Convert from GORM model to domain entity
func (pd *ProjectDocument) ToEntity() *entities.ProjectDocument {
	entity := &entities.ProjectDocument{
		ID:             pd.ID,
		ProjectID:      pd.ProjectID,
		UploadedByID:   pd.UploadedByID,
		Title:          pd.Title,
		Description:    pd.Description,
		Type:           pd.Type,
		Status:         pd.Status,
		Visibility:     pd.Visibility,
		FileName:       pd.FileName,
		FilePath:       pd.FilePath,
		FileSize:       pd.FileSize,
		MimeType:       pd.MimeType,
		Version:        pd.Version,
		Tags:           []string(pd.Tags),
		IsRequired:     pd.IsRequired,
		IsTemplate:     pd.IsTemplate,
		DownloadCount:  pd.DownloadCount,
		LastAccessedAt: pd.LastAccessedAt,
		ReviewedByID:   pd.ReviewedByID,
		ReviewedAt:     pd.ReviewedAt,
		ReviewComments: pd.ReviewComments,
		ApprovedByID:   pd.ApprovedByID,
		ApprovedAt:     pd.ApprovedAt,
		CreatedAt:      pd.CreatedAt,
		UpdatedAt:      pd.UpdatedAt,
	}
	return entity
}
