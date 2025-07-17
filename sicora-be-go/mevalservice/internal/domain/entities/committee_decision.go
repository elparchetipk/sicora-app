package entities

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// DecisionType represents the type of committee decision
type DecisionType string

const (
	DecisionTypeRecognition  DecisionType = "RECOGNITION"
	DecisionTypeSanction     DecisionType = "SANCTION"
	DecisionTypePlanRenewal  DecisionType = "PLAN_RENEWAL"
	DecisionTypeAppealResult DecisionType = "APPEAL_RESULT"
)

// CommitteeDecision represents a decision made by a committee
type CommitteeDecision struct {
	ID                  uuid.UUID    `json:"id" gorm:"type:uuid;primaryKey;default:gen_random_uuid()"`
	CommitteeID         uuid.UUID    `json:"committee_id" gorm:"type:uuid;not null"`
	StudentCaseID       uuid.UUID    `json:"student_case_id" gorm:"type:uuid;not null"`
	DecisionType        DecisionType `json:"decision_type" gorm:"type:varchar(50);not null"`
	DecisionDescription string       `json:"decision_description" gorm:"type:text;not null"`
	VotesFor            int          `json:"votes_for" gorm:"default:0"`
	VotesAgainst        int          `json:"votes_against" gorm:"default:0"`
	VotesAbstain        int          `json:"votes_abstain" gorm:"default:0"`
	Unanimous           bool         `json:"unanimous" gorm:"default:false"`
	DecisionRationale   *string      `json:"decision_rationale,omitempty" gorm:"type:text"`
	CreatedAt           time.Time    `json:"created_at" gorm:"autoCreateTime"`

	// Relationships
	Committee   Committee   `json:"-" gorm:"foreignKey:CommitteeID"`
	StudentCase StudentCase `json:"-" gorm:"foreignKey:StudentCaseID"`
}

// BeforeCreate sets the ID before creating a new committee decision
func (cd *CommitteeDecision) BeforeCreate(tx *gorm.DB) error {
	if cd.ID == uuid.Nil {
		cd.ID = uuid.New()
	}
	return nil
}

// TableName specifies the table name for CommitteeDecision
func (CommitteeDecision) TableName() string {
	return "mevalservice_schema.committee_decisions"
}

// GetTotalVotes returns the total number of votes cast
func (cd *CommitteeDecision) GetTotalVotes() int {
	return cd.VotesFor + cd.VotesAgainst + cd.VotesAbstain
}

// IsApproved checks if the decision was approved
func (cd *CommitteeDecision) IsApproved() bool {
	return cd.VotesFor > cd.VotesAgainst
}

// IsUnanimous checks if the decision was unanimous
func (cd *CommitteeDecision) IsUnanimous() bool {
	return cd.Unanimous || (cd.VotesAgainst == 0 && cd.VotesAbstain == 0)
}

// GetApprovalPercentage returns the percentage of approval votes
func (cd *CommitteeDecision) GetApprovalPercentage() float64 {
	total := cd.GetTotalVotes()
	if total == 0 {
		return 0.0
	}
	return float64(cd.VotesFor) / float64(total) * 100
}
