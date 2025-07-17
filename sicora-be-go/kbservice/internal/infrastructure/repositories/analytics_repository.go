package repositories

import (
	"context"
	"kbservice/internal/domain/repositories"
	"time"

	"gorm.io/gorm"
)

type analyticsRepository struct {
	db *gorm.DB
}

// AnalyticsData represents analytics data structure
type AnalyticsData struct {
	TenantID     string    `json:"tenant_id"`
	ResourceType string    `json:"resource_type"` // "document" or "faq"
	ResourceID   string    `json:"resource_id"`
	Action       string    `json:"action"` // "view", "download", "search", "rating"
	UserID       string    `json:"user_id,omitempty"`
	Timestamp    time.Time `json:"timestamp"`
	Metadata     string    `json:"metadata,omitempty"` // JSON metadata
}

// SearchAnalytics represents search analytics
type SearchAnalytics struct {
	ID           string    `gorm:"primaryKey" json:"id"`
	TenantID     string    `gorm:"index" json:"tenant_id"`
	Query        string    `json:"query"`
	ResultsFound int       `json:"results_found"`
	UserID       string    `json:"user_id,omitempty"`
	Timestamp    time.Time `json:"timestamp"`
}

// NewAnalyticsRepository creates a new analytics repository instance
func NewAnalyticsRepository(db *gorm.DB) repositories.AnalyticsRepository {
	return &analyticsRepository{db: db}
}

func (r *analyticsRepository) TrackEvent(ctx context.Context, tenantID, resourceType, resourceID, action string, metadata map[string]interface{}) error {
	// Create analytics entry in a dedicated analytics table
	// For now, we'll create a simple analytics event
	query := `
		INSERT INTO analytics_events (tenant_id, resource_type, resource_id, action, metadata, timestamp)
		VALUES (?, ?, ?, ?, ?, ?)
	`
	
	metadataJSON := ""
	if metadata != nil {
		// Convert metadata to JSON string (simplified)
		metadataJSON = "{'event': 'tracked'}"
	}
	
	return r.db.WithContext(ctx).
		Exec(query, tenantID, resourceType, resourceID, action, metadataJSON, time.Now()).Error
}

func (r *analyticsRepository) GetResourceViews(ctx context.Context, tenantID, resourceType, resourceID string, from, to time.Time) (int64, error) {
	var count int64
	
	query := `
		SELECT COUNT(*) FROM analytics_events 
		WHERE tenant_id = ? AND resource_type = ? AND resource_id = ? 
		AND action = 'view' AND timestamp BETWEEN ? AND ?
	`
	
	err := r.db.WithContext(ctx).
		Raw(query, tenantID, resourceType, resourceID, from, to).
		Scan(&count).Error
	
	return count, err
}

func (r *analyticsRepository) GetResourceDownloads(ctx context.Context, tenantID, resourceType, resourceID string, from, to time.Time) (int64, error) {
	var count int64
	
	query := `
		SELECT COUNT(*) FROM analytics_events 
		WHERE tenant_id = ? AND resource_type = ? AND resource_id = ? 
		AND action = 'download' AND timestamp BETWEEN ? AND ?
	`
	
	err := r.db.WithContext(ctx).
		Raw(query, tenantID, resourceType, resourceID, from, to).
		Scan(&count).Error
	
	return count, err
}

func (r *analyticsRepository) GetTopSearchQueries(ctx context.Context, tenantID string, limit int, from, to time.Time) ([]repositories.SearchQuery, error) {
	var results []repositories.SearchQuery
	
	query := `
		SELECT query, COUNT(*) as count
		FROM search_analytics 
		WHERE tenant_id = ? AND timestamp BETWEEN ? AND ?
		GROUP BY query 
		ORDER BY count DESC 
		LIMIT ?
	`
	
	err := r.db.WithContext(ctx).
		Raw(query, tenantID, from, to, limit).
		Scan(&results).Error
	
	return results, err
}

func (r *analyticsRepository) GetPopularResources(ctx context.Context, tenantID, resourceType string, limit int, from, to time.Time) ([]repositories.ResourceStats, error) {
	var results []repositories.ResourceStats
	
	query := `
		SELECT resource_id, COUNT(*) as views, 0 as downloads
		FROM analytics_events 
		WHERE tenant_id = ? AND resource_type = ? AND action = 'view'
		AND timestamp BETWEEN ? AND ?
		GROUP BY resource_id 
		ORDER BY views DESC 
		LIMIT ?
	`
	
	err := r.db.WithContext(ctx).
		Raw(query, tenantID, resourceType, from, to, limit).
		Scan(&results).Error
	
	return results, err
}

func (r *analyticsRepository) GetDashboardStats(ctx context.Context, tenantID string, from, to time.Time) (*repositories.DashboardStats, error) {
	stats := &repositories.DashboardStats{}
	
	// Total documents
	err := r.db.WithContext(ctx).
		Model(&struct {
			ID       string `gorm:"column:id"`
			TenantID string `gorm:"column:tenant_id"`
		}{}).
		Table("documents").
		Where("tenant_id = ?", tenantID).
		Count(&stats.TotalDocuments).Error
	if err != nil {
		return nil, err
	}
	
	// Total FAQs
	err = r.db.WithContext(ctx).
		Model(&struct {
			ID       string `gorm:"column:id"`
			TenantID string `gorm:"column:tenant_id"`
		}{}).
		Table("faqs").
		Where("tenant_id = ?", tenantID).
		Count(&stats.TotalFAQs).Error
	if err != nil {
		return nil, err
	}
	
	// Total views in period
	query := `
		SELECT COUNT(*) FROM analytics_events 
		WHERE tenant_id = ? AND action = 'view' AND timestamp BETWEEN ? AND ?
	`
	err = r.db.WithContext(ctx).
		Raw(query, tenantID, from, to).
		Scan(&stats.TotalViews).Error
	if err != nil {
		return nil, err
	}
	
	// Total searches in period
	query = `
		SELECT COUNT(*) FROM search_analytics 
		WHERE tenant_id = ? AND timestamp BETWEEN ? AND ?
	`
	err = r.db.WithContext(ctx).
		Raw(query, tenantID, from, to).
		Scan(&stats.TotalSearches).Error
	if err != nil {
		return nil, err
	}
	
	return stats, nil
}

func (r *analyticsRepository) TrackSearch(ctx context.Context, tenantID, query string, resultsFound int, userID string) error {
	searchAnalytics := SearchAnalytics{
		TenantID:     tenantID,
		Query:        query,
		ResultsFound: resultsFound,
		UserID:       userID,
		Timestamp:    time.Now(),
	}
	
	// Insert into search_analytics table
	return r.db.WithContext(ctx).
		Table("search_analytics").
		Create(&searchAnalytics).Error
}

func (r *analyticsRepository) GetUserActivity(ctx context.Context, tenantID, userID string, from, to time.Time) ([]repositories.UserActivity, error) {
	var activities []repositories.UserActivity
	
	query := `
		SELECT action, resource_type, resource_id, timestamp
		FROM analytics_events 
		WHERE tenant_id = ? AND user_id = ? AND timestamp BETWEEN ? AND ?
		ORDER BY timestamp DESC
	`
	
	err := r.db.WithContext(ctx).
		Raw(query, tenantID, userID, from, to).
		Scan(&activities).Error
	
	return activities, err
}
