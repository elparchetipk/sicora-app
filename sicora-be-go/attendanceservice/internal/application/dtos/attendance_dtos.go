package dtos

import (
	"time"

	"github.com/google/uuid"
)

// CreateAttendanceRequest representa la solicitud para crear un registro de asistencia
type CreateAttendanceRequest struct {
	StudentID    uuid.UUID  `json:"student_id" validate:"required"`
	ScheduleID   uuid.UUID  `json:"schedule_id" validate:"required"`
	InstructorID uuid.UUID  `json:"instructor_id" validate:"required"`
	Date         time.Time  `json:"date" validate:"required"`
	Status       string     `json:"status" validate:"required,oneof=PRESENT ABSENT JUSTIFIED LATE"`
	CheckInTime  *time.Time `json:"check_in_time,omitempty"`
	QRCodeID     *uuid.UUID `json:"qr_code_id,omitempty"`
	QRCodeData   string     `json:"qr_code_data,omitempty"`
	Method       string     `json:"method" validate:"required,oneof=QR_SCAN MANUAL"`
	Notes        string     `json:"notes,omitempty"`
}

// UpdateAttendanceRequest representa la solicitud para actualizar un registro de asistencia
type UpdateAttendanceRequest struct {
	Status      *string    `json:"status,omitempty" validate:"omitempty,oneof=PRESENT ABSENT JUSTIFIED LATE"`
	CheckInTime *time.Time `json:"check_in_time,omitempty"`
	Notes       *string    `json:"notes,omitempty"`
}

// AttendanceResponse representa la respuesta de un registro de asistencia
type AttendanceResponse struct {
	ID           uuid.UUID  `json:"id"`
	StudentID    uuid.UUID  `json:"student_id"`
	ScheduleID   uuid.UUID  `json:"schedule_id"`
	InstructorID uuid.UUID  `json:"instructor_id"`
	Date         time.Time  `json:"date"`
	Status       string     `json:"status"`
	CheckInTime  *time.Time `json:"check_in_time,omitempty"`
	QRCodeID     *uuid.UUID `json:"qr_code_id,omitempty"`
	QRCodeData   string     `json:"qr_code_data,omitempty"`
	Method       string     `json:"method"`
	Notes        string     `json:"notes,omitempty"`
	IsActive     bool       `json:"is_active"`
	CreatedAt    time.Time  `json:"created_at"`
	UpdatedAt    time.Time  `json:"updated_at"`
}

// AttendanceSummaryRequest representa la solicitud para obtener un resumen de asistencia
type AttendanceSummaryRequest struct {
	UserID    uuid.UUID `json:"user_id" validate:"required"`
	StartDate time.Time `json:"start_date" validate:"required"`
	EndDate   time.Time `json:"end_date" validate:"required"`
}

// AttendanceSummaryResponse representa la respuesta del resumen de asistencia
type AttendanceSummaryResponse struct {
	UserID            uuid.UUID `json:"user_id"`
	StartDate         time.Time `json:"start_date"`
	EndDate           time.Time `json:"end_date"`
	TotalScheduled    int       `json:"total_scheduled"`
	TotalPresent      int       `json:"total_present"`
	TotalAbsent       int       `json:"total_absent"`
	TotalJustified    int       `json:"total_justified"`
	TotalLate         int       `json:"total_late"`
	AttendanceRate    float64   `json:"attendance_rate"`
	PunctualityRate   float64   `json:"punctuality_rate"`
	AverageLateness   float64   `json:"average_lateness_minutes"`
	ConsecutiveAbsent int       `json:"consecutive_absent"`
}

// BulkAttendanceRequest representa la solicitud para crear múltiples registros de asistencia
type BulkAttendanceRequest struct {
	Attendances []CreateAttendanceRequest `json:"attendances" validate:"required,min=1,dive"`
}

// QRCodeAttendanceRequest representa la solicitud para registrar asistencia via QR
type QRCodeAttendanceRequest struct {
	QRCodeData string    `json:"qr_code_data" validate:"required"`
	StudentID  uuid.UUID `json:"student_id" validate:"required"`
}

// AttendanceHistoryRequest representa la solicitud para obtener el historial de asistencia
type AttendanceHistoryRequest struct {
	UserID    uuid.UUID `json:"user_id" validate:"required"`
	StartDate time.Time `json:"start_date" validate:"required"`
	EndDate   time.Time `json:"end_date" validate:"required"`
	Status    *string   `json:"status,omitempty" validate:"omitempty,oneof=PRESENT ABSENT JUSTIFIED LATE"`
	Limit     int       `json:"limit" validate:"min=1,max=100"`
	Offset    int       `json:"offset" validate:"min=0"`
}

// AttendanceHistoryResponse representa la respuesta del historial de asistencia
type AttendanceHistoryResponse struct {
	Attendances []AttendanceResponse `json:"attendances"`
	Total       int                  `json:"total"`
	Limit       int                  `json:"limit"`
	Offset      int                  `json:"offset"`
}
