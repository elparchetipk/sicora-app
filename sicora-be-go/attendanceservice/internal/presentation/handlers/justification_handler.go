package handlers

import (
	"net/http"
	"strconv"

	"attendanceservice/internal/application/dtos"
	"attendanceservice/internal/application/usecases"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type JustificationHandler struct {
	justificationUseCase *usecases.JustificationUseCase
}

// NewJustificationHandler crea una nueva instancia del handler de justificaciones
func NewJustificationHandler(justificationUseCase *usecases.JustificationUseCase) *JustificationHandler {
	return &JustificationHandler{
		justificationUseCase: justificationUseCase,
	}
}

// CreateJustification crea una nueva justificación
// @Summary Crear justificación
// @Description Crea una nueva justificación para un registro de asistencia
// @Tags justifications
// @Accept json
// @Produce json
// @Param justification body dtos.CreateJustificationRequest true "Datos de la justificación"
// @Success 201 {object} dtos.JustificationResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 401 {object} dtos.ErrorResponse
// @Router /api/v1/justifications [post]
func (h *JustificationHandler) CreateJustification(c *gin.Context) {
	var req dtos.CreateJustificationRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request format",
			"code":    "INVALID_REQUEST",
			"message": err.Error(),
		})
		return
	}

	response, err := h.justificationUseCase.CreateJustification(c.Request.Context(), &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to create justification",
			"code":    "CREATE_JUSTIFICATION_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusCreated, response)
}

// GetJustificationByID obtiene una justificación por ID
// @Summary Obtener justificación por ID
// @Description Obtiene una justificación específica por su ID
// @Tags justifications
// @Accept json
// @Produce json
// @Param id path string true "ID de la justificación"
// @Success 200 {object} dtos.JustificationResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 404 {object} dtos.ErrorResponse
// @Router /api/v1/justifications/{id} [get]
func (h *JustificationHandler) GetJustificationByID(c *gin.Context) {
	idStr := c.Param("id")
	id, err := uuid.Parse(idStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid ID format",
			"code":    "INVALID_ID",
			"message": "The provided ID is not a valid UUID",
		})
		return
	}

	response, err := h.justificationUseCase.GetJustificationByID(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error":   "Justification not found",
			"code":    "JUSTIFICATION_NOT_FOUND",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// UpdateJustification actualiza una justificación
// @Summary Actualizar justificación
// @Description Actualiza una justificación existente (solo si está pendiente)
// @Tags justifications
// @Accept json
// @Produce json
// @Param id path string true "ID de la justificación"
// @Param justification body dtos.UpdateJustificationRequest true "Datos a actualizar"
// @Success 200 {object} dtos.JustificationResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 404 {object} dtos.ErrorResponse
// @Router /api/v1/justifications/{id} [put]
func (h *JustificationHandler) UpdateJustification(c *gin.Context) {
	idStr := c.Param("id")
	id, err := uuid.Parse(idStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid ID format",
			"code":    "INVALID_ID",
			"message": "The provided ID is not a valid UUID",
		})
		return
	}

	var req dtos.UpdateJustificationRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request format",
			"code":    "INVALID_REQUEST",
			"message": err.Error(),
		})
		return
	}

	response, err := h.justificationUseCase.UpdateJustification(c.Request.Context(), id, &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to update justification",
			"code":    "UPDATE_JUSTIFICATION_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// DeleteJustification elimina una justificación
// @Summary Eliminar justificación
// @Description Elimina una justificación (solo si está pendiente)
// @Tags justifications
// @Accept json
// @Produce json
// @Param id path string true "ID de la justificación"
// @Success 204
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 404 {object} dtos.ErrorResponse
// @Router /api/v1/justifications/{id} [delete]
func (h *JustificationHandler) DeleteJustification(c *gin.Context) {
	idStr := c.Param("id")
	id, err := uuid.Parse(idStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid ID format",
			"code":    "INVALID_ID",
			"message": "The provided ID is not a valid UUID",
		})
		return
	}

	err = h.justificationUseCase.DeleteJustification(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to delete justification",
			"code":    "DELETE_JUSTIFICATION_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusNoContent, nil)
}

