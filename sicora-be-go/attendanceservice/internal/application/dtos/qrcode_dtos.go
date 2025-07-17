package dtos

import (
	"time"

	"github.com/google/uuid"
)

// QRCodeRequest representa la solicitud para generar un código QR
type QRCodeRequest struct {
	StudentID  uuid.UUID `json:"student_id" binding:"required"`
	ScheduleID uuid.UUID `json:"schedule_id" binding:"required"`
}

// QRCodeResponse representa la respuesta con el código QR generado
type QRCodeResponse struct {
	ID          uuid.UUID `json:"id"`
	StudentID   uuid.UUID `json:"student_id"`
	ScheduleID  uuid.UUID `json:"schedule_id"`
	Code        string    `json:"code"`
	Status      string    `json:"status"`
	ExpiresAt   time.Time `json:"expires_at"`
	ExpiresIn   int       `json:"expires_in_seconds"` // Segundos hasta expirar
	IsActive    bool      `json:"is_active"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

// QRScanRequest representa la solicitud para escanear un código QR
type QRScanRequest struct {
	Code         string     `json:"code" binding:"required"`
	InstructorID uuid.UUID  `json:"instructor_id" binding:"required"`
	Location     string     `json:"location,omitempty"`
	Latitude     *float64   `json:"latitude,omitempty"`
	Longitude    *float64   `json:"longitude,omitempty"`
	ScanTime     *time.Time `json:"scan_time,omitempty"`
}

// QRScanResponse representa la respuesta del escaneo de QR
type QRScanResponse struct {
	Success          bool                   `json:"success"`
	Message          string                 `json:"message"`
	AttendanceRecord *AttendanceResponse    `json:"attendance_record,omitempty"`
	StudentInfo      *StudentInfoResponse   `json:"student_info,omitempty"`
	ScanDetails      *QRScanDetailsResponse `json:"scan_details,omitempty"`
}

// StudentInfoResponse información básica del estudiante
type StudentInfoResponse struct {
	ID        uuid.UUID `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email,omitempty"`
	Code      string    `json:"code,omitempty"`
	Photo     string    `json:"photo,omitempty"`
}

// QRScanDetailsResponse detalles del escaneo realizado
type QRScanDetailsResponse struct {
	QRCodeID     uuid.UUID  `json:"qr_code_id"`
	ScanTime     time.Time  `json:"scan_time"`
	Location     string     `json:"location,omitempty"`
	Latitude     *float64   `json:"latitude,omitempty"`
	Longitude    *float64   `json:"longitude,omitempty"`
	InstructorID uuid.UUID  `json:"instructor_id"`
	Method       string     `json:"method"`
	WasExpired   bool       `json:"was_expired"`
	TimeDiff     int        `json:"time_diff_seconds"` // Diferencia con hora esperada
}

// StudentQRStatusRequest para consultar el estado del QR de un estudiante
type StudentQRStatusRequest struct {
	StudentID  uuid.UUID `json:"student_id" binding:"required"`
	ScheduleID uuid.UUID `json:"schedule_id" binding:"required"`
}

// StudentQRStatusResponse estado del QR del estudiante
type StudentQRStatusResponse struct {
	HasActiveQR      bool                `json:"has_active_qr"`
	CurrentQR        *QRCodeResponse     `json:"current_qr,omitempty"`
	NextRefresh      *time.Time          `json:"next_refresh,omitempty"`
	AttendanceStatus string              `json:"attendance_status"`
	CanGenerate      bool                `json:"can_generate"`
	Message          string              `json:"message"`
}

// InstructorScanSessionRequest para iniciar sesión de escaneo
type InstructorScanSessionRequest struct {
	InstructorID uuid.UUID `json:"instructor_id" binding:"required"`
	ScheduleID   uuid.UUID `json:"schedule_id" binding:"required"`
	Location     string    `json:"location,omitempty"`
}

// InstructorScanSessionResponse respuesta de sesión de escaneo
type InstructorScanSessionResponse struct {
	SessionID     uuid.UUID  `json:"session_id"`
	InstructorID  uuid.UUID  `json:"instructor_id"`
	ScheduleID    uuid.UUID  `json:"schedule_id"`
	Location      string     `json:"location"`
	StartTime     time.Time  `json:"start_time"`
	ExpectedCount int        `json:"expected_student_count"`
	ScannedCount  int        `json:"scanned_count"`
	IsActive      bool       `json:"is_active"`
}

// BulkQRGenerationRequest para generar códigos QR masivamente
type BulkQRGenerationRequest struct {
	ScheduleID uuid.UUID   `json:"schedule_id" binding:"required"`
	StudentIDs []uuid.UUID `json:"student_ids" binding:"required"`
}

// BulkQRGenerationResponse respuesta de generación masiva
type BulkQRGenerationResponse struct {
	ScheduleID      uuid.UUID         `json:"schedule_id"`
	TotalRequested  int               `json:"total_requested"`
	TotalGenerated  int               `json:"total_generated"`
	TotalFailed     int               `json:"total_failed"`
	GeneratedCodes  []QRCodeResponse  `json:"generated_codes"`
	FailedStudents  []uuid.UUID       `json:"failed_students,omitempty"`
	Message         string            `json:"message"`
}
