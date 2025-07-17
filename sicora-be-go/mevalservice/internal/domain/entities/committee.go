package entities

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// CommitteeType represents the type of committee according to SENA Agreement 009 of 2024
type CommitteeType string

const (
	CommitteeTypeMonthly       CommitteeType = "MONTHLY"
	CommitteeTypeExtraordinary CommitteeType = "EXTRAORDINARY"
	CommitteeTypeAppeals       CommitteeType = "APPEALS"
	CommitteeTypeSpecial       CommitteeType = "SPECIAL"
)

// CommitteeStatus represents the current status of a committee session
type CommitteeStatus string

const (
	CommitteeStatusScheduled CommitteeStatus = "SCHEDULED"
	CommitteeStatusInSession CommitteeStatus = "IN_SESSION"
	CommitteeStatusCompleted CommitteeStatus = "COMPLETED"
	CommitteeStatusCancelled CommitteeStatus = "CANCELLED"
	CommitteeStatusPostponed CommitteeStatus = "POSTPONED"
)

// Committee represents a committee session for academic/disciplinary evaluation
type Committee struct {
	ID               uuid.UUID       `json:"id" gorm:"type:uuid;primaryKey;default:gen_random_uuid()"`
	CommitteeDate    time.Time       `json:"committee_date" gorm:"not null"`
	CommitteeType    CommitteeType   `json:"committee_type" gorm:"type:varchar(50);not null"`
	Status           CommitteeStatus `json:"status" gorm:"type:varchar(50);not null;default:'SCHEDULED'"`
	ProgramID        *uuid.UUID      `json:"program_id,omitempty" gorm:"type:uuid"`
	AcademicPeriod   string          `json:"academic_period" gorm:"type:varchar(20)"`
	AgendaGenerated  bool            `json:"agenda_generated" gorm:"default:false"`
	QuorumAchieved   bool            `json:"quorum_achieved" gorm:"default:false"`
	SessionMinutes   *string         `json:"session_minutes,omitempty" gorm:"type:text"`
	CreatedAt        time.Time       `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt        time.Time       `json:"updated_at" gorm:"autoUpdateTime"`

	// Relationships
	Members   []CommitteeMember `json:"members,omitempty" gorm:"foreignKey:CommitteeID"`
	Cases     []StudentCase     `json:"cases,omitempty" gorm:"foreignKey:CommitteeID"`
	Decisions []CommitteeDecision `json:"decisions,omitempty" gorm:"foreignKey:CommitteeID"`
}

// BeforeCreate sets the ID before creating a new committee
func (c *Committee) BeforeCreate(tx *gorm.DB) error {
	if c.ID == uuid.Nil {
		c.ID = uuid.New()
	}
	return nil
}

// TableName specifies the table name for Committee
func (Committee) TableName() string {
	return "mevalservice_schema.committees"
}

// IsMonthlyCommittee checks if this is a monthly committee
func (c *Committee) IsMonthlyCommittee() bool {
	return c.CommitteeType == CommitteeTypeMonthly
}

// CanStartSession validates if the committee can start a session
func (c *Committee) CanStartSession() bool {
	return c.Status == CommitteeStatusScheduled && c.QuorumAchieved
}

// IsCompleted checks if the committee session is completed
func (c *Committee) IsCompleted() bool {
	return c.Status == CommitteeStatusCompleted
}

// GetFormattedDate returns the committee date in a human-readable format
func (c *Committee) GetFormattedDate() string {
	return c.CommitteeDate.Format("2006-01-02 15:04")
}
