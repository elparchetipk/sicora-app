package database

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// CommitteeModel representa el modelo de datos para comités
type CommitteeModel struct {
	ID                  uuid.UUID            `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	Name                string               `gorm:"not null" json:"name"`
	Type                string               `gorm:"not null" json:"type"` // DISCIPLINARY, ACADEMIC
	Status              string               `gorm:"not null;default:'ACTIVE'" json:"status"` // ACTIVE, INACTIVE
	Center              string               `gorm:"not null" json:"center"`
	Coordinator         string               `gorm:"not null" json:"coordinator"`
	MaxMembers          int                  `gorm:"not null;default:5" json:"max_members"`
	CurrentMembers      int                  `gorm:"default:0" json:"current_members"`
	CreatedAt           time.Time            `gorm:"autoCreateTime" json:"created_at"`
	UpdatedAt           time.Time            `gorm:"autoUpdateTime" json:"updated_at"`
	DeletedAt           gorm.DeletedAt       `gorm:"index" json:"deleted_at,omitempty"`
	
	// Relaciones
	Members             []CommitteeMemberModel `gorm:"foreignKey:CommitteeID" json:"members,omitempty"`
	Cases               []StudentCaseModel     `gorm:"foreignKey:CommitteeID" json:"cases,omitempty"`
	Decisions           []CommitteeDecisionModel `gorm:"foreignKey:CommitteeID" json:"decisions,omitempty"`
}

// CommitteeMemberModel representa el modelo de datos para miembros de comité
type CommitteeMemberModel struct {
	ID                  uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	CommitteeID         uuid.UUID      `gorm:"type:uuid;not null" json:"committee_id"`
	UserID              uuid.UUID      `gorm:"type:uuid;not null" json:"user_id"`
	Role                string         `gorm:"not null" json:"role"` // PRESIDENT, SECRETARY, MEMBER, COORDINATOR
	Status              string         `gorm:"not null;default:'ACTIVE'" json:"status"` // ACTIVE, INACTIVE
	AppointmentDate     time.Time      `gorm:"not null" json:"appointment_date"`
	EndDate             *time.Time     `json:"end_date,omitempty"`
	CreatedAt           time.Time      `gorm:"autoCreateTime" json:"created_at"`
	UpdatedAt           time.Time      `gorm:"autoUpdateTime" json:"updated_at"`
	DeletedAt           gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`
	
	// Relaciones
	Committee           CommitteeModel `gorm:"foreignKey:CommitteeID" json:"committee,omitempty"`
}

