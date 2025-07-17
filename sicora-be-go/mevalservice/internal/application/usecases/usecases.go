package usecases

import (
	"context"
	"fmt"
	"time"

	"github.com/google/uuid"

	"mevalservice/internal/application/dto"
	"mevalservice/internal/domain/entities"
	"mevalservice/internal/domain/repositories"
)

// Error constants
const (
	ErrFailedToGetStudentCase      = "failed to get student case: %w"
	ErrStudentCaseNotFound         = "student case not found"
	ErrFailedToGetCommittee        = "failed to get committee: %w"
	ErrCommitteeNotFound           = "committee not found"
	ErrFailedToGetImprovementPlan  = "failed to get improvement plan: %w"
	ErrImprovementPlanNotFound     = "improvement plan not found"
	ErrFailedToGetImprovementPlans = "failed to get improvement plans: %w"
	ErrFailedToGetSanction         = "failed to get sanction: %w"
	ErrSanctionNotFound            = "sanction not found"
	ErrFailedToGetSanctions        = "failed to get sanctions: %w"
	ErrFailedToGetAppeal           = "failed to get appeal: %w"
	ErrAppealNotFound              = "appeal not found"
	ErrFailedToGetAppeals          = "failed to get appeals: %w"
)

type CommitteeUseCases interface {
	CreateCommittee(ctx context.Context, req *dto.CreateCommitteeRequest) (*dto.CommitteeResponse, error)
	GetCommitteeByID(ctx context.Context, id uuid.UUID) (*dto.CommitteeResponse, error)
	GetAllCommittees(ctx context.Context) ([]*dto.CommitteeResponse, error)
	GetCommitteesByCenter(ctx context.Context, center string) ([]*dto.CommitteeResponse, error)
	GetCommitteesByType(ctx context.Context, committeeType string) ([]*dto.CommitteeResponse, error)
	UpdateCommittee(ctx context.Context, id uuid.UUID, req *dto.UpdateCommitteeRequest) (*dto.CommitteeResponse, error)
	DeleteCommittee(ctx context.Context, id uuid.UUID) error
	GetAvailableCommitteesForAssignment(ctx context.Context, committeeType, center string) ([]*dto.CommitteeResponse, error)
}

type StudentCaseUseCases interface {
	CreateStudentCase(ctx context.Context, req *dto.CreateStudentCaseRequest) (*dto.StudentCaseResponse, error)
	GetStudentCaseByID(ctx context.Context, id uuid.UUID) (*dto.StudentCaseResponse, error)
	GetStudentCasesByCaseNumber(ctx context.Context, caseNumber string) (*dto.StudentCaseResponse, error)
	GetStudentCasesByStudentID(ctx context.Context, studentID uuid.UUID) ([]*dto.StudentCaseResponse, error)
	GetStudentCasesByCommitteeID(ctx context.Context, committeeID uuid.UUID) ([]*dto.StudentCaseResponse, error)
	GetStudentCasesByStatus(ctx context.Context, status string) ([]*dto.StudentCaseResponse, error)
	GetPendingStudentCases(ctx context.Context) ([]*dto.StudentCaseResponse, error)
	GetOverdueStudentCases(ctx context.Context) ([]*dto.StudentCaseResponse, error)
	UpdateStudentCase(ctx context.Context, id uuid.UUID, req *dto.UpdateStudentCaseRequest) (*dto.StudentCaseResponse, error)
	DeleteStudentCase(ctx context.Context, id uuid.UUID) error
	AssignCaseToCommittee(ctx context.Context, caseID, committeeID uuid.UUID) error
}

type ImprovementPlanUseCases interface {
	CreateImprovementPlan(ctx context.Context, req *dto.CreateImprovementPlanRequest) (*dto.ImprovementPlanResponse, error)
	GetImprovementPlanByID(ctx context.Context, id uuid.UUID) (*dto.ImprovementPlanResponse, error)
	GetImprovementPlansByStudentCaseID(ctx context.Context, studentCaseID uuid.UUID) ([]*dto.ImprovementPlanResponse, error)
	GetImprovementPlansByStudentID(ctx context.Context, studentID uuid.UUID) ([]*dto.ImprovementPlanResponse, error)
	GetImprovementPlansBySupervisorID(ctx context.Context, supervisorID uuid.UUID) ([]*dto.ImprovementPlanResponse, error)
	UpdateImprovementPlan(ctx context.Context, id uuid.UUID, req *dto.UpdateImprovementPlanRequest) (*dto.ImprovementPlanResponse, error)
	DeleteImprovementPlan(ctx context.Context, id uuid.UUID) error
	UpdateProgress(ctx context.Context, id uuid.UUID, progress int, notes string) error
}

type SanctionUseCases interface {
	CreateSanction(ctx context.Context, req *dto.CreateSanctionRequest) (*dto.SanctionResponse, error)
	GetSanctionByID(ctx context.Context, id uuid.UUID) (*dto.SanctionResponse, error)
	GetSanctionsByStudentCaseID(ctx context.Context, studentCaseID uuid.UUID) ([]*dto.SanctionResponse, error)
	GetSanctionsByStudentID(ctx context.Context, studentID uuid.UUID) ([]*dto.SanctionResponse, error)
	GetSanctionsByType(ctx context.Context, sanctionType string) ([]*dto.SanctionResponse, error)
	GetSanctionsByStatus(ctx context.Context, status string) ([]*dto.SanctionResponse, error)
	UpdateSanction(ctx context.Context, id uuid.UUID, req *dto.UpdateSanctionRequest) (*dto.SanctionResponse, error)
	DeleteSanction(ctx context.Context, id uuid.UUID) error
	ActivateSanction(ctx context.Context, id uuid.UUID) error
	CompleteSanction(ctx context.Context, id uuid.UUID) error
	RevokeSanction(ctx context.Context, id uuid.UUID, reason string) error
}

