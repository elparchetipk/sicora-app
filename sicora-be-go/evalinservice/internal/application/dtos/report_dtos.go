package dtos

import (
	"time"

	"github.com/google/uuid"
)

type ReportCreateRequest struct {
	PeriodID    uuid.UUID              `json:"period_id" binding:"required"`
	Type        string                 `json:"type" binding:"required"`
	Title       string                 `json:"title" binding:"required,min=1,max=255"`
	Description string                 `json:"description" binding:"max=2000"`
	Parameters  map[string]interface{} `json:"parameters"`
}

type ReportUpdateRequest struct {
	Title       string                 `json:"title" binding:"required,min=1,max=255"`
	Description string                 `json:"description" binding:"max=2000"`
	Parameters  map[string]interface{} `json:"parameters"`
}

type ReportResponse struct {
	ID            uuid.UUID              `json:"id"`
	PeriodID      uuid.UUID              `json:"period_id"`
	Type          string                 `json:"type"`
	Status        string                 `json:"status"`
	Title         string                 `json:"title"`
	Description   string                 `json:"description"`
	Parameters    map[string]interface{} `json:"parameters"`
	Results       map[string]interface{} `json:"results"`
	FilePath      string                 `json:"file_path"`
	GeneratedBy   uuid.UUID              `json:"generated_by"`
	GeneratedAt   *time.Time             `json:"generated_at"`
	ErrorMessage  string                 `json:"error_message"`
	CreatedAt     time.Time              `json:"created_at"`
	UpdatedAt     time.Time              `json:"updated_at"`
	PeriodName    string                 `json:"period_name,omitempty"`
	GeneratorName string                 `json:"generator_name,omitempty"`
}

type ReportFilterRequest struct {
	PeriodID    *uuid.UUID `form:"period_id"`
	Type        *string    `form:"type"`
	Status      *string    `form:"status"`
	GeneratedBy *uuid.UUID `form:"generated_by"`
	StartDate   *string    `form:"start_date"`
	EndDate     *string    `form:"end_date"`
	Page        int        `form:"page" binding:"min=1"`
	PageSize    int        `form:"page_size" binding:"min=1,max=100"`
}

type ReportStatsResponse struct {
	TotalReports     int64   `json:"total_reports"`
	CompletedReports int64   `json:"completed_reports"`
	PendingReports   int64   `json:"pending_reports"`
	FailedReports    int64   `json:"failed_reports"`
	SuccessRate      float64 `json:"success_rate"`
	AverageGenTime   float64 `json:"average_generation_time_minutes"`
}

type ReportGenerationRequest struct {
	PeriodID      uuid.UUID              `json:"period_id" binding:"required"`
	Type          string                 `json:"type" binding:"required"`
	Title         string                 `json:"title" binding:"required"`
	Description   string                 `json:"description"`
	Parameters    map[string]interface{} `json:"parameters"`
	IncludeCharts bool                   `json:"include_charts"`
	Format        string                 `json:"format" binding:"oneof=pdf xlsx csv"`
	Recipients    []uuid.UUID            `json:"recipients"`
}

type ReportDownloadResponse struct {
	ReportID uuid.UUID `json:"report_id"`
	FileName string    `json:"file_name"`
	FileSize int64     `json:"file_size"`
	MimeType string    `json:"mime_type"`
	URL      string    `json:"url"`
}
