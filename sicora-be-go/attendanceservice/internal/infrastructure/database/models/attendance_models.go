package models

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// AttendanceRecord modelo GORM para registros de asistencia
type AttendanceRecord struct {
	ID           uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	StudentID    uuid.UUID      `gorm:"type:uuid;not null;index" json:"student_id"`
	ScheduleID   uuid.UUID      `gorm:"type:uuid;not null;index" json:"schedule_id"`
	InstructorID uuid.UUID      `gorm:"type:uuid;not null;index" json:"instructor_id"`
	Date         time.Time      `gorm:"type:date;not null;index" json:"date"`
	Status       string         `gorm:"type:varchar(20);not null;check:status IN ('PRESENT','ABSENT','JUSTIFIED','LATE')" json:"status"`
	CheckInTime  *time.Time     `gorm:"type:timestamp" json:"check_in_time"`
	QRCodeID     *uuid.UUID     `gorm:"type:uuid;index" json:"qr_code_id"`
	QRCodeData   string         `gorm:"type:varchar(500)" json:"qr_code_data"`
	Method       string         `gorm:"type:varchar(20);not null;check:method IN ('QR_SCAN','MANUAL');default:'MANUAL'" json:"method"`
	Notes        string         `gorm:"type:text" json:"notes"`
	IsActive     bool           `gorm:"type:boolean;default:true;not null" json:"is_active"`
	CreatedAt    time.Time      `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt    time.Time      `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"updated_at"`
	DeletedAt    gorm.DeletedAt `gorm:"index" json:"deleted_at"`
}

// TableName especifica el nombre de la tabla
func (AttendanceRecord) TableName() string {
	return "attendance_records"
}

// BeforeCreate hook de GORM ejecutado antes de crear
func (ar *AttendanceRecord) BeforeCreate(tx *gorm.DB) error {
	if ar.ID == uuid.Nil {
		ar.ID = uuid.New()
	}
	return nil
}

// Justification modelo GORM para justificaciones
type Justification struct {
	ID             uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	AttendanceID   uuid.UUID      `gorm:"type:uuid;not null;index" json:"attendance_id"`
	StudentID      uuid.UUID      `gorm:"type:uuid;not null;index" json:"student_id"`
	Reason         string         `gorm:"type:varchar(500);not null" json:"reason"`
	Description    string         `gorm:"type:text" json:"description"`
	DocumentURL    string         `gorm:"type:varchar(1000)" json:"document_url"`
	Status         string         `gorm:"type:varchar(20);not null;check:status IN ('PENDING','APPROVED','REJECTED');default:'PENDING'" json:"status"`
	ReviewedBy     *uuid.UUID     `gorm:"type:uuid" json:"reviewed_by"`
	ReviewDate     *time.Time     `gorm:"type:timestamp" json:"review_date"`
	ReviewComments string         `gorm:"type:text" json:"review_comments"`
	IsActive       bool           `gorm:"type:boolean;default:true;not null" json:"is_active"`
	CreatedAt      time.Time      `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt      time.Time      `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"updated_at"`
	DeletedAt      gorm.DeletedAt `gorm:"index" json:"deleted_at"`

	// Relaciones
	AttendanceRecord *AttendanceRecord `gorm:"foreignKey:AttendanceID" json:"attendance_record,omitempty"`
}

// TableName especifica el nombre de la tabla
func (Justification) TableName() string {
	return "justifications"
}

// BeforeCreate hook de GORM ejecutado antes de crear
func (j *Justification) BeforeCreate(tx *gorm.DB) error {
	if j.ID == uuid.Nil {
		j.ID = uuid.New()
	}
	return nil
}

// AttendanceAlert modelo GORM para alertas de asistencia
type AttendanceAlert struct {
	ID          uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	StudentID   uuid.UUID      `gorm:"type:uuid;not null;index" json:"student_id"`
	Type        string         `gorm:"type:varchar(20);not null;check:type IN ('ABSENCE','LATE','PATTERN','CONSECUTIVE','PERCENTAGE','CUSTOM')" json:"type"`
	Level       string         `gorm:"type:varchar(20);not null;check:level IN ('LOW','MEDIUM','HIGH','CRITICAL')" json:"level"`
	Title       string         `gorm:"type:varchar(200);not null" json:"title"`
	Description string         `gorm:"type:text;not null" json:"description"`
	Metadata    string         `gorm:"type:jsonb" json:"metadata"`
	IsRead      bool           `gorm:"type:boolean;default:false;not null" json:"is_read"`
	ReadBy      *uuid.UUID     `gorm:"type:uuid" json:"read_by"`
	ReadAt      *time.Time     `gorm:"type:timestamp" json:"read_at"`
	IsActive    bool           `gorm:"type:boolean;default:true;not null" json:"is_active"`
	CreatedAt   time.Time      `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt   time.Time      `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"updated_at"`
	DeletedAt   gorm.DeletedAt `gorm:"index" json:"deleted_at"`
}

// TableName especifica el nombre de la tabla
func (AttendanceAlert) TableName() string {
	return "attendance_alerts"
}

// BeforeCreate hook de GORM ejecutado antes de crear
func (aa *AttendanceAlert) BeforeCreate(tx *gorm.DB) error {
	if aa.ID == uuid.Nil {
		aa.ID = uuid.New()
	}
	return nil
}

// AttendanceQRCode modelo GORM para códigos QR de asistencia
type AttendanceQRCode struct {
	ID          uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	StudentID   uuid.UUID      `gorm:"type:uuid;not null;index" json:"student_id"`
	ScheduleID  uuid.UUID      `gorm:"type:uuid;not null;index" json:"schedule_id"`
	Code        string         `gorm:"type:varchar(500);not null;unique;index" json:"code"`
	Status      string         `gorm:"type:varchar(20);not null;check:status IN ('ACTIVE','EXPIRED','USED');default:'ACTIVE'" json:"status"`
	ExpiresAt   time.Time      `gorm:"type:timestamp;not null;index" json:"expires_at"`
	UsedAt      *time.Time     `gorm:"type:timestamp" json:"used_at"`
	ScannerID   *uuid.UUID     `gorm:"type:uuid" json:"scanner_id"`
	Location    string         `gorm:"type:varchar(255)" json:"location"`
	IsActive    bool           `gorm:"type:boolean;default:true;not null" json:"is_active"`
	CreatedAt   time.Time      `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt   time.Time      `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"updated_at"`
	DeletedAt   gorm.DeletedAt `gorm:"index" json:"deleted_at"`
}

// TableName especifica el nombre de la tabla
func (AttendanceQRCode) TableName() string {
	return "attendance_qrcodes"
}

// BeforeCreate hook de GORM ejecutado antes de crear
func (qr *AttendanceQRCode) BeforeCreate(tx *gorm.DB) error {
	if qr.ID == uuid.Nil {
		qr.ID = uuid.New()
	}
	return nil
}
