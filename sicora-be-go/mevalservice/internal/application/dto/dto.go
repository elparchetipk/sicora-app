package dto

import (
	"time"

	"github.com/google/uuid"
)

// Committee DTOs
type CreateCommitteeRequest struct {
	Name        string `json:"name" validate:"required,min=3,max=100"`
	Type        string `json:"type" validate:"required,oneof=DISCIPLINARY ACADEMIC"`
	Center      string `json:"center" validate:"required,min=3,max=50"`
	Coordinator string `json:"coordinator" validate:"required,min=3,max=100"`
	MaxMembers  int    `json:"max_members" validate:"required,min=3,max=15"`
}

type UpdateCommitteeRequest struct {
	Name        string `json:"name,omitempty" validate:"omitempty,min=3,max=100"`
	Status      string `json:"status,omitempty" validate:"omitempty,oneof=ACTIVE INACTIVE"`
	Coordinator string `json:"coordinator,omitempty" validate:"omitempty,min=3,max=100"`
	MaxMembers  int    `json:"max_members,omitempty" validate:"omitempty,min=3,max=15"`
}

type CommitteeResponse struct {
	ID             uuid.UUID                 `json:"id"`
	Name           string                    `json:"name"`
	Type           string                    `json:"type"`
	Status         string                    `json:"status"`
	Center         string                    `json:"center"`
	Coordinator    string                    `json:"coordinator"`
	MaxMembers     int                       `json:"max_members"`
	CurrentMembers int                       `json:"current_members"`
	Members        []CommitteeMemberResponse `json:"members,omitempty"`
	CreatedAt      time.Time                 `json:"created_at"`
	UpdatedAt      time.Time                 `json:"updated_at"`
}

// Committee Member DTOs
type CreateCommitteeMemberRequest struct {
	CommitteeID     uuid.UUID `json:"committee_id" validate:"required"`
	UserID          uuid.UUID `json:"user_id" validate:"required"`
	Role            string    `json:"role" validate:"required,oneof=PRESIDENT SECRETARY MEMBER COORDINATOR"`
	AppointmentDate time.Time `json:"appointment_date" validate:"required"`
}

type UpdateCommitteeMemberRequest struct {
	Role    string     `json:"role,omitempty" validate:"omitempty,oneof=PRESIDENT SECRETARY MEMBER COORDINATOR"`
	Status  string     `json:"status,omitempty" validate:"omitempty,oneof=ACTIVE INACTIVE"`
	EndDate *time.Time `json:"end_date,omitempty"`
}

type CommitteeMemberResponse struct {
	ID              uuid.UUID  `json:"id"`
	CommitteeID     uuid.UUID  `json:"committee_id"`
	UserID          uuid.UUID  `json:"user_id"`
	Role            string     `json:"role"`
	Status          string     `json:"status"`
	AppointmentDate time.Time  `json:"appointment_date"`
	EndDate         *time.Time `json:"end_date,omitempty"`
	CreatedAt       time.Time  `json:"created_at"`
	UpdatedAt       time.Time  `json:"updated_at"`
}

// Student Case DTOs
type CreateStudentCaseRequest struct {
	StudentID   uuid.UUID  `json:"student_id" validate:"required"`
	CommitteeID uuid.UUID  `json:"committee_id" validate:"required"`
	Type        string     `json:"type" validate:"required,oneof=DISCIPLINARY ACADEMIC"`
	Severity    string     `json:"severity" validate:"required,oneof=MINOR MODERATE SEVERE CRITICAL"`
	Priority    string     `json:"priority,omitempty" validate:"omitempty,oneof=LOW MEDIUM HIGH URGENT"`
	Title       string     `json:"title" validate:"required,min=5,max=200"`
	Description string     `json:"description" validate:"required,min=10"`
	Evidence    string     `json:"evidence,omitempty"`
	ReportedBy  string     `json:"reported_by" validate:"required,min=3,max=100"`
	DueDate     *time.Time `json:"due_date,omitempty"`
}

