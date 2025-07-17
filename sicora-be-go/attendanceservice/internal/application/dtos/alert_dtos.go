package dtos

import (
	"time"

	"github.com/google/uuid"
)

// CreateAlertRequest representa la solicitud para crear una alerta de asistencia
type CreateAlertRequest struct {
	UserID   uuid.UUID `json:"user_id" validate:"required"`
	Type     string    `json:"type" validate:"required,oneof=ABSENCE LATE PATTERN CONSECUTIVE PERCENTAGE CUSTOM"`
	Level    string    `json:"level" validate:"required,oneof=LOW MEDIUM HIGH CRITICAL"`
	Title    string    `json:"title" validate:"required,min=5,max=200"`
	Message  string    `json:"message" validate:"required,min=10,max=1000"`
	Metadata string    `json:"metadata,omitempty"`
}

// UpdateAlertRequest representa la solicitud para actualizar una alerta
type UpdateAlertRequest struct {
	Title    *string `json:"title,omitempty" validate:"omitempty,min=5,max=200"`
	Message  *string `json:"message,omitempty" validate:"omitempty,min=10,max=1000"`
	Metadata *string `json:"metadata,omitempty"`
}

// AlertResponse representa la respuesta de una alerta de asistencia
type AlertResponse struct {
	ID        uuid.UUID  `json:"id"`
	UserID    uuid.UUID  `json:"user_id"`
	Type      string     `json:"type"`
	Level     string     `json:"level"`
	Title     string     `json:"title"`
	Message   string     `json:"message"`
	Metadata  string     `json:"metadata,omitempty"`
	IsRead    bool       `json:"is_read"`
	ReadBy    *uuid.UUID `json:"read_by,omitempty"`
	ReadAt    *time.Time `json:"read_at,omitempty"`
	IsActive  bool       `json:"is_active"`
	CreatedAt time.Time  `json:"created_at"`
	UpdatedAt time.Time  `json:"updated_at"`
}

// AlertListRequest representa la solicitud para listar alertas
type AlertListRequest struct {
	UserID   *uuid.UUID `json:"user_id,omitempty"`
	Type     *string    `json:"type,omitempty" validate:"omitempty,oneof=ABSENCE LATE PATTERN CONSECUTIVE PERCENTAGE CUSTOM"`
	Level    *string    `json:"level,omitempty" validate:"omitempty,oneof=LOW MEDIUM HIGH CRITICAL"`
	IsRead   *bool      `json:"is_read,omitempty"`
	IsActive *bool      `json:"is_active,omitempty"`
	Limit    int        `json:"limit" validate:"min=1,max=100"`
	Offset   int        `json:"offset" validate:"min=0"`
}

// AlertListResponse representa la respuesta de la lista de alertas
type AlertListResponse struct {
	Alerts []AlertResponse `json:"alerts"`
	Total  int             `json:"total"`
	Limit  int             `json:"limit"`
	Offset int             `json:"offset"`
}

// MarkAlertAsReadRequest representa la solicitud para marcar una alerta como leída
type MarkAlertAsReadRequest struct {
	UserID uuid.UUID `json:"user_id" validate:"required"`
}

// AlertStatsResponse representa las estadísticas de alertas
type AlertStatsResponse struct {
	TotalAlerts    int            `json:"total_alerts"`
	UnreadAlerts   int            `json:"unread_alerts"`
	CriticalAlerts int            `json:"critical_alerts"`
	AlertsByType   map[string]int `json:"alerts_by_type"`
	AlertsByLevel  map[string]int `json:"alerts_by_level"`
}