type AppealUseCases interface {
	CreateAppeal(ctx context.Context, req *dto.CreateAppealRequest) (*dto.AppealResponse, error)
	GetAppealByID(ctx context.Context, id uuid.UUID) (*dto.AppealResponse, error)
	GetAppealsByStudentCaseID(ctx context.Context, studentCaseID uuid.UUID) ([]*dto.AppealResponse, error)
	GetAppealsByStudentID(ctx context.Context, studentID uuid.UUID) ([]*dto.AppealResponse, error)
	GetAppealsByStatus(ctx context.Context, status string) ([]*dto.AppealResponse, error)
	UpdateAppeal(ctx context.Context, id uuid.UUID, req *dto.UpdateAppealRequest) (*dto.AppealResponse, error)
	DeleteAppeal(ctx context.Context, id uuid.UUID) error
	ProcessAppeal(ctx context.Context, id uuid.UUID, accepted bool, resolution string) error
}

// Implementation of Committee Use Cases
type committeeUseCases struct {
	committeeRepo repositories.CommitteeRepository
	memberRepo    repositories.CommitteeMemberRepository
}

func NewCommitteeUseCases(
	committeeRepo repositories.CommitteeRepository,
	memberRepo repositories.CommitteeMemberRepository,
) CommitteeUseCases {
	return &committeeUseCases{
		committeeRepo: committeeRepo,
		memberRepo:    memberRepo,
	}
}

func (uc *committeeUseCases) CreateCommittee(ctx context.Context, req *dto.CreateCommitteeRequest) (*dto.CommitteeResponse, error) {
	// Validate committee type
	if req.Type != "DISCIPLINARY" && req.Type != "ACADEMIC" {
		return nil, fmt.Errorf("invalid committee type: %s", req.Type)
	}

	// Create committee entity
	committee := &entities.Committee{
		ID:          uuid.New(),
		Name:        req.Name,
		Type:        entities.CommitteeType(req.Type),
		Status:      entities.CommitteeStatusActive,
		Center:      req.Center,
		Coordinator: req.Coordinator,
		MaxMembers:  req.MaxMembers,
		CreatedAt:   time.Now(),
		UpdatedAt:   time.Now(),
	}

	// Save to repository
	if err := uc.committeeRepo.Create(ctx, committee); err != nil {
		return nil, fmt.Errorf("failed to create committee: %w", err)
	}

	return uc.toCommitteeResponse(committee), nil
}

func (uc *committeeUseCases) GetCommitteeByID(ctx context.Context, id uuid.UUID) (*dto.CommitteeResponse, error) {
	committee, err := uc.committeeRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get committee: %w", err)
	}
	if committee == nil {
		return nil, fmt.Errorf("committee not found")
	}

	return uc.toCommitteeResponse(committee), nil
}

func (uc *committeeUseCases) GetAllCommittees(ctx context.Context) ([]*dto.CommitteeResponse, error) {
	committees, err := uc.committeeRepo.GetAll(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get committees: %w", err)
	}

	responses := make([]*dto.CommitteeResponse, len(committees))
	for i, committee := range committees {
		responses[i] = uc.toCommitteeResponse(committee)
	}

	return responses, nil
}

func (uc *committeeUseCases) GetCommitteesByCenter(ctx context.Context, center string) ([]*dto.CommitteeResponse, error) {
	committees, err := uc.committeeRepo.GetByCenter(ctx, center)
	if err != nil {
		return nil, fmt.Errorf("failed to get committees by center: %w", err)
	}

	responses := make([]*dto.CommitteeResponse, len(committees))
	for i, committee := range committees {
		responses[i] = uc.toCommitteeResponse(committee)
	}

	return responses, nil
}

func (uc *committeeUseCases) GetCommitteesByType(ctx context.Context, committeeType string) ([]*dto.CommitteeResponse, error) {
	committees, err := uc.committeeRepo.GetByType(ctx, committeeType)
	if err != nil {
		return nil, fmt.Errorf("failed to get committees by type: %w", err)
	}

	responses := make([]*dto.CommitteeResponse, len(committees))
	for i, committee := range committees {
		responses[i] = uc.toCommitteeResponse(committee)
	}

	return responses, nil
}

func (uc *committeeUseCases) UpdateCommittee(ctx context.Context, id uuid.UUID, req *dto.UpdateCommitteeRequest) (*dto.CommitteeResponse, error) {
	committee, err := uc.committeeRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get committee: %w", err)
	}
	if committee == nil {
		return nil, fmt.Errorf("committee not found")
	}

	// Update fields if provided
	if req.Name != "" {
		committee.Name = req.Name
	}
	if req.Status != "" {
		committee.Status = entities.CommitteeStatus(req.Status)
	}
	if req.Coordinator != "" {
		committee.Coordinator = req.Coordinator
	}
	if req.MaxMembers > 0 {
		committee.MaxMembers = req.MaxMembers
	}

	committee.UpdatedAt = time.Now()

	if err := uc.committeeRepo.Update(ctx, committee); err != nil {
		return nil, fmt.Errorf("failed to update committee: %w", err)
	}

	return uc.toCommitteeResponse(committee), nil
}

func (uc *committeeUseCases) DeleteCommittee(ctx context.Context, id uuid.UUID) error {
	committee, err := uc.committeeRepo.GetByID(ctx, id)
	if err != nil {
		return fmt.Errorf("failed to get committee: %w", err)
	}
	if committee == nil {
		return fmt.Errorf("committee not found")
	}

	return uc.committeeRepo.Delete(ctx, id)
}

