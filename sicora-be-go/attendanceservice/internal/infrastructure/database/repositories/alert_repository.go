package repositories

import (
	"context"

	"attendanceservice/internal/domain/entities"
	"attendanceservice/internal/domain/repositories"
	"attendanceservice/internal/infrastructure/database/models"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type alertRepository struct {
	db *gorm.DB
}

// NewAttendanceAlertRepository crea una nueva instancia del repositorio de alertas
func NewAttendanceAlertRepository(db *gorm.DB) repositories.AttendanceAlertRepository {
	return &alertRepository{db: db}
}

// Create crea una nueva alerta
func (r *alertRepository) Create(ctx context.Context, alert *entities.AttendanceAlert) error {
	model := r.mapToModel(alert)
	return r.db.WithContext(ctx).Create(model).Error
}

// GetByID obtiene una alerta por ID
func (r *alertRepository) GetByID(ctx context.Context, id uuid.UUID) (*entities.AttendanceAlert, error) {
	var model models.AttendanceAlert
	err := r.db.WithContext(ctx).First(&model, "id = ?", id).Error
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, err
	}
	return r.mapToEntity(&model), nil
}

// GetByUserID obtiene alertas por ID de usuario
func (r *alertRepository) GetByUserID(ctx context.Context, userID uuid.UUID, limit, offset int) ([]*entities.AttendanceAlert, error) {
	var models []models.AttendanceAlert
	err := r.db.WithContext(ctx).
		Where("student_id = ?", userID).
		Order("created_at DESC").
		Limit(limit).
		Offset(offset).
		Find(&models).Error
	if err != nil {
		return nil, err
	}

	entities := make([]*entities.AttendanceAlert, len(models))
	for i, model := range models {
		entities[i] = r.mapToEntity(&model)
	}
	return entities, nil
}

// GetActiveAlerts obtiene alertas activas
func (r *alertRepository) GetActiveAlerts(ctx context.Context, limit, offset int) ([]*entities.AttendanceAlert, error) {
	var models []models.AttendanceAlert
	err := r.db.WithContext(ctx).
		Where("is_active = ?", true).
		Order("created_at DESC").
		Limit(limit).
		Offset(offset).
		Find(&models).Error
	if err != nil {
		return nil, err
	}

	entities := make([]*entities.AttendanceAlert, len(models))
	for i, model := range models {
		entities[i] = r.mapToEntity(&model)
	}
	return entities, nil
}

// Update actualiza una alerta
func (r *alertRepository) Update(ctx context.Context, alert *entities.AttendanceAlert) error {
	model := r.mapToModel(alert)
	return r.db.WithContext(ctx).Save(model).Error
}

// Delete elimina una alerta
func (r *alertRepository) Delete(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&models.AttendanceAlert{}, id).Error
}

// MarkAsRead marca una alerta como leída
func (r *alertRepository) MarkAsRead(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Model(&models.AttendanceAlert{}).
		Where("id = ?", id).
		Update("is_read", true).Error
}

// GetUnreadCount obtiene el número de alertas no leídas
func (r *alertRepository) GetUnreadCount(ctx context.Context, userID uuid.UUID) (int, error) {
	var count int64
	err := r.db.WithContext(ctx).Model(&models.AttendanceAlert{}).
		Where("student_id = ? AND is_read = ?", userID, false).
		Count(&count).Error
	return int(count), err
}

// mapToModel convierte una entidad a modelo GORM
func (r *alertRepository) mapToModel(entity *entities.AttendanceAlert) *models.AttendanceAlert {
	return &models.AttendanceAlert{
		ID:          entity.ID,
		StudentID:   entity.StudentID,
		Type:        string(entity.Type),
		Level:       string(entity.Level),
		Title:       entity.Title,
		Description: entity.Description,
		Metadata:    entity.Metadata,
		IsRead:      entity.IsRead,
		ReadBy:      entity.ReadBy,
		ReadAt:      entity.ReadAt,
		IsActive:    entity.IsActive,
		CreatedAt:   entity.CreatedAt,
		UpdatedAt:   entity.UpdatedAt,
	}
}

// mapToEntity convierte un modelo GORM a entidad
func (r *alertRepository) mapToEntity(model *models.AttendanceAlert) *entities.AttendanceAlert {
	return &entities.AttendanceAlert{
		ID:          model.ID,
		StudentID:   model.StudentID,
		Type:        entities.AlertType(model.Type),
		Level:       entities.AlertLevel(model.Level),
		Title:       model.Title,
		Description: model.Description,
		Metadata:    model.Metadata,
		IsRead:      model.IsRead,
		ReadBy:      model.ReadBy,
		ReadAt:      model.ReadAt,
		IsActive:    model.IsActive,
		CreatedAt:   model.CreatedAt,
		UpdatedAt:   model.UpdatedAt,
	}
}
