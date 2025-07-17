package repositories

import (
	"context"
	"time"

	"mevalservice/internal/domain/entities"

	"github.com/google/uuid"
)

// CommitteeRepository defines the interface for committee data operations
type CommitteeRepository interface {
	// Basic CRUD operations
	Create(ctx context.Context, committee *entities.Committee) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.Committee, error)
	Update(ctx context.Context, committee *entities.Committee) error
	Delete(ctx context.Context, id uuid.UUID) error

	// Query operations
	GetAll(ctx context.Context, limit, offset int) ([]*entities.Committee, error)
	GetByDateRange(ctx context.Context, startDate, endDate time.Time) ([]*entities.Committee, error)
	GetByType(ctx context.Context, committeeType entities.CommitteeType) ([]*entities.Committee, error)
	GetByStatus(ctx context.Context, status entities.CommitteeStatus) ([]*entities.Committee, error)
	GetByProgramID(ctx context.Context, programID uuid.UUID) ([]*entities.Committee, error)
	GetByAcademicPeriod(ctx context.Context, period string) ([]*entities.Committee, error)

	// Monthly committee operations
	GetMonthlyCommitteeForDate(ctx context.Context, date time.Time) (*entities.Committee, error)
	GetNextScheduledCommittee(ctx context.Context) (*entities.Committee, error)
	GetCurrentMonthCommittees(ctx context.Context) ([]*entities.Committee, error)

	// Committee with relationships
	GetWithMembers(ctx context.Context, id uuid.UUID) (*entities.Committee, error)
	GetWithCases(ctx context.Context, id uuid.UUID) (*entities.Committee, error)
	GetWithDecisions(ctx context.Context, id uuid.UUID) (*entities.Committee, error)
	GetWithAllRelations(ctx context.Context, id uuid.UUID) (*entities.Committee, error)

	// Committee statistics
	GetCommitteeCount(ctx context.Context) (int64, error)
	GetCommitteeCountByType(ctx context.Context, committeeType entities.CommitteeType) (int64, error)
	GetCommitteeCountByDateRange(ctx context.Context, startDate, endDate time.Time) (int64, error)
}

// StudentCaseRepository defines the interface for student case data operations
type StudentCaseRepository interface {
	// Basic CRUD operations
	Create(ctx context.Context, studentCase *entities.StudentCase) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.StudentCase, error)
	Update(ctx context.Context, studentCase *entities.StudentCase) error
	Delete(ctx context.Context, id uuid.UUID) error

	// Query operations
	GetAll(ctx context.Context, limit, offset int) ([]*entities.StudentCase, error)
	GetByStudentID(ctx context.Context, studentID uuid.UUID) ([]*entities.StudentCase, error)
	GetByCommitteeID(ctx context.Context, committeeID uuid.UUID) ([]*entities.StudentCase, error)
	GetByType(ctx context.Context, caseType entities.CaseType) ([]*entities.StudentCase, error)
	GetByStatus(ctx context.Context, status entities.CaseStatus) ([]*entities.StudentCase, error)

	// Automatic detection operations
	GetAutoDetectedCases(ctx context.Context) ([]*entities.StudentCase, error)
	GetManualCases(ctx context.Context) ([]*entities.StudentCase, error)
	GetPendingCases(ctx context.Context) ([]*entities.StudentCase, error)

	// Case type specific operations
	GetRecognitionCases(ctx context.Context) ([]*entities.StudentCase, error)
	GetSanctionCases(ctx context.Context) ([]*entities.StudentCase, error)
	GetAppealCases(ctx context.Context) ([]*entities.StudentCase, error)

	// Case statistics
	GetCaseCount(ctx context.Context) (int64, error)
	GetCaseCountByType(ctx context.Context, caseType entities.CaseType) (int64, error)
	GetCaseCountByStudent(ctx context.Context, studentID uuid.UUID) (int64, error)
}

// ImprovementPlanRepository defines the interface for improvement plan data operations
type ImprovementPlanRepository interface {
	// Basic CRUD operations
	Create(ctx context.Context, plan *entities.ImprovementPlan) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.ImprovementPlan, error)
	Update(ctx context.Context, plan *entities.ImprovementPlan) error
	Delete(ctx context.Context, id uuid.UUID) error

	// Query operations
	GetAll(ctx context.Context, limit, offset int) ([]*entities.ImprovementPlan, error)
	GetByStudentID(ctx context.Context, studentID uuid.UUID) ([]*entities.ImprovementPlan, error)
	GetByStatus(ctx context.Context, status entities.PlanStatus) ([]*entities.ImprovementPlan, error)
	GetByType(ctx context.Context, planType entities.PlanType) ([]*entities.ImprovementPlan, error)
	GetByInstructor(ctx context.Context, instructorID uuid.UUID) ([]*entities.ImprovementPlan, error)

	// Plan monitoring operations
	GetActivePlans(ctx context.Context) ([]*entities.ImprovementPlan, error)
	GetOverduePlans(ctx context.Context) ([]*entities.ImprovementPlan, error)
	GetPlansEndingSoon(ctx context.Context, days int) ([]*entities.ImprovementPlan, error)
	GetCompletedPlans(ctx context.Context) ([]*entities.ImprovementPlan, error)

	// Plan effectiveness operations
	GetPlansByComplianceRange(ctx context.Context, minCompliance, maxCompliance float64) ([]*entities.ImprovementPlan, error)
	GetSuccessfulPlans(ctx context.Context, minCompliance float64) ([]*entities.ImprovementPlan, error)
}

