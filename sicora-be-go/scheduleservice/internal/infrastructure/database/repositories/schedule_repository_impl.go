package repositories

import (
	"context"
	"fmt"
	"time"

	"scheduleservice/internal/domain/entities"
	"scheduleservice/internal/domain/repositories"
	"scheduleservice/internal/infrastructure/database/models"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// ScheduleRepositoryImpl implementa ScheduleRepository usando GORM
type ScheduleRepositoryImpl struct {
	db *gorm.DB
}

// NewScheduleRepository crea una nueva instancia del repositorio
func NewScheduleRepository(db *gorm.DB) repositories.ScheduleRepository {
	return &ScheduleRepositoryImpl{
		db: db,
	}
}

// Create implementa la creación de un horario
func (r *ScheduleRepositoryImpl) Create(ctx context.Context, schedule *entities.Schedule) (*entities.Schedule, error) {
	model := &models.ScheduleModel{}
	model.FromEntity(schedule)

	if err := r.db.WithContext(ctx).Create(model).Error; err != nil {
		return nil, fmt.Errorf("error creating schedule: %w", err)
	}

	// Preload relaciones para retornar entidad completa
	if err := r.db.WithContext(ctx).
		Preload("AcademicGroup.AcademicProgram").
		Preload("Venue.Campus").
		First(model, model.ID).Error; err != nil {
		return nil, fmt.Errorf("error loading created schedule: %w", err)
	}

	return model.ToEntity(), nil
}

// GetByID implementa la búsqueda por ID
func (r *ScheduleRepositoryImpl) GetByID(ctx context.Context, id uuid.UUID) (*entities.Schedule, error) {
	var model models.ScheduleModel

	if err := r.db.WithContext(ctx).
		Preload("AcademicGroup.AcademicProgram").
		Preload("Venue.Campus").
		First(&model, "id = ?", id).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, fmt.Errorf("error getting schedule by ID: %w", err)
	}

	return model.ToEntity(), nil
}

// Update implementa la actualización de un horario
func (r *ScheduleRepositoryImpl) Update(ctx context.Context, schedule *entities.Schedule) (*entities.Schedule, error) {
	model := &models.ScheduleModel{}
	model.FromEntity(schedule)

	if err := r.db.WithContext(ctx).
		Where("id = ?", schedule.ID).
		Updates(model).Error; err != nil {
		return nil, fmt.Errorf("error updating schedule: %w", err)
	}

	// Preload relaciones para retornar entidad completa
	if err := r.db.WithContext(ctx).
		Preload("AcademicGroup.AcademicProgram").
		Preload("Venue.Campus").
		First(model, schedule.ID).Error; err != nil {
		return nil, fmt.Errorf("error loading updated schedule: %w", err)
	}

	return model.ToEntity(), nil
}

// Delete implementa la eliminación de un horario
func (r *ScheduleRepositoryImpl) Delete(ctx context.Context, id uuid.UUID) error {
	if err := r.db.WithContext(ctx).Delete(&models.ScheduleModel{}, "id = ?", id).Error; err != nil {
		return fmt.Errorf("error deleting schedule: %w", err)
	}
	return nil
}

// List implementa el listado con filtros
func (r *ScheduleRepositoryImpl) List(ctx context.Context, filter repositories.ScheduleFilter) ([]*entities.Schedule, int64, error) {
	var modelList []models.ScheduleModel
	var total int64

	query := r.db.WithContext(ctx).Model(&models.ScheduleModel{})

	// Aplicar filtros
	if filter.InstructorID != nil {
		query = query.Where("instructor_id = ?", *filter.InstructorID)
	}
	if filter.AcademicGroupID != nil {
		query = query.Where("academic_group_id = ?", *filter.AcademicGroupID)
	}
	if filter.VenueID != nil {
		query = query.Where("venue_id = ?", *filter.VenueID)
	}
	if filter.DayOfWeek != nil {
		query = query.Where("day_of_week = ?", *filter.DayOfWeek)
	}
	if filter.StartDate != nil {
		query = query.Where("start_date >= ?", *filter.StartDate)
	}
	if filter.EndDate != nil {
		query = query.Where("end_date <= ?", *filter.EndDate)
	}
	if filter.Status != "" {
		query = query.Where("status = ?", filter.Status)
	}
	if filter.IsActive != nil {
		query = query.Where("is_active = ?", *filter.IsActive)
	}

	// Contar total
	if err := query.Count(&total).Error; err != nil {
		return nil, 0, fmt.Errorf("error counting schedules: %w", err)
	}

	// Aplicar paginación
	if filter.GetLimit() > 0 {
		query = query.Limit(filter.GetLimit())
	}
	if filter.GetOffset() > 0 {
		query = query.Offset(filter.GetOffset())
	}

	// Aplicar ordenamiento por defecto
	query = query.Order("start_date ASC, start_time ASC")

	// Ejecutar consulta con preloads
	if err := query.
		Preload("AcademicGroup.AcademicProgram").
		Preload("Venue.Campus").
		Find(&modelList).Error; err != nil {
		return nil, 0, fmt.Errorf("error listing schedules: %w", err)
	}

	// Convertir a entidades
	schedules := make([]*entities.Schedule, len(modelList))
	for i, model := range modelList {
		schedules[i] = model.ToEntity()
	}

	return schedules, total, nil
}

