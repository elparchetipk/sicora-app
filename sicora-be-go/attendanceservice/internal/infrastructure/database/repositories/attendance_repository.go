package repositories

import (
	"context"
	"database/sql"
	"time"

	"attendanceservice/internal/domain/entities"
	"attendanceservice/internal/domain/repositories"
	"attendanceservice/internal/infrastructure/database/models"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

const (
	dateFormat      = "2006-01-02"
	dateDescOrder   = "date DESC"
	statusCondition = "status = ?"
)

type attendanceRepository struct {
	db *gorm.DB
}

// NewAttendanceRepository crea una nueva instancia del repositorio de asistencia
func NewAttendanceRepository(db *gorm.DB) repositories.AttendanceRepository {
	return &attendanceRepository{db: db}
}

// Create crea un nuevo registro de asistencia
func (r *attendanceRepository) Create(ctx context.Context, attendance *entities.AttendanceRecord) error {
	model := r.mapToModel(attendance)
	return r.db.WithContext(ctx).Create(model).Error
}

// GetByID obtiene un registro de asistencia por ID
func (r *attendanceRepository) GetByID(ctx context.Context, id uuid.UUID) (*entities.AttendanceRecord, error) {
	var model models.AttendanceRecord
	err := r.db.WithContext(ctx).First(&model, "id = ?", id).Error
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, err
	}
	return r.mapToEntity(&model), nil
}

// GetByUserAndDate obtiene un registro de asistencia por usuario y fecha
func (r *attendanceRepository) GetByUserAndDate(ctx context.Context, userID uuid.UUID, date time.Time) (*entities.AttendanceRecord, error) {
	var model models.AttendanceRecord
	err := r.db.WithContext(ctx).
		Where("student_id = ? AND date = ?", userID, date.Format(dateFormat)).
		First(&model).Error
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, err
	}
	return r.mapToEntity(&model), nil
}

// GetByDateRange obtiene registros de asistencia por rango de fechas
func (r *attendanceRepository) GetByDateRange(ctx context.Context, userID uuid.UUID, startDate, endDate time.Time) ([]*entities.AttendanceRecord, error) {
	var models []models.AttendanceRecord
	err := r.db.WithContext(ctx).
		Where("student_id = ? AND date BETWEEN ? AND ?", userID, startDate.Format(dateFormat), endDate.Format(dateFormat)).
		Order(dateDescOrder).
		Find(&models).Error
	if err != nil {
		return nil, err
	}

	entities := make([]*entities.AttendanceRecord, len(models))
	for i, model := range models {
		entities[i] = r.mapToEntity(&model)
	}
	return entities, nil
}

// GetByScheduleID obtiene registros de asistencia por ID de horario
func (r *attendanceRepository) GetByScheduleID(ctx context.Context, scheduleID uuid.UUID) ([]*entities.AttendanceRecord, error) {
	var models []models.AttendanceRecord
	err := r.db.WithContext(ctx).
		Where("schedule_id = ?", scheduleID).
		Order("date DESC").
		Find(&models).Error
	if err != nil {
		return nil, err
	}

	entities := make([]*entities.AttendanceRecord, len(models))
	for i, model := range models {
		entities[i] = r.mapToEntity(&model)
	}
	return entities, nil
}

// Update actualiza un registro de asistencia
func (r *attendanceRepository) Update(ctx context.Context, attendance *entities.AttendanceRecord) error {
	model := r.mapToModel(attendance)
	return r.db.WithContext(ctx).Save(model).Error
}

// Delete elimina un registro de asistencia
func (r *attendanceRepository) Delete(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&models.AttendanceRecord{}, id).Error
}

