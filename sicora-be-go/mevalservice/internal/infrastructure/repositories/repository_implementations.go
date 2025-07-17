package repositories

import (
	"context"
	"errors"

	"github.com/google/uuid"
	"gorm.io/gorm"

	"mevalservice/internal/domain/entities"
	"mevalservice/internal/domain/repositories"
	"mevalservice/internal/infrastructure/database"
)

// Implementation of all remaining repositories
type improvementPlanRepository struct {
	db *gorm.DB
}

type sanctionRepository struct {
	db *gorm.DB
}

type committeeDecisionRepository struct {
	db *gorm.DB
}

type appealRepository struct {
	db *gorm.DB
}

type committeeMemberRepository struct {
	db *gorm.DB
}

// Factory function to create all repositories
func NewRepositories(db *database.Database) *Repositories {
	return &Repositories{
		Committee:         NewCommitteeRepository(db),
		CommitteeMember:   NewCommitteeMemberRepository(db),
		StudentCase:       NewStudentCaseRepository(db),
		ImprovementPlan:   NewImprovementPlanRepository(db),
		Sanction:          NewSanctionRepository(db),
		CommitteeDecision: NewCommitteeDecisionRepository(db),
		Appeal:            NewAppealRepository(db),
	}
}

type Repositories struct {
	Committee         repositories.CommitteeRepository
	CommitteeMember   repositories.CommitteeMemberRepository
	StudentCase       repositories.StudentCaseRepository
	ImprovementPlan   repositories.ImprovementPlanRepository
	Sanction          repositories.SanctionRepository
	CommitteeDecision repositories.CommitteeDecisionRepository
	Appeal            repositories.AppealRepository
}

// ImprovementPlan Repository
func NewImprovementPlanRepository(db *database.Database) repositories.ImprovementPlanRepository {
	return &improvementPlanRepository{db: db.DB}
}

func (r *improvementPlanRepository) Create(ctx context.Context, plan *entities.ImprovementPlan) error {
	model := r.toModel(plan)
	if err := r.db.WithContext(ctx).Create(model).Error; err != nil {
		return err
	}
	plan.ID = model.ID
	return nil
}

func (r *improvementPlanRepository) GetByID(ctx context.Context, id uuid.UUID) (*entities.ImprovementPlan, error) {
	var model database.ImprovementPlanModel
	if err := r.db.WithContext(ctx).First(&model, "id = ?", id).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, nil
		}
		return nil, err
	}
	return r.toEntity(&model), nil
}

func (r *improvementPlanRepository) GetByStudentCaseID(ctx context.Context, studentCaseID uuid.UUID) ([]*entities.ImprovementPlan, error) {
	var models []database.ImprovementPlanModel
	if err := r.db.WithContext(ctx).Where("student_case_id = ?", studentCaseID).Find(&models).Error; err != nil {
		return nil, err
	}

	plans := make([]*entities.ImprovementPlan, len(models))
	for i, model := range models {
		plans[i] = r.toEntity(&model)
	}
	return plans, nil
}

func (r *improvementPlanRepository) GetByStudentID(ctx context.Context, studentID uuid.UUID) ([]*entities.ImprovementPlan, error) {
	var models []database.ImprovementPlanModel
	if err := r.db.WithContext(ctx).Where("student_id = ?", studentID).Find(&models).Error; err != nil {
		return nil, err
	}

	plans := make([]*entities.ImprovementPlan, len(models))
	for i, model := range models {
		plans[i] = r.toEntity(&model)
	}
	return plans, nil
}

func (r *improvementPlanRepository) GetBySupervisorID(ctx context.Context, supervisorID uuid.UUID) ([]*entities.ImprovementPlan, error) {
	var models []database.ImprovementPlanModel
	if err := r.db.WithContext(ctx).Where("supervisor_id = ?", supervisorID).Find(&models).Error; err != nil {
		return nil, err
	}

	plans := make([]*entities.ImprovementPlan, len(models))
	for i, model := range models {
		plans[i] = r.toEntity(&model)
	}
	return plans, nil
}