// StudentCaseModel representa el modelo de datos para casos de estudiantes
type StudentCaseModel struct {
	ID                  uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	StudentID           uuid.UUID      `gorm:"type:uuid;not null" json:"student_id"`
	CommitteeID         uuid.UUID      `gorm:"type:uuid;not null" json:"committee_id"`
	CaseNumber          string         `gorm:"uniqueIndex;not null" json:"case_number"`
	Type                string         `gorm:"not null" json:"type"` // DISCIPLINARY, ACADEMIC
	Severity            string         `gorm:"not null" json:"severity"` // MINOR, MODERATE, SEVERE, CRITICAL
	Status              string         `gorm:"not null;default:'PENDING'" json:"status"` // PENDING, IN_PROGRESS, RESOLVED, APPEALED, CLOSED
	Priority            string         `gorm:"not null;default:'MEDIUM'" json:"priority"` // LOW, MEDIUM, HIGH, URGENT
	Title               string         `gorm:"not null" json:"title"`
	Description         string         `gorm:"type:text;not null" json:"description"`
	Evidence            string         `gorm:"type:text" json:"evidence"`
	ReportedBy          string         `gorm:"not null" json:"reported_by"`
	ReportDate          time.Time      `gorm:"not null" json:"report_date"`
	DueDate             *time.Time     `json:"due_date,omitempty"`
	ResolutionDate      *time.Time     `json:"resolution_date,omitempty"`
	CreatedAt           time.Time      `gorm:"autoCreateTime" json:"created_at"`
	UpdatedAt           time.Time      `gorm:"autoUpdateTime" json:"updated_at"`
	DeletedAt           gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`
	
	// Relaciones
	Committee           CommitteeModel         `gorm:"foreignKey:CommitteeID" json:"committee,omitempty"`
	ImprovementPlans    []ImprovementPlanModel `gorm:"foreignKey:StudentCaseID" json:"improvement_plans,omitempty"`
	Sanctions           []SanctionModel        `gorm:"foreignKey:StudentCaseID" json:"sanctions,omitempty"`
	Decisions           []CommitteeDecisionModel `gorm:"foreignKey:StudentCaseID" json:"decisions,omitempty"`
	Appeals             []AppealModel          `gorm:"foreignKey:StudentCaseID" json:"appeals,omitempty"`
}

// ImprovementPlanModel representa el modelo de datos para planes de mejoramiento
type ImprovementPlanModel struct {
	ID                  uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	StudentCaseID       uuid.UUID      `gorm:"type:uuid;not null" json:"student_case_id"`
	StudentID           uuid.UUID      `gorm:"type:uuid;not null" json:"student_id"`
	Title               string         `gorm:"not null" json:"title"`
	Description         string         `gorm:"type:text;not null" json:"description"`
	Objectives          string         `gorm:"type:text;not null" json:"objectives"`
	Activities          string         `gorm:"type:text;not null" json:"activities"`
	Resources           string         `gorm:"type:text" json:"resources"`
	Timeline            string         `gorm:"type:text;not null" json:"timeline"`
	Status              string         `gorm:"not null;default:'PENDING'" json:"status"` // PENDING, IN_PROGRESS, COMPLETED, FAILED
	StartDate           time.Time      `gorm:"not null" json:"start_date"`
	EndDate             time.Time      `gorm:"not null" json:"end_date"`
	CompletionDate      *time.Time     `json:"completion_date,omitempty"`
	Progress            int            `gorm:"default:0" json:"progress"` // 0-100
	SupervisorID        uuid.UUID      `gorm:"type:uuid;not null" json:"supervisor_id"`
	SupervisorNotes     string         `gorm:"type:text" json:"supervisor_notes"`
	CreatedAt           time.Time      `gorm:"autoCreateTime" json:"created_at"`
	UpdatedAt           time.Time      `gorm:"autoUpdateTime" json:"updated_at"`
	DeletedAt           gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`
	
	// Relaciones
	StudentCase         StudentCaseModel `gorm:"foreignKey:StudentCaseID" json:"student_case,omitempty"`
}

// SanctionModel representa el modelo de datos para sanciones
type SanctionModel struct {
	ID                  uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	StudentCaseID       uuid.UUID      `gorm:"type:uuid;not null" json:"student_case_id"`
	StudentID           uuid.UUID      `gorm:"type:uuid;not null" json:"student_id"`
	Type                string         `gorm:"not null" json:"type"` // WARNING, CONDITIONAL_ENROLLMENT, ENROLLMENT_CANCELLATION
	Severity            string         `gorm:"not null" json:"severity"` // MINOR, MODERATE, SEVERE, CRITICAL
	Status              string         `gorm:"not null;default:'PENDING'" json:"status"` // PENDING, ACTIVE, COMPLETED, REVOKED
	Title               string         `gorm:"not null" json:"title"`
	Description         string         `gorm:"type:text;not null" json:"description"`
	Justification       string         `gorm:"type:text;not null" json:"justification"`
	StartDate           time.Time      `gorm:"not null" json:"start_date"`
	EndDate             *time.Time     `json:"end_date,omitempty"`
	CompletionDate      *time.Time     `json:"completion_date,omitempty"`
	IsAppealable        bool           `gorm:"default:true" json:"is_appealable"`
	AppealDeadline      *time.Time     `json:"appeal_deadline,omitempty"`
	CreatedAt           time.Time      `gorm:"autoCreateTime" json:"created_at"`
	UpdatedAt           time.Time      `gorm:"autoUpdateTime" json:"updated_at"`
	DeletedAt           gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`
	
	// Relaciones
	StudentCase         StudentCaseModel `gorm:"foreignKey:StudentCaseID" json:"student_case,omitempty"`
}

// CommitteeDecisionModel representa el modelo de datos para decisiones de comité
type CommitteeDecisionModel struct {
	ID                  uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	CommitteeID         uuid.UUID      `gorm:"type:uuid;not null" json:"committee_id"`
	StudentCaseID       *uuid.UUID     `gorm:"type:uuid" json:"student_case_id,omitempty"`
	DecisionNumber      string         `gorm:"uniqueIndex;not null" json:"decision_number"`
	Type                string         `gorm:"not null" json:"type"` // CASE_RESOLUTION, SANCTION_APPROVAL, APPEAL_RESOLUTION, POLICY_DECISION
	Title               string         `gorm:"not null" json:"title"`
	Description         string         `gorm:"type:text;not null" json:"description"`
	Resolution          string         `gorm:"type:text;not null" json:"resolution"`
	Justification       string         `gorm:"type:text;not null" json:"justification"`
	VotingResult        string         `gorm:"type:text" json:"voting_result"`
	AttendeesList       string         `gorm:"type:text" json:"attendees_list"`
	Status              string         `gorm:"not null;default:'DRAFT'" json:"status"` // DRAFT, APPROVED, EXECUTED, APPEALED
	DecisionDate        time.Time      `gorm:"not null" json:"decision_date"`
	ExecutionDate       *time.Time     `json:"execution_date,omitempty"`
	PresidentSignature  bool           `gorm:"default:false" json:"president_signature"`
	SecretarySignature  bool           `gorm:"default:false" json:"secretary_signature"`
	CreatedAt           time.Time      `gorm:"autoCreateTime" json:"created_at"`
	UpdatedAt           time.Time      `gorm:"autoUpdateTime" json:"updated_at"`
	DeletedAt           gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`
	
	// Relaciones
	Committee           CommitteeModel `gorm:"foreignKey:CommitteeID" json:"committee,omitempty"`
	StudentCase         *StudentCaseModel `gorm:"foreignKey:StudentCaseID" json:"student_case,omitempty"`
}

