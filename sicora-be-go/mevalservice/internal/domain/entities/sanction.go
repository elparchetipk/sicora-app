package entities

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// SanctionType represents the types of sanctions according to SENA Agreement 009 of 2024
type SanctionType string

const (
	SanctionTypeVerbalWarning        SanctionType = "VERBAL_WARNING"
	SanctionTypeWrittenWarning       SanctionType = "WRITTEN_WARNING"
	SanctionTypeAcademicCommitment   SanctionType = "ACADEMIC_COMMITMENT"
	SanctionTypeImprovementPlan      SanctionType = "IMPROVEMENT_PLAN"
	SanctionTypeConditionalEnrollment SanctionType = "CONDITIONAL_ENROLLMENT"
	SanctionTypeTemporarySuspension  SanctionType = "TEMPORARY_SUSPENSION"
	SanctionTypeDefinitiveCancellation SanctionType = "DEFINITIVE_CANCELLATION"
)

// ComplianceStatus represents the compliance status of a sanction
type ComplianceStatus string

const (
	ComplianceStatusPending    ComplianceStatus = "PENDING"
	ComplianceStatusInProgress ComplianceStatus = "IN_PROGRESS"
	ComplianceStatusCompleted  ComplianceStatus = "COMPLETED"
	ComplianceStatusViolated   ComplianceStatus = "VIOLATED"
)

// AppealResult represents the result of an appeal
type AppealResult string

const (
	AppealResultConfirmed AppealResult = "CONFIRMED"
	AppealResultModified  AppealResult = "MODIFIED"
	AppealResultRevoked   AppealResult = "REVOKED"
)

// Sanction represents a sanction applied to a student
type Sanction struct {
	ID                 uuid.UUID        `json:"id" gorm:"type:uuid;primaryKey;default:gen_random_uuid()"`
	StudentID          uuid.UUID        `json:"student_id" gorm:"type:uuid;not null"`
	StudentCaseID      uuid.UUID        `json:"student_case_id" gorm:"type:uuid;not null"`
	SanctionType       SanctionType     `json:"sanction_type" gorm:"type:varchar(100);not null"`
	SeverityLevel      int              `json:"severity_level" gorm:"not null"`
	Description        string           `json:"description" gorm:"type:text;not null"`
	StartDate          time.Time        `json:"start_date" gorm:"not null"`
	EndDate            *time.Time       `json:"end_date,omitempty"`
	ComplianceRequired bool             `json:"compliance_required" gorm:"default:false"`
	ComplianceStatus   ComplianceStatus `json:"compliance_status" gorm:"type:varchar(50);default:'PENDING'"`
	AppealDeadline     *time.Time       `json:"appeal_deadline,omitempty"`
	Appealed           bool             `json:"appealed" gorm:"default:false"`
	AppealResult       *AppealResult    `json:"appeal_result,omitempty" gorm:"type:varchar(50)"`
	CreatedAt          time.Time        `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt          time.Time        `json:"updated_at" gorm:"autoUpdateTime"`

	// Relationships
	StudentCase StudentCase `json:"-" gorm:"foreignKey:StudentCaseID"`
	Appeals     []Appeal    `json:"appeals,omitempty" gorm:"foreignKey:SanctionID"`
}

// BeforeCreate sets the ID and appeal deadline before creating a new sanction
func (s *Sanction) BeforeCreate(tx *gorm.DB) error {
	if s.ID == uuid.Nil {
		s.ID = uuid.New()
	}
	
	// Set appeal deadline (5 business days after start date)
	if s.AppealDeadline == nil {
		deadline := s.StartDate.AddDate(0, 0, 7) // 7 days to account for weekends
		s.AppealDeadline = &deadline
	}
	
	return nil
}

// TableName specifies the table name for Sanction
func (Sanction) TableName() string {
	return "mevalservice_schema.sanctions"
}

// GetSeverityDescription returns a description based on severity level
func (s *Sanction) GetSeverityDescription() string {
	switch s.SeverityLevel {
	case 1:
		return "Leve"
	case 2, 3:
		return "Moderada"
	case 4, 5:
		return "Grave"
	case 6, 7:
		return "Muy Grave"
	default:
		return "No Clasificada"
	}
}

// IsAppealable checks if the sanction can be appealed
func (s *Sanction) IsAppealable() bool {
	if s.AppealDeadline == nil {
		return false
	}
	return time.Now().Before(*s.AppealDeadline) && !s.Appealed
}

// IsActive checks if the sanction is currently active
func (s *Sanction) IsActive() bool {
	now := time.Now()
	if s.EndDate != nil {
		return now.After(s.StartDate) && now.Before(*s.EndDate)
	}
	return now.After(s.StartDate)
}

// IsTemporary checks if the sanction has an end date
func (s *Sanction) IsTemporary() bool {
	return s.EndDate != nil
}

// IsPermanent checks if the sanction is permanent
func (s *Sanction) IsPermanent() bool {
	return s.SanctionType == SanctionTypeDefinitiveCancellation
}

// RequiresCompliance checks if the sanction requires active compliance
func (s *Sanction) RequiresCompliance() bool {
	return s.ComplianceRequired
}

// MarkAsAppealed marks the sanction as appealed
func (s *Sanction) MarkAsAppealed() {
	s.Appealed = true
}

// SetAppealResult sets the result of an appeal
func (s *Sanction) SetAppealResult(result AppealResult) {
	s.AppealResult = &result
}

// GetDurationDays returns the duration of the sanction in days
func (s *Sanction) GetDurationDays() int {
	if s.EndDate == nil {
		return -1 // Permanent
	}
	return int(s.EndDate.Sub(s.StartDate).Hours() / 24)
}
