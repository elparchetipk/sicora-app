package dtos

import (
	"time"

	"github.com/google/uuid"
)

type NotificationCreateRequest struct {
	Type       string                 `json:"type" binding:"required"`
	Title      string                 `json:"title" binding:"required,min=1,max=255"`
	Message    string                 `json:"message" binding:"required,min=1,max=2000"`
	Recipient  uuid.UUID              `json:"recipient" binding:"required"`
	EntityType string                 `json:"entity_type"`
	EntityID   *uuid.UUID             `json:"entity_id"`
	Metadata   map[string]interface{} `json:"metadata"`
}

type NotificationUpdateRequest struct {
	Title    string                 `json:"title" binding:"required,min=1,max=255"`
	Message  string                 `json:"message" binding:"required,min=1,max=2000"`
	Metadata map[string]interface{} `json:"metadata"`
}

type NotificationResponse struct {
	ID         uuid.UUID              `json:"id"`
	Type       string                 `json:"type"`
	Title      string                 `json:"title"`
	Message    string                 `json:"message"`
	Recipient  uuid.UUID              `json:"recipient"`
	EntityType string                 `json:"entity_type"`
	EntityID   *uuid.UUID             `json:"entity_id"`
	Metadata   map[string]interface{} `json:"metadata"`
	IsRead     bool                   `json:"is_read"`
	IsSent     bool                   `json:"is_sent"`
	SentAt     *time.Time             `json:"sent_at"`
	ReadAt     *time.Time             `json:"read_at"`
	CreatedAt  time.Time              `json:"created_at"`
	UpdatedAt  time.Time              `json:"updated_at"`
}

type NotificationFilterRequest struct {
	Recipient  *uuid.UUID `form:"recipient"`
	Type       *string    `form:"type"`
	EntityType *string    `form:"entity_type"`
	EntityID   *uuid.UUID `form:"entity_id"`
	IsRead     *bool      `form:"is_read"`
	IsSent     *bool      `form:"is_sent"`
	StartDate  *string    `form:"start_date"`
	EndDate    *string    `form:"end_date"`
	Page       int        `form:"page" binding:"min=1"`
	PageSize   int        `form:"page_size" binding:"min=1,max=100"`
}

type NotificationStatsResponse struct {
	TotalNotifications  int64   `json:"total_notifications"`
	ReadNotifications   int64   `json:"read_notifications"`
	UnreadNotifications int64   `json:"unread_notifications"`
	SentNotifications   int64   `json:"sent_notifications"`
	ReadRate            float64 `json:"read_rate"`
	DeliveryRate        float64 `json:"delivery_rate"`
}

type NotificationBulkMarkReadRequest struct {
	NotificationIDs []uuid.UUID `json:"notification_ids" binding:"required"`
}

type NotificationBulkCreateRequest struct {
	Type        string                 `json:"type" binding:"required"`
	Title       string                 `json:"title" binding:"required,min=1,max=255"`
	Message     string                 `json:"message" binding:"required,min=1,max=2000"`
	Recipients  []uuid.UUID            `json:"recipients" binding:"required"`
	EntityType  string                 `json:"entity_type"`
	EntityID    *uuid.UUID             `json:"entity_id"`
	Metadata    map[string]interface{} `json:"metadata"`
	SendInstant bool                   `json:"send_instant"`
}

type NotificationPreferencesRequest struct {
	Types []string `json:"types" binding:"required"`
	Email bool     `json:"email"`
	InApp bool     `json:"in_app"`
	SMS   bool     `json:"sms"`
	Push  bool     `json:"push"`
}

type NotificationPreferencesResponse struct {
	UserID uuid.UUID                     `json:"user_id"`
	Types  map[string]NotificationMethod `json:"types"`
}

type NotificationMethod struct {
	Email bool `json:"email"`
	InApp bool `json:"in_app"`
	SMS   bool `json:"sms"`
	Push  bool `json:"push"`
}