// GetByInstructor implementa la búsqueda por instructor
func (r *ScheduleRepositoryImpl) GetByInstructor(ctx context.Context, instructorID uuid.UUID, date time.Time) ([]*entities.Schedule, error) {
	var modelList []models.ScheduleModel

	if err := r.db.WithContext(ctx).
		Where("instructor_id = ? AND start_date <= ? AND end_date >= ?", instructorID, date, date).
		Preload("AcademicGroup.AcademicProgram").
		Preload("Venue.Campus").
		Find(&modelList).Error; err != nil {
		return nil, fmt.Errorf("error getting schedules by instructor: %w", err)
	}

	schedules := make([]*entities.Schedule, len(modelList))
	for i, model := range modelList {
		schedules[i] = model.ToEntity()
	}

	return schedules, nil
}

// GetByAcademicGroup implementa la búsqueda por grupo académico
func (r *ScheduleRepositoryImpl) GetByAcademicGroup(ctx context.Context, groupID uuid.UUID, startDate, endDate time.Time) ([]*entities.Schedule, error) {
	var modelList []models.ScheduleModel

	query := r.db.WithContext(ctx).Where("academic_group_id = ?", groupID)

	if !startDate.IsZero() {
		query = query.Where("start_date >= ?", startDate)
	}
	if !endDate.IsZero() {
		query = query.Where("end_date <= ?", endDate)
	}

	if err := query.
		Preload("AcademicGroup.AcademicProgram").
		Preload("Venue.Campus").
		Find(&modelList).Error; err != nil {
		return nil, fmt.Errorf("error getting schedules by academic group: %w", err)
	}

	schedules := make([]*entities.Schedule, len(modelList))
	for i, model := range modelList {
		schedules[i] = model.ToEntity()
	}

	return schedules, nil
}

// GetByVenue implementa la búsqueda por venue
func (r *ScheduleRepositoryImpl) GetByVenue(ctx context.Context, venueID uuid.UUID, date time.Time) ([]*entities.Schedule, error) {
	var modelList []models.ScheduleModel

	if err := r.db.WithContext(ctx).
		Where("venue_id = ? AND start_date <= ? AND end_date >= ?", venueID, date, date).
		Preload("AcademicGroup.AcademicProgram").
		Preload("Venue.Campus").
		Find(&modelList).Error; err != nil {
		return nil, fmt.Errorf("error getting schedules by venue: %w", err)
	}

	schedules := make([]*entities.Schedule, len(modelList))
	for i, model := range modelList {
		schedules[i] = model.ToEntity()
	}

	return schedules, nil
}

// CheckInstructorConflict verifica conflictos de instructor
func (r *ScheduleRepositoryImpl) CheckInstructorConflict(ctx context.Context, instructorID uuid.UUID, dayOfWeek int, startTime, endTime time.Time, excludeID *uuid.UUID) (bool, error) {
	var count int64

	query := r.db.WithContext(ctx).Model(&models.ScheduleModel{}).
		Where("instructor_id = ? AND day_of_week = ? AND is_active = true", instructorID, dayOfWeek).
		Where("(start_time < ? AND end_time > ?) OR (start_time < ? AND end_time > ?) OR (start_time >= ? AND end_time <= ?)",
			endTime, startTime, startTime, endTime, startTime, endTime)

	if excludeID != nil {
		query = query.Where("id != ?", *excludeID)
	}

	if err := query.Count(&count).Error; err != nil {
		return false, fmt.Errorf("error checking instructor conflict: %w", err)
	}

	return count > 0, nil
}

