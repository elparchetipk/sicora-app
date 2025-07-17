package handlers

import (
	"net/http"
	"time"

	"attendanceservice/internal/application/dtos"
	"attendanceservice/internal/application/usecases"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type QRCodeHandler struct {
	qrCodeUseCase *usecases.QRCodeUseCase
}

// NewQRCodeHandler crea una nueva instancia del handler de códigos QR
func NewQRCodeHandler(qrCodeUseCase *usecases.QRCodeUseCase) *QRCodeHandler {
	return &QRCodeHandler{
		qrCodeUseCase: qrCodeUseCase,
	}
}

// GenerateQRCode genera un nuevo código QR para un estudiante
// @Summary Generar código QR de asistencia
// @Description Genera un nuevo código QR para que un estudiante registre su asistencia
// @Tags qrcode
// @Accept json
// @Produce json
// @Param request body dtos.QRCodeRequest true "Datos para generar el código QR"
// @Success 201 {object} dtos.QRCodeResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 401 {object} dtos.ErrorResponse
// @Failure 403 {object} dtos.ErrorResponse "Solo estudiantes pueden generar códigos QR"
// @Router /api/v1/qr/generate [post]
func (h *QRCodeHandler) GenerateQRCode(c *gin.Context) {
	var req dtos.QRCodeRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request format",
			"code":    "INVALID_REQUEST",
			"message": err.Error(),
		})
		return
	}

	// Verificar que el usuario tiene permisos (debe ser el mismo estudiante)
	userID := c.GetString("user_id")
	if userID != req.StudentID.String() {
		c.JSON(http.StatusForbidden, gin.H{
			"error":   "Access denied",
			"code":    "ACCESS_DENIED", 
			"message": "Solo puedes generar códigos QR para tu propia asistencia",
		})
		return
	}

	response, err := h.qrCodeUseCase.GenerateQRCode(c.Request.Context(), &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to generate QR code",
			"code":    "QR_GENERATION_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusCreated, response)
}

// ScanQRCode procesa el escaneo de un código QR por un instructor
// @Summary Escanear código QR para registrar asistencia
// @Description Permite a un instructor escanear el código QR de un estudiante para registrar su asistencia
// @Tags qrcode
// @Accept json
// @Produce json
// @Param request body dtos.QRScanRequest true "Datos del escaneo del código QR"
// @Success 200 {object} dtos.QRScanResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 401 {object} dtos.ErrorResponse
// @Failure 403 {object} dtos.ErrorResponse "Solo instructores pueden escanear códigos QR"
// @Router /api/v1/qr/scan [post]
func (h *QRCodeHandler) ScanQRCode(c *gin.Context) {
	var req dtos.QRScanRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request format",
			"code":    "INVALID_REQUEST",
			"message": err.Error(),
		})
		return
	}

	// Verificar que el usuario es instructor
	userRole := c.GetString("user_role")
	if userRole != "INSTRUCTOR" {
		c.JSON(http.StatusForbidden, gin.H{
			"error":   "Access denied",
			"code":    "ACCESS_DENIED",
			"message": "Solo los instructores pueden escanear códigos QR para tomar asistencia",
		})
		return
	}

	// Verificar que el instructor ID coincide con el usuario autenticado
	userID := c.GetString("user_id")
	if userID != req.InstructorID.String() {
		c.JSON(http.StatusForbidden, gin.H{
			"error":   "Access denied",
			"code":    "ACCESS_DENIED",
			"message": "Solo puedes escanear códigos con tu propio ID de instructor",
		})
		return
	}

	response, err := h.qrCodeUseCase.ScanQRCode(c.Request.Context(), &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to scan QR code",
			"code":    "QR_SCAN_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// GetStudentQRStatus obtiene el estado del código QR de un estudiante
// @Summary Obtener estado del código QR del estudiante
// @Description Obtiene el estado actual del código QR de un estudiante para un horario específico
// @Tags qrcode
// @Accept json
// @Produce json
// @Param student_id path string true "ID del estudiante"
// @Param schedule_id query string true "ID del horario"
// @Success 200 {object} dtos.StudentQRStatusResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 401 {object} dtos.ErrorResponse
// @Failure 403 {object} dtos.ErrorResponse
// @Router /api/v1/qr/student/{student_id}/status [get]
func (h *QRCodeHandler) GetStudentQRStatus(c *gin.Context) {
	studentIDStr := c.Param("student_id")
	studentID, err := uuid.Parse(studentIDStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid student ID format",
			"code":    "INVALID_ID",
			"message": "The provided student ID is not a valid UUID",
		})
		return
	}

	scheduleIDStr := c.Query("schedule_id")
	scheduleID, err := uuid.Parse(scheduleIDStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid schedule ID format",
			"code":    "INVALID_ID",
			"message": "The provided schedule ID is not a valid UUID",
		})
		return
	}

	// Verificar permisos: estudiante solo puede ver su propio estado, instructores pueden ver cualquiera
	userID := c.GetString("user_id")
	userRole := c.GetString("user_role")
	
	if userRole == "STUDENT" && userID != studentID.String() {
		c.JSON(http.StatusForbidden, gin.H{
			"error":   "Access denied",
			"code":    "ACCESS_DENIED",
			"message": "Solo puedes consultar el estado de tu propio código QR",
		})
		return
	}

	req := &dtos.StudentQRStatusRequest{
		StudentID:  studentID,
		ScheduleID: scheduleID,
	}

	response, err := h.qrCodeUseCase.GetStudentQRStatus(c.Request.Context(), req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to get QR status",
			"code":    "QR_STATUS_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// BulkGenerateQRCodes genera códigos QR para múltiples estudiantes
// @Summary Generar códigos QR masivamente
// @Description Genera códigos QR para múltiples estudiantes de un horario específico
// @Tags qrcode
// @Accept json
// @Produce json
// @Param request body dtos.BulkQRGenerationRequest true "Datos para generación masiva"
// @Success 201 {object} dtos.BulkQRGenerationResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 401 {object} dtos.ErrorResponse
// @Failure 403 {object} dtos.ErrorResponse "Solo instructores pueden generar códigos masivamente"
// @Router /api/v1/qr/bulk-generate [post]
func (h *QRCodeHandler) BulkGenerateQRCodes(c *gin.Context) {
	var req dtos.BulkQRGenerationRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request format",
			"code":    "INVALID_REQUEST",
			"message": err.Error(),
		})
		return
	}

	// Verificar que el usuario es instructor
	userRole := c.GetString("user_role")
	if userRole != "INSTRUCTOR" {
		c.JSON(http.StatusForbidden, gin.H{
			"error":   "Access denied",
			"code":    "ACCESS_DENIED",
			"message": "Solo los instructores pueden generar códigos QR masivamente",
		})
		return
	}

	response, err := h.qrCodeUseCase.BulkGenerateQRCodes(c.Request.Context(), &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to bulk generate QR codes",
			"code":    "BULK_QR_GENERATION_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusCreated, response)
}

