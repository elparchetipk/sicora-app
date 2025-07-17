package routes

import (
	"attendanceservice/configs"
	"attendanceservice/internal/presentation/handlers"
	"attendanceservice/internal/presentation/middleware"

	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

// SetupRoutes configura todas las rutas del servicio
func SetupRoutes(
	config *configs.Config,
	attendanceHandler *handlers.AttendanceHandler,
	justificationHandler *handlers.JustificationHandler,
	alertHandler *handlers.AlertHandler,
	qrCodeHandler *handlers.QRCodeHandler,
	healthHandler *handlers.HealthHandler,
) *gin.Engine {

	router := gin.Default()

	// Middleware globales
	router.Use(middleware.CORSMiddleware(config))
	router.Use(middleware.RequestLoggingMiddleware())
	router.Use(middleware.RecoveryMiddleware())

	// Documentación Swagger
	router.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	// Health checks (sin autenticación)
	router.GET("/health", healthHandler.HealthCheck)
	router.GET("/ready", healthHandler.ReadinessCheck)

	// API v1
	v1 := router.Group("/api/v1")
	v1.Use(middleware.AuthMiddleware(config))

	// Rutas de asistencia
	attendanceGroup := v1.Group("/attendance")
	{
		attendanceGroup.POST("", attendanceHandler.CreateAttendance)
		attendanceGroup.GET("/:id", attendanceHandler.GetAttendanceByID)
		attendanceGroup.PUT("/:id", attendanceHandler.UpdateAttendance)
		attendanceGroup.DELETE("/:id", attendanceHandler.DeleteAttendance)
		attendanceGroup.GET("/history", attendanceHandler.GetAttendanceHistory)
		attendanceGroup.GET("/summary", attendanceHandler.GetAttendanceSummary)
		attendanceGroup.POST("/qr", attendanceHandler.RegisterQRAttendance)
		attendanceGroup.POST("/bulk", attendanceHandler.BulkCreateAttendance)
	}

	// Rutas de justificaciones
	justificationGroup := v1.Group("/justifications")
	{
		justificationGroup.POST("", justificationHandler.CreateJustification)
		justificationGroup.GET("/:id", justificationHandler.GetJustificationByID)
		justificationGroup.PUT("/:id", justificationHandler.UpdateJustification)
		justificationGroup.DELETE("/:id", justificationHandler.DeleteJustification)
		justificationGroup.GET("/user", justificationHandler.GetJustificationsByUser)
		justificationGroup.GET("/pending", justificationHandler.GetPendingJustifications)
		justificationGroup.POST("/:id/approve", justificationHandler.ApproveJustification)
		justificationGroup.POST("/:id/reject", justificationHandler.RejectJustification)
	}

	// Rutas de alertas
	alertGroup := v1.Group("/alerts")
	{
		alertGroup.POST("", alertHandler.CreateAlert)
		alertGroup.GET("/:id", alertHandler.GetAlertByID)
		alertGroup.PUT("/:id", alertHandler.UpdateAlert)
		alertGroup.DELETE("/:id", alertHandler.DeleteAlert)
		alertGroup.GET("/user", alertHandler.GetAlertsByUser)
		alertGroup.GET("/active", alertHandler.GetActiveAlerts)
		alertGroup.POST("/:id/read", alertHandler.MarkAlertAsRead)
		alertGroup.GET("/unread-count", alertHandler.GetUnreadCount)
		alertGroup.GET("/stats", alertHandler.GetAlertStats)
	}

	// Rutas de códigos QR
	qrGroup := v1.Group("/qr")
	{
		// Para estudiantes - generar y consultar códigos QR
		qrGroup.POST("/generate", qrCodeHandler.GenerateQRCode)
		qrGroup.POST("/refresh", qrCodeHandler.RefreshQRCode)
		qrGroup.GET("/student/:student_id/status", qrCodeHandler.GetStudentQRStatus)
		
		// Para instructores - escanear códigos QR
		qrGroup.POST("/scan", qrCodeHandler.ScanQRCode)
		qrGroup.POST("/bulk-generate", qrCodeHandler.BulkGenerateQRCodes)
		
		// Endpoints administrativos
		qrGroup.POST("/admin/expire-old", qrCodeHandler.ExpireOldQRCodes)
	}

	return router
}
