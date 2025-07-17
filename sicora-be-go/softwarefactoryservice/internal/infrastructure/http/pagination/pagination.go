package pagination

import (
	"fmt"
	"strconv"

	"github.com/gin-gonic/gin"
)

// PaginationRequest holds pagination parameters from request
type PaginationRequest struct {
	Page     int    `form:"page" json:"page"`
	PageSize int    `form:"page_size" json:"page_size"`
	SortBy   string `form:"sort_by" json:"sort_by"`
	SortDir  string `form:"sort_dir" json:"sort_dir"`
}

// PaginationResponse holds pagination metadata for response
type PaginationResponse struct {
	Page         int   `json:"page"`
	PageSize     int   `json:"page_size"`
	TotalItems   int64 `json:"total_items"`
	TotalPages   int   `json:"total_pages"`
	HasNext      bool  `json:"has_next"`
	HasPrevious  bool  `json:"has_previous"`
	NextPage     *int  `json:"next_page,omitempty"`
	PreviousPage *int  `json:"previous_page,omitempty"`
}

// PaginationConfig defines pagination limits
type PaginationConfig struct {
	DefaultPageSize int
	MaxPageSize     int
	DefaultPage     int
}

// DefaultConfig returns standard pagination configuration
func DefaultConfig() PaginationConfig {
	return PaginationConfig{
		DefaultPageSize: 20,
		MaxPageSize:     100,
		DefaultPage:     1,
	}
}

// ParsePaginationFromQuery extracts pagination parameters from Gin context
func ParsePaginationFromQuery(c *gin.Context, config PaginationConfig) PaginationRequest {
	page := getIntParam(c, "page", config.DefaultPage)
	pageSize := getIntParam(c, "page_size", config.DefaultPageSize)
	sortBy := c.DefaultQuery("sort_by", "created_at")
	sortDir := c.DefaultQuery("sort_dir", "desc")

	// Validate and enforce limits
	if page < 1 {
		page = config.DefaultPage
	}
	
	if pageSize < 1 {
		pageSize = config.DefaultPageSize
	}
	
	if pageSize > config.MaxPageSize {
		pageSize = config.MaxPageSize
	}

	// Validate sort direction
	if sortDir != "asc" && sortDir != "desc" {
		sortDir = "desc"
	}

	return PaginationRequest{
		Page:     page,
		PageSize: pageSize,
		SortBy:   sortBy,
		SortDir:  sortDir,
	}
}

// CalculateOffset returns the OFFSET value for SQL queries
func (p PaginationRequest) CalculateOffset() int {
	return (p.Page - 1) * p.PageSize
}

// GetLimit returns the LIMIT value for SQL queries
func (p PaginationRequest) GetLimit() int {
	return p.PageSize
}

// GetOrderBy returns the ORDER BY clause for SQL queries
func (p PaginationRequest) GetOrderBy(allowedFields map[string]string) string {
	// Validate sortBy field against allowed fields for security
	sqlField, exists := allowedFields[p.SortBy]
	if !exists {
		// Default to created_at if field is not allowed
		sqlField = allowedFields["created_at"]
		if sqlField == "" {
			sqlField = "created_at"
		}
	}
	
	return fmt.Sprintf("%s %s", sqlField, p.SortDir)
}

// CreateResponse creates a pagination response with metadata
func CreateResponse(req PaginationRequest, totalItems int64) PaginationResponse {
	totalPages := int((totalItems + int64(req.PageSize) - 1) / int64(req.PageSize))
	
	response := PaginationResponse{
		Page:        req.Page,
		PageSize:    req.PageSize,
		TotalItems:  totalItems,
		TotalPages:  totalPages,
		HasNext:     req.Page < totalPages,
		HasPrevious: req.Page > 1,
	}
	
	// Set next page if available
	if response.HasNext {
		nextPage := req.Page + 1
		response.NextPage = &nextPage
	}
	
	// Set previous page if available
	if response.HasPrevious {
		previousPage := req.Page - 1
		response.PreviousPage = &previousPage
	}
	
	return response
}

// PaginatedResult represents a paginated result with data and metadata
type PaginatedResult struct {
	Data       interface{}        `json:"data"`
	Pagination PaginationResponse `json:"pagination"`
}

// CreatePaginatedResult creates a complete paginated response
func CreatePaginatedResult(data interface{}, req PaginationRequest, totalItems int64) PaginatedResult {
	return PaginatedResult{
		Data:       data,
		Pagination: CreateResponse(req, totalItems),
	}
}

// Helper function to get integer parameter from query
func getIntParam(c *gin.Context, key string, defaultValue int) int {
	if value := c.Query(key); value != "" {
		if intValue, err := strconv.Atoi(value); err == nil && intValue > 0 {
			return intValue
		}
	}
	return defaultValue
}

// ValidatePaginationRequest validates and sanitizes pagination request
func ValidatePaginationRequest(req *PaginationRequest, config PaginationConfig) {
	if req.Page < 1 {
		req.Page = config.DefaultPage
	}
	
	if req.PageSize < 1 {
		req.PageSize = config.DefaultPageSize
	}
	
	if req.PageSize > config.MaxPageSize {
		req.PageSize = config.MaxPageSize
	}
	
	if req.SortDir != "asc" && req.SortDir != "desc" {
		req.SortDir = "desc"
	}
}

// GetSortableFields returns the default sortable fields for each entity
func GetSortableFields() map[string]map[string]string {
	return map[string]map[string]string{
		"projects": {
			"created_at":    "created_at",
			"updated_at":    "updated_at",
			"name":          "name",
			"start_date":    "start_date",
			"end_date":      "end_date",
			"status":        "status",
			"instructor_id": "instructor_id",
		},
		"user_stories": {
			"created_at":     "created_at",
			"updated_at":     "updated_at",
			"title":          "title",
			"status":         "status",
			"priority":       "priority",
			"story_points":   "story_points",
			"business_value": "business_value",
		},
		"evaluations": {
			"created_at":      "created_at",
			"updated_at":      "updated_at",
			"evaluation_date": "evaluation_date",
			"overall_score":   "overall_score",
			"student_id":      "student_id",
			"evaluator_id":    "evaluator_id",
		},
		"teams": {
			"created_at":    "created_at",
			"updated_at":    "updated_at",
			"name":          "name",
			"current_size":  "current_size",
			"max_members":   "max_members",
		},
		"sprints": {
			"created_at": "created_at",
			"updated_at": "updated_at",
			"name":       "name",
			"number":     "number",
			"start_date": "start_date",
			"end_date":   "end_date",
			"status":     "status",
		},
		"technologies": {
			"created_at":         "created_at",
			"updated_at":         "updated_at",
			"name":               "name",
			"category":           "category",
			"learning_difficulty": "learning_difficulty",
		},
	}
}