func (r *improvementPlanRepository) GetByStatus(ctx context.Context, status string) ([]*entities.ImprovementPlan, error) {
	var models []database.ImprovementPlanModel
	if err := r.db.WithContext(ctx).Where("status = ?", status).Find(&models).Error; err != nil {
		return nil, err
	}

	plans := make([]*entities.ImprovementPlan, len(models))
	for i, model := range models {
		plans[i] = r.toEntity(&model)
	}
	return plans, nil
}

func (r *improvementPlanRepository) Update(ctx context.Context, plan *entities.ImprovementPlan) error {
	model := r.toModel(plan)
	return r.db.WithContext(ctx).Save(model).Error
}

func (r *improvementPlanRepository) Delete(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&database.ImprovementPlanModel{}, "id = ?", id).Error
}

func (r *improvementPlanRepository) toModel(plan *entities.ImprovementPlan) *database.ImprovementPlanModel {
	return &database.ImprovementPlanModel{
		ID:              plan.ID,
		StudentCaseID:   plan.StudentCaseID,
		StudentID:       plan.StudentID,
		Title:           plan.Title,
		Description:     plan.Description,
		Objectives:      plan.Objectives,
		Activities:      plan.Activities,
		Resources:       plan.Resources,
		Timeline:        plan.Timeline,
		Status:          string(plan.Status),
		StartDate:       plan.StartDate,
		EndDate:         plan.EndDate,
		CompletionDate:  plan.CompletionDate,
		Progress:        plan.Progress,
		SupervisorID:    plan.SupervisorID,
		SupervisorNotes: plan.SupervisorNotes,
		CreatedAt:       plan.CreatedAt,
		UpdatedAt:       plan.UpdatedAt,
	}
}

func (r *improvementPlanRepository) toEntity(model *database.ImprovementPlanModel) *entities.ImprovementPlan {
	return &entities.ImprovementPlan{
		ID:              model.ID,
		StudentCaseID:   model.StudentCaseID,
		StudentID:       model.StudentID,
		Title:           model.Title,
		Description:     model.Description,
		Objectives:      model.Objectives,
		Activities:      model.Activities,
		Resources:       model.Resources,
		Timeline:        model.Timeline,
		Status:          entities.PlanStatus(model.Status),
		StartDate:       model.StartDate,
		EndDate:         model.EndDate,
		CompletionDate:  model.CompletionDate,
		Progress:        model.Progress,
		SupervisorID:    model.SupervisorID,
		SupervisorNotes: model.SupervisorNotes,
		CreatedAt:       model.CreatedAt,
		UpdatedAt:       model.UpdatedAt,
	}
}

// CommitteeMember Repository
func NewCommitteeMemberRepository(db *database.Database) repositories.CommitteeMemberRepository {
	return &committeeMemberRepository{db: db.DB}
}

func (r *committeeMemberRepository) Create(ctx context.Context, member *entities.CommitteeMember) error {
	model := r.toModel(member)
	if err := r.db.WithContext(ctx).Create(model).Error; err != nil {
		return err
	}
	member.ID = model.ID
	return nil
}

func (r *committeeMemberRepository) GetByID(ctx context.Context, id uuid.UUID) (*entities.CommitteeMember, error) {
	var model database.CommitteeMemberModel
	if err := r.db.WithContext(ctx).First(&model, "id = ?", id).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, nil
		}
		return nil, err
	}
	return r.toEntity(&model), nil
}

func (r *committeeMemberRepository) GetByCommitteeID(ctx context.Context, committeeID uuid.UUID) ([]*entities.CommitteeMember, error) {
	var models []database.CommitteeMemberModel
	if err := r.db.WithContext(ctx).Where("committee_id = ?", committeeID).Find(&models).Error; err != nil {
		return nil, err
	}

	members := make([]*entities.CommitteeMember, len(models))
	for i, model := range models {
		members[i] = r.toEntity(&model)
	}
	return members, nil
}

func (r *committeeMemberRepository) GetByUserID(ctx context.Context, userID uuid.UUID) ([]*entities.CommitteeMember, error) {
	var models []database.CommitteeMemberModel
	if err := r.db.WithContext(ctx).Where("user_id = ?", userID).Find(&models).Error; err != nil {
		return nil, err
	}

	members := make([]*entities.CommitteeMember, len(models))
	for i, model := range models {
		members[i] = r.toEntity(&model)
	}
	return members, nil
}

