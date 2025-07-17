package entities

import (
	"time"

	"github.com/google/uuid"
)

type WorkGroup struct {
	ID          uuid.UUID       `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	ProjectID   uuid.UUID       `json:"project_id" gorm:"type:uuid;not null" validate:"required"`
	Name        string          `json:"name" gorm:"not null" validate:"required,min=3,max=100"`
	Description string          `json:"description" gorm:"type:text"`
	LeaderID    *uuid.UUID      `json:"leader_id" gorm:"type:uuid"`
	Status      WorkGroupStatus `json:"status" gorm:"type:varchar(20);not null;default:'active'" validate:"required"`
	MaxMembers  int             `json:"max_members" gorm:"not null;default:5" validate:"min=3,max=7"`

	// Metadata
	CreatedAt time.Time `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt time.Time `json:"updated_at" gorm:"autoUpdateTime"`

	// Relationships
	Project Project       `json:"project,omitempty" gorm:"foreignKey:ProjectID"`
	Members []GroupMember `json:"members,omitempty" gorm:"foreignKey:WorkGroupID;constraint:OnDelete:CASCADE"`
	Ideas   []ProjectIdea `json:"ideas,omitempty" gorm:"foreignKey:WorkGroupID;constraint:OnDelete:CASCADE"`
}

type GroupMember struct {
	ID          uuid.UUID         `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	WorkGroupID uuid.UUID         `json:"work_group_id" gorm:"type:uuid;not null" validate:"required"`
	StudentID   uuid.UUID         `json:"student_id" gorm:"type:uuid;not null" validate:"required"`
	Role        GroupMemberRole   `json:"role" gorm:"type:varchar(20);not null;default:'member'" validate:"required"`
	Status      GroupMemberStatus `json:"status" gorm:"type:varchar(20);not null;default:'active'" validate:"required"`
	JoinedAt    time.Time         `json:"joined_at" gorm:"autoCreateTime"`
	LeftAt      *time.Time        `json:"left_at"`

	// Relationships
	WorkGroup WorkGroup `json:"work_group,omitempty" gorm:"foreignKey:WorkGroupID"`
}

type WorkGroupStatus string

const (
	WorkGroupStatusActive    WorkGroupStatus = "active"
	WorkGroupStatusInactive  WorkGroupStatus = "inactive"
	WorkGroupStatusComplete  WorkGroupStatus = "complete"
	WorkGroupStatusDisbanded WorkGroupStatus = "disbanded"
)

type GroupMemberRole string

const (
	GroupMemberRoleLeader    GroupMemberRole = "leader"
	GroupMemberRoleMember    GroupMemberRole = "member"
	GroupMemberRoleDeveloper GroupMemberRole = "developer"
	GroupMemberRoleDesigner  GroupMemberRole = "designer"
	GroupMemberRoleAnalyst   GroupMemberRole = "analyst"
)

type GroupMemberStatus string

const (
	GroupMemberStatusActive   GroupMemberStatus = "active"
	GroupMemberStatusInactive GroupMemberStatus = "inactive"
	GroupMemberStatusLeft     GroupMemberStatus = "left"
)

func (wgs WorkGroupStatus) String() string {
	return string(wgs)
}

func (wgs WorkGroupStatus) IsValid() bool {
	switch wgs {
	case WorkGroupStatusActive, WorkGroupStatusInactive, WorkGroupStatusComplete, WorkGroupStatusDisbanded:
		return true
	default:
		return false
	}
}

func (gmr GroupMemberRole) String() string {
	return string(gmr)
}

func (gmr GroupMemberRole) IsValid() bool {
	switch gmr {
	case GroupMemberRoleLeader, GroupMemberRoleMember, GroupMemberRoleDeveloper, GroupMemberRoleDesigner, GroupMemberRoleAnalyst:
		return true
	default:
		return false
	}
}

func (gms GroupMemberStatus) String() string {
	return string(gms)
}

func (gms GroupMemberStatus) IsValid() bool {
	switch gms {
	case GroupMemberStatusActive, GroupMemberStatusInactive, GroupMemberStatusLeft:
		return true
	default:
		return false
	}
}

func (wg *WorkGroup) IsActive() bool {
	return wg.Status == WorkGroupStatusActive
}

func (wg *WorkGroup) GetActiveMembers() []GroupMember {
	var activeMembers []GroupMember
	for _, member := range wg.Members {
		if member.Status == GroupMemberStatusActive {
			activeMembers = append(activeMembers, member)
		}
	}
	return activeMembers
}

func (wg *WorkGroup) GetMemberCount() int {
	return len(wg.GetActiveMembers())
}

func (wg *WorkGroup) IsFull() bool {
	return wg.GetMemberCount() >= wg.MaxMembers
}

func (wg *WorkGroup) CanAddMember() bool {
	return wg.IsActive() && !wg.IsFull()
}

func (wg *WorkGroup) HasLeader() bool {
	return wg.LeaderID != nil
}

func (wg *WorkGroup) GetLeader() *GroupMember {
	if !wg.HasLeader() {
		return nil
	}

	for _, member := range wg.Members {
		if member.StudentID == *wg.LeaderID && member.Status == GroupMemberStatusActive {
			return &member
		}
	}
	return nil
}

func (wg *WorkGroup) SetLeader(studentID uuid.UUID) error {
	// Verify the student is an active member
	for _, member := range wg.Members {
		if member.StudentID == studentID && member.Status == GroupMemberStatusActive {
			wg.LeaderID = &studentID
			return nil
		}
	}
	return nil // Should return proper error
}

func (wg *WorkGroup) RemoveMember(studentID uuid.UUID) {
	for i, member := range wg.Members {
		if member.StudentID == studentID {
			wg.Members[i].Status = GroupMemberStatusLeft
			now := time.Now()
			wg.Members[i].LeftAt = &now

			// If removing leader, clear leadership
			if wg.LeaderID != nil && *wg.LeaderID == studentID {
				wg.LeaderID = nil
			}
			break
		}
	}
}
