package dtos

// ErrorResponse representa una respuesta de error estándar
type ErrorResponse struct {
	Error   string      `json:"error" example:"Error message"`
	Code    string      `json:"code" example:"ERROR_CODE"`
	Message string      `json:"message" example:"Detailed error message"`
	Details interface{} `json:"details,omitempty"`
}

// SuccessResponse representa una respuesta exitosa estándar
type SuccessResponse struct {
	Success bool        `json:"success" example:"true"`
	Message string      `json:"message" example:"Operation completed successfully"`
	Data    interface{} `json:"data,omitempty"`
}

// PaginationResponse representa metadatos de paginación
type PaginationResponse struct {
	Page       int   `json:"page" example:"1"`
	Limit      int   `json:"limit" example:"10"`
	Total      int64 `json:"total" example:"100"`
	TotalPages int   `json:"total_pages" example:"10"`
}
