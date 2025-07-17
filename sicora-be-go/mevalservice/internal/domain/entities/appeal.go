package entities

import (
	"encoding/json"
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// AdmissibilityStatus represents the admissibility status of an appeal
type AdmissibilityStatus string

const (
	AdmissibilityStatusPending  AdmissibilityStatus = "PENDING"
	AdmissibilityStatusAdmitted AdmissibilityStatus = "ADMITTED"
	AdmissibilityStatusRejected AdmissibilityStatus = "REJECTED"
)

// FinalDecision represents the final decision on an appeal
type FinalDecision string

const (
	FinalDecisionConfirmed FinalDecision = "CONFIRMED"
	FinalDecisionModified  FinalDecision = "MODIFIED"
	FinalDecisionRevoked   FinalDecision = "REVOKED"
)

// SupportingDocument represents a supporting document for an appeal
type SupportingDocument struct {
	URL         string    `json:"url"`
	Type        string    `json:"type"`
	Description string    `json:"description"`
	UploadedAt  time.Time `json:"uploaded_at"`
}

// Appeal represents an appeal process for a sanction
type Appeal struct {
	ID                         uuid.UUID             `json:"id" gorm:"type:uuid;primaryKey;default:gen_random_uuid()"`
	SanctionID                 uuid.UUID             `json:"sanction_id" gorm:"type:uuid;not null"`
	StudentID                  uuid.UUID             `json:"student_id" gorm:"type:uuid;not null"`
	SubmissionDate             time.Time             `json:"submission_date" gorm:"not null"`
	DeadlineDate               time.Time             `json:"deadline_date" gorm:"not null"`
	AppealGrounds              string                `json:"appeal_grounds" gorm:"type:text;not null"`
	SupportingDocuments        []SupportingDocument  `json:"supporting_documents" gorm:"type:jsonb"`
	AdmissibilityStatus        AdmissibilityStatus   `json:"admissibility_status" gorm:"type:varchar(50);default:'PENDING'"`
	AdmissibilityRationale     *string               `json:"admissibility_rationale,omitempty" gorm:"type:text"`
	SecondInstanceCommitteeID  *uuid.UUID            `json:"second_instance_committee_id,omitempty" gorm:"type:uuid"`
	FinalDecision              *FinalDecision        `json:"final_decision,omitempty" gorm:"type:varchar(50)"`
	FinalRationale             *string               `json:"final_rationale,omitempty" gorm:"type:text"`
	CreatedAt                  time.Time             `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt                  time.Time             `json:"updated_at" gorm:"autoUpdateTime"`

	// Relationships
	Sanction                   Sanction              `json:"-" gorm:"foreignKey:SanctionID"`
	SecondInstanceCommittee    *Committee            `json:"second_instance_committee,omitempty" gorm:"foreignKey:SecondInstanceCommitteeID"`
}

// BeforeCreate sets the ID before creating a new appeal
func (a *Appeal) BeforeCreate(tx *gorm.DB) error {
	if a.ID == uuid.Nil {
		a.ID = uuid.New()
	}
	return nil
}

// TableName specifies the table name for Appeal
func (Appeal) TableName() string {
	return "mevalservice_schema.appeals"
}

// IsWithinDeadline checks if the appeal was submitted within the legal deadline
func (a *Appeal) IsWithinDeadline() bool {
	return a.SubmissionDate.Before(a.DeadlineDate) || a.SubmissionDate.Equal(a.DeadlineDate)
}

// IsAdmitted checks if the appeal has been admitted
func (a *Appeal) IsAdmitted() bool {
	return a.AdmissibilityStatus == AdmissibilityStatusAdmitted
}

// IsRejected checks if the appeal has been rejected
func (a *Appeal) IsRejected() bool {
	return a.AdmissibilityStatus == AdmissibilityStatusRejected
}

// IsPending checks if the appeal is still pending review
func (a *Appeal) IsPending() bool {
	return a.AdmissibilityStatus == AdmissibilityStatusPending
}

// HasFinalDecision checks if a final decision has been made
func (a *Appeal) HasFinalDecision() bool {
	return a.FinalDecision != nil
}

// IsSuccessful checks if the appeal was successful (modified or revoked)
func (a *Appeal) IsSuccessful() bool {
	return a.FinalDecision != nil && 
		(*a.FinalDecision == FinalDecisionModified || *a.FinalDecision == FinalDecisionRevoked)
}

// Admit admits the appeal for review
func (a *Appeal) Admit(rationale string) {
	a.AdmissibilityStatus = AdmissibilityStatusAdmitted
	a.AdmissibilityRationale = &rationale
}

// Reject rejects the appeal
func (a *Appeal) Reject(rationale string) {
	a.AdmissibilityStatus = AdmissibilityStatusRejected
	a.AdmissibilityRationale = &rationale
}

// SetFinalDecision sets the final decision of the appeal
func (a *Appeal) SetFinalDecision(decision FinalDecision, rationale string) {
	a.FinalDecision = &decision
	a.FinalRationale = &rationale
}

// AddSupportingDocument adds a supporting document to the appeal
func (a *Appeal) AddSupportingDocument(doc SupportingDocument) {
	if a.SupportingDocuments == nil {
		a.SupportingDocuments = make([]SupportingDocument, 0)
	}
	doc.UploadedAt = time.Now()
	a.SupportingDocuments = append(a.SupportingDocuments, doc)
}

// GetSupportingDocumentsJSON returns supporting documents as JSON string
func (a *Appeal) GetSupportingDocumentsJSON() (string, error) {
	bytes, err := json.Marshal(a.SupportingDocuments)
	return string(bytes), err
}

// SetSupportingDocumentsFromJSON sets supporting documents from JSON string
func (a *Appeal) SetSupportingDocumentsFromJSON(jsonStr string) error {
	return json.Unmarshal([]byte(jsonStr), &a.SupportingDocuments)
}
