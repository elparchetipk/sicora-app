package repositories

import (
	"context"
	"scheduleservice/internal/domain/entities"
	"scheduleservice/internal/domain/repositories"
	"scheduleservice/internal/infrastructure/database/models"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type campusRepositoryImpl struct {
	db *gorm.DB
}

func NewCampusRepository(db *gorm.DB) repositories.CampusRepository {
	return &campusRepositoryImpl{db: db}
}

func (r *campusRepositoryImpl) Create(ctx context.Context, campus *entities.Campus) (*entities.Campus, error) {
	model := models.FromCampusDomain(campus)
	if err := r.db.WithContext(ctx).Create(model).Error; err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *campusRepositoryImpl) GetByID(ctx context.Context, id uuid.UUID) (*entities.Campus, error) {
	var model models.CampusModel
	err := r.db.WithContext(ctx).First(&model, "id = ?", id).Error
	if err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *campusRepositoryImpl) GetByCode(ctx context.Context, code string) (*entities.Campus, error) {
	var model models.CampusModel
	err := r.db.WithContext(ctx).First(&model, "code = ?", code).Error
	if err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *campusRepositoryImpl) Update(ctx context.Context, campus *entities.Campus) (*entities.Campus, error) {
	model := models.FromCampusDomain(campus)
	if err := r.db.WithContext(ctx).Save(model).Error; err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *campusRepositoryImpl) Delete(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&models.CampusModel{}, "id = ?", id).Error
}

func (r *campusRepositoryImpl) List(ctx context.Context, filter repositories.BaseFilter) ([]*entities.Campus, int64, error) {
	var modelList []models.CampusModel
	var total int64

	query := r.db.WithContext(ctx).Model(&models.CampusModel{})

	// Aplicar filtros
	if filter.IsActive != nil {
		query = query.Where("is_active = ?", *filter.IsActive)
	}

	if filter.Search != "" {
		query = query.Where("LOWER(name) LIKE ? OR LOWER(code) LIKE ? OR LOWER(city) LIKE ?",
			"%"+filter.Search+"%", "%"+filter.Search+"%", "%"+filter.Search+"%")
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

	campuses := make([]*entities.Campus, len(modelList))
	for i, model := range modelList {
		campuses[i] = model.ToEntity()
	}

	return campuses, total, nil
}

func (r *campusRepositoryImpl) ListActive(ctx context.Context) ([]*entities.Campus, error) {
	var modelList []models.CampusModel
	err := r.db.WithContext(ctx).
		Where("is_active = ?", true).
		Find(&modelList).Error
	if err != nil {
		return nil, err
	}

	campuses := make([]*entities.Campus, len(modelList))
	for i, model := range modelList {
		campuses[i] = model.ToEntity()
	}

	return campuses, nil
}
