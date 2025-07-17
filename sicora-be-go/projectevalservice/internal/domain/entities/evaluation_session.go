package entities

import (
	"time"

	"github.com/google/uuid"
)

type EvaluationSession struct {
	ID          uuid.UUID               `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	ProjectID   uuid.UUID               `json:"project_id" gorm:"type:uuid;not null" validate:"required"`
	Name        string                  `json:"name" gorm:"not null" validate:"required,min=5,max=200"`
	Description string                  `json:"description" gorm:"type:text"`
	Trimester   int                     `json:"trimester" gorm:"not null" validate:"required,min=2,max=7"`
	SessionType EvaluationSessionType   `json:"session_type" gorm:"type:varchar(30);not null" validate:"required"`
	Status      EvaluationSessionStatus `json:"status" gorm:"type:varchar(20);not null;default:'scheduled'" validate:"required"`

	// Schedule
	ScheduledDate     time.Time `json:"scheduled_date" gorm:"not null" validate:"required"`
	StartTime         time.Time `json:"start_time" gorm:"not null" validate:"required"`
	EndTime           time.Time `json:"end_time" gorm:"not null" validate:"required"`
	Location          string    `json:"location" gorm:"not null" validate:"required"`
	VirtualMeetingURL string    `json:"virtual_meeting_url"`

	// Configuration
	MinJurors    int        `json:"min_jurors" gorm:"not null;default:2" validate:"min=2"`
	MaxGroups    int        `json:"max_groups" gorm:"not null;default:10" validate:"min=1"`
	TimePerGroup int        `json:"time_per_group" gorm:"not null;default:30" validate:"min=15,max=120"` // minutes
	ChecklistID  *uuid.UUID `json:"checklist_id" gorm:"type:uuid"`

	// Notifications
	NotifyBefore     int        `json:"notify_before" gorm:"not null;default:48"` // hours
	LastNotification *time.Time `json:"last_notification"`

	// Metadata
	CreatedAt time.Time `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt time.Time `json:"updated_at" gorm:"autoUpdateTime"`

	// Relationships
	Project            Project              `json:"project,omitempty" gorm:"foreignKey:ProjectID"`
	Checklist          *Checklist           `json:"checklist,omitempty" gorm:"foreignKey:ChecklistID"`
	Jurors             []SessionJuror       `json:"jurors,omitempty" gorm:"foreignKey:SessionID;constraint:OnDelete:CASCADE"`
	Participants       []SessionParticipant `json:"participants,omitempty" gorm:"foreignKey:SessionID;constraint:OnDelete:CASCADE"`
	SessionEvaluations []SessionEvaluation  `json:"session_evaluations,omitempty" gorm:"foreignKey:SessionID;constraint:OnDelete:CASCADE"`
}

type SessionJuror struct {
	ID           uuid.UUID   `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	SessionID    uuid.UUID   `json:"session_id" gorm:"type:uuid;not null" validate:"required"`
	InstructorID uuid.UUID   `json:"instructor_id" gorm:"type:uuid;not null" validate:"required"`
	Role         JurorRole   `json:"role" gorm:"type:varchar(20);not null;default:'evaluator'" validate:"required"`
	Status       JurorStatus `json:"status" gorm:"type:varchar(20);not null;default:'assigned'" validate:"required"`
	AssignedAt   time.Time   `json:"assigned_at" gorm:"autoCreateTime"`
	ConfirmedAt  *time.Time  `json:"confirmed_at"`

	// Relationships
	Session EvaluationSession `json:"session,omitempty" gorm:"foreignKey:SessionID"`
}

type SessionParticipant struct {
	ID                uuid.UUID         `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	SessionID         uuid.UUID         `json:"session_id" gorm:"type:uuid;not null" validate:"required"`
	WorkGroupID       uuid.UUID         `json:"work_group_id" gorm:"type:uuid;not null" validate:"required"`
	Status            ParticipantStatus `json:"status" gorm:"type:varchar(20);not null;default:'registered'" validate:"required"`
	PresentationOrder int               `json:"presentation_order" gorm:"not null;default:1"`
	StartTime         *time.Time        `json:"start_time"`
	EndTime           *time.Time        `json:"end_time"`

	// Relationships
	Session   EvaluationSession `json:"session,omitempty" gorm:"foreignKey:SessionID"`
	WorkGroup WorkGroup         `json:"work_group,omitempty" gorm:"foreignKey:WorkGroupID"`
}