type UpdateStudentCaseRequest struct {
	Status         string     `json:"status,omitempty" validate:"omitempty,oneof=PENDING IN_PROGRESS RESOLVED APPEALED CLOSED"`
	Priority       string     `json:"priority,omitempty" validate:"omitempty,oneof=LOW MEDIUM HIGH URGENT"`
	Description    string     `json:"description,omitempty" validate:"omitempty,min=10"`
	Evidence       string     `json:"evidence,omitempty"`
	DueDate        *time.Time `json:"due_date,omitempty"`
	ResolutionDate *time.Time `json:"resolution_date,omitempty"`
}

type StudentCaseResponse struct {
	ID                uuid.UUID                    `json:"id"`
	StudentID         uuid.UUID                    `json:"student_id"`
	CommitteeID       uuid.UUID                    `json:"committee_id"`
	CaseNumber        string                       `json:"case_number"`
	Type              string                       `json:"type"`
	Severity          string                       `json:"severity"`
	Status            string                       `json:"status"`
	Priority          string                       `json:"priority"`
	Title             string                       `json:"title"`
	Description       string                       `json:"description"`
	Evidence          string                       `json:"evidence"`
	ReportedBy        string                       `json:"reported_by"`
	ReportDate        time.Time                    `json:"report_date"`
	DueDate           *time.Time                   `json:"due_date,omitempty"`
	ResolutionDate    *time.Time                   `json:"resolution_date,omitempty"`
	Committee         *CommitteeResponse           `json:"committee,omitempty"`
	ImprovementPlans  []ImprovementPlanResponse    `json:"improvement_plans,omitempty"`
	Sanctions         []SanctionResponse           `json:"sanctions,omitempty"`
	Decisions         []CommitteeDecisionResponse  `json:"decisions,omitempty"`
	Appeals           []AppealResponse             `json:"appeals,omitempty"`
	CreatedAt         time.Time                    `json:"created_at"`
	UpdatedAt         time.Time                    `json:"updated_at"`
}

// Improvement Plan DTOs
type CreateImprovementPlanRequest struct {
	StudentCaseID uuid.UUID `json:"student_case_id" validate:"required"`
	StudentID     uuid.UUID `json:"student_id" validate:"required"`
	Title         string    `json:"title" validate:"required,min=5,max=200"`
	Description   string    `json:"description" validate:"required,min=10"`
	Objectives    string    `json:"objectives" validate:"required,min=10"`
	Activities    string    `json:"activities" validate:"required,min=10"`
	Resources     string    `json:"resources,omitempty"`
	Timeline      string    `json:"timeline" validate:"required,min=10"`
	StartDate     time.Time `json:"start_date" validate:"required"`
	EndDate       time.Time `json:"end_date" validate:"required"`
	SupervisorID  uuid.UUID `json:"supervisor_id" validate:"required"`
}

type UpdateImprovementPlanRequest struct {
	Status          string     `json:"status,omitempty" validate:"omitempty,oneof=PENDING IN_PROGRESS COMPLETED FAILED"`
	Progress        int        `json:"progress,omitempty" validate:"omitempty,min=0,max=100"`
	SupervisorNotes string     `json:"supervisor_notes,omitempty"`
	CompletionDate  *time.Time `json:"completion_date,omitempty"`
}

type ImprovementPlanResponse struct {
	ID              uuid.UUID  `json:"id"`
	StudentCaseID   uuid.UUID  `json:"student_case_id"`
	StudentID       uuid.UUID  `json:"student_id"`
	Title           string     `json:"title"`
	Description     string     `json:"description"`
	Objectives      string     `json:"objectives"`
	Activities      string     `json:"activities"`
	Resources       string     `json:"resources"`
	Timeline        string     `json:"timeline"`
	Status          string     `json:"status"`
	StartDate       time.Time  `json:"start_date"`
	EndDate         time.Time  `json:"end_date"`
	CompletionDate  *time.Time `json:"completion_date,omitempty"`
	Progress        int        `json:"progress"`
	SupervisorID    uuid.UUID  `json:"supervisor_id"`
	SupervisorNotes string     `json:"supervisor_notes"`
	CreatedAt       time.Time  `json:"created_at"`
	UpdatedAt       time.Time  `json:"updated_at"`
}

