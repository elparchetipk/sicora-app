package main

//	@title			SICORA ProjectEvalService API - Go
//	@version		1.0.0
//	@description	Sistema de Información de Coordinación Académica - ProjectEvalService implementado con Go, Gin y Clean Architecture
//	@termsOfService	http://swagger.io/terms/

//	@contact.name	Equipo de Desarrollo SICORA
//	@contact.email	dev@sicora.sena.edu.co

//	@license.name	MIT
//	@license.url	https://opensource.org/licenses/MIT

//	@host		localhost:8007
//	@BasePath	/api/v1

//	@securityDefinitions.apikey	BearerAuth
//	@in							header
//	@name						Authorization
//	@description				Type "Bearer" followed by a space and JWT token.

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	_ "projectevalservice/docs"
	"syscall"
	"time"

	_ "projectevalservice/docs"
	"projectevalservice/internal/application/usecases"
	"projectevalservice/internal/infrastructure/auth"
	"projectevalservice/internal/infrastructure/database"
	"projectevalservice/internal/infrastructure/database/repositories"
	"projectevalservice/internal/presentation/handlers"
	"projectevalservice/internal/presentation/routes"

	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

func main() {
	// Load environment variables
	if err := godotenv.Load(); err != nil {
		log.Println("Warning: .env file not found")
	}

	// Initialize database
	db := database.NewDatabase()
	if err := db.Connect(); err != nil {
		log.Fatal("Failed to connect to database:", err)
	}
	defer db.Close()

	// Run migrations
	if err := db.Migrate(); err != nil {
		log.Fatal("Failed to run migrations:", err)
	}

	// Initialize repositories
	projectRepo := repositories.NewProjectRepository(db.GetDB())
	submissionRepo := repositories.NewSubmissionRepository(db.GetDB())
	evaluationRepo := repositories.NewEvaluationRepository(db.GetDB())

	// Initialize use cases
	projectUseCase := usecases.NewProjectUseCase(projectRepo)
	submissionUseCase := usecases.NewSubmissionUseCase(submissionRepo, projectRepo)
	evaluationUseCase := usecases.NewEvaluationUseCase(evaluationRepo, submissionRepo)

	// Initialize handlers
	projectHandler := handlers.NewProjectHandler(projectUseCase)
	submissionHandler := handlers.NewSubmissionHandler(submissionUseCase)
	evaluationHandler := handlers.NewEvaluationHandler(evaluationUseCase)

	// Initialize JWT service
	jwtSecret := os.Getenv("JWT_SECRET")
	if jwtSecret == "" {
		jwtSecret = "your-super-secret-jwt-key-change-in-production"
	}

	jwtService := auth.NewJWTService(
		jwtSecret,
		"sicora-projectevalservice",
		24*time.Hour,
	)

	// Initialize Gin router
	if os.Getenv("GIN_MODE") == "release" {
		gin.SetMode(gin.ReleaseMode)
	}

	router := gin.New()
	router.Use(gin.Logger())
	router.Use(gin.Recovery())

	// Setup routes
	routes.SetupRoutes(router, projectHandler, submissionHandler, evaluationHandler, jwtService)

	// Swagger documentation
	router.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	// Server configuration
	port := os.Getenv("PORT")
	if port == "" {
		port = "8007"
	}

	srv := &http.Server{
		Addr:    ":" + port,
		Handler: router,
	}

	// Graceful shutdown
	go func() {
		log.Printf("Server starting on port %s", port)
		log.Printf("Swagger documentation available at http://localhost:%s/swagger/index.html", port)

		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Failed to start server: %v", err)
		}
	}()

	// Wait for interrupt signal to gracefully shutdown the server
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("Shutting down server...")

	// Give outstanding requests 30 seconds to complete
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("Server forced to shutdown:", err)
	}

	log.Println("Server exited")
}
