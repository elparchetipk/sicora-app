package repositories

import (
	"context"
	"time"

	"attendanceservice/internal/domain/entities"

	"github.com/google/uuid"
)

type AttendanceRepository interface {
	Create(ctx context.Context, attendance *entities.AttendanceRecord) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.AttendanceRecord, error)
	GetByUserAndDate(ctx context.Context, userID uuid.UUID, date time.Time) (*entities.AttendanceRecord, error)
	GetByDateRange(ctx context.Context, userID uuid.UUID, startDate, endDate time.Time) ([]*entities.AttendanceRecord, error)
	GetByScheduleID(ctx context.Context, scheduleID uuid.UUID) ([]*entities.AttendanceRecord, error)
	Update(ctx context.Context, attendance *entities.AttendanceRecord) error
	Delete(ctx context.Context, id uuid.UUID) error
	GetAttendanceSummary(ctx context.Context, userID uuid.UUID, startDate, endDate time.Time) (*entities.AttendanceSummary, error)
	GetLateArrivals(ctx context.Context, userID uuid.UUID, startDate, endDate time.Time) ([]*entities.AttendanceRecord, error)
	GetAbsences(ctx context.Context, userID uuid.UUID, startDate, endDate time.Time) ([]*entities.AttendanceRecord, error)
	BulkCreate(ctx context.Context, attendances []*entities.AttendanceRecord) error
}

type JustificationRepository interface {
	Create(ctx context.Context, justification *entities.Justification) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.Justification, error)
	GetByAttendanceID(ctx context.Context, attendanceID uuid.UUID) (*entities.Justification, error)
	GetByUserID(ctx context.Context, userID uuid.UUID, limit, offset int) ([]*entities.Justification, error)
	Update(ctx context.Context, justification *entities.Justification) error
	Delete(ctx context.Context, id uuid.UUID) error
	GetPendingJustifications(ctx context.Context, limit, offset int) ([]*entities.Justification, error)
	ApproveJustification(ctx context.Context, id uuid.UUID, approverID uuid.UUID) error
	RejectJustification(ctx context.Context, id uuid.UUID, approverID uuid.UUID, reason string) error
}

type AttendanceAlertRepository interface {
	Create(ctx context.Context, alert *entities.AttendanceAlert) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.AttendanceAlert, error)
	GetByUserID(ctx context.Context, userID uuid.UUID, limit, offset int) ([]*entities.AttendanceAlert, error)
	GetActiveAlerts(ctx context.Context, limit, offset int) ([]*entities.AttendanceAlert, error)
	Update(ctx context.Context, alert *entities.AttendanceAlert) error
	Delete(ctx context.Context, id uuid.UUID) error
	MarkAsRead(ctx context.Context, id uuid.UUID) error
	GetUnreadCount(ctx context.Context, userID uuid.UUID) (int, error)
}
