package repositories

import (
	"context"
	"scheduleservice/internal/domain/entities"
	"scheduleservice/internal/domain/repositories"
	"scheduleservice/internal/infrastructure/database/models"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type academicGroupRepositoryImpl struct {
	db *gorm.DB
}

func NewAcademicGroupRepository(db *gorm.DB) repositories.AcademicGroupRepository {
	return &academicGroupRepositoryImpl{db: db}
}

func (r *academicGroupRepositoryImpl) Create(ctx context.Context, group *entities.AcademicGroup) (*entities.AcademicGroup, error) {
	model := models.FromAcademicGroupDomain(group)
	if err := r.db.WithContext(ctx).Create(model).Error; err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *academicGroupRepositoryImpl) GetByID(ctx context.Context, id uuid.UUID) (*entities.AcademicGroup, error) {
	var model models.AcademicGroupModel
	err := r.db.WithContext(ctx).Preload("AcademicProgram").First(&model, "id = ?", id).Error
	if err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *academicGroupRepositoryImpl) GetByCode(ctx context.Context, code string) (*entities.AcademicGroup, error) {
	var model models.AcademicGroupModel
	err := r.db.WithContext(ctx).Preload("AcademicProgram").First(&model, "number = ?", code).Error
	if err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *academicGroupRepositoryImpl) GetByNumber(ctx context.Context, number string) (*entities.AcademicGroup, error) {
	var model models.AcademicGroupModel
	err := r.db.WithContext(ctx).Preload("AcademicProgram").First(&model, "number = ?", number).Error
	if err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *academicGroupRepositoryImpl) Update(ctx context.Context, group *entities.AcademicGroup) (*entities.AcademicGroup, error) {
	model := models.FromAcademicGroupDomain(group)
	if err := r.db.WithContext(ctx).Save(model).Error; err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *academicGroupRepositoryImpl) Delete(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&models.AcademicGroupModel{}, "id = ?", id).Error
}

func (r *academicGroupRepositoryImpl) List(ctx context.Context, filter repositories.AcademicGroupFilter) ([]*entities.AcademicGroup, int64, error) {
	var modelList []models.AcademicGroupModel
	var total int64

	query := r.db.WithContext(ctx).Model(&models.AcademicGroupModel{}).Preload("AcademicProgram")

	// Aplicar filtros
	if filter.AcademicProgramID != nil {
		query = query.Where("academic_program_id = ?", *filter.AcademicProgramID)
	}

	if filter.IsActive != nil {
		query = query.Where("is_active = ?", *filter.IsActive)
	}

	if filter.Search != "" {
		query = query.Where("LOWER(number) LIKE ? OR LOWER(shift) LIKE ?",
			"%"+filter.Search+"%", "%"+filter.Search+"%")
	}

	if filter.Quarter != nil {
		query = query.Where("quarter = ?", *filter.Quarter)
	}

	if filter.Year != nil {
		query = query.Where("year = ?", *filter.Year)
	}

	if filter.Shift != "" {
		query = query.Where("shift = ?", filter.Shift)
	}

	// Contar total
	if err := query.Count(&total).Error; err != nil {
		return nil, 0, err
	}

	// Aplicar paginación
	filter.SetDefaults()
	query = query.Offset(filter.GetOffset()).Limit(filter.GetLimit())

	if err := query.Find(&modelList).Error; err != nil {
		return nil, 0, err
	}

	groups := make([]*entities.AcademicGroup, len(modelList))
	for i, model := range modelList {
		groups[i] = model.ToEntity()
	}

	return groups, total, nil
}

func (r *academicGroupRepositoryImpl) ListActive(ctx context.Context) ([]*entities.AcademicGroup, error) {
	var modelList []models.AcademicGroupModel
	err := r.db.WithContext(ctx).Preload("AcademicProgram").
		Where("is_active = ?", true).
		Find(&modelList).Error
	if err != nil {
		return nil, err
	}

	groups := make([]*entities.AcademicGroup, len(modelList))
	for i, model := range modelList {
		groups[i] = model.ToEntity()
	}

	return groups, nil
}

func (r *academicGroupRepositoryImpl) GetByProgram(ctx context.Context, programID uuid.UUID) ([]*entities.AcademicGroup, error) {
	var modelList []models.AcademicGroupModel
	err := r.db.WithContext(ctx).Preload("AcademicProgram").
		Where("academic_program_id = ? AND is_active = ?", programID, true).
		Find(&modelList).Error
	if err != nil {
		return nil, err
	}

	groups := make([]*entities.AcademicGroup, len(modelList))
	for i, model := range modelList {
		groups[i] = model.ToEntity()
	}

	return groups, nil
}