func (uc *committeeUseCases) GetAvailableCommitteesForAssignment(ctx context.Context, committeeType, center string) ([]*dto.CommitteeResponse, error) {
	committees, err := uc.committeeRepo.GetAvailableForAssignment(ctx, committeeType, center)
	if err != nil {
		return nil, fmt.Errorf("failed to get available committees: %w", err)
	}

	responses := make([]*dto.CommitteeResponse, len(committees))
	for i, committee := range committees {
		responses[i] = uc.toCommitteeResponse(committee)
	}

	return responses, nil
}

// Helper methods
func (uc *committeeUseCases) toCommitteeResponse(committee *entities.Committee) *dto.CommitteeResponse {
	response := &dto.CommitteeResponse{
		ID:             committee.ID,
		Name:           committee.Name,
		Type:           string(committee.Type),
		Status:         string(committee.Status),
		Center:         committee.Center,
		Coordinator:    committee.Coordinator,
		MaxMembers:     committee.MaxMembers,
		CurrentMembers: committee.CurrentMembers,
		CreatedAt:      committee.CreatedAt,
		UpdatedAt:      committee.UpdatedAt,
	}

	// Convert members if present
	if len(committee.Members) > 0 {
		response.Members = make([]dto.CommitteeMemberResponse, len(committee.Members))
		for i, member := range committee.Members {
			response.Members[i] = dto.CommitteeMemberResponse{
				ID:              member.ID,
				CommitteeID:     member.CommitteeID,
				UserID:          member.UserID,
				Role:            string(member.Role),
				Status:          string(member.Status),
				AppointmentDate: member.AppointmentDate,
				EndDate:         member.EndDate,
				CreatedAt:       member.CreatedAt,
				UpdatedAt:       member.UpdatedAt,
			}
		}
	}

	return response
}

// Implementation of Student Case Use Cases
type studentCaseUseCases struct {
	studentCaseRepo repositories.StudentCaseRepository
	committeeRepo   repositories.CommitteeRepository
}

func NewStudentCaseUseCases(
	studentCaseRepo repositories.StudentCaseRepository,
	committeeRepo repositories.CommitteeRepository,
) StudentCaseUseCases {
	return &studentCaseUseCases{
		studentCaseRepo: studentCaseRepo,
		committeeRepo:   committeeRepo,
	}
}

func (uc *studentCaseUseCases) CreateStudentCase(ctx context.Context, req *dto.CreateStudentCaseRequest) (*dto.StudentCaseResponse, error) {
	// Validate committee exists
	committee, err := uc.committeeRepo.GetByID(ctx, req.CommitteeID)
	if err != nil {
		return nil, fmt.Errorf("failed to get committee: %w", err)
	}
	if committee == nil {
		return nil, fmt.Errorf("committee not found")
	}

	// Generate case number
	caseNumber, err := uc.studentCaseRepo.GenerateCaseNumber(ctx, req.Type)
	if err != nil {
		return nil, fmt.Errorf("failed to generate case number: %w", err)
	}

	// Set priority if not provided
	priority := req.Priority
	if priority == "" {
		priority = "MEDIUM"
	}

	// Create student case entity
	studentCase := &entities.StudentCase{
		ID:          uuid.New(),
		StudentID:   req.StudentID,
		CommitteeID: req.CommitteeID,
		CaseNumber:  caseNumber,
		Type:        entities.CaseType(req.Type),
		Severity:    entities.CaseSeverity(req.Severity),
		Status:      entities.CaseStatusPending,
		Priority:    entities.CasePriority(priority),
		Title:       req.Title,
		Description: req.Description,
		Evidence:    req.Evidence,
		ReportedBy:  req.ReportedBy,
		ReportDate:  time.Now(),
		DueDate:     req.DueDate,
		CreatedAt:   time.Now(),
		UpdatedAt:   time.Now(),
	}

	// Save to repository
	if err := uc.studentCaseRepo.Create(ctx, studentCase); err != nil {
		return nil, fmt.Errorf("failed to create student case: %w", err)
	}

	return uc.toStudentCaseResponse(studentCase), nil
}

func (uc *studentCaseUseCases) GetStudentCaseByID(ctx context.Context, id uuid.UUID) (*dto.StudentCaseResponse, error) {
	studentCase, err := uc.studentCaseRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get student case: %w", err)
	}
	if studentCase == nil {
		return nil, fmt.Errorf("student case not found")
	}

	return uc.toStudentCaseResponse(studentCase), nil
}

func (uc *studentCaseUseCases) GetStudentCasesByCaseNumber(ctx context.Context, caseNumber string) (*dto.StudentCaseResponse, error) {
	studentCase, err := uc.studentCaseRepo.GetByCaseNumber(ctx, caseNumber)
	if err != nil {
		return nil, fmt.Errorf("failed to get student case: %w", err)
	}
	if studentCase == nil {
		return nil, fmt.Errorf("student case not found")
	}

	return uc.toStudentCaseResponse(studentCase), nil
}

func (uc *studentCaseUseCases) GetStudentCasesByStudentID(ctx context.Context, studentID uuid.UUID) ([]*dto.StudentCaseResponse, error) {
	cases, err := uc.studentCaseRepo.GetByStudentID(ctx, studentID)
	if err != nil {
		return nil, fmt.Errorf("failed to get student cases: %w", err)
	}

	responses := make([]*dto.StudentCaseResponse, len(cases))
	for i, studentCase := range cases {
		responses[i] = uc.toStudentCaseResponse(studentCase)
	}

	return responses, nil
}

func (uc *studentCaseUseCases) GetStudentCasesByCommitteeID(ctx context.Context, committeeID uuid.UUID) ([]*dto.StudentCaseResponse, error) {
	cases, err := uc.studentCaseRepo.GetByCommitteeID(ctx, committeeID)
	if err != nil {
		return nil, fmt.Errorf("failed to get student cases: %w", err)
	}

	responses := make([]*dto.StudentCaseResponse, len(cases))
	for i, studentCase := range cases {
		responses[i] = uc.toStudentCaseResponse(studentCase)
	}

	return responses, nil
}