// GetJustificationsByUser obtiene las justificaciones de un usuario
// @Summary Obtener justificaciones por usuario
// @Description Obtiene las justificaciones de un usuario con filtros y paginación
// @Tags justifications
// @Accept json
// @Produce json
// @Param user_id query string true "ID del usuario"
// @Param status query string false "Estado de la justificación (PENDING, APPROVED, REJECTED)"
// @Param limit query int false "Límite de resultados" default(10)
// @Param offset query int false "Offset para paginación" default(0)
// @Success 200 {object} dtos.JustificationListResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Router /api/v1/justifications/user [get]
func (h *JustificationHandler) GetJustificationsByUser(c *gin.Context) {
	userIDStr := c.Query("user_id")
	userID, err := uuid.Parse(userIDStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid user_id format",
			"code":    "INVALID_USER_ID",
			"message": "The provided user_id is not a valid UUID",
		})
		return
	}

	status := c.Query("status")
	var statusPtr *string
	if status != "" {
		statusPtr = &status
	}

	limitStr := c.DefaultQuery("limit", "10")
	limit, err := strconv.Atoi(limitStr)
	if err != nil || limit <= 0 {
		limit = 10
	}

	offsetStr := c.DefaultQuery("offset", "0")
	offset, err := strconv.Atoi(offsetStr)
	if err != nil || offset < 0 {
		offset = 0
	}

	req := &dtos.JustificationListRequest{
		UserID: &userID,
		Status: statusPtr,
		Limit:  limit,
		Offset: offset,
	}

	response, err := h.justificationUseCase.GetJustificationsByUser(c.Request.Context(), req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to get justifications",
			"code":    "GET_JUSTIFICATIONS_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// GetPendingJustifications obtiene las justificaciones pendientes
// @Summary Obtener justificaciones pendientes
// @Description Obtiene todas las justificaciones pendientes de revisión
// @Tags justifications
// @Accept json
// @Produce json
// @Param limit query int false "Límite de resultados" default(10)
// @Param offset query int false "Offset para paginación" default(0)
// @Success 200 {object} dtos.JustificationListResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Router /api/v1/justifications/pending [get]
func (h *JustificationHandler) GetPendingJustifications(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "10")
	limit, err := strconv.Atoi(limitStr)
	if err != nil || limit <= 0 {
		limit = 10
	}

	offsetStr := c.DefaultQuery("offset", "0")
	offset, err := strconv.Atoi(offsetStr)
	if err != nil || offset < 0 {
		offset = 0
	}

	req := &dtos.JustificationListRequest{
		Limit:  limit,
		Offset: offset,
	}

	response, err := h.justificationUseCase.GetPendingJustifications(c.Request.Context(), req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to get pending justifications",
			"code":    "GET_PENDING_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// ApproveJustification aprueba una justificación
// @Summary Aprobar justificación
// @Description Aprueba una justificación pendiente
// @Tags justifications
// @Accept json
// @Produce json
// @Param id path string true "ID de la justificación"
// @Param approval body dtos.ApproveJustificationRequest true "Datos de aprobación"
// @Success 200 {object} dtos.JustificationResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 404 {object} dtos.ErrorResponse
// @Router /api/v1/justifications/{id}/approve [post]
func (h *JustificationHandler) ApproveJustification(c *gin.Context) {
	idStr := c.Param("id")
	id, err := uuid.Parse(idStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid ID format",
			"code":    "INVALID_ID",
			"message": "The provided ID is not a valid UUID",
		})
		return
	}

	var req dtos.ApproveJustificationRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request format",
			"code":    "INVALID_REQUEST",
			"message": err.Error(),
		})
		return
	}

	response, err := h.justificationUseCase.ApproveJustification(c.Request.Context(), id, &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to approve justification",
			"code":    "APPROVE_JUSTIFICATION_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// RejectJustification rechaza una justificación
// @Summary Rechazar justificación
// @Description Rechaza una justificación pendiente
// @Tags justifications
// @Accept json
// @Produce json
// @Param id path string true "ID de la justificación"
// @Param rejection body dtos.RejectJustificationRequest true "Datos de rechazo"
// @Success 200 {object} dtos.JustificationResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 404 {object} dtos.ErrorResponse
// @Router /api/v1/justifications/{id}/reject [post]
func (h *JustificationHandler) RejectJustification(c *gin.Context) {
	idStr := c.Param("id")
	id, err := uuid.Parse(idStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid ID format",
			"code":    "INVALID_ID",
			"message": "The provided ID is not a valid UUID",
		})
		return
	}

	var req dtos.RejectJustificationRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request format",
			"code":    "INVALID_REQUEST",
			"message": err.Error(),
		})
		return
	}

	response, err := h.justificationUseCase.RejectJustification(c.Request.Context(), id, &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to reject justification",
			"code":    "REJECT_JUSTIFICATION_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}