// SanctionRepository defines the interface for sanction data operations
type SanctionRepository interface {
	// Basic CRUD operations
	Create(ctx context.Context, sanction *entities.Sanction) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.Sanction, error)
	Update(ctx context.Context, sanction *entities.Sanction) error
	Delete(ctx context.Context, id uuid.UUID) error

	// Query operations
	GetAll(ctx context.Context, limit, offset int) ([]*entities.Sanction, error)
	GetByStudentID(ctx context.Context, studentID uuid.UUID) ([]*entities.Sanction, error)
	GetByType(ctx context.Context, sanctionType entities.SanctionType) ([]*entities.Sanction, error)
	GetBySeverityLevel(ctx context.Context, level int) ([]*entities.Sanction, error)
	GetByDateRange(ctx context.Context, startDate, endDate time.Time) ([]*entities.Sanction, error)

	// Sanction status operations
	GetActiveSanctions(ctx context.Context) ([]*entities.Sanction, error)
	GetExpiredSanctions(ctx context.Context) ([]*entities.Sanction, error)
	GetAppealableSanctions(ctx context.Context) ([]*entities.Sanction, error)
	GetAppealedSanctions(ctx context.Context) ([]*entities.Sanction, error)

	// Sanction statistics
	GetSanctionCountByType(ctx context.Context, sanctionType entities.SanctionType) (int64, error)
	GetSanctionCountByStudent(ctx context.Context, studentID uuid.UUID) (int64, error)
	GetReincidenceCount(ctx context.Context, studentID uuid.UUID) (int64, error)
}

// AppealRepository defines the interface for appeal data operations
type AppealRepository interface {
	// Basic CRUD operations
	Create(ctx context.Context, appeal *entities.Appeal) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.Appeal, error)
	Update(ctx context.Context, appeal *entities.Appeal) error
	Delete(ctx context.Context, id uuid.UUID) error

	// Query operations
	GetAll(ctx context.Context, limit, offset int) ([]*entities.Appeal, error)
	GetByStudentID(ctx context.Context, studentID uuid.UUID) ([]*entities.Appeal, error)
	GetBySanctionID(ctx context.Context, sanctionID uuid.UUID) ([]*entities.Appeal, error)
	GetByStatus(ctx context.Context, status entities.AdmissibilityStatus) ([]*entities.Appeal, error)

	// Appeal processing operations
	GetPendingAppeals(ctx context.Context) ([]*entities.Appeal, error)
	GetAdmittedAppeals(ctx context.Context) ([]*entities.Appeal, error)
	GetRejectedAppeals(ctx context.Context) ([]*entities.Appeal, error)
	GetAppealsWithFinalDecision(ctx context.Context) ([]*entities.Appeal, error)

	// Appeal deadlines
	GetAppealsNearDeadline(ctx context.Context, days int) ([]*entities.Appeal, error)
	GetOverdueAppeals(ctx context.Context) ([]*entities.Appeal, error)
}

// CommitteeDecisionRepository defines the interface for committee decision data operations
type CommitteeDecisionRepository interface {
	// Basic CRUD operations
	Create(ctx context.Context, decision *entities.CommitteeDecision) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.CommitteeDecision, error)
	Update(ctx context.Context, decision *entities.CommitteeDecision) error
	Delete(ctx context.Context, id uuid.UUID) error

	// Query operations
	GetAll(ctx context.Context, limit, offset int) ([]*entities.CommitteeDecision, error)
	GetByCommitteeID(ctx context.Context, committeeID uuid.UUID) ([]*entities.CommitteeDecision, error)
	GetByStudentCaseID(ctx context.Context, studentCaseID uuid.UUID) ([]*entities.CommitteeDecision, error)
	GetByType(ctx context.Context, decisionType entities.DecisionType) ([]*entities.CommitteeDecision, error)
	GetByDateRange(ctx context.Context, startDate, endDate time.Time) ([]*entities.CommitteeDecision, error)

	// Decision analysis operations
	GetUnanimousDecisions(ctx context.Context) ([]*entities.CommitteeDecision, error)
	GetApprovedDecisions(ctx context.Context) ([]*entities.CommitteeDecision, error)
	GetRejectedDecisions(ctx context.Context) ([]*entities.CommitteeDecision, error)

	// Decision statistics
	GetDecisionCountByType(ctx context.Context, decisionType entities.DecisionType) (int64, error)
	GetApprovalRate(ctx context.Context) (float64, error)
}

// CommitteeMemberRepository defines the interface for committee member data operations
type CommitteeMemberRepository interface {
	// Basic CRUD operations
	Create(ctx context.Context, member *entities.CommitteeMember) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.CommitteeMember, error)
	Update(ctx context.Context, member *entities.CommitteeMember) error
	Delete(ctx context.Context, id uuid.UUID) error

	// Query operations
	GetByCommitteeID(ctx context.Context, committeeID uuid.UUID) ([]*entities.CommitteeMember, error)
	GetByUserID(ctx context.Context, userID uuid.UUID) ([]*entities.CommitteeMember, error)
	GetByRole(ctx context.Context, role entities.MemberRole) ([]*entities.CommitteeMember, error)

	// Committee composition operations
	GetPresentMembers(ctx context.Context, committeeID uuid.UUID) ([]*entities.CommitteeMember, error)
	GetAbsentMembers(ctx context.Context, committeeID uuid.UUID) ([]*entities.CommitteeMember, error)
	GetVotingMembers(ctx context.Context, committeeID uuid.UUID) ([]*entities.CommitteeMember, error)

	// Member statistics
	GetMemberAttendanceRate(ctx context.Context, userID uuid.UUID) (float64, error)
	GetQuorumCount(ctx context.Context, committeeID uuid.UUID) (int, error)
}