func (uc *studentCaseUseCases) GetStudentCasesByStatus(ctx context.Context, status string) ([]*dto.StudentCaseResponse, error) {
	cases, err := uc.studentCaseRepo.GetByStatus(ctx, status)
	if err != nil {
		return nil, fmt.Errorf("failed to get student cases: %w", err)
	}

	responses := make([]*dto.StudentCaseResponse, len(cases))
	for i, studentCase := range cases {
		responses[i] = uc.toStudentCaseResponse(studentCase)
	}

	return responses, nil
}

func (uc *studentCaseUseCases) GetPendingStudentCases(ctx context.Context) ([]*dto.StudentCaseResponse, error) {
	cases, err := uc.studentCaseRepo.GetPendingCases(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get pending cases: %w", err)
	}

	responses := make([]*dto.StudentCaseResponse, len(cases))
	for i, studentCase := range cases {
		responses[i] = uc.toStudentCaseResponse(studentCase)
	}

	return responses, nil
}

func (uc *studentCaseUseCases) GetOverdueStudentCases(ctx context.Context) ([]*dto.StudentCaseResponse, error) {
	cases, err := uc.studentCaseRepo.GetOverdueCases(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get overdue cases: %w", err)
	}

	responses := make([]*dto.StudentCaseResponse, len(cases))
	for i, studentCase := range cases {
		responses[i] = uc.toStudentCaseResponse(studentCase)
	}

	return responses, nil
}

func (uc *studentCaseUseCases) UpdateStudentCase(ctx context.Context, id uuid.UUID, req *dto.UpdateStudentCaseRequest) (*dto.StudentCaseResponse, error) {
	studentCase, err := uc.studentCaseRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get student case: %w", err)
	}
	if studentCase == nil {
		return nil, fmt.Errorf("student case not found")
	}

	// Update fields if provided
	if req.Status != "" {
		studentCase.Status = entities.CaseStatus(req.Status)
	}
	if req.Priority != "" {
		studentCase.Priority = entities.CasePriority(req.Priority)
	}
	if req.Description != "" {
		studentCase.Description = req.Description
	}
	if req.Evidence != "" {
		studentCase.Evidence = req.Evidence
	}
	if req.DueDate != nil {
		studentCase.DueDate = req.DueDate
	}
	if req.ResolutionDate != nil {
		studentCase.ResolutionDate = req.ResolutionDate
	}

	studentCase.UpdatedAt = time.Now()

	if err := uc.studentCaseRepo.Update(ctx, studentCase); err != nil {
		return nil, fmt.Errorf("failed to update student case: %w", err)
	}

	return uc.toStudentCaseResponse(studentCase), nil
}

func (uc *studentCaseUseCases) DeleteStudentCase(ctx context.Context, id uuid.UUID) error {
	studentCase, err := uc.studentCaseRepo.GetByID(ctx, id)
	if err != nil {
		return fmt.Errorf("failed to get student case: %w", err)
	}
	if studentCase == nil {
		return fmt.Errorf("student case not found")
	}

	return uc.studentCaseRepo.Delete(ctx, id)
}

func (uc *studentCaseUseCases) AssignCaseToCommittee(ctx context.Context, caseID, committeeID uuid.UUID) error {
	// Get student case
	studentCase, err := uc.studentCaseRepo.GetByID(ctx, caseID)
	if err != nil {
		return fmt.Errorf("failed to get student case: %w", err)
	}
	if studentCase == nil {
		return fmt.Errorf("student case not found")
	}

	// Validate committee exists
	committee, err := uc.committeeRepo.GetByID(ctx, committeeID)
	if err != nil {
		return fmt.Errorf("failed to get committee: %w", err)
	}
	if committee == nil {
		return fmt.Errorf("committee not found")
	}

	// Update case with new committee
	studentCase.CommitteeID = committeeID
	studentCase.UpdatedAt = time.Now()

	return uc.studentCaseRepo.Update(ctx, studentCase)
}

// Helper methods
func (uc *studentCaseUseCases) toStudentCaseResponse(studentCase *entities.StudentCase) *dto.StudentCaseResponse {
	return &dto.StudentCaseResponse{
		ID:             studentCase.ID,
		StudentID:      studentCase.StudentID,
		CommitteeID:    studentCase.CommitteeID,
		CaseNumber:     studentCase.CaseNumber,
		Type:           string(studentCase.Type),
		Severity:       string(studentCase.Severity),
		Status:         string(studentCase.Status),
		Priority:       string(studentCase.Priority),
		Title:          studentCase.Title,
		Description:    studentCase.Description,
		Evidence:       studentCase.Evidence,
		ReportedBy:     studentCase.ReportedBy,
		ReportDate:     studentCase.ReportDate,
		DueDate:        studentCase.DueDate,
		ResolutionDate: studentCase.ResolutionDate,
		CreatedAt:      studentCase.CreatedAt,
		UpdatedAt:      studentCase.UpdatedAt,
	}
}

// Implementation of ImprovementPlan Use Cases
type improvementPlanUseCases struct {
	improvementPlanRepo repositories.ImprovementPlanRepository
	studentCaseRepo     repositories.StudentCaseRepository
}

func NewImprovementPlanUseCases(
	improvementPlanRepo repositories.ImprovementPlanRepository,
	studentCaseRepo repositories.StudentCaseRepository,
) ImprovementPlanUseCases {
	return &improvementPlanUseCases{
		improvementPlanRepo: improvementPlanRepo,
		studentCaseRepo:     studentCaseRepo,
	}
}