// AppealModel representa el modelo de datos para apelaciones
type AppealModel struct {
	ID                  uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	StudentCaseID       uuid.UUID      `gorm:"type:uuid;not null" json:"student_case_id"`
	StudentID           uuid.UUID      `gorm:"type:uuid;not null" json:"student_id"`
	AppealNumber        string         `gorm:"uniqueIndex;not null" json:"appeal_number"`
	Type                string         `gorm:"not null" json:"type"` // SANCTION_APPEAL, DECISION_APPEAL, PROCESS_APPEAL
	Status              string         `gorm:"not null;default:'SUBMITTED'" json:"status"` // SUBMITTED, UNDER_REVIEW, ACCEPTED, REJECTED, WITHDRAWN
	Priority            string         `gorm:"not null;default:'MEDIUM'" json:"priority"` // LOW, MEDIUM, HIGH, URGENT
	Subject             string         `gorm:"not null" json:"subject"`
	Description         string         `gorm:"type:text;not null" json:"description"`
	Justification       string         `gorm:"type:text;not null" json:"justification"`
	Evidence            string         `gorm:"type:text" json:"evidence"`
	RequestedResolution string         `gorm:"type:text;not null" json:"requested_resolution"`
	SubmissionDate      time.Time      `gorm:"not null" json:"submission_date"`
	ReviewDate          *time.Time     `json:"review_date,omitempty"`
	ResolutionDate      *time.Time     `json:"resolution_date,omitempty"`
	ReviewerNotes       string         `gorm:"type:text" json:"reviewer_notes"`
	FinalResolution     string         `gorm:"type:text" json:"final_resolution"`
	CreatedAt           time.Time      `gorm:"autoCreateTime" json:"created_at"`
	UpdatedAt           time.Time      `gorm:"autoUpdateTime" json:"updated_at"`
	DeletedAt           gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`
	
	// Relaciones
	StudentCase         StudentCaseModel `gorm:"foreignKey:StudentCaseID" json:"student_case,omitempty"`
}

// TableName methods for custom table names
func (CommitteeModel) TableName() string         { return "committees" }
func (CommitteeMemberModel) TableName() string  { return "committee_members" }
func (StudentCaseModel) TableName() string      { return "student_cases" }
func (ImprovementPlanModel) TableName() string  { return "improvement_plans" }
func (SanctionModel) TableName() string         { return "sanctions" }
func (CommitteeDecisionModel) TableName() string { return "committee_decisions" }
func (AppealModel) TableName() string           { return "appeals" }
