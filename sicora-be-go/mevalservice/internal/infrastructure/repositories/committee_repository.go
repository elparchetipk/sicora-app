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

type committeeRepository struct {
	db *gorm.DB
}

func NewCommitteeRepository(db *database.Database) repositories.CommitteeRepository {
	return &committeeRepository{
		db: db.DB,
	}
}

func (r *committeeRepository) Create(ctx context.Context, committee *entities.Committee) error {
	model := r.toModel(committee)
	if err := r.db.WithContext(ctx).Create(model).Error; err != nil {
		return err
	}
	committee.ID = model.ID
	return nil
}

func (r *committeeRepository) GetByID(ctx context.Context, id uuid.UUID) (*entities.Committee, error) {
	var model database.CommitteeModel
	if err := r.db.WithContext(ctx).
		Preload("Members").
		First(&model, "id = ?", id).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, nil
		}
		return nil, err
	}
	return r.toEntity(&model), nil
}

func (r *committeeRepository) GetAll(ctx context.Context) ([]*entities.Committee, error) {
	var models []database.CommitteeModel
	if err := r.db.WithContext(ctx).
		Preload("Members").
		Find(&models).Error; err != nil {
		return nil, err
	}

	committees := make([]*entities.Committee, len(models))
	for i, model := range models {
		committees[i] = r.toEntity(&model)
	}
	return committees, nil
}

func (r *committeeRepository) GetByCenter(ctx context.Context, center string) ([]*entities.Committee, error) {
	var models []database.CommitteeModel
	if err := r.db.WithContext(ctx).
		Preload("Members").
		Where("center = ? AND status = ?", center, "ACTIVE").
		Find(&models).Error; err != nil {
		return nil, err
	}

	committees := make([]*entities.Committee, len(models))
	for i, model := range models {
		committees[i] = r.toEntity(&model)
	}
	return committees, nil
}

func (r *committeeRepository) GetByType(ctx context.Context, committeeType string) ([]*entities.Committee, error) {
	var models []database.CommitteeModel
	if err := r.db.WithContext(ctx).
		Preload("Members").
		Where("type = ? AND status = ?", committeeType, "ACTIVE").
		Find(&models).Error; err != nil {
		return nil, err
	}

	committees := make([]*entities.Committee, len(models))
	for i, model := range models {
		committees[i] = r.toEntity(&model)
	}
	return committees, nil
}

func (r *committeeRepository) Update(ctx context.Context, committee *entities.Committee) error {
	model := r.toModel(committee)
	return r.db.WithContext(ctx).Save(model).Error
}

func (r *committeeRepository) Delete(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&database.CommitteeModel{}, "id = ?", id).Error
}

func (r *committeeRepository) GetAvailableForAssignment(ctx context.Context, committeeType, center string) ([]*entities.Committee, error) {
	var models []database.CommitteeModel
	if err := r.db.WithContext(ctx).
		Preload("Members").
		Where("type = ? AND center = ? AND status = ? AND current_members < max_members", 
			committeeType, center, "ACTIVE").
		Find(&models).Error; err != nil {
		return nil, err
	}

	committees := make([]*entities.Committee, len(models))
	for i, model := range models {
		committees[i] = r.toEntity(&model)
	}
	return committees, nil
}

// Conversion methods
func (r *committeeRepository) toModel(committee *entities.Committee) *database.CommitteeModel {
	return &database.CommitteeModel{
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
}

func (r *committeeRepository) toEntity(model *database.CommitteeModel) *entities.Committee {
	committee := &entities.Committee{
		ID:             model.ID,
		Name:           model.Name,
		Type:           entities.CommitteeType(model.Type),
		Status:         entities.CommitteeStatus(model.Status),
		Center:         model.Center,
		Coordinator:    model.Coordinator,
		MaxMembers:     model.MaxMembers,
		CurrentMembers: model.CurrentMembers,
		CreatedAt:      model.CreatedAt,
		UpdatedAt:      model.UpdatedAt,
	}

	// Convert members if loaded
	if len(model.Members) > 0 {
		for _, memberModel := range model.Members {
			member := &entities.CommitteeMember{
				ID:              memberModel.ID,
				CommitteeID:     memberModel.CommitteeID,
				UserID:          memberModel.UserID,
				Role:            entities.MemberRole(memberModel.Role),
				Status:          entities.MemberStatus(memberModel.Status),
				AppointmentDate: memberModel.AppointmentDate,
				EndDate:         memberModel.EndDate,
				CreatedAt:       memberModel.CreatedAt,
				UpdatedAt:       memberModel.UpdatedAt,
			}
			committee.AddMember(member)
		}
	}

	return committee
}
