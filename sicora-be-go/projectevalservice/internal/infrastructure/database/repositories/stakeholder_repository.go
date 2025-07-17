package repositories

import (
	"context"
	"fmt"

	"projectevalservice/internal/domain/entities"
	"projectevalservice/internal/domain/repositories"
	"projectevalservice/internal/infrastructure/database/models"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type stakeholderRepository struct {
	db *gorm.DB
}

func NewStakeholderRepository(db *gorm.DB) repositories.StakeholderRepository {
	return &stakeholderRepository{db: db}
}

func (r *stakeholderRepository) Create(ctx context.Context, stakeholder *entities.Stakeholder) error {
	model := models.StakeholderFromEntity(stakeholder)
	return r.db.WithContext(ctx).Create(model).Error
}

func (r *stakeholderRepository) GetByID(ctx context.Context, id uuid.UUID) (*entities.Stakeholder, error) {
	var model models.Stakeholder
	err := r.db.WithContext(ctx).Where("id = ?", id).First(&model).Error
	if err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *stakeholderRepository) GetByProjectID(ctx context.Context, projectID uuid.UUID) ([]*entities.Stakeholder, error) {
	var modelList []models.Stakeholder
	err := r.db.WithContext(ctx).Where("project_id = ?", projectID).Find(&modelList).Error
	if err != nil {
		return nil, err
	}

	var entities []*entities.Stakeholder
	for _, model := range modelList {
		entities = append(entities, model.ToEntity())
	}
	return entities, nil
}

func (r *stakeholderRepository) GetByUserID(ctx context.Context, userID uuid.UUID) ([]*entities.Stakeholder, error) {
	var modelList []models.Stakeholder
	err := r.db.WithContext(ctx).Where("user_id = ?", userID).Find(&modelList).Error
	if err != nil {
		return nil, err
	}

	var entities []*entities.Stakeholder
	for _, model := range modelList {
		entities = append(entities, model.ToEntity())
	}
	return entities, nil
}

func (r *stakeholderRepository) GetByProjectAndUser(ctx context.Context, projectID, userID uuid.UUID) (*entities.Stakeholder, error) {
	var model models.Stakeholder
	err := r.db.WithContext(ctx).Where("project_id = ? AND user_id = ?", projectID, userID).First(&model).Error
	if err != nil {
		return nil, err
	}
	return model.ToEntity(), nil
}

func (r *stakeholderRepository) GetByRole(ctx context.Context, projectID uuid.UUID, role entities.StakeholderRole) ([]*entities.Stakeholder, error) {
	var modelList []models.Stakeholder
	err := r.db.WithContext(ctx).Where("project_id = ? AND role = ?", projectID, role).Find(&modelList).Error
	if err != nil {
		return nil, err
	}

	var entities []*entities.Stakeholder
	for _, model := range modelList {
		entities = append(entities, model.ToEntity())
	}
	return entities, nil
}

func (r *stakeholderRepository) Update(ctx context.Context, stakeholder *entities.Stakeholder) error {
	model := models.StakeholderFromEntity(stakeholder)
	return r.db.WithContext(ctx).Save(model).Error
}

func (r *stakeholderRepository) Delete(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&models.Stakeholder{}, "id = ?", id).Error
}

func (r *stakeholderRepository) List(ctx context.Context, filters map[string]interface{}) ([]*entities.Stakeholder, error) {
	var modelList []models.Stakeholder
	query := r.db.WithContext(ctx)

	// Apply filters
	for key, value := range filters {
		switch key {
		case "project_id":
			query = query.Where("project_id = ?", value)
		case "role":
			query = query.Where("role = ?", value)
		case "type":
			query = query.Where("type = ?", value)
		case "status":
			query = query.Where("status = ?", value)
		case "can_evaluate":
			query = query.Where("can_evaluate = ?", value)
		case "can_review":
			query = query.Where("can_review = ?", value)
		case "can_approve":
			query = query.Where("can_approve = ?", value)
		case "organization":
			query = query.Where("organization ILIKE ?", fmt.Sprintf("%%%s%%", value))
		case "limit":
			if limit, ok := value.(int); ok {
				query = query.Limit(limit)
			}
		case "offset":
			if offset, ok := value.(int); ok {
				query = query.Offset(offset)
			}
		}
	}

	err := query.Find(&modelList).Error
	if err != nil {
		return nil, err
	}

	var entities []*entities.Stakeholder
	for _, model := range modelList {
		entities = append(entities, model.ToEntity())
	}
	return entities, nil
}