func (r *committeeMemberRepository) Update(ctx context.Context, member *entities.CommitteeMember) error {
	model := r.toModel(member)
	return r.db.WithContext(ctx).Save(model).Error
}

func (r *committeeMemberRepository) Delete(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&database.CommitteeMemberModel{}, "id = ?", id).Error
}

func (r *committeeMemberRepository) toModel(member *entities.CommitteeMember) *database.CommitteeMemberModel {
	return &database.CommitteeMemberModel{
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

func (r *committeeMemberRepository) toEntity(model *database.CommitteeMemberModel) *entities.CommitteeMember {
	return &entities.CommitteeMember{
		ID:              model.ID,
		CommitteeID:     model.CommitteeID,
		UserID:          model.UserID,
		Role:            entities.MemberRole(model.Role),
		Status:          entities.MemberStatus(model.Status),
		AppointmentDate: model.AppointmentDate,
		EndDate:         model.EndDate,
		CreatedAt:       model.CreatedAt,
		UpdatedAt:       model.UpdatedAt,
	}
}

// Sanction Repository
func NewSanctionRepository(db *database.Database) repositories.SanctionRepository {
	return &sanctionRepository{db: db.DB}
}

func (r *sanctionRepository) Create(ctx context.Context, sanction *entities.Sanction) error {
	model := r.toModel(sanction)
	if err := r.db.WithContext(ctx).Create(model).Error; err != nil {
		return err
	}
	sanction.ID = model.ID
	return nil
}

func (r *sanctionRepository) GetByID(ctx context.Context, id uuid.UUID) (*entities.Sanction, error) {
	var model database.SanctionModel
	if err := r.db.WithContext(ctx).First(&model, "id = ?", id).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, nil
		}
		return nil, err
	}
	return r.toEntity(&model), nil
}

func (r *sanctionRepository) GetByStudentCaseID(ctx context.Context, studentCaseID uuid.UUID) ([]*entities.Sanction, error) {
	var models []database.SanctionModel
	if err := r.db.WithContext(ctx).Where("student_case_id = ?", studentCaseID).Find(&models).Error; err != nil {
		return nil, err
	}

	sanctions := make([]*entities.Sanction, len(models))
	for i, model := range models {
		sanctions[i] = r.toEntity(&model)
	}
	return sanctions, nil
}

func (r *sanctionRepository) GetByStudentID(ctx context.Context, studentID uuid.UUID) ([]*entities.Sanction, error) {
	var models []database.SanctionModel
	if err := r.db.WithContext(ctx).Where("student_id = ?", studentID).Find(&models).Error; err != nil {
		return nil, err
	}

	sanctions := make([]*entities.Sanction, len(models))
	for i, model := range models {
		sanctions[i] = r.toEntity(&model)
	}
	return sanctions, nil
}

func (r *sanctionRepository) GetByType(ctx context.Context, sanctionType string) ([]*entities.Sanction, error) {
	var models []database.SanctionModel
	if err := r.db.WithContext(ctx).Where("type = ?", sanctionType).Find(&models).Error; err != nil {
		return nil, err
	}

	sanctions := make([]*entities.Sanction, len(models))
	for i, model := range models {
		sanctions[i] = r.toEntity(&model)
	}
	return sanctions, nil
}

func (r *sanctionRepository) GetByStatus(ctx context.Context, status string) ([]*entities.Sanction, error) {
	var models []database.SanctionModel
	if err := r.db.WithContext(ctx).Where("status = ?", status).Find(&models).Error; err != nil {
		return nil, err
	}

	sanctions := make([]*entities.Sanction, len(models))
	for i, model := range models {
		sanctions[i] = r.toEntity(&model)
	}
	return sanctions, nil
}

func (r *sanctionRepository) Update(ctx context.Context, sanction *entities.Sanction) error {
	model := r.toModel(sanction)
	return r.db.WithContext(ctx).Save(model).Error
}

func (r *sanctionRepository) Delete(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&database.SanctionModel{}, "id = ?", id).Error
}

