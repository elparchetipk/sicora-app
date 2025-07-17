package repositories

import (
	"context"
	"time"

	"attendanceservice/internal/domain/entities"

	"github.com/google/uuid"
)

// QRCodeRepository define la interfaz para operaciones con códigos QR
type QRCodeRepository interface {
	// Create crea un nuevo código QR
	Create(ctx context.Context, qrCode *entities.AttendanceQRCode) error
	
	// GetByID obtiene un código QR por su ID
	GetByID(ctx context.Context, id uuid.UUID) (*entities.AttendanceQRCode, error)
	
	// GetByCode obtiene un código QR por su código
	GetByCode(ctx context.Context, code string) (*entities.AttendanceQRCode, error)
	
	// GetActiveByStudent obtiene el código QR activo de un estudiante para un horario
	GetActiveByStudent(ctx context.Context, studentID, scheduleID uuid.UUID) (*entities.AttendanceQRCode, error)
	
	// GetByStudentAndSchedule obtiene todos los códigos QR de un estudiante para un horario
	GetByStudentAndSchedule(ctx context.Context, studentID, scheduleID uuid.UUID) ([]*entities.AttendanceQRCode, error)
	
	// Update actualiza un código QR
	Update(ctx context.Context, qrCode *entities.AttendanceQRCode) error
	
	// Delete elimina un código QR (soft delete)
	Delete(ctx context.Context, id uuid.UUID) error
	
	// ExpireOldCodes marca como expirados los códigos que han sobrepasado su tiempo
	ExpireOldCodes(ctx context.Context) error
	
	// GetExpiredCodes obtiene códigos QR expirados para limpieza
	GetExpiredCodes(ctx context.Context, olderThan time.Time) ([]*entities.AttendanceQRCode, error)
	
	// BulkCreate crea múltiples códigos QR
	BulkCreate(ctx context.Context, qrCodes []*entities.AttendanceQRCode) error
	
	// GetActiveBySchedule obtiene todos los códigos QR activos para un horario
	GetActiveBySchedule(ctx context.Context, scheduleID uuid.UUID) ([]*entities.AttendanceQRCode, error)
	
	// DeactivateByStudent desactiva todos los códigos QR de un estudiante
	DeactivateByStudent(ctx context.Context, studentID uuid.UUID) error
	
	// GetUsageStats obtiene estadísticas de uso de códigos QR
	GetUsageStats(ctx context.Context, scheduleID uuid.UUID, startDate, endDate time.Time) (*QRUsageStats, error)
}

// QRUsageStats representa estadísticas de uso de códigos QR
type QRUsageStats struct {
	ScheduleID        uuid.UUID `json:"schedule_id"`
	TotalGenerated    int64     `json:"total_generated"`
	TotalUsed         int64     `json:"total_used"`
	TotalExpired      int64     `json:"total_expired"`
	AverageUsageTime  float64   `json:"average_usage_time_seconds"`
	PeakUsageHour     int       `json:"peak_usage_hour"`
	UsageByDay        map[string]int `json:"usage_by_day"`
	UsageRate         float64   `json:"usage_rate_percent"`
}
