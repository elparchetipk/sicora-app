package entities

import (
	"encoding/json"
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// PlanType represents the type of improvement plan
type PlanType string

const (
	PlanTypeAcademic      PlanType = "ACADEMIC"
	PlanTypeDisciplinary  PlanType = "DISCIPLINARY"
	PlanTypeMixed         PlanType = "MIXED"
)

// PlanStatus represents the current status of an improvement plan
type PlanStatus string

const (
	PlanStatusActive    PlanStatus = "ACTIVE"
	PlanStatusCompleted PlanStatus = "COMPLETED"
	PlanStatusFailed    PlanStatus = "FAILED"
	PlanStatusExtended  PlanStatus = "EXTENDED"
)

// Objective represents a specific objective in the improvement plan
type Objective struct {
	ID          string    `json:"id"`
	Description string    `json:"description"`
	Target      string    `json:"target"`
	Deadline    time.Time `json:"deadline"`
	Completed   bool      `json:"completed"`
}

// Activity represents an activity to be completed
type Activity struct {
	ID          string    `json:"id"`
	Name        string    `json:"name"`
	Description string    `json:"description"`
	DueDate     time.Time `json:"due_date"`
	Completed   bool      `json:"completed"`
	CompletedAt *time.Time `json:"completed_at,omitempty"`
}

// SuccessCriteria represents criteria for success
type SuccessCriteria struct {
	ID          string  `json:"id"`
	Description string  `json:"description"`
	Metric      string  `json:"metric"`
	Target      float64 `json:"target"`
	Achieved    bool    `json:"achieved"`
}

// ImprovementPlan represents an academic/disciplinary improvement plan
type ImprovementPlan struct {
	ID                     uuid.UUID         `json:"id" gorm:"type:uuid;primaryKey;default:gen_random_uuid()"`
	StudentID              uuid.UUID         `json:"student_id" gorm:"type:uuid;not null"`
	StudentCaseID          *uuid.UUID        `json:"student_case_id,omitempty" gorm:"type:uuid"`
	PlanType               PlanType          `json:"plan_type" gorm:"type:varchar(50);not null"`
	StartDate              time.Time         `json:"start_date" gorm:"not null"`
	EndDate                time.Time         `json:"end_date" gorm:"not null"`
	Objectives             []Objective       `json:"objectives" gorm:"type:jsonb;not null"`
	Activities             []Activity        `json:"activities" gorm:"type:jsonb;not null"`
	SuccessCriteria        []SuccessCriteria `json:"success_criteria" gorm:"type:jsonb;not null"`
	ResponsibleInstructorID *uuid.UUID       `json:"responsible_instructor_id,omitempty" gorm:"type:uuid"`
	CurrentStatus          PlanStatus        `json:"current_status" gorm:"type:varchar(50);default:'ACTIVE'"`
	CompliancePercentage   float64           `json:"compliance_percentage" gorm:"default:0"`
	FinalEvaluation        *string           `json:"final_evaluation,omitempty" gorm:"type:text"`
	CreatedAt              time.Time         `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt              time.Time         `json:"updated_at" gorm:"autoUpdateTime"`

	// Relationships
	StudentCase *StudentCase `json:"-" gorm:"foreignKey:StudentCaseID"`
}

// BeforeCreate sets the ID before creating a new improvement plan
func (ip *ImprovementPlan) BeforeCreate(tx *gorm.DB) error {
	if ip.ID == uuid.Nil {
		ip.ID = uuid.New()
	}
	return nil
}

// TableName specifies the table name for ImprovementPlan
func (ImprovementPlan) TableName() string {
	return "mevalservice_schema.improvement_plans"
}

// IsActive checks if the improvement plan is currently active
func (ip *ImprovementPlan) IsActive() bool {
	return ip.CurrentStatus == PlanStatusActive
}

// IsCompleted checks if the improvement plan is completed
func (ip *ImprovementPlan) IsCompleted() bool {
	return ip.CurrentStatus == PlanStatusCompleted
}

// IsFailed checks if the improvement plan has failed
func (ip *ImprovementPlan) IsFailed() bool {
	return ip.CurrentStatus == PlanStatusFailed
}

// IsOverdue checks if the improvement plan is overdue
func (ip *ImprovementPlan) IsOverdue() bool {
	return time.Now().After(ip.EndDate) && ip.CurrentStatus == PlanStatusActive
}

// CalculateCompliancePercentage calculates the current compliance percentage
func (ip *ImprovementPlan) CalculateCompliancePercentage() float64 {
	if len(ip.Activities) == 0 {
		return 0.0
	}

	completedActivities := 0
	for _, activity := range ip.Activities {
		if activity.Completed {
			completedActivities++
		}
	}

	percentage := float64(completedActivities) / float64(len(ip.Activities)) * 100
	ip.CompliancePercentage = percentage
	return percentage
}

// GetCompletedObjectives returns the number of completed objectives
func (ip *ImprovementPlan) GetCompletedObjectives() int {
	completed := 0
	for _, objective := range ip.Objectives {
		if objective.Completed {
			completed++
		}
	}
	return completed
}

// GetObjectivesJSON returns objectives as JSON string
func (ip *ImprovementPlan) GetObjectivesJSON() (string, error) {
	bytes, err := json.Marshal(ip.Objectives)
	return string(bytes), err
}

// SetObjectivesFromJSON sets objectives from JSON string
func (ip *ImprovementPlan) SetObjectivesFromJSON(jsonStr string) error {
	return json.Unmarshal([]byte(jsonStr), &ip.Objectives)
}

// GetActivitiesJSON returns activities as JSON string
func (ip *ImprovementPlan) GetActivitiesJSON() (string, error) {
	bytes, err := json.Marshal(ip.Activities)
	return string(bytes), err
}

// SetActivitiesFromJSON sets activities from JSON string
func (ip *ImprovementPlan) SetActivitiesFromJSON(jsonStr string) error {
	return json.Unmarshal([]byte(jsonStr), &ip.Activities)
}

// MarkActivityCompleted marks an activity as completed
func (ip *ImprovementPlan) MarkActivityCompleted(activityID string) bool {
	for i, activity := range ip.Activities {
		if activity.ID == activityID {
			now := time.Now()
			ip.Activities[i].Completed = true
			ip.Activities[i].CompletedAt = &now
			ip.CalculateCompliancePercentage()
			return true
		}
	}
	return false
}