func (uc *improvementPlanUseCases) CreateImprovementPlan(ctx context.Context, req *dto.CreateImprovementPlanRequest) (*dto.ImprovementPlanResponse, error) {
	// Validate student case exists
	studentCase, err := uc.studentCaseRepo.GetByID(ctx, req.StudentCaseID)
	if err != nil {
		return nil, fmt.Errorf("failed to get student case: %w", err)
	}
	if studentCase == nil {
		return nil, fmt.Errorf("student case not found")
	}

	plan := &entities.ImprovementPlan{
		ID:                 uuid.New(),
		StudentCaseID:      req.StudentCaseID,
		StudentID:          req.StudentID,
		SupervisorID:       req.SupervisorID,
		PlanNumber:         req.PlanNumber,
		Title:              req.Title,
		Description:        req.Description,
		Objectives:         req.Objectives,
		Activities:         req.Activities,
		Resources:          req.Resources,
		Timeline:           req.Timeline,
		EvaluationCriteria: req.EvaluationCriteria,
		StartDate:          req.StartDate,
		EndDate:            req.EndDate,
		Status:             entities.PlanStatusActive,
		Progress:           0,
		CreatedAt:          time.Now(),
		UpdatedAt:          time.Now(),
	}

	if err := uc.improvementPlanRepo.Create(ctx, plan); err != nil {
		return nil, fmt.Errorf("failed to create improvement plan: %w", err)
	}

	return uc.toImprovementPlanResponse(plan), nil
}

func (uc *improvementPlanUseCases) GetImprovementPlanByID(ctx context.Context, id uuid.UUID) (*dto.ImprovementPlanResponse, error) {
	plan, err := uc.improvementPlanRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get improvement plan: %w", err)
	}
	if plan == nil {
		return nil, fmt.Errorf("improvement plan not found")
	}

	return uc.toImprovementPlanResponse(plan), nil
}

func (uc *improvementPlanUseCases) GetImprovementPlansByStudentCaseID(ctx context.Context, studentCaseID uuid.UUID) ([]*dto.ImprovementPlanResponse, error) {
	plans, err := uc.improvementPlanRepo.GetByStudentCaseID(ctx, studentCaseID)
	if err != nil {
		return nil, fmt.Errorf("failed to get improvement plans: %w", err)
	}

	responses := make([]*dto.ImprovementPlanResponse, len(plans))
	for i, plan := range plans {
		responses[i] = uc.toImprovementPlanResponse(plan)
	}

	return responses, nil
}

func (uc *improvementPlanUseCases) GetImprovementPlansByStudentID(ctx context.Context, studentID uuid.UUID) ([]*dto.ImprovementPlanResponse, error) {
	plans, err := uc.improvementPlanRepo.GetByStudentID(ctx, studentID)
	if err != nil {
		return nil, fmt.Errorf("failed to get improvement plans: %w", err)
	}

	responses := make([]*dto.ImprovementPlanResponse, len(plans))
	for i, plan := range plans {
		responses[i] = uc.toImprovementPlanResponse(plan)
	}

	return responses, nil
}

func (uc *improvementPlanUseCases) GetImprovementPlansBySupervisorID(ctx context.Context, supervisorID uuid.UUID) ([]*dto.ImprovementPlanResponse, error) {
	plans, err := uc.improvementPlanRepo.GetBySupervisorID(ctx, supervisorID)
	if err != nil {
		return nil, fmt.Errorf("failed to get improvement plans: %w", err)
	}

	responses := make([]*dto.ImprovementPlanResponse, len(plans))
	for i, plan := range plans {
		responses[i] = uc.toImprovementPlanResponse(plan)
	}

	return responses, nil
}

func (uc *improvementPlanUseCases) UpdateImprovementPlan(ctx context.Context, id uuid.UUID, req *dto.UpdateImprovementPlanRequest) (*dto.ImprovementPlanResponse, error) {
	plan, err := uc.improvementPlanRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get improvement plan: %w", err)
	}
	if plan == nil {
		return nil, fmt.Errorf("improvement plan not found")
	}

	// Update fields if provided
	if req.Title != "" {
		plan.Title = req.Title
	}
	if req.Description != "" {
		plan.Description = req.Description
	}
	if req.Objectives != "" {
		plan.Objectives = req.Objectives
	}
	if req.Activities != "" {
		plan.Activities = req.Activities
	}
	if req.Resources != "" {
		plan.Resources = req.Resources
	}
	if req.Timeline != "" {
		plan.Timeline = req.Timeline
	}
	if req.EvaluationCriteria != "" {
		plan.EvaluationCriteria = req.EvaluationCriteria
	}
	if req.StartDate != nil {
		plan.StartDate = *req.StartDate
	}
	if req.EndDate != nil {
		plan.EndDate = *req.EndDate
	}
	if req.Status != "" {
		plan.Status = entities.PlanStatus(req.Status)
	}

	plan.UpdatedAt = time.Now()

	if err := uc.improvementPlanRepo.Update(ctx, plan); err != nil {
		return nil, fmt.Errorf("failed to update improvement plan: %w", err)
	}

	return uc.toImprovementPlanResponse(plan), nil
}

func (uc *improvementPlanUseCases) DeleteImprovementPlan(ctx context.Context, id uuid.UUID) error {
	plan, err := uc.improvementPlanRepo.GetByID(ctx, id)
	if err != nil {
		return fmt.Errorf("failed to get improvement plan: %w", err)
	}
	if plan == nil {
		return fmt.Errorf("improvement plan not found")
	}

	return uc.improvementPlanRepo.Delete(ctx, id)
}