type SessionEvaluation struct {
	ID           uuid.UUID  `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	SessionID    uuid.UUID  `json:"session_id" gorm:"type:uuid;not null" validate:"required"`
	WorkGroupID  uuid.UUID  `json:"work_group_id" gorm:"type:uuid;not null" validate:"required"`
	JurorID      uuid.UUID  `json:"juror_id" gorm:"type:uuid;not null" validate:"required"`
	EvaluationID uuid.UUID  `json:"evaluation_id" gorm:"type:uuid;not null" validate:"required"`
	CompletedAt  *time.Time `json:"completed_at"`

	// Relationships
	Session    EvaluationSession `json:"session,omitempty" gorm:"foreignKey:SessionID"`
	WorkGroup  WorkGroup         `json:"work_group,omitempty" gorm:"foreignKey:WorkGroupID"`
	Evaluation Evaluation        `json:"evaluation,omitempty" gorm:"foreignKey:EvaluationID"`
}

// Enums
type EvaluationSessionType string

const (
	EvaluationSessionTypeIdeaPresentation  EvaluationSessionType = "idea_presentation"
	EvaluationSessionTypeProgressReview    EvaluationSessionType = "progress_review"
	EvaluationSessionTypeFinalPresentation EvaluationSessionType = "final_presentation"
	EvaluationSessionTypeMidTermReview     EvaluationSessionType = "midterm_review"
)

type EvaluationSessionStatus string

const (
	EvaluationSessionStatusScheduled  EvaluationSessionStatus = "scheduled"
	EvaluationSessionStatusConfirmed  EvaluationSessionStatus = "confirmed"
	EvaluationSessionStatusInProgress EvaluationSessionStatus = "in_progress"
	EvaluationSessionStatusCompleted  EvaluationSessionStatus = "completed"
	EvaluationSessionStatusCancelled  EvaluationSessionStatus = "cancelled"
	EvaluationSessionStatusPostponed  EvaluationSessionStatus = "postponed"
)

type JurorRole string

const (
	JurorRoleChair     JurorRole = "chair"
	JurorRoleEvaluator JurorRole = "evaluator"
	JurorRoleObserver  JurorRole = "observer"
)

type JurorStatus string

const (
	JurorStatusAssigned  JurorStatus = "assigned"
	JurorStatusConfirmed JurorStatus = "confirmed"
	JurorStatusDeclined  JurorStatus = "declined"
	JurorStatusAttended  JurorStatus = "attended"
	JurorStatusAbsent    JurorStatus = "absent"
)

type ParticipantStatus string

const (
	ParticipantStatusRegistered ParticipantStatus = "registered"
	ParticipantStatusConfirmed  ParticipantStatus = "confirmed"
	ParticipantStatusPresented  ParticipantStatus = "presented"
	ParticipantStatusAbsent     ParticipantStatus = "absent"
	ParticipantStatusExcused    ParticipantStatus = "excused"
)

// Methods
func (est EvaluationSessionType) String() string {
	return string(est)
}

func (est EvaluationSessionType) IsValid() bool {
	switch est {
	case EvaluationSessionTypeIdeaPresentation, EvaluationSessionTypeProgressReview, EvaluationSessionTypeFinalPresentation, EvaluationSessionTypeMidTermReview:
		return true
	default:
		return false
	}
}

func (ess EvaluationSessionStatus) String() string {
	return string(ess)
}

func (ess EvaluationSessionStatus) IsValid() bool {
	switch ess {
	case EvaluationSessionStatusScheduled, EvaluationSessionStatusConfirmed, EvaluationSessionStatusInProgress, EvaluationSessionStatusCompleted, EvaluationSessionStatusCancelled, EvaluationSessionStatusPostponed:
		return true
	default:
		return false
	}
}

func (es *EvaluationSession) CanBeModified() bool {
	return es.Status == EvaluationSessionStatusScheduled || es.Status == EvaluationSessionStatusPostponed
}

func (es *EvaluationSession) CanStart() bool {
	return es.Status == EvaluationSessionStatusConfirmed && time.Now().After(es.StartTime.Add(-15*time.Minute))
}

func (es *EvaluationSession) GetConfirmedJurors() []SessionJuror {
	var confirmed []SessionJuror
	for _, juror := range es.Jurors {
		if juror.Status == JurorStatusConfirmed || juror.Status == JurorStatusAttended {
			confirmed = append(confirmed, juror)
		}
	}
	return confirmed
}

func (es *EvaluationSession) HasMinimumJurors() bool {
	return len(es.GetConfirmedJurors()) >= es.MinJurors
}

func (es *EvaluationSession) GetDuration() time.Duration {
	return es.EndTime.Sub(es.StartTime)
}

func (es *EvaluationSession) IsInProgress() bool {
	now := time.Now()
	return es.Status == EvaluationSessionStatusInProgress && now.After(es.StartTime) && now.Before(es.EndTime)
}
