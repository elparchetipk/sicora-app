package repositories

import (
	"context"
	"scheduleservice/internal/domain/entities"
	"scheduleservice/internal/domain/repositories"
	"scheduleservice/internal/infrastructure/database/models"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type venueRepositoryImpl struct {
	db *gorm.DB
}

func NewVenueRepository(db *gorm.DB) repositories.VenueRepository {
	return &venueRepositoryImpl{db: db}
}

func (r *venueRepositoryImpl) Create(ctx context.Context, venue *entities.Venue) (*entities.Venue, error) {
	model := models.FromVenueDomain(venue)
	if err := r.db.WithContext(ctx).Create(model).Error; err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *venueRepositoryImpl) GetByID(ctx context.Context, id uuid.UUID) (*entities.Venue, error) {
	var model models.VenueModel
	err := r.db.WithContext(ctx).Preload("Campus").First(&model, "id = ?", id).Error
	if err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *venueRepositoryImpl) GetByCode(ctx context.Context, code string) (*entities.Venue, error) {
	var model models.VenueModel
	err := r.db.WithContext(ctx).Preload("Campus").First(&model, "code = ?", code).Error
	if err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *venueRepositoryImpl) Update(ctx context.Context, venue *entities.Venue) (*entities.Venue, error) {
	model := models.FromVenueDomain(venue)
	if err := r.db.WithContext(ctx).Save(model).Error; err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *venueRepositoryImpl) Delete(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&models.VenueModel{}, "id = ?", id).Error
}

func (r *venueRepositoryImpl) List(ctx context.Context, filter repositories.VenueFilter) ([]*entities.Venue, int64, error) {
	var modelList []models.VenueModel
	var total int64

	query := r.db.WithContext(ctx).Model(&models.VenueModel{}).Preload("Campus")

	// Aplicar filtros
	if filter.CampusID != nil {
		query = query.Where("campus_id = ?", *filter.CampusID)
	}

	if filter.IsActive != nil {
		query = query.Where("is_active = ?", *filter.IsActive)
	}

	if filter.Search != "" {
		query = query.Where("LOWER(name) LIKE ? OR LOWER(code) LIKE ?",
			"%"+filter.Search+"%", "%"+filter.Search+"%")
	}

	if filter.Type != "" {
		query = query.Where("type = ?", filter.Type)
	}

	if filter.Floor != "" {
		query = query.Where("floor = ?", filter.Floor)
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

	venues := make([]*entities.Venue, len(modelList))
	for i, model := range modelList {
		venues[i] = model.ToEntity()
	}

	return venues, total, nil
}

func (r *venueRepositoryImpl) ListActive(ctx context.Context) ([]*entities.Venue, error) {
	var modelList []models.VenueModel
	err := r.db.WithContext(ctx).Preload("Campus").
		Where("is_active = ?", true).
		Find(&modelList).Error
	if err != nil {
		return nil, err
	}

	venues := make([]*entities.Venue, len(modelList))
	for i, model := range modelList {
		venues[i] = model.ToEntity()
	}

	return venues, nil
}

func (r *venueRepositoryImpl) GetByCampus(ctx context.Context, campusID uuid.UUID) ([]*entities.Venue, error) {
	var modelList []models.VenueModel
	err := r.db.WithContext(ctx).Preload("Campus").
		Where("campus_id = ? AND is_active = ?", campusID, true).
		Find(&modelList).Error
	if err != nil {
		return nil, err
	}

	venues := make([]*entities.Venue, len(modelList))
	for i, model := range modelList {
		venues[i] = model.ToEntity()
	}

	return venues, nil
}