func (uc *improvementPlanUseCases) UpdateProgress(ctx context.Context, id uuid.UUID, progress int, notes string) error {
	plan, err := uc.improvementPlanRepo.GetByID(ctx, id)
	if err != nil {
		return fmt.Errorf("failed to get improvement plan: %w", err)
	}
	if plan == nil {
		return fmt.Errorf("improvement plan not found")
	}

	if progress < 0 || progress > 100 {
		return fmt.Errorf("progress must be between 0 and 100")
	}

	plan.Progress = progress
	plan.ProgressNotes = notes
	plan.UpdatedAt = time.Now()

	// Update status based on progress
	if progress == 100 {
		plan.Status = entities.PlanStatusCompleted
	} else if progress > 0 {
		plan.Status = entities.PlanStatusInProgress
	}

	return uc.improvementPlanRepo.Update(ctx, plan)
}

func (uc *improvementPlanUseCases) toImprovementPlanResponse(plan *entities.ImprovementPlan) *dto.ImprovementPlanResponse {
	return &dto.ImprovementPlanResponse{
		ID:                 plan.ID,
		StudentCaseID:      plan.StudentCaseID,
		StudentID:          plan.StudentID,
		SupervisorID:       plan.SupervisorID,
		PlanNumber:         plan.PlanNumber,
		Title:              plan.Title,
		Description:        plan.Description,
		Objectives:         plan.Objectives,
		Activities:         plan.Activities,
		Resources:          plan.Resources,
		Timeline:           plan.Timeline,
		EvaluationCriteria: plan.EvaluationCriteria,
		StartDate:          plan.StartDate,
		EndDate:            plan.EndDate,
		Status:             string(plan.Status),
		Progress:           plan.Progress,
		ProgressNotes:      plan.ProgressNotes,
		SupervisorNotes:    plan.SupervisorNotes,
		CreatedAt:          plan.CreatedAt,
		UpdatedAt:          plan.UpdatedAt,
	}
}

// Implementation of Sanction Use Cases
type sanctionUseCases struct {
	sanctionRepo    repositories.SanctionRepository
	studentCaseRepo repositories.StudentCaseRepository
}

func NewSanctionUseCases(
	sanctionRepo repositories.SanctionRepository,
	studentCaseRepo repositories.StudentCaseRepository,
) SanctionUseCases {
	return &sanctionUseCases{
		sanctionRepo:    sanctionRepo,
		studentCaseRepo: studentCaseRepo,
	}
}

func (uc *sanctionUseCases) CreateSanction(ctx context.Context, req *dto.CreateSanctionRequest) (*dto.SanctionResponse, error) {
	// Validate student case exists
	studentCase, err := uc.studentCaseRepo.GetByID(ctx, req.StudentCaseID)
	if err != nil {
		return nil, fmt.Errorf("failed to get student case: %w", err)
	}
	if studentCase == nil {
		return nil, fmt.Errorf("student case not found")
	}

	sanction := &entities.Sanction{
		ID:               uuid.New(),
		StudentCaseID:    req.StudentCaseID,
		StudentID:        req.StudentID,
		SanctionNumber:   req.SanctionNumber,
		Type:             entities.SanctionType(req.Type),
		Severity:         entities.SeverityLevel(req.Severity),
		Status:           entities.SanctionStatusActive,
		Title:            req.Title,
		Description:      req.Description,
		StartDate:        req.StartDate,
		EndDate:          req.EndDate,
		Conditions:       req.Conditions,
		RequiredActions:  req.RequiredActions,
		ComplianceNotes:  "",
		IssuedBy:         req.IssuedBy,
		ApprovedBy:       req.ApprovedBy,
		CreatedAt:        time.Now(),
		UpdatedAt:        time.Now(),
	}

	if err := uc.sanctionRepo.Create(ctx, sanction); err != nil {
		return nil, fmt.Errorf("failed to create sanction: %w", err)
	}

	return uc.toSanctionResponse(sanction), nil
}

func (uc *sanctionUseCases) GetSanctionByID(ctx context.Context, id uuid.UUID) (*dto.SanctionResponse, error) {
	sanction, err := uc.sanctionRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get sanction: %w", err)
	}
	if sanction == nil {
		return nil, fmt.Errorf("sanction not found")
	}

	return uc.toSanctionResponse(sanction), nil
}

func (uc *sanctionUseCases) GetSanctionsByStudentCaseID(ctx context.Context, studentCaseID uuid.UUID) ([]*dto.SanctionResponse, error) {
	sanctions, err := uc.sanctionRepo.GetByStudentCaseID(ctx, studentCaseID)
	if err != nil {
		return nil, fmt.Errorf("failed to get sanctions: %w", err)
	}

	responses := make([]*dto.SanctionResponse, len(sanctions))
	for i, sanction := range sanctions {
		responses[i] = uc.toSanctionResponse(sanction)
	}

	return responses, nil
}

func (uc *sanctionUseCases) GetSanctionsByStudentID(ctx context.Context, studentID uuid.UUID) ([]*dto.SanctionResponse, error) {
	sanctions, err := uc.sanctionRepo.GetByStudentID(ctx, studentID)
	if err != nil {
		return nil, fmt.Errorf("failed to get sanctions: %w", err)
	}

	responses := make([]*dto.SanctionResponse, len(sanctions))
	for i, sanction := range sanctions {
		responses[i] = uc.toSanctionResponse(sanction)
	}

	return responses, nil
}

func (uc *sanctionUseCases) GetSanctionsByType(ctx context.Context, sanctionType string) ([]*dto.SanctionResponse, error) {
	sanctions, err := uc.sanctionRepo.GetByType(ctx, sanctionType)
	if err != nil {
		return nil, fmt.Errorf("failed to get sanctions: %w", err)
	}

	responses := make([]*dto.SanctionResponse, len(sanctions))
	for i, sanction := range sanctions {
		responses[i] = uc.toSanctionResponse(sanction)
	}

	return responses, nil
}

