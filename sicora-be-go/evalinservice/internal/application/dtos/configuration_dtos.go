package dtos

import (
	"time"

	"github.com/google/uuid"
)

type ConfigurationCreateRequest struct {
	Key         string `json:"key" binding:"required,min=1,max=100"`
	Value       string `json:"value" binding:"required"`
	Description string `json:"description" binding:"max=2000"`
	Category    string `json:"category" binding:"required,min=1,max=50"`
	IsEditable  bool   `json:"is_editable"`
}

type ConfigurationUpdateRequest struct {
	Value       string `json:"value" binding:"required"`
	Description string `json:"description" binding:"max=2000"`
	IsActive    bool   `json:"is_active"`
}

type ConfigurationResponse struct {
	ID          uuid.UUID `json:"id"`
	Key         string    `json:"key"`
	Value       string    `json:"value"`
	Description string    `json:"description"`
	Category    string    `json:"category"`
	IsActive    bool      `json:"is_active"`
	IsEditable  bool      `json:"is_editable"`
	CreatedBy   uuid.UUID `json:"created_by"`
	UpdatedBy   uuid.UUID `json:"updated_by"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
	CreatorName string    `json:"creator_name,omitempty"`
	UpdaterName string    `json:"updater_name,omitempty"`
}

type ConfigurationFilterRequest struct {
	Category   *string `form:"category"`
	IsActive   *bool   `form:"is_active"`
	IsEditable *bool   `form:"is_editable"`
	Search     *string `form:"search"`
	Page       int     `form:"page" binding:"min=1"`
	PageSize   int     `form:"page_size" binding:"min=1,max=100"`
}

type ConfigurationBulkUpdateRequest struct {
	Configurations []ConfigurationBulkItem `json:"configurations" binding:"required"`
}

type ConfigurationBulkItem struct {
	Key      string `json:"key" binding:"required"`
	Value    string `json:"value" binding:"required"`
	IsActive bool   `json:"is_active"`
}

type ConfigurationCategoryResponse struct {
	Category       string                  `json:"category"`
	Count          int64                   `json:"count"`
	ActiveCount    int64                   `json:"active_count"`
	EditableCount  int64                   `json:"editable_count"`
	Configurations []ConfigurationResponse `json:"configurations,omitempty"`
}

type ConfigurationExportRequest struct {
	Categories      []string `json:"categories"`
	Format          string   `json:"format" binding:"oneof=json yaml env"`
	IncludeInactive bool     `json:"include_inactive"`
}

type ConfigurationImportRequest struct {
	Data      map[string]interface{} `json:"data" binding:"required"`
	Category  string                 `json:"category" binding:"required"`
	Overwrite bool                   `json:"overwrite"`
	DryRun    bool                   `json:"dry_run"`
}
