package entities

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// AnalyticsEvent represents a generic analytics event
type AnalyticsEvent struct {
	ID           uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	TenantID     string         `gorm:"type:varchar(100);not null;index" json:"tenant_id"`
	ResourceType string         `gorm:"type:varchar(50);not null;index" json:"resource_type"` // "document" or "faq"
	ResourceID   string         `gorm:"type:varchar(100);not null;index" json:"resource_id"`
	Action       string         `gorm:"type:varchar(50);not null;index" json:"action"` // "view", "download", "search", "rating"
	UserID       string         `gorm:"type:varchar(100);index" json:"user_id,omitempty"`
	SessionID    string         `gorm:"type:varchar(100);index" json:"session_id,omitempty"`
	IPAddress    string         `gorm:"type:varchar(45)" json:"ip_address,omitempty"`
	UserAgent    string         `gorm:"type:text" json:"user_agent,omitempty"`
	Metadata     string         `gorm:"type:jsonb" json:"metadata,omitempty"` // Additional metadata as JSON
	Timestamp    time.Time      `gorm:"default:current_timestamp;not null;index" json:"timestamp"`
	CreatedAt    time.Time      `gorm:"default:current_timestamp" json:"created_at"`
	UpdatedAt    time.Time      `gorm:"default:current_timestamp" json:"updated_at"`
	DeletedAt    gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`
}

// TableName returns the table name for AnalyticsEvent
func (AnalyticsEvent) TableName() string {
	return "analytics_events"
}

// SearchAnalytics represents search analytics data
type SearchAnalytics struct {
	ID           uuid.UUID      `gorm:"type:uuid;primary_key;default:gen_random_uuid()" json:"id"`
	TenantID     string         `gorm:"type:varchar(100);not null;index" json:"tenant_id"`
	Query        string         `gorm:"type:text;not null" json:"query"`
	ResultsFound int            `gorm:"default:0" json:"results_found"`
	UserID       string         `gorm:"type:varchar(100);index" json:"user_id,omitempty"`
	SessionID    string         `gorm:"type:varchar(100);index" json:"session_id,omitempty"`
	SearchType   string         `gorm:"type:varchar(50);default:'text'" json:"search_type"` // "text", "semantic", "hybrid"
	Category     string         `gorm:"type:varchar(100);index" json:"category,omitempty"`
	Filters      string         `gorm:"type:jsonb" json:"filters,omitempty"` // Applied filters as JSON
	ResponseTime float64        `gorm:"default:0" json:"response_time"`      // Response time in milliseconds
	Timestamp    time.Time      `gorm:"default:current_timestamp;not null;index" json:"timestamp"`
	CreatedAt    time.Time      `gorm:"default:current_timestamp" json:"created_at"`
	UpdatedAt    time.Time      `gorm:"default:current_timestamp" json:"updated_at"`
	DeletedAt    gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`
}

// TableName returns the table name for SearchAnalytics
func (SearchAnalytics) TableName() string {
	return "search_analytics"
}
