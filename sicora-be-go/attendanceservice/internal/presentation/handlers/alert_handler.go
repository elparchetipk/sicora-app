package handlers

import (
	"net/http"
	"strconv"

	"attendanceservice/internal/application/dtos"
	"attendanceservice/internal/application/usecases"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type AlertHandler struct {
	alertUseCase *usecases.AlertUseCase
}

// NewAlertHandler crea una nueva instancia del handler de alertas
func NewAlertHandler(alertUseCase *usecases.AlertUseCase) *AlertHandler {
	return &AlertHandler{
		alertUseCase: alertUseCase,
	}
}

// CreateAlert crea una nueva alerta
// @Summary Crear alerta
// @Description Crea una nueva alerta de asistencia
// @Tags alerts
// @Accept json
// @Produce json
// @Param alert body dtos.CreateAlertRequest true "Datos de la alerta"
// @Success 201 {object} dtos.AlertResponse
// @Failure 400 {object} dtos.dtos.ErrorResponse
// @Failure 401 {object} dtos.dtos.ErrorResponse
// @Router /api/v1/alerts [post]
func (h *AlertHandler) CreateAlert(c *gin.Context) {
	var req dtos.CreateAlertRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request format",
			"code":    "INVALID_REQUEST",
			"message": err.Error(),
		})
		return
	}

	response, err := h.alertUseCase.CreateAlert(c.Request.Context(), &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to create alert",
			"code":    "CREATE_ALERT_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusCreated, response)
}