// Sanction DTOs
type CreateSanctionRequest struct {
	StudentCaseID  uuid.UUID  `json:"student_case_id" validate:"required"`
	StudentID      uuid.UUID  `json:"student_id" validate:"required"`
	Type           string     `json:"type" validate:"required,oneof=WARNING CONDITIONAL_ENROLLMENT ENROLLMENT_CANCELLATION"`
	Severity       string     `json:"severity" validate:"required,oneof=MINOR MODERATE SEVERE CRITICAL"`
	Title          string     `json:"title" validate:"required,min=5,max=200"`
	Description    string     `json:"description" validate:"required,min=10"`
	Justification  string     `json:"justification" validate:"required,min=10"`
	StartDate      time.Time  `json:"start_date" validate:"required"`
	EndDate        *time.Time `json:"end_date,omitempty"`
	IsAppealable   bool       `json:"is_appealable"`
	AppealDeadline *time.Time `json:"appeal_deadline,omitempty"`
}

type UpdateSanctionRequest struct {
	Status         string     `json:"status,omitempty" validate:"omitempty,oneof=PENDING ACTIVE COMPLETED REVOKED"`
	CompletionDate *time.Time `json:"completion_date,omitempty"`
}

type SanctionResponse struct {
	ID              uuid.UUID  `json:"id"`
	StudentCaseID   uuid.UUID  `json:"student_case_id"`
	StudentID       uuid.UUID  `json:"student_id"`
	Type            string     `json:"type"`
	Severity        string     `json:"severity"`
	Status          string     `json:"status"`
	Title           string     `json:"title"`
	Description     string     `json:"description"`
	Justification   string     `json:"justification"`
	StartDate       time.Time  `json:"start_date"`
	EndDate         *time.Time `json:"end_date,omitempty"`
	CompletionDate  *time.Time `json:"completion_date,omitempty"`
	IsAppealable    bool       `json:"is_appealable"`
	AppealDeadline  *time.Time `json:"appeal_deadline,omitempty"`
	CreatedAt       time.Time  `json:"created_at"`
	UpdatedAt       time.Time  `json:"updated_at"`
}

// Committee Decision DTOs
type CreateCommitteeDecisionRequest struct {
	CommitteeID     uuid.UUID  `json:"committee_id" validate:"required"`
	StudentCaseID   *uuid.UUID `json:"student_case_id,omitempty"`
	Type            string     `json:"type" validate:"required,oneof=CASE_RESOLUTION SANCTION_APPROVAL APPEAL_RESOLUTION POLICY_DECISION"`
	Title           string     `json:"title" validate:"required,min=5,max=200"`
	Description     string     `json:"description" validate:"required,min=10"`
	Resolution      string     `json:"resolution" validate:"required,min=10"`
	Justification   string     `json:"justification" validate:"required,min=10"`
	VotingResult    string     `json:"voting_result,omitempty"`
	AttendeesList   string     `json:"attendees_list,omitempty"`
	DecisionDate    time.Time  `json:"decision_date" validate:"required"`
}

type UpdateCommitteeDecisionRequest struct {
	Status             string     `json:"status,omitempty" validate:"omitempty,oneof=DRAFT APPROVED EXECUTED APPEALED"`
	ExecutionDate      *time.Time `json:"execution_date,omitempty"`
	PresidentSignature bool       `json:"president_signature,omitempty"`
	SecretarySignature bool       `json:"secretary_signature,omitempty"`
}

