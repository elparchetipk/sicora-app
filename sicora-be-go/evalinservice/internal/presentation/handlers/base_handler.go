package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/sirupsen/logrus"
)

// BaseHandler contiene funcionalidades comunes para todos los handlers
type BaseHandler struct {
	logger *logrus.Logger
}

// NewBaseHandler crea un nuevo handler base
func NewBaseHandler(logger *logrus.Logger) *BaseHandler {
	return &BaseHandler{
		logger: logger,
	}
}

// APIResponse representa la estructura estándar de respuesta de la API
type APIResponse struct {
	Success bool        `json:"success"`
	Message string      `json:"message"`
	Data    interface{} `json:"data,omitempty"`
	Meta    *Meta       `json:"meta,omitempty"`
	Error   *ErrorInfo  `json:"error,omitempty"`
}

// Meta contiene metadatos para respuestas paginadas
type Meta struct {
	Page      int   `json:"page"`
	Limit     int   `json:"limit"`
	Total     int64 `json:"total"`
	TotalPage int   `json:"total_pages"`
}

// ErrorInfo contiene información detallada del error
type ErrorInfo struct {
	Code    string      `json:"code"`
	Message string      `json:"message"`
	Details interface{} `json:"details,omitempty"`
}

// PaginationParams representa los parámetros de paginación
type PaginationParams struct {
	Page  int `form:"page" binding:"omitempty,min=1"`
	Limit int `form:"limit" binding:"omitempty,min=1,max=100"`
}

// GetPaginationParams extrae y valida los parámetros de paginación
func (h *BaseHandler) GetPaginationParams(c *gin.Context) PaginationParams {
	var params PaginationParams

	// Valores por defecto
	params.Page = 1
	params.Limit = 20

	// Obtener page
	if pageStr := c.Query("page"); pageStr != "" {
		if page, err := strconv.Atoi(pageStr); err == nil && page > 0 {
			params.Page = page
		}
	}

	// Obtener limit
	if limitStr := c.Query("limit"); limitStr != "" {
		if limit, err := strconv.Atoi(limitStr); err == nil && limit > 0 && limit <= 100 {
			params.Limit = limit
		}
	}

	return params
}

// GetUserIDFromParams extrae y valida el ID de usuario de los parámetros
func (h *BaseHandler) GetUserIDFromParams(c *gin.Context, paramName string) (uuid.UUID, error) {
	userIDStr := c.Param(paramName)
	if userIDStr == "" {
		return uuid.Nil, gin.Error{Err: gin.Error{Err: nil}, Type: gin.ErrorTypeBind}
	}

	userID, err := uuid.Parse(userIDStr)
	if err != nil {
		return uuid.Nil, err
	}

	return userID, nil
}

// SuccessResponse envía una respuesta exitosa
func (h *BaseHandler) SuccessResponse(c *gin.Context, message string, data interface{}) {
	response := APIResponse{
		Success: true,
		Message: message,
		Data:    data,
	}

	c.JSON(http.StatusOK, response)
}

// SuccessResponseWithMeta envía una respuesta exitosa con metadatos
func (h *BaseHandler) SuccessResponseWithMeta(c *gin.Context, message string, data interface{}, meta *Meta) {
	response := APIResponse{
		Success: true,
		Message: message,
		Data:    data,
		Meta:    meta,
	}

	c.JSON(http.StatusOK, response)
}

// CreatedResponse envía una respuesta de recurso creado
func (h *BaseHandler) CreatedResponse(c *gin.Context, message string, data interface{}) {
	response := APIResponse{
		Success: true,
		Message: message,
		Data:    data,
	}

	c.JSON(http.StatusCreated, response)
}

// ErrorResponse envía una respuesta de error
func (h *BaseHandler) ErrorResponse(c *gin.Context, statusCode int, code, message string, details interface{}) {
	response := APIResponse{
		Success: false,
		Message: "Request failed",
		Error: &ErrorInfo{
			Code:    code,
			Message: message,
			Details: details,
		},
	}

	h.logger.WithFields(logrus.Fields{
		"status_code": statusCode,
		"error_code":  code,
		"message":     message,
		"details":     details,
		"path":        c.Request.URL.Path,
		"method":      c.Request.Method,
	}).Error("API Error Response")

	c.JSON(statusCode, response)
}

// BadRequestResponse envía una respuesta de request inválido
func (h *BaseHandler) BadRequestResponse(c *gin.Context, message string, details interface{}) {
	h.ErrorResponse(c, http.StatusBadRequest, "BAD_REQUEST", message, details)
}

// NotFoundResponse envía una respuesta de recurso no encontrado
func (h *BaseHandler) NotFoundResponse(c *gin.Context, message string) {
	h.ErrorResponse(c, http.StatusNotFound, "NOT_FOUND", message, nil)
}

// UnauthorizedResponse envía una respuesta de no autorizado
func (h *BaseHandler) UnauthorizedResponse(c *gin.Context, message string) {
	h.ErrorResponse(c, http.StatusUnauthorized, "UNAUTHORIZED", message, nil)
}

// ForbiddenResponse envía una respuesta de acceso prohibido
func (h *BaseHandler) ForbiddenResponse(c *gin.Context, message string) {
	h.ErrorResponse(c, http.StatusForbidden, "FORBIDDEN", message, nil)
}

// InternalErrorResponse envía una respuesta de error interno
func (h *BaseHandler) InternalErrorResponse(c *gin.Context, message string, err error) {
	details := map[string]interface{}{}
	if err != nil {
		details["error"] = err.Error()
	}

	h.ErrorResponse(c, http.StatusInternalServerError, "INTERNAL_ERROR", message, details)
}

// ConflictResponse envía una respuesta de conflicto
func (h *BaseHandler) ConflictResponse(c *gin.Context, message string, details interface{}) {
	h.ErrorResponse(c, http.StatusConflict, "CONFLICT", message, details)
}

// CalculateMeta calcula los metadatos de paginación
func (h *BaseHandler) CalculateMeta(page, limit int, total int64) *Meta {
	totalPages := int((total + int64(limit) - 1) / int64(limit))

	return &Meta{
		Page:      page,
		Limit:     limit,
		Total:     total,
		TotalPage: totalPages,
	}
}

// HealthCheck endpoint de health check
func (h *BaseHandler) HealthCheck(c *gin.Context) {
	h.SuccessResponse(c, "Service is healthy", gin.H{
		"service": "evalinservice",
		"status":  "up",
		"version": "1.0.0",
	})
}
