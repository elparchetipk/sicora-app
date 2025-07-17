package repositories

import (
	"context"
	"time"
)

// AnalyticsRepository defines the interface for analytics data operations
type AnalyticsRepository interface {
	// Basic tracking
	TrackEvent(ctx context.Context, tenantID, resourceType, resourceID, action string, metadata map[string]interface{}) error
	TrackSearch(ctx context.Context, tenantID, query string, resultsFound int, userID string) error
	
	// Resource analytics
	GetResourceViews(ctx context.Context, tenantID, resourceType, resourceID string, from, to time.Time) (int64, error)
	GetResourceDownloads(ctx context.Context, tenantID, resourceType, resourceID string, from, to time.Time) (int64, error)
	
	// Search analytics
	GetTopSearchQueries(ctx context.Context, tenantID string, limit int, from, to time.Time) ([]SearchQuery, error)
	
	// Popular content
	GetPopularResources(ctx context.Context, tenantID, resourceType string, limit int, from, to time.Time) ([]ResourceStats, error)
	
	// Dashboard
	GetDashboardStats(ctx context.Context, tenantID string, from, to time.Time) (*DashboardStats, error)
	
	// User activity
	GetUserActivity(ctx context.Context, tenantID, userID string, from, to time.Time) ([]UserActivity, error)
}

// SearchQuery represents a search query with count
type SearchQuery struct {
	Query string `json:"query"`
	Count int64  `json:"count"`
}

// ResourceStats represents resource statistics
type ResourceStats struct {
	ResourceID string `json:"resource_id"`
	Views      int64  `json:"views"`
	Downloads  int64  `json:"downloads"`
}

// DashboardStats represents dashboard statistics
type DashboardStats struct {
	TotalDocuments int64 `json:"total_documents"`
	TotalFAQs     int64 `json:"total_faqs"`
	TotalViews    int64 `json:"total_views"`
	TotalSearches int64 `json:"total_searches"`
}

// UserActivity represents user activity
type UserActivity struct {
	Action       string    `json:"action"`
	ResourceType string    `json:"resource_type"`
	ResourceID   string    `json:"resource_id"`
	Timestamp    time.Time `json:"timestamp"`
}
