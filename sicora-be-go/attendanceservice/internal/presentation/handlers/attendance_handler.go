package handlers

import (
	"net/http"
	"strconv"
	"time"

	"attendanceservice/internal/application/dtos"
	"attendanceservice/internal/application/usecases"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type AttendanceHandler struct {
	attendanceUseCase *usecases.AttendanceUseCase
}

// NewAttendanceHandler crea una nueva instancia del handler de asistencia
func NewAttendanceHandler(attendanceUseCase *usecases.AttendanceUseCase) *AttendanceHandler {
	return &AttendanceHandler{
		attendanceUseCase: attendanceUseCase,
	}
}

// CreateAttendance crea un nuevo registro de asistencia
// @Summary Crear registro de asistencia
// @Description Crea un nuevo registro de asistencia
// @Tags attendance
// @Accept json
// @Produce json
// @Param attendance body dtos.CreateAttendanceRequest true "Datos del registro de asistencia"
// @Success 201 {object} dtos.AttendanceResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 401 {object} dtos.ErrorResponse
// @Router /api/v1/attendance [post]
func (h *AttendanceHandler) CreateAttendance(c *gin.Context) {
	var req dtos.CreateAttendanceRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request format",
			"code":    "INVALID_REQUEST",
			"message": err.Error(),
		})
		return
	}

	response, err := h.attendanceUseCase.CreateAttendance(c.Request.Context(), &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to create attendance",
			"code":    "CREATE_ATTENDANCE_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusCreated, response)
}

