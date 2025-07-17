package entities

import (
	"errors"
	"time"

	"github.com/google/uuid"
)

type DocumentType string

const (
	DocumentTypeRequirement   DocumentType = "requirement"
	DocumentTypeSpecification DocumentType = "specification"
	DocumentTypeDesign        DocumentType = "design"
	DocumentTypeTestPlan      DocumentType = "test_plan"
	DocumentTypeUserManual    DocumentType = "user_manual"
	DocumentTypeReport        DocumentType = "report"
	DocumentTypePresentation  DocumentType = "presentation"
	DocumentTypeOther         DocumentType = "other"
)

type DocumentStatus string

const (
	DocumentStatusDraft    DocumentStatus = "draft"
	DocumentStatusReview   DocumentStatus = "review"
	DocumentStatusApproved DocumentStatus = "approved"
	DocumentStatusRejected DocumentStatus = "rejected"
	DocumentStatusArchived DocumentStatus = "archived"
)

type DocumentVisibility string

const (
	DocumentVisibilityPublic     DocumentVisibility = "public"
	DocumentVisibilityPrivate    DocumentVisibility = "private"
	DocumentVisibilityRestricted DocumentVisibility = "restricted"
	DocumentVisibilityInternal   DocumentVisibility = "internal"
)

type ProjectDocument struct {
	ID             uuid.UUID          `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	ProjectID      uuid.UUID          `json:"project_id" gorm:"type:uuid;not null;index"`
	UploadedByID   uuid.UUID          `json:"uploaded_by_id" gorm:"type:uuid;not null"`
	Title          string             `json:"title" gorm:"not null" validate:"required,min=3,max=200"`
	Description    string             `json:"description" gorm:"type:text"`
	Type           DocumentType       `json:"type" gorm:"type:varchar(50);not null"`
	Status         DocumentStatus     `json:"status" gorm:"type:varchar(50);not null;default:'draft'"`
	Visibility     DocumentVisibility `json:"visibility" gorm:"type:varchar(50);not null;default:'private'"`
	FileName       string             `json:"file_name" gorm:"not null"`
	FilePath       string             `json:"file_path" gorm:"not null"`
	FileSize       int64              `json:"file_size" gorm:"not null"`
	MimeType       string             `json:"mime_type" gorm:"type:varchar(255)"`
	Version        string             `json:"version" gorm:"type:varchar(50);default:'1.0'"`
	Tags           []string           `json:"tags" gorm:"type:text[]"`
	IsRequired     bool               `json:"is_required" gorm:"default:false"`
	IsTemplate     bool               `json:"is_template" gorm:"default:false"`
	DownloadCount  int                `json:"download_count" gorm:"default:0"`
	LastAccessedAt *time.Time         `json:"last_accessed_at"`
	ReviewedByID   *uuid.UUID         `json:"reviewed_by_id" gorm:"type:uuid"`
	ReviewedAt     *time.Time         `json:"reviewed_at"`
	ReviewComments string             `json:"review_comments" gorm:"type:text"`
	ApprovedByID   *uuid.UUID         `json:"approved_by_id" gorm:"type:uuid"`
	ApprovedAt     *time.Time         `json:"approved_at"`
	CreatedAt      time.Time          `json:"created_at" gorm:"default:CURRENT_TIMESTAMP"`
	UpdatedAt      time.Time          `json:"updated_at" gorm:"default:CURRENT_TIMESTAMP"`

	// Relations
	Project    *Project     `json:"project,omitempty" gorm:"foreignKey:ProjectID"`
	UploadedBy *Stakeholder `json:"uploaded_by,omitempty" gorm:"foreignKey:UploadedByID"`
	ReviewedBy *Stakeholder `json:"reviewed_by,omitempty" gorm:"foreignKey:ReviewedByID"`
	ApprovedBy *Stakeholder `json:"approved_by,omitempty" gorm:"foreignKey:ApprovedByID"`
}

func NewProjectDocument(projectID, uploadedByID uuid.UUID, title, fileName, filePath string, fileSize int64, docType DocumentType) *ProjectDocument {
	return &ProjectDocument{
		ID:           uuid.New(),
		ProjectID:    projectID,
		UploadedByID: uploadedByID,
		Title:        title,
		Type:         docType,
		Status:       DocumentStatusDraft,
		Visibility:   DocumentVisibilityPrivate,
		FileName:     fileName,
		FilePath:     filePath,
		FileSize:     fileSize,
		Version:      "1.0",
		CreatedAt:    time.Now(),
		UpdatedAt:    time.Now(),
	}
}

func (pd *ProjectDocument) IsValid() error {
	if pd.ProjectID == uuid.Nil {
		return errors.New("project ID is required")
	}
	if pd.UploadedByID == uuid.Nil {
		return errors.New("uploaded by ID is required")
	}
	if pd.Title == "" || len(pd.Title) < 3 || len(pd.Title) > 200 {
		return errors.New("title must be between 3 and 200 characters")
	}
	if pd.FileName == "" {
		return errors.New("file name is required")
	}
	if pd.FilePath == "" {
		return errors.New("file path is required")
	}
	if pd.FileSize <= 0 {
		return errors.New("file size must be greater than 0")
	}
	if !pd.IsValidType(pd.Type) {
		return errors.New("invalid document type")
	}
	if !pd.IsValidStatus(pd.Status) {
		return errors.New("invalid document status")
	}
	if !pd.IsValidVisibility(pd.Visibility) {
		return errors.New("invalid document visibility")
	}
	return nil
}

func (pd *ProjectDocument) IsValidType(docType DocumentType) bool {
	validTypes := []DocumentType{
		DocumentTypeRequirement,
		DocumentTypeSpecification,
		DocumentTypeDesign,
		DocumentTypeTestPlan,
		DocumentTypeUserManual,
		DocumentTypeReport,
		DocumentTypePresentation,
		DocumentTypeOther,
	}
	for _, validType := range validTypes {
		if docType == validType {
			return true
		}
	}
	return false
}

func (pd *ProjectDocument) IsValidStatus(status DocumentStatus) bool {
	validStatuses := []DocumentStatus{
		DocumentStatusDraft,
		DocumentStatusReview,
		DocumentStatusApproved,
		DocumentStatusRejected,
		DocumentStatusArchived,
	}
	for _, validStatus := range validStatuses {
		if status == validStatus {
			return true
		}
	}
	return false
}

func (pd *ProjectDocument) IsValidVisibility(visibility DocumentVisibility) bool {
	validVisibilities := []DocumentVisibility{
		DocumentVisibilityPublic,
		DocumentVisibilityPrivate,
		DocumentVisibilityRestricted,
		DocumentVisibilityInternal,
	}
	for _, validVisibility := range validVisibilities {
		if visibility == validVisibility {
			return true
		}
	}
	return false
}

func (pd *ProjectDocument) CanBeAccessedBy(userID uuid.UUID, userRole string) bool {
	// Uploader always has access
	if pd.UploadedByID == userID {
		return true
	}

	switch pd.Visibility {
	case DocumentVisibilityPublic:
		return true
	case DocumentVisibilityPrivate:
		return pd.UploadedByID == userID
	case DocumentVisibilityRestricted:
		// Only coordinators and managers can access
		return userRole == "coordinator" || userRole == "manager"
	case DocumentVisibilityInternal:
		// All project stakeholders can access
		return true
	default:
		return false
	}
}

func (pd *ProjectDocument) SubmitForReview() error {
	if pd.Status != DocumentStatusDraft {
		return errors.New("only draft documents can be submitted for review")
	}
	pd.Status = DocumentStatusReview
	pd.UpdatedAt = time.Now()
	return nil
}

func (pd *ProjectDocument) Review(reviewerID uuid.UUID, comments string) error {
	if pd.Status != DocumentStatusReview {
		return errors.New("document is not in review status")
	}
	pd.ReviewedByID = &reviewerID
	now := time.Now()
	pd.ReviewedAt = &now
	pd.ReviewComments = comments
	pd.UpdatedAt = now
	return nil
}

func (pd *ProjectDocument) Approve(approverID uuid.UUID) error {
	if pd.Status != DocumentStatusReview {
		return errors.New("document must be reviewed before approval")
	}
	pd.Status = DocumentStatusApproved
	pd.ApprovedByID = &approverID
	now := time.Now()
	pd.ApprovedAt = &now
	pd.UpdatedAt = now
	return nil
}

func (pd *ProjectDocument) Reject(reviewerID uuid.UUID, reason string) error {
	if pd.Status != DocumentStatusReview {
		return errors.New("document is not in review status")
	}
	pd.Status = DocumentStatusRejected
	pd.ReviewedByID = &reviewerID
	now := time.Now()
	pd.ReviewedAt = &now
	pd.ReviewComments = reason
	pd.UpdatedAt = now
	return nil
}

func (pd *ProjectDocument) Archive() {
	pd.Status = DocumentStatusArchived
	pd.UpdatedAt = time.Now()
}

func (pd *ProjectDocument) IncrementDownloadCount() {
	pd.DownloadCount++
	now := time.Now()
	pd.LastAccessedAt = &now
	pd.UpdatedAt = now
}

func (pd *ProjectDocument) UpdateVersion(newVersion string) {
	pd.Version = newVersion
	pd.UpdatedAt = time.Now()
}

func (pd *ProjectDocument) IsApproved() bool {
	return pd.Status == DocumentStatusApproved
}

func (pd *ProjectDocument) IsDraft() bool {
	return pd.Status == DocumentStatusDraft
}

func (pd *ProjectDocument) IsInReview() bool {
	return pd.Status == DocumentStatusReview
}

func (pd *ProjectDocument) IsRejected() bool {
	return pd.Status == DocumentStatusRejected
}

func (pd *ProjectDocument) AddTag(tag string) {
	if tag == "" {
		return
	}

	// Check if tag already exists
	for _, existingTag := range pd.Tags {
		if existingTag == tag {
			return
		}
	}

	pd.Tags = append(pd.Tags, tag)
	pd.UpdatedAt = time.Now()
}

func (pd *ProjectDocument) RemoveTag(tag string) {
	for i, existingTag := range pd.Tags {
		if existingTag == tag {
			pd.Tags = append(pd.Tags[:i], pd.Tags[i+1:]...)
			pd.UpdatedAt = time.Now()
			return
		}
	}
}

func (pd *ProjectDocument) HasTag(tag string) bool {
	for _, existingTag := range pd.Tags {
		if existingTag == tag {
			return true
		}
	}
	return false
}