// CheckVenueConflict verifica conflictos de venue
func (r *ScheduleRepositoryImpl) CheckVenueConflict(ctx context.Context, venueID uuid.UUID, dayOfWeek int, startTime, endTime time.Time, excludeID *uuid.UUID) (bool, error) {
	var count int64

	query := r.db.WithContext(ctx).Model(&models.ScheduleModel{}).
		Where("venue_id = ? AND day_of_week = ? AND is_active = true", venueID, dayOfWeek).
		Where("(start_time < ? AND end_time > ?) OR (start_time < ? AND end_time > ?) OR (start_time >= ? AND end_time <= ?)",
			endTime, startTime, startTime, endTime, startTime, endTime)

	if excludeID != nil {
		query = query.Where("id != ?", *excludeID)
	}

	if err := query.Count(&count).Error; err != nil {
		return false, fmt.Errorf("error checking venue conflict: %w", err)
	}

	return count > 0, nil
}

// CheckGroupConflict verifica conflictos de grupo
func (r *ScheduleRepositoryImpl) CheckGroupConflict(ctx context.Context, groupID uuid.UUID, dayOfWeek int, startTime, endTime time.Time, excludeID *uuid.UUID) (bool, error) {
	var count int64

	query := r.db.WithContext(ctx).Model(&models.ScheduleModel{}).
		Where("academic_group_id = ? AND day_of_week = ? AND is_active = true", groupID, dayOfWeek).
		Where("(start_time < ? AND end_time > ?) OR (start_time < ? AND end_time > ?) OR (start_time >= ? AND end_time <= ?)",
			endTime, startTime, startTime, endTime, startTime, endTime)

	if excludeID != nil {
		query = query.Where("id != ?", *excludeID)
	}

	if err := query.Count(&count).Error; err != nil {
		return false, fmt.Errorf("error checking group conflict: %w", err)
	}

	return count > 0, nil
}

// CreateBatch implementa la creación masiva
func (r *ScheduleRepositoryImpl) CreateBatch(ctx context.Context, schedules []*entities.Schedule) ([]*entities.Schedule, error) {
	if len(schedules) == 0 {
		return []*entities.Schedule{}, nil
	}

	models := make([]models.ScheduleModel, len(schedules))
	for i, schedule := range schedules {
		models[i].FromEntity(schedule)
	}

	if err := r.db.WithContext(ctx).CreateInBatches(models, 100).Error; err != nil {
		return nil, fmt.Errorf("error creating schedules batch: %w", err)
	}

	// Retornar entidades creadas
	result := make([]*entities.Schedule, len(models))
	for i, model := range models {
		result[i] = model.ToEntity()
	}

	return result, nil
}

// UpdateBatch implementa la actualización masiva
func (r *ScheduleRepositoryImpl) UpdateBatch(ctx context.Context, schedules []*entities.Schedule) ([]*entities.Schedule, error) {
	if len(schedules) == 0 {
		return []*entities.Schedule{}, nil
	}

	// GORM no tiene UpdateInBatches, así que actualizamos uno por uno en transacción
	tx := r.db.WithContext(ctx).Begin()
	if tx.Error != nil {
		return nil, fmt.Errorf("error starting transaction: %w", tx.Error)
	}

	defer func() {
		if r := recover(); r != nil {
			tx.Rollback()
		}
	}()

	result := make([]*entities.Schedule, len(schedules))
	for i, schedule := range schedules {
		model := &models.ScheduleModel{}
		model.FromEntity(schedule)

		if err := tx.Where("id = ?", schedule.ID).Updates(model).Error; err != nil {
			tx.Rollback()
			return nil, fmt.Errorf("error updating schedule %s: %w", schedule.ID, err)
		}

		result[i] = model.ToEntity()
	}

	if err := tx.Commit().Error; err != nil {
		return nil, fmt.Errorf("error committing batch update: %w", err)
	}

	return result, nil
}

// DeleteBatch implementa la eliminación masiva
func (r *ScheduleRepositoryImpl) DeleteBatch(ctx context.Context, ids []uuid.UUID) error {
	if len(ids) == 0 {
		return nil
	}

	if err := r.db.WithContext(ctx).Delete(&models.ScheduleModel{}, "id IN ?", ids).Error; err != nil {
		return fmt.Errorf("error deleting schedules batch: %w", err)
	}

	return nil
}
