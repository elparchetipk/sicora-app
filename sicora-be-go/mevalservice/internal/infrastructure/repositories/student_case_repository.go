package repositories

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"

	"mevalservice/internal/domain/entities"
	"mevalservice/internal/domain/repositories"
	"mevalservice/internal/infrastructure/database"
)

type studentCaseRepository struct {
	db *gorm.DB
}

func NewStudentCaseRepository(db *database.Database) repositories.StudentCaseRepository {
	return &studentCaseRepository{
		db: db.DB,
	}
}

func (r *studentCaseRepository) Create(ctx context.Context, studentCase *entities.StudentCase) error {
	model := r.toModel(studentCase)
	if err := r.db.WithContext(ctx).Create(model).Error; err != nil {
		return err
	}
	studentCase.ID = model.ID
	return nil
}

func (r *studentCaseRepository) GetByID(ctx context.Context, id uuid.UUID) (*entities.StudentCase, error) {
	var model database.StudentCaseModel
	if err := r.db.WithContext(ctx).
		Preload("Committee").
		Preload("ImprovementPlans").
		Preload("Sanctions").
		Preload("Decisions").
		Preload("Appeals").
		First(&model, "id = ?", id).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, nil
		}
		return nil, err
	}
	return r.toEntity(&model), nil
}

func (r *studentCaseRepository) GetByCaseNumber(ctx context.Context, caseNumber string) (*entities.StudentCase, error) {
	var model database.StudentCaseModel
	if err := r.db.WithContext(ctx).
		Preload("Committee").
		Preload("ImprovementPlans").
		Preload("Sanctions").
		Preload("Decisions").
		Preload("Appeals").
		First(&model, "case_number = ?", caseNumber).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, nil
		}
		return nil, err
	}
	return r.toEntity(&model), nil
}

func (r *studentCaseRepository) GetByStudentID(ctx context.Context, studentID uuid.UUID) ([]*entities.StudentCase, error) {
	var models []database.StudentCaseModel
	if err := r.db.WithContext(ctx).
		Preload("Committee").
		Preload("ImprovementPlans").
		Preload("Sanctions").
		Preload("Decisions").
		Preload("Appeals").
		Where("student_id = ?", studentID).
		Order("created_at DESC").
		Find(&models).Error; err != nil {
		return nil, err
	}

	cases := make([]*entities.StudentCase, len(models))
	for i, model := range models {
		cases[i] = r.toEntity(&model)
	}
	return cases, nil
}

func (r *studentCaseRepository) GetByCommitteeID(ctx context.Context, committeeID uuid.UUID) ([]*entities.StudentCase, error) {
	var models []database.StudentCaseModel
	if err := r.db.WithContext(ctx).
		Preload("Committee").
		Preload("ImprovementPlans").
		Preload("Sanctions").
		Preload("Decisions").
		Preload("Appeals").
		Where("committee_id = ?", committeeID).
		Order("created_at DESC").
		Find(&models).Error; err != nil {
		return nil, err
	}

	cases := make([]*entities.StudentCase, len(models))
	for i, model := range models {
		cases[i] = r.toEntity(&model)
	}
	return cases, nil
}

func (r *studentCaseRepository) GetByStatus(ctx context.Context, status string) ([]*entities.StudentCase, error) {
	var models []database.StudentCaseModel
	if err := r.db.WithContext(ctx).
		Preload("Committee").
		Preload("ImprovementPlans").
		Preload("Sanctions").
		Preload("Decisions").
		Preload("Appeals").
		Where("status = ?", status).
		Order("created_at DESC").
		Find(&models).Error; err != nil {
		return nil, err
	}

	cases := make([]*entities.StudentCase, len(models))
	for i, model := range models {
		cases[i] = r.toEntity(&model)
	}
	return cases, nil
}