// GetAttendanceByID obtiene un registro de asistencia por ID
// @Summary Obtener registro de asistencia por ID
// @Description Obtiene un registro de asistencia específico por su ID
// @Tags attendance
// @Accept json
// @Produce json
// @Param id path string true "ID del registro de asistencia"
// @Success 200 {object} dtos.AttendanceResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 404 {object} dtos.ErrorResponse
// @Router /api/v1/attendance/{id} [get]
func (h *AttendanceHandler) GetAttendanceByID(c *gin.Context) {
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

	response, err := h.attendanceUseCase.GetAttendanceByID(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error":   "Attendance not found",
			"code":    "ATTENDANCE_NOT_FOUND",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// UpdateAttendance actualiza un registro de asistencia
// @Summary Actualizar registro de asistencia
// @Description Actualiza un registro de asistencia existente
// @Tags attendance
// @Accept json
// @Produce json
// @Param id path string true "ID del registro de asistencia"
// @Param attendance body dtos.UpdateAttendanceRequest true "Datos a actualizar"
// @Success 200 {object} dtos.AttendanceResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 404 {object} dtos.ErrorResponse
// @Router /api/v1/attendance/{id} [put]
func (h *AttendanceHandler) UpdateAttendance(c *gin.Context) {
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

	var req dtos.UpdateAttendanceRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request format",
			"code":    "INVALID_REQUEST",
			"message": err.Error(),
		})
		return
	}

	response, err := h.attendanceUseCase.UpdateAttendance(c.Request.Context(), id, &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to update attendance",
			"code":    "UPDATE_ATTENDANCE_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// DeleteAttendance elimina un registro de asistencia
// @Summary Eliminar registro de asistencia
// @Description Elimina un registro de asistencia
// @Tags attendance
// @Accept json
// @Produce json
// @Param id path string true "ID del registro de asistencia"
// @Success 204
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 404 {object} dtos.ErrorResponse
// @Router /api/v1/attendance/{id} [delete]
func (h *AttendanceHandler) DeleteAttendance(c *gin.Context) {
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

	err = h.attendanceUseCase.DeleteAttendance(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to delete attendance",
			"code":    "DELETE_ATTENDANCE_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusNoContent, nil)
}

// GetAttendanceHistory obtiene el historial de asistencia
// @Summary Obtener historial de asistencia
// @Description Obtiene el historial de asistencia con filtros y paginación
// @Tags attendance
// @Accept json
// @Produce json
// @Param user_id query string true "ID del usuario"
// @Param start_date query string true "Fecha de inicio (YYYY-MM-DD)"
// @Param end_date query string true "Fecha de fin (YYYY-MM-DD)"
// @Param status query string false "Estado de asistencia (PRESENT, ABSENT, JUSTIFIED, LATE)"
// @Param limit query int false "Límite de resultados" default(10)
// @Param offset query int false "Offset para paginación" default(0)
// @Success 200 {object} dtos.AttendanceHistoryResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Router /api/v1/attendance/history [get]
func (h *AttendanceHandler) GetAttendanceHistory(c *gin.Context) {
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

	startDateStr := c.Query("start_date")
	startDate, err := time.Parse("2006-01-02", startDateStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid start_date format",
			"code":    "INVALID_START_DATE",
			"message": "start_date must be in format YYYY-MM-DD",
		})
		return
	}

	endDateStr := c.Query("end_date")
	endDate, err := time.Parse("2006-01-02", endDateStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid end_date format",
			"code":    "INVALID_END_DATE",
			"message": "end_date must be in format YYYY-MM-DD",
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

	req := &dtos.AttendanceHistoryRequest{
		UserID:    userID,
		StartDate: startDate,
		EndDate:   endDate,
		Status:    statusPtr,
		Limit:     limit,
		Offset:    offset,
	}

	response, err := h.attendanceUseCase.GetAttendanceHistory(c.Request.Context(), req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to get attendance history",
			"code":    "GET_HISTORY_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// GetAttendanceSummary obtiene un resumen de asistencia
// @Summary Obtener resumen de asistencia
// @Description Obtiene un resumen estadístico de asistencia para un usuario en un período
// @Tags attendance
// @Accept json
// @Produce json
// @Param user_id query string true "ID del usuario"
// @Param start_date query string true "Fecha de inicio (YYYY-MM-DD)"
// @Param end_date query string true "Fecha de fin (YYYY-MM-DD)"
// @Success 200 {object} dtos.AttendanceSummaryResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Router /api/v1/attendance/summary [get]
func (h *AttendanceHandler) GetAttendanceSummary(c *gin.Context) {
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

	startDateStr := c.Query("start_date")
	startDate, err := time.Parse("2006-01-02", startDateStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid start_date format",
			"code":    "INVALID_START_DATE",
			"message": "start_date must be in format YYYY-MM-DD",
		})
		return
	}

	endDateStr := c.Query("end_date")
	endDate, err := time.Parse("2006-01-02", endDateStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid end_date format",
			"code":    "INVALID_END_DATE",
			"message": "end_date must be in format YYYY-MM-DD",
		})
		return
	}

	req := &dtos.AttendanceSummaryRequest{
		UserID:    userID,
		StartDate: startDate,
		EndDate:   endDate,
	}

	response, err := h.attendanceUseCase.GetAttendanceSummary(c.Request.Context(), req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to get attendance summary",
			"code":    "GET_SUMMARY_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// RegisterQRAttendance registra asistencia via código QR
// @Summary Registrar asistencia con código QR
// @Description Registra la asistencia de un estudiante usando un código QR
// @Tags attendance
// @Accept json
// @Produce json
// @Param qr_attendance body dtos.QRCodeAttendanceRequest true "Datos del código QR"
// @Success 201 {object} dtos.AttendanceResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Router /api/v1/attendance/qr [post]
func (h *AttendanceHandler) RegisterQRAttendance(c *gin.Context) {
	var req dtos.QRCodeAttendanceRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request format",
			"code":    "INVALID_REQUEST",
			"message": err.Error(),
		})
		return
	}

	response, err := h.attendanceUseCase.RegisterQRCodeAttendance(c.Request.Context(), &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to register QR attendance",
			"code":    "QR_ATTENDANCE_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusCreated, response)
}

// BulkCreateAttendance crea múltiples registros de asistencia
// @Summary Crear múltiples registros de asistencia
// @Description Crea múltiples registros de asistencia en una sola operación
// @Tags attendance
// @Accept json
// @Produce json
// @Param bulk_attendance body dtos.BulkAttendanceRequest true "Lista de registros de asistencia"
// @Success 201 {object} SuccessResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Router /api/v1/attendance/bulk [post]
func (h *AttendanceHandler) BulkCreateAttendance(c *gin.Context) {
	var req dtos.BulkAttendanceRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request format",
			"code":    "INVALID_REQUEST",
			"message": err.Error(),
		})
		return
	}

	err := h.attendanceUseCase.BulkCreateAttendance(c.Request.Context(), &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to create bulk attendance",
			"code":    "BULK_CREATE_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusCreated, gin.H{
		"message": "Bulk attendance records created successfully",
		"count":   len(req.Attendances),
	})
}