func (uc *sanctionUseCases) GetSanctionsByStatus(ctx context.Context, status string) ([]*dto.SanctionResponse, error) {
	sanctions, err := uc.sanctionRepo.GetByStatus(ctx, status)
	if err != nil {
		return nil, fmt.Errorf("failed to get sanctions: %w", err)
	}

	responses := make([]*dto.SanctionResponse, len(sanctions))
	for i, sanction := range sanctions {
		responses[i] = uc.toSanctionResponse(sanction)
	}

	return responses, nil
}

func (uc *sanctionUseCases) UpdateSanction(ctx context.Context, id uuid.UUID, req *dto.UpdateSanctionRequest) (*dto.SanctionResponse, error) {
	sanction, err := uc.sanctionRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get sanction: %w", err)
	}
	if sanction == nil {
		return nil, fmt.Errorf("sanction not found")
	}

	// Update fields if provided
	if req.Title != "" {
		sanction.Title = req.Title
	}
	if req.Description != "" {
		sanction.Description = req.Description
	}
	if req.StartDate != nil {
		sanction.StartDate = *req.StartDate
	}
	if req.EndDate != nil {
		sanction.EndDate = *req.EndDate
	}
	if req.Conditions != "" {
		sanction.Conditions = req.Conditions
	}
	if req.RequiredActions != "" {
		sanction.RequiredActions = req.RequiredActions
	}
	if req.ComplianceNotes != "" {
		sanction.ComplianceNotes = req.ComplianceNotes
	}
	if req.Status != "" {
		sanction.Status = entities.SanctionStatus(req.Status)
	}

	sanction.UpdatedAt = time.Now()

	if err := uc.sanctionRepo.Update(ctx, sanction); err != nil {
		return nil, fmt.Errorf("failed to update sanction: %w", err)
	}

	return uc.toSanctionResponse(sanction), nil
}

func (uc *sanctionUseCases) DeleteSanction(ctx context.Context, id uuid.UUID) error {
	sanction, err := uc.sanctionRepo.GetByID(ctx, id)
	if err != nil {
		return fmt.Errorf("failed to get sanction: %w", err)
	}
	if sanction == nil {
		return fmt.Errorf("sanction not found")
	}

	return uc.sanctionRepo.Delete(ctx, id)
}

func (uc *sanctionUseCases) ActivateSanction(ctx context.Context, id uuid.UUID) error {
	sanction, err := uc.sanctionRepo.GetByID(ctx, id)
	if err != nil {
		return fmt.Errorf("failed to get sanction: %w", err)
	}
	if sanction == nil {
		return fmt.Errorf("sanction not found")
	}

	sanction.Status = entities.SanctionStatusActive
	sanction.UpdatedAt = time.Now()

	return uc.sanctionRepo.Update(ctx, sanction)
}

func (uc *sanctionUseCases) CompleteSanction(ctx context.Context, id uuid.UUID) error {
	sanction, err := uc.sanctionRepo.GetByID(ctx, id)
	if err != nil {
		return fmt.Errorf("failed to get sanction: %w", err)
	}
	if sanction == nil {
		return fmt.Errorf("sanction not found")
	}

	sanction.Status = entities.SanctionStatusCompleted
	sanction.UpdatedAt = time.Now()

	return uc.sanctionRepo.Update(ctx, sanction)
}

func (uc *sanctionUseCases) RevokeSanction(ctx context.Context, id uuid.UUID, reason string) error {
	sanction, err := uc.sanctionRepo.GetByID(ctx, id)
	if err != nil {
		return fmt.Errorf("failed to get sanction: %w", err)
	}
	if sanction == nil {
		return fmt.Errorf("sanction not found")
	}

	sanction.Status = entities.SanctionStatusRevoked
	sanction.ComplianceNotes = fmt.Sprintf("Revoked: %s", reason)
	sanction.UpdatedAt = time.Now()

	return uc.sanctionRepo.Update(ctx, sanction)
}

func (uc *sanctionUseCases) toSanctionResponse(sanction *entities.Sanction) *dto.SanctionResponse {
	return &dto.SanctionResponse{
		ID:              sanction.ID,
		StudentCaseID:   sanction.StudentCaseID,
		StudentID:       sanction.StudentID,
		SanctionNumber:  sanction.SanctionNumber,
		Type:            string(sanction.Type),
		Severity:        string(sanction.Severity),
		Status:          string(sanction.Status),
		Title:           sanction.Title,
		Description:     sanction.Description,
		StartDate:       sanction.StartDate,
		EndDate:         sanction.EndDate,
		Conditions:      sanction.Conditions,
		RequiredActions: sanction.RequiredActions,
		ComplianceNotes: sanction.ComplianceNotes,
		IssuedBy:        sanction.IssuedBy,
		ApprovedBy:      sanction.ApprovedBy,
		CreatedAt:       sanction.CreatedAt,
		UpdatedAt:       sanction.UpdatedAt,
	}
}

// Implementation of Appeal Use Cases
type appealUseCases struct {
	appealRepo      repositories.AppealRepository
	studentCaseRepo repositories.StudentCaseRepository
}

func NewAppealUseCases(
	appealRepo repositories.AppealRepository,
	studentCaseRepo repositories.StudentCaseRepository,
) AppealUseCases {
	return &appealUseCases{
		appealRepo:      appealRepo,
		studentCaseRepo: studentCaseRepo,
	}
}

func (uc *appealUseCases) CreateAppeal(ctx context.Context, req *dto.CreateAppealRequest) (*dto.AppealResponse, error) {
	// Validate student case exists
	studentCase, err := uc.studentCaseRepo.GetByID(ctx, req.StudentCaseID)
	if err != nil {
		return nil, fmt.Errorf("failed to get student case: %w", err)
	}
	if studentCase == nil {
		return nil, fmt.Errorf("student case not found")
	}

	appeal := &entities.Appeal{
		ID:            uuid.New(),
		StudentCaseID: req.StudentCaseID,
		StudentID:     req.StudentID,
		AppealNumber:  req.AppealNumber,
		Type:          entities.AppealType(req.Type),
		Status:        entities.AppealStatusSubmitted,
		Reason:        req.Reason,
		Evidence:      req.Evidence,
		RequestedBy:   req.RequestedBy,
		RequestDate:   req.RequestDate,
		Priority:      entities.CasePriority(req.Priority),
		CreatedAt:     time.Now(),
		UpdatedAt:     time.Now(),
	}

	if err := uc.appealRepo.Create(ctx, appeal); err != nil {
		return nil, fmt.Errorf("failed to create appeal: %w", err)
	}

	return uc.toAppealResponse(appeal), nil
}

