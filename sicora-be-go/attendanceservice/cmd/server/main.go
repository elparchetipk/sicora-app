package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"syscall"

	"attendanceservice/configs"
	"attendanceservice/internal/application/services"
	"attendanceservice/internal/application/usecases"
	"attendanceservice/internal/infrastructure/database"
	"attendanceservice/internal/infrastructure/database/repositories"
	"attendanceservice/internal/presentation/handlers"
	"attendanceservice/internal/presentation/routes"

	_ "attendanceservice/docs"
)

// @title AttendanceService API
// @version 1.0
// @description API para la gestión de asistencia, justificaciones y alertas del sistema SICORA
// @termsOfService http://swagger.io/terms/

// @contact.name API Support
// @contact.url http://www.swagger.io/support
// @contact.email support@swagger.io

// @license.name MIT
// @license.url https://opensource.org/licenses/MIT

// @host localhost:8003
// @BasePath /
// @schemes http https

// @securityDefinitions.apikey ApiKeyAuth
// @in header
// @name Authorization
// @description Type "Bearer" followed by a space and JWT token.

func main() {
	// Cargar configuración
	config, err := configs.LoadConfig()
	if err != nil {
		log.Fatalf("Failed to load config: %v", err)
	}

	// Configurar base de datos
	dbConfig := database.Config{
		Host:     config.Database.Host,
		Port:     config.Database.Port,
		User:     config.Database.User,
		Password: config.Database.Password,
		DBName:   config.Database.DBName,
		Schema:   config.Database.Schema,
		SSLMode:  config.Database.SSLMode,
	}

	db, err := database.NewDatabase(dbConfig)
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	defer db.Close()

	// Crear schema y ejecutar migraciones
	if err := db.CreateSchema(config.Database.Schema); err != nil {
		log.Fatalf("Failed to create schema: %v", err)
	}

	if err := db.AutoMigrate(); err != nil {
		log.Fatalf("Failed to run migrations: %v", err)
	}

	// Inicializar repositorios
	attendanceRepo := repositories.NewAttendanceRepository(db.DB)
	justificationRepo := repositories.NewJustificationRepository(db.DB)
	alertRepo := repositories.NewAttendanceAlertRepository(db.DB)
	qrCodeRepo := repositories.NewQRCodeRepository(db.DB)

	// Inicializar casos de uso
	attendanceUseCase := usecases.NewAttendanceUseCase(attendanceRepo, alertRepo)
	justificationUseCase := usecases.NewJustificationUseCase(justificationRepo, attendanceRepo)
	alertUseCase := usecases.NewAlertUseCase(alertRepo)
	qrCodeUseCase := usecases.NewQRCodeUseCase(qrCodeRepo, attendanceRepo)

	// Inicializar handlers
	attendanceHandler := handlers.NewAttendanceHandler(attendanceUseCase)
	justificationHandler := handlers.NewJustificationHandler(justificationUseCase)
	alertHandler := handlers.NewAlertHandler(alertUseCase)
	qrCodeHandler := handlers.NewQRCodeHandler(qrCodeUseCase)
	healthHandler := handlers.NewHealthHandler()

	// Configurar rutas
	router := routes.SetupRoutes(
		config,
		attendanceHandler,
		justificationHandler,
		alertHandler,
		qrCodeHandler,
		healthHandler,
	)

	// Crear contexto para el servicio programador
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Inicializar y arrancar el servicio programador de códigos QR
	qrScheduler := services.NewQRSchedulerService(qrCodeRepo, qrCodeUseCase)
	go qrScheduler.Start(ctx)

	// Configurar manejo de señales para shutdown graceful
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	// Iniciar servidor en una goroutine
	go func() {
		log.Printf("🚀 AttendanceService starting on %s", config.GetServerAddress())
		log.Printf("📋 Swagger docs available at: http://%s/swagger/index.html", config.GetServerAddress())
		log.Printf("🔧 Health check available at: http://%s/health", config.GetServerAddress())
		
		if err := router.Run(config.GetServerAddress()); err != nil {
			log.Fatalf("Failed to start server: %v", err)
		}
	}()

	// Esperar señal de terminación
	<-sigChan
	log.Println("🛑 Recibida señal de terminación, cerrando servicios...")
	
	// Detener servicios
	qrScheduler.Stop()
	cancel()
	
	log.Println("✅ AttendanceService cerrado correctamente")
}