type CommitteeDecisionResponse struct {
	ID                 uuid.UUID  `json:"id"`
	CommitteeID        uuid.UUID  `json:"committee_id"`
	StudentCaseID      *uuid.UUID `json:"student_case_id,omitempty"`
	DecisionNumber     string     `json:"decision_number"`
	Type               string     `json:"type"`
	Title              string     `json:"title"`
	Description        string     `json:"description"`
	Resolution         string     `json:"resolution"`
	Justification      string     `json:"justification"`
	VotingResult       string     `json:"voting_result"`
	AttendeesList      string     `json:"attendees_list"`
	Status             string     `json:"status"`
	DecisionDate       time.Time  `json:"decision_date"`
	ExecutionDate      *time.Time `json:"execution_date,omitempty"`
	PresidentSignature bool       `json:"president_signature"`
	SecretarySignature bool       `json:"secretary_signature"`
	CreatedAt          time.Time  `json:"created_at"`
	UpdatedAt          time.Time  `json:"updated_at"`
}

// Appeal DTOs
type CreateAppealRequest struct {
	StudentCaseID       uuid.UUID `json:"student_case_id" validate:"required"`
	StudentID           uuid.UUID `json:"student_id" validate:"required"`
	Type                string    `json:"type" validate:"required,oneof=SANCTION_APPEAL DECISION_APPEAL PROCESS_APPEAL"`
	Priority            string    `json:"priority,omitempty" validate:"omitempty,oneof=LOW MEDIUM HIGH URGENT"`
	Subject             string    `json:"subject" validate:"required,min=5,max=200"`
	Description         string    `json:"description" validate:"required,min=10"`
	Justification       string    `json:"justification" validate:"required,min=10"`
	Evidence            string    `json:"evidence,omitempty"`
	RequestedResolution string    `json:"requested_resolution" validate:"required,min=10"`
}

type UpdateAppealRequest struct {
	Status          string     `json:"status,omitempty" validate:"omitempty,oneof=SUBMITTED UNDER_REVIEW ACCEPTED REJECTED WITHDRAWN"`
	ReviewDate      *time.Time `json:"review_date,omitempty"`
	ResolutionDate  *time.Time `json:"resolution_date,omitempty"`
	ReviewerNotes   string     `json:"reviewer_notes,omitempty"`
	FinalResolution string     `json:"final_resolution,omitempty"`
}

type AppealResponse struct {
	ID                  uuid.UUID  `json:"id"`
	StudentCaseID       uuid.UUID  `json:"student_case_id"`
	StudentID           uuid.UUID  `json:"student_id"`
	AppealNumber        string     `json:"appeal_number"`
	Type                string     `json:"type"`
	Status              string     `json:"status"`
	Priority            string     `json:"priority"`
	Subject             string     `json:"subject"`
	Description         string     `json:"description"`
	Justification       string     `json:"justification"`
	Evidence            string     `json:"evidence"`
	RequestedResolution string     `json:"requested_resolution"`
	SubmissionDate      time.Time  `json:"submission_date"`
	ReviewDate          *time.Time `json:"review_date,omitempty"`
	ResolutionDate      *time.Time `json:"resolution_date,omitempty"`
	ReviewerNotes       string     `json:"reviewer_notes"`
	FinalResolution     string     `json:"final_resolution"`
	CreatedAt           time.Time  `json:"created_at"`
	UpdatedAt           time.Time  `json:"updated_at"`
}

// Common DTOs
type PaginationRequest struct {
	Page     int    `json:"page" validate:"min=1"`
	PageSize int    `json:"page_size" validate:"min=1,max=100"`
	OrderBy  string `json:"order_by,omitempty"`
	Order    string `json:"order,omitempty" validate:"omitempty,oneof=asc desc"`
}

type PaginatedResponse struct {
	Data       interface{} `json:"data"`
	Page       int         `json:"page"`
	PageSize   int         `json:"page_size"`
	TotalItems int64       `json:"total_items"`
	TotalPages int         `json:"total_pages"`
}

type ErrorResponse struct {
	Error   string            `json:"error"`
	Message string            `json:"message"`
	Details map[string]string `json:"details,omitempty"`
}

type SuccessResponse struct {
	Message string      `json:"message"`
	Data    interface{} `json:"data,omitempty"`
}