func (r *studentCaseRepository) GetPendingCases(ctx context.Context) ([]*entities.StudentCase, error) {
	var models []database.StudentCaseModel
	if err := r.db.WithContext(ctx).
		Preload("Committee").
		Preload("ImprovementPlans").
		Preload("Sanctions").
		Preload("Decisions").
		Preload("Appeals").
		Where("status IN ?", []string{"PENDING", "IN_PROGRESS"}).
		Order("priority DESC, created_at ASC").
		Find(&models).Error; err != nil {
		return nil, err
	}

	cases := make([]*entities.StudentCase, len(models))
	for i, model := range models {
		cases[i] = r.toEntity(&model)
	}
	return cases, nil
}

func (r *studentCaseRepository) GetOverdueCases(ctx context.Context) ([]*entities.StudentCase, error) {
	var models []database.StudentCaseModel
	if err := r.db.WithContext(ctx).
		Preload("Committee").
		Preload("ImprovementPlans").
		Preload("Sanctions").
		Preload("Decisions").
		Preload("Appeals").
		Where("due_date < ? AND status IN ?", time.Now(), []string{"PENDING", "IN_PROGRESS"}).
		Order("due_date ASC").
		Find(&models).Error; err != nil {
		return nil, err
	}

	cases := make([]*entities.StudentCase, len(models))
	for i, model := range models {
		cases[i] = r.toEntity(&model)
	}
	return cases, nil
}

func (r *studentCaseRepository) GetBySeverity(ctx context.Context, severity string) ([]*entities.StudentCase, error) {
	var models []database.StudentCaseModel
	if err := r.db.WithContext(ctx).
		Preload("Committee").
		Preload("ImprovementPlans").
		Preload("Sanctions").
		Preload("Decisions").
		Preload("Appeals").
		Where("severity = ?", severity).
		Order("created_at DESC").
		Find(&models).Error; err != nil {
		return nil, err
	}

	cases := make([]*entities.StudentCase, len(models))
	for i, model := range models {
		cases[i] = r.toEntity(&model)
	}
	return cases, nil
}

func (r *studentCaseRepository) Update(ctx context.Context, studentCase *entities.StudentCase) error {
	model := r.toModel(studentCase)
	return r.db.WithContext(ctx).Save(model).Error
}

func (r *studentCaseRepository) Delete(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&database.StudentCaseModel{}, "id = ?", id).Error
}

func (r *studentCaseRepository) GenerateCaseNumber(ctx context.Context, caseType string) (string, error) {
	var count int64
	year := time.Now().Year()
	prefix := "DIS" // Disciplinary
	if caseType == "ACADEMIC" {
		prefix = "ACA"
	}

	// Count cases for this year and type
	if err := r.db.WithContext(ctx).Model(&database.StudentCaseModel{}).
		Where("case_number LIKE ? AND EXTRACT(year FROM created_at) = ?", 
			fmt.Sprintf("%s-%d-%%", prefix, year), year).
		Count(&count).Error; err != nil {
		return "", err
	}

	// Generate next case number
	return fmt.Sprintf("%s-%d-%04d", prefix, year, count+1), nil
}

// Conversion methods
func (r *studentCaseRepository) toModel(studentCase *entities.StudentCase) *database.StudentCaseModel {
	model := &database.StudentCaseModel{
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
	return model
}

func (r *studentCaseRepository) toEntity(model *database.StudentCaseModel) *entities.StudentCase {
	return &entities.StudentCase{
		ID:             model.ID,
		StudentID:      model.StudentID,
		CommitteeID:    model.CommitteeID,
		CaseNumber:     model.CaseNumber,
		Type:           entities.CaseType(model.Type),
		Severity:       entities.CaseSeverity(model.Severity),
		Status:         entities.CaseStatus(model.Status),
		Priority:       entities.CasePriority(model.Priority),
		Title:          model.Title,
		Description:    model.Description,
		Evidence:       model.Evidence,
		ReportedBy:     model.ReportedBy,
		ReportDate:     model.ReportDate,
		DueDate:        model.DueDate,
		ResolutionDate: model.ResolutionDate,
		CreatedAt:      model.CreatedAt,
		UpdatedAt:      model.UpdatedAt,
	}
}
