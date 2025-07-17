package entities

import (
	"time"

	"github.com/google/uuid"
)

type Notification struct {
	ID         uuid.UUID              `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	Type       string                 `json:"type" gorm:"type:varchar(50);not null;index"`
	Title      string                 `json:"title" gorm:"type:varchar(255);not null"`
	Message    string                 `json:"message" gorm:"type:text;not null"`
	Recipient  uuid.UUID              `json:"recipient" gorm:"type:uuid;not null;index"`
	EntityType string                 `json:"entity_type" gorm:"type:varchar(50);index"`
	EntityID   *uuid.UUID             `json:"entity_id" gorm:"type:uuid;index"`
	Metadata   map[string]interface{} `json:"metadata" gorm:"type:jsonb"`
	IsRead     bool                   `json:"is_read" gorm:"default:false"`
	IsSent     bool                   `json:"is_sent" gorm:"default:false"`
	SentAt     *time.Time             `json:"sent_at"`
	ReadAt     *time.Time             `json:"read_at"`
	CreatedAt  time.Time              `json:"created_at" gorm:"not null;default:CURRENT_TIMESTAMP"`
	UpdatedAt  time.Time              `json:"updated_at" gorm:"not null;default:CURRENT_TIMESTAMP"`
}

func NewNotification(notificationType, title, message string, recipient uuid.UUID, entityType string, entityID *uuid.UUID, metadata map[string]interface{}) *Notification {
	return &Notification{
		ID:         uuid.New(),
		Type:       notificationType,
		Title:      title,
		Message:    message,
		Recipient:  recipient,
		EntityType: entityType,
		EntityID:   entityID,
		Metadata:   metadata,
		IsRead:     false,
		IsSent:     false,
		CreatedAt:  time.Now(),
		UpdatedAt:  time.Now(),
	}
}

func (n *Notification) MarkAsSent() {
	n.IsSent = true
	now := time.Now()
	n.SentAt = &now
	n.UpdatedAt = now
}

func (n *Notification) MarkAsRead() {
	n.IsRead = true
	now := time.Now()
	n.ReadAt = &now
	n.UpdatedAt = now
}

func (n *Notification) UpdateMetadata(metadata map[string]interface{}) {
	n.Metadata = metadata
	n.UpdatedAt = time.Now()
}

func (n *Notification) IsValid() bool {
	return n.Type != "" && n.Title != "" && n.Message != ""
}