// GetAlertByID obtiene una alerta por ID
// @Summary Obtener alerta por ID
// @Description Obtiene una alerta específica por su ID
// @Tags alerts
// @Accept json
// @Produce json
// @Param id path string true "ID de la alerta"
// @Success 200 {object} dtos.AlertResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 404 {object} dtos.ErrorResponse
// @Router /api/v1/alerts/{id} [get]
func (h *AlertHandler) GetAlertByID(c *gin.Context) {
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

	response, err := h.alertUseCase.GetAlertByID(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error":   "Alert not found",
			"code":    "ALERT_NOT_FOUND",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// UpdateAlert actualiza una alerta
// @Summary Actualizar alerta
// @Description Actualiza una alerta existente
// @Tags alerts
// @Accept json
// @Produce json
// @Param id path string true "ID de la alerta"
// @Param alert body dtos.UpdateAlertRequest true "Datos a actualizar"
// @Success 200 {object} dtos.AlertResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 404 {object} dtos.ErrorResponse
// @Router /api/v1/alerts/{id} [put]
func (h *AlertHandler) UpdateAlert(c *gin.Context) {
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

	var req dtos.UpdateAlertRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request format",
			"code":    "INVALID_REQUEST",
			"message": err.Error(),
		})
		return
	}

	response, err := h.alertUseCase.UpdateAlert(c.Request.Context(), id, &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to update alert",
			"code":    "UPDATE_ALERT_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// DeleteAlert elimina una alerta
// @Summary Eliminar alerta
// @Description Elimina una alerta
// @Tags alerts
// @Accept json
// @Produce json
// @Param id path string true "ID de la alerta"
// @Success 204
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 404 {object} dtos.ErrorResponse
// @Router /api/v1/alerts/{id} [delete]
func (h *AlertHandler) DeleteAlert(c *gin.Context) {
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

	err = h.alertUseCase.DeleteAlert(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to delete alert",
			"code":    "DELETE_ALERT_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusNoContent, nil)
}

// GetAlertsByUser obtiene las alertas de un usuario
// @Summary Obtener alertas por usuario
// @Description Obtiene las alertas de un usuario con filtros y paginación
// @Tags alerts
// @Accept json
// @Produce json
// @Param user_id query string true "ID del usuario"
// @Param type query string false "Tipo de alerta (ABSENCE, LATE, PATTERN, CONSECUTIVE, PERCENTAGE, CUSTOM)"
// @Param level query string false "Nivel de alerta (LOW, MEDIUM, HIGH, CRITICAL)"
// @Param is_read query bool false "Estado de lectura"
// @Param is_active query bool false "Estado activo"
// @Param limit query int false "Límite de resultados" default(10)
// @Param offset query int false "Offset para paginación" default(0)
// @Success 200 {object} dtos.AlertListResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Router /api/v1/alerts/user [get]
func (h *AlertHandler) GetAlertsByUser(c *gin.Context) {
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

	alertType := c.Query("type")
	var typePtr *string
	if alertType != "" {
		typePtr = &alertType
	}

	level := c.Query("level")
	var levelPtr *string
	if level != "" {
		levelPtr = &level
	}

	isReadStr := c.Query("is_read")
	var isReadPtr *bool
	if isReadStr != "" {
		if isRead, err := strconv.ParseBool(isReadStr); err == nil {
			isReadPtr = &isRead
		}
	}

	isActiveStr := c.Query("is_active")
	var isActivePtr *bool
	if isActiveStr != "" {
		if isActive, err := strconv.ParseBool(isActiveStr); err == nil {
			isActivePtr = &isActive
		}
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

	req := &dtos.AlertListRequest{
		UserID:   &userID,
		Type:     typePtr,
		Level:    levelPtr,
		IsRead:   isReadPtr,
		IsActive: isActivePtr,
		Limit:    limit,
		Offset:   offset,
	}

	response, err := h.alertUseCase.GetAlertsByUser(c.Request.Context(), req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to get alerts",
			"code":    "GET_ALERTS_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// GetActiveAlerts obtiene las alertas activas
// @Summary Obtener alertas activas
// @Description Obtiene todas las alertas activas con filtros y paginación
// @Tags alerts
// @Accept json
// @Produce json
// @Param type query string false "Tipo de alerta (ABSENCE, LATE, PATTERN, CONSECUTIVE, PERCENTAGE, CUSTOM)"
// @Param level query string false "Nivel de alerta (LOW, MEDIUM, HIGH, CRITICAL)"
// @Param is_read query bool false "Estado de lectura"
// @Param limit query int false "Límite de resultados" default(10)
// @Param offset query int false "Offset para paginación" default(0)
// @Success 200 {object} dtos.AlertListResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Router /api/v1/alerts/active [get]
func (h *AlertHandler) GetActiveAlerts(c *gin.Context) {
	alertType := c.Query("type")
	var typePtr *string
	if alertType != "" {
		typePtr = &alertType
	}

	level := c.Query("level")
	var levelPtr *string
	if level != "" {
		levelPtr = &level
	}

	isReadStr := c.Query("is_read")
	var isReadPtr *bool
	if isReadStr != "" {
		if isRead, err := strconv.ParseBool(isReadStr); err == nil {
			isReadPtr = &isRead
		}
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

	req := &dtos.AlertListRequest{
		Type:     typePtr,
		Level:    levelPtr,
		IsRead:   isReadPtr,
		IsActive: &[]bool{true}[0], // Pointer to true
		Limit:    limit,
		Offset:   offset,
	}

	response, err := h.alertUseCase.GetActiveAlerts(c.Request.Context(), req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to get active alerts",
			"code":    "GET_ACTIVE_ALERTS_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// MarkAlertAsRead marca una alerta como leída
// @Summary Marcar alerta como leída
// @Description Marca una alerta como leída por un usuario
// @Tags alerts
// @Accept json
// @Produce json
// @Param id path string true "ID de la alerta"
// @Param read_request body dtos.MarkAlertAsReadRequest true "Datos de lectura"
// @Success 200 {object} dtos.AlertResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 404 {object} dtos.ErrorResponse
// @Router /api/v1/alerts/{id}/read [post]
func (h *AlertHandler) MarkAlertAsRead(c *gin.Context) {
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

	var req dtos.MarkAlertAsReadRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request format",
			"code":    "INVALID_REQUEST",
			"message": err.Error(),
		})
		return
	}

	response, err := h.alertUseCase.MarkAlertAsRead(c.Request.Context(), id, &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to mark alert as read",
			"code":    "MARK_READ_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// GetUnreadCount obtiene el número de alertas no leídas
// @Summary Obtener contador de alertas no leídas
// @Description Obtiene el número de alertas no leídas para un usuario
// @Tags alerts
// @Accept json
// @Produce json
// @Param user_id query string true "ID del usuario"
// @Success 200 {object} map[string]int
// @Failure 400 {object} dtos.ErrorResponse
// @Router /api/v1/alerts/unread-count [get]
func (h *AlertHandler) GetUnreadCount(c *gin.Context) {
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

	count, err := h.alertUseCase.GetUnreadCount(c.Request.Context(), userID)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to get unread count",
			"code":    "GET_UNREAD_COUNT_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"unread_count": count,
	})
}

// GetAlertStats obtiene estadísticas de alertas
// @Summary Obtener estadísticas de alertas
// @Description Obtiene estadísticas detalladas de alertas para un usuario
// @Tags alerts
// @Accept json
// @Produce json
// @Param user_id query string true "ID del usuario"
// @Success 200 {object} dtos.AlertStatsResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Router /api/v1/alerts/stats [get]
func (h *AlertHandler) GetAlertStats(c *gin.Context) {
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

	stats, err := h.alertUseCase.GetAlertStats(c.Request.Context(), userID)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to get alert stats",
			"code":    "GET_STATS_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, stats)
}