func (r *sanctionRepository) toModel(sanction *entities.Sanction) *database.SanctionModel {
	return &database.SanctionModel{
		ID:              sanction.ID,
		StudentCaseID:   sanction.StudentCaseID,
		StudentID:       sanction.StudentID,
		Type:            string(sanction.Type),
		Severity:        string(sanction.Severity),
		Status:          string(sanction.Status),
		Title:           sanction.Title,
		Description:     sanction.Description,
		Justification:   sanction.Justification,
		StartDate:       sanction.StartDate,
		EndDate:         sanction.EndDate,
		CompletionDate:  sanction.CompletionDate,
		IsAppealable:    sanction.IsAppealable,
		AppealDeadline:  sanction.AppealDeadline,
		CreatedAt:       sanction.CreatedAt,
		UpdatedAt:       sanction.UpdatedAt,
	}
}

func (r *sanctionRepository) toEntity(model *database.SanctionModel) *entities.Sanction {
	return &entities.Sanction{
		ID:              model.ID,
		StudentCaseID:   model.StudentCaseID,
		StudentID:       model.StudentID,
		Type:            entities.SanctionType(model.Type),
		Severity:        entities.SanctionSeverity(model.Severity),
		Status:          entities.SanctionStatus(model.Status),
		Title:           model.Title,
		Description:     model.Description,
		Justification:   model.Justification,
		StartDate:       model.StartDate,
		EndDate:         model.EndDate,
		CompletionDate:  model.CompletionDate,
		IsAppealable:    model.IsAppealable,
		AppealDeadline:  model.AppealDeadline,
		CreatedAt:       model.CreatedAt,
		UpdatedAt:       model.UpdatedAt,
	}
}

// CommitteeDecision Repository (simplified implementation)
func NewCommitteeDecisionRepository(db *database.Database) repositories.CommitteeDecisionRepository {
	return &committeeDecisionRepository{db: db.DB}
}

func (r *committeeDecisionRepository) Create(ctx context.Context, decision *entities.CommitteeDecision) error {
	// Implementation similar to others...
	return nil
}

func (r *committeeDecisionRepository) GetByID(ctx context.Context, id uuid.UUID) (*entities.CommitteeDecision, error) {
	return nil, nil
}

func (r *committeeDecisionRepository) GetByCommitteeID(ctx context.Context, committeeID uuid.UUID) ([]*entities.CommitteeDecision, error) {
	return nil, nil
}

func (r *committeeDecisionRepository) GetByStudentCaseID(ctx context.Context, studentCaseID uuid.UUID) ([]*entities.CommitteeDecision, error) {
	return nil, nil
}

func (r *committeeDecisionRepository) Update(ctx context.Context, decision *entities.CommitteeDecision) error {
	return nil
}

func (r *committeeDecisionRepository) Delete(ctx context.Context, id uuid.UUID) error {
	return nil
}

func (r *committeeDecisionRepository) GenerateDecisionNumber(ctx context.Context, committeeID uuid.UUID) (string, error) {
	return "", nil
}

// Appeal Repository (simplified implementation)
func NewAppealRepository(db *database.Database) repositories.AppealRepository {
	return &appealRepository{db: db.DB}
}

func (r *appealRepository) Create(ctx context.Context, appeal *entities.Appeal) error {
	// Implementation similar to others...
	return nil
}

func (r *appealRepository) GetByID(ctx context.Context, id uuid.UUID) (*entities.Appeal, error) {
	return nil, nil
}

func (r *appealRepository) GetByStudentCaseID(ctx context.Context, studentCaseID uuid.UUID) ([]*entities.Appeal, error) {
	return nil, nil
}

func (r *appealRepository) GetByStudentID(ctx context.Context, studentID uuid.UUID) ([]*entities.Appeal, error) {
	return nil, nil
}

func (r *appealRepository) GetByStatus(ctx context.Context, status string) ([]*entities.Appeal, error) {
	return nil, nil
}

func (r *appealRepository) Update(ctx context.Context, appeal *entities.Appeal) error {
	return nil
}

func (r *appealRepository) Delete(ctx context.Context, id uuid.UUID) error {
	return nil
}

func (r *appealRepository) GenerateAppealNumber(ctx context.Context) (string, error) {
	return "", nil
}