// GetAttendanceSummary obtiene un resumen de asistencia
func (r *attendanceRepository) GetAttendanceSummary(ctx context.Context, userID uuid.UUID, startDate, endDate time.Time) (*entities.AttendanceSummary, error) {
	summary := &entities.AttendanceSummary{
		UserID:    userID,
		StartDate: startDate,
		EndDate:   endDate,
	}

	// Obtener conteos por estado
	var result struct {
		TotalScheduled    int64
		TotalPresent      int64
		TotalAbsent       int64
		TotalJustified    int64
		TotalLate         int64
		AverageLateness   float64
		ConsecutiveAbsent int64
	}

	query := r.db.WithContext(ctx).Model(&models.AttendanceRecord{}).
		Where("student_id = ? AND date BETWEEN ? AND ?", userID, startDate.Format("2006-01-02"), endDate.Format("2006-01-02"))

	// Contar total programado (asumiendo que hay un registro para cada día programado)
	query.Count(&result.TotalScheduled)

	// Contar por estado
	query.Where("status = ?", "PRESENT").Count(&result.TotalPresent)
	query.Where("status = ?", "ABSENT").Count(&result.TotalAbsent)
	query.Where("status = ?", "JUSTIFIED").Count(&result.TotalJustified)
	query.Where("status = ?", "LATE").Count(&result.TotalLate)

	// Calcular promedio de tardanzas (simplificado)
	var avgLateness sql.NullFloat64
	r.db.WithContext(ctx).Model(&models.AttendanceRecord{}).
		Select("AVG(EXTRACT(EPOCH FROM (check_in_time - date)) / 60) as average_lateness").
		Where("student_id = ? AND status = 'LATE' AND date BETWEEN ? AND ?", userID, startDate.Format("2006-01-02"), endDate.Format("2006-01-02")).
		Scan(&avgLateness)

	if avgLateness.Valid {
		result.AverageLateness = avgLateness.Float64
	}

	// Calcular ausencias consecutivas (simplificado)
	var consecutiveAbsent int64
	r.db.WithContext(ctx).Raw(`
		WITH consecutive_absences AS (
			SELECT 
				ROW_NUMBER() OVER (ORDER BY date) - 
				ROW_NUMBER() OVER (PARTITION BY status ORDER BY date) as grp,
				status,
				COUNT(*) OVER (PARTITION BY status, ROW_NUMBER() OVER (ORDER BY date) - ROW_NUMBER() OVER (PARTITION BY status ORDER BY date)) as consecutive_count
			FROM attendance_records 
			WHERE student_id = ? AND date BETWEEN ? AND ?
			ORDER BY date DESC
		)
		SELECT COALESCE(MAX(consecutive_count), 0) as consecutive_absent
		FROM consecutive_absences 
		WHERE status = 'ABSENT'
	`, userID, startDate.Format("2006-01-02"), endDate.Format("2006-01-02")).Scan(&consecutiveAbsent)

	// Mapear resultados
	summary.TotalScheduled = int(result.TotalScheduled)
	summary.TotalPresent = int(result.TotalPresent)
	summary.TotalAbsent = int(result.TotalAbsent)
	summary.TotalJustified = int(result.TotalJustified)
	summary.TotalLate = int(result.TotalLate)
	summary.AverageLateness = result.AverageLateness
	summary.ConsecutiveAbsent = int(consecutiveAbsent)

	// Calcular tasas
	summary.CalculateRates()

	return summary, nil
}

// GetLateArrivals obtiene registros de llegadas tardías
func (r *attendanceRepository) GetLateArrivals(ctx context.Context, userID uuid.UUID, startDate, endDate time.Time) ([]*entities.AttendanceRecord, error) {
	var models []models.AttendanceRecord
	err := r.db.WithContext(ctx).
		Where("student_id = ? AND status = 'LATE' AND date BETWEEN ? AND ?", userID, startDate.Format("2006-01-02"), endDate.Format("2006-01-02")).
		Order("date DESC").
		Find(&models).Error
	if err != nil {
		return nil, err
	}

	entities := make([]*entities.AttendanceRecord, len(models))
	for i, model := range models {
		entities[i] = r.mapToEntity(&model)
	}
	return entities, nil
}

// GetAbsences obtiene registros de ausencias
func (r *attendanceRepository) GetAbsences(ctx context.Context, userID uuid.UUID, startDate, endDate time.Time) ([]*entities.AttendanceRecord, error) {
	var models []models.AttendanceRecord
	err := r.db.WithContext(ctx).
		Where("student_id = ? AND status = 'ABSENT' AND date BETWEEN ? AND ?", userID, startDate.Format("2006-01-02"), endDate.Format("2006-01-02")).
		Order("date DESC").
		Find(&models).Error
	if err != nil {
		return nil, err
	}

	entities := make([]*entities.AttendanceRecord, len(models))
	for i, model := range models {
		entities[i] = r.mapToEntity(&model)
	}
	return entities, nil
}

// BulkCreate crea múltiples registros de asistencia
func (r *attendanceRepository) BulkCreate(ctx context.Context, attendances []*entities.AttendanceRecord) error {
	models := make([]models.AttendanceRecord, len(attendances))
	for i, attendance := range attendances {
		models[i] = *r.mapToModel(attendance)
	}
	return r.db.WithContext(ctx).CreateInBatches(models, 100).Error
}

// mapToModel convierte una entidad a modelo GORM
func (r *attendanceRepository) mapToModel(entity *entities.AttendanceRecord) *models.AttendanceRecord {
	return &models.AttendanceRecord{
		ID:           entity.ID,
		StudentID:    entity.StudentID,
		ScheduleID:   entity.ScheduleID,
		InstructorID: entity.InstructorID,
		Date:         entity.Date,
		Status:       string(entity.Status),
		CheckInTime:  entity.CheckInTime,
		QRCodeData:   entity.QRCodeData,
		Notes:        entity.Notes,
		IsActive:     entity.IsActive,
		CreatedAt:    entity.CreatedAt,
		UpdatedAt:    entity.UpdatedAt,
	}
}

// mapToEntity convierte un modelo GORM a entidad
func (r *attendanceRepository) mapToEntity(model *models.AttendanceRecord) *entities.AttendanceRecord {
	return &entities.AttendanceRecord{
		ID:           model.ID,
		StudentID:    model.StudentID,
		ScheduleID:   model.ScheduleID,
		InstructorID: model.InstructorID,
		Date:         model.Date,
		Status:       entities.AttendanceStatus(model.Status),
		CheckInTime:  model.CheckInTime,
		QRCodeData:   model.QRCodeData,
		Notes:        model.Notes,
		IsActive:     model.IsActive,
		CreatedAt:    model.CreatedAt,
		UpdatedAt:    model.UpdatedAt,
	}
}