// RefreshQRCode refresca un código QR existente (regenera)
// @Summary Refrescar código QR
// @Description Regenera un código QR existente para extender su tiempo de vida
// @Tags qrcode
// @Accept json
// @Produce json
// @Param request body dtos.QRCodeRequest true "Datos para refrescar el código QR"
// @Success 200 {object} dtos.QRCodeResponse
// @Failure 400 {object} dtos.ErrorResponse
// @Failure 401 {object} dtos.ErrorResponse
// @Router /api/v1/qr/refresh [post]
func (h *QRCodeHandler) RefreshQRCode(c *gin.Context) {
	var req dtos.QRCodeRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request format",
			"code":    "INVALID_REQUEST",
			"message": err.Error(),
		})
		return
	}

	// Verificar que el usuario tiene permisos (debe ser el mismo estudiante)
	userID := c.GetString("user_id")
	if userID != req.StudentID.String() {
		c.JSON(http.StatusForbidden, gin.H{
			"error":   "Access denied",
			"code":    "ACCESS_DENIED",
			"message": "Solo puedes refrescar tu propio código QR",
		})
		return
	}

	// Usar el mismo método de generación que automáticamente maneja la renovación
	response, err := h.qrCodeUseCase.GenerateQRCode(c.Request.Context(), &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Failed to refresh QR code",
			"code":    "QR_REFRESH_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, response)
}

// ExpireOldQRCodes endpoint administrativo para expirar códigos antiguos
// @Summary Expirar códigos QR antiguos
// @Description Marca como expirados todos los códigos QR que han sobrepasado su tiempo de vida
// @Tags qrcode
// @Accept json
// @Produce json
// @Success 200 {object} map[string]string
// @Failure 500 {object} dtos.ErrorResponse
// @Router /api/v1/qr/admin/expire-old [post]
func (h *QRCodeHandler) ExpireOldQRCodes(c *gin.Context) {
	// Este endpoint normalmente se llamaría desde un cron job o tarea programada
	err := h.qrCodeUseCase.ExpireOldQRCodes(c.Request.Context())
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   "Failed to expire old QR codes",
			"code":    "QR_EXPIRE_FAILED",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message":   "Old QR codes expired successfully",
		"timestamp": time.Now().Format(time.RFC3339),
	})
}
