package entities

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// MemberRole represents the role of a committee member
type MemberRole string

const (
	MemberRoleCoordinator    MemberRole = "COORDINATOR"
	MemberRoleInstructor     MemberRole = "INSTRUCTOR"
	MemberRoleRepresentative MemberRole = "REPRESENTATIVE"
	MemberRoleSecretary      MemberRole = "SECRETARY"
	MemberRolePresident      MemberRole = "PRESIDENT"
)

// CommitteeMember represents a member of a committee
type CommitteeMember struct {
	ID          uuid.UUID  `json:"id" gorm:"type:uuid;primaryKey;default:gen_random_uuid()"`
	CommitteeID uuid.UUID  `json:"committee_id" gorm:"type:uuid;not null"`
	UserID      uuid.UUID  `json:"user_id" gorm:"type:uuid;not null"`
	MemberRole  MemberRole `json:"member_role" gorm:"type:varchar(50);not null"`
	IsPresent   bool       `json:"is_present" gorm:"default:false"`
	VotePower   int        `json:"vote_power" gorm:"default:1"`
	CreatedAt   time.Time  `json:"created_at" gorm:"autoCreateTime"`

	// Relationships
	Committee Committee `json:"-" gorm:"foreignKey:CommitteeID"`
}

// BeforeCreate sets the ID before creating a new committee member
func (cm *CommitteeMember) BeforeCreate(tx *gorm.DB) error {
	if cm.ID == uuid.Nil {
		cm.ID = uuid.New()
	}
	return nil
}

// TableName specifies the table name for CommitteeMember
func (CommitteeMember) TableName() string {
	return "mevalservice_schema.committee_members"
}

// IsDecisionMaker checks if this member can make decisions
func (cm *CommitteeMember) IsDecisionMaker() bool {
	return cm.MemberRole == MemberRoleCoordinator ||
		cm.MemberRole == MemberRoleInstructor ||
		cm.MemberRole == MemberRolePresident
}

// HasVotingRights checks if this member has voting rights
func (cm *CommitteeMember) HasVotingRights() bool {
	return cm.VotePower > 0 && cm.IsPresent
}