func (uc *appealUseCases) GetAppealByID(ctx context.Context, id uuid.UUID) (*dto.AppealResponse, error) {
	appeal, err := uc.appealRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get appeal: %w", err)
	}
	if appeal == nil {
		return nil, fmt.Errorf("appeal not found")
	}

	return uc.toAppealResponse(appeal), nil
}

func (uc *appealUseCases) GetAppealsByStudentCaseID(ctx context.Context, studentCaseID uuid.UUID) ([]*dto.AppealResponse, error) {
	appeals, err := uc.appealRepo.GetByStudentCaseID(ctx, studentCaseID)
	if err != nil {
		return nil, fmt.Errorf("failed to get appeals: %w", err)
	}

	responses := make([]*dto.AppealResponse, len(appeals))
	for i, appeal := range appeals {
		responses[i] = uc.toAppealResponse(appeal)
	}

	return responses, nil
}

func (uc *appealUseCases) GetAppealsByStudentID(ctx context.Context, studentID uuid.UUID) ([]*dto.AppealResponse, error) {
	appeals, err := uc.appealRepo.GetByStudentID(ctx, studentID)
	if err != nil {
		return nil, fmt.Errorf("failed to get appeals: %w", err)
	}

	responses := make([]*dto.AppealResponse, len(appeals))
	for i, appeal := range appeals {
		responses[i] = uc.toAppealResponse(appeal)
	}

	return responses, nil
}

func (uc *appealUseCases) GetAppealsByStatus(ctx context.Context, status string) ([]*dto.AppealResponse, error) {
	appeals, err := uc.appealRepo.GetByStatus(ctx, status)
	if err != nil {
		return nil, fmt.Errorf("failed to get appeals: %w", err)
	}

	responses := make([]*dto.AppealResponse, len(appeals))
	for i, appeal := range appeals {
		responses[i] = uc.toAppealResponse(appeal)
	}

	return responses, nil
}

func (uc *appealUseCases) UpdateAppeal(ctx context.Context, id uuid.UUID, req *dto.UpdateAppealRequest) (*dto.AppealResponse, error) {
	appeal, err := uc.appealRepo.GetByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get appeal: %w", err)
	}
	if appeal == nil {
		return nil, fmt.Errorf("appeal not found")
	}

	// Update fields if provided
	if req.Reason != "" {
		appeal.Reason = req.Reason
	}
	if req.Evidence != "" {
		appeal.Evidence = req.Evidence
	}
	if req.Status != "" {
		appeal.Status = entities.AppealStatus(req.Status)
	}
	if req.Priority != "" {
		appeal.Priority = entities.CasePriority(req.Priority)
	}
	if req.ReviewDate != nil {
		appeal.ReviewDate = req.ReviewDate
	}
	if req.Resolution != "" {
		appeal.Resolution = req.Resolution
	}
	if req.ReviewedBy != nil {
		appeal.ReviewedBy = req.ReviewedBy
	}

	appeal.UpdatedAt = time.Now()

	if err := uc.appealRepo.Update(ctx, appeal); err != nil {
		return nil, fmt.Errorf("failed to update appeal: %w", err)
	}

	return uc.toAppealResponse(appeal), nil
}

func (uc *appealUseCases) DeleteAppeal(ctx context.Context, id uuid.UUID) error {
	appeal, err := uc.appealRepo.GetByID(ctx, id)
	if err != nil {
		return fmt.Errorf("failed to get appeal: %w", err)
	}
	if appeal == nil {
		return fmt.Errorf("appeal not found")
	}

	return uc.appealRepo.Delete(ctx, id)
}

func (uc *appealUseCases) ProcessAppeal(ctx context.Context, id uuid.UUID, accepted bool, resolution string) error {
	appeal, err := uc.appealRepo.GetByID(ctx, id)
	if err != nil {
		return fmt.Errorf("failed to get appeal: %w", err)
	}
	if appeal == nil {
		return fmt.Errorf("appeal not found")
	}

	if accepted {
		appeal.Status = entities.AppealStatusAccepted
	} else {
		appeal.Status = entities.AppealStatusRejected
	}

	appeal.Resolution = resolution
	now := time.Now()
	appeal.ReviewDate = &now
	appeal.UpdatedAt = now

	return uc.appealRepo.Update(ctx, appeal)
}

func (uc *appealUseCases) toAppealResponse(appeal *entities.Appeal) *dto.AppealResponse {
	return &dto.AppealResponse{
		ID:            appeal.ID,
		StudentCaseID: appeal.StudentCaseID,
		StudentID:     appeal.StudentID,
		AppealNumber:  appeal.AppealNumber,
		Type:          string(appeal.Type),
		Status:        string(appeal.Status),
		Reason:        appeal.Reason,
		Evidence:      appeal.Evidence,
		RequestedBy:   appeal.RequestedBy,
		RequestDate:   appeal.RequestDate,
		ReviewDate:    appeal.ReviewDate,
		Resolution:    appeal.Resolution,
		ReviewedBy:    appeal.ReviewedBy,
		Priority:      string(appeal.Priority),
		CreatedAt:     appeal.CreatedAt,
		UpdatedAt:     appeal.UpdatedAt,
	}
}