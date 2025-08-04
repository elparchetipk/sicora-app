package main

//	@title			SICORA UserService API - Go
//	@version		1.0.0
//	@description	Sistema de Información de Coordinación Académica - UserService implementado con Go, Gin y Clean Architecture
//	@termsOfService	http://swagger.io/terms/

//	@contact.name	Equipo de Desarrollo SICORA
//	@contact.email	dev@sicora.sena.edu.co

//	@license.name	MIT
//	@license.url	https://opensource.org/licenses/MIT

//	@host		localhost:8002
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
	"syscall"
	"time"

	_ "userservice/docs"
	"userservice/internal/application/usecases"
	"userservice/internal/infrastructure/auth"
	"userservice/internal/infrastructure/database"
	"userservice/internal/infrastructure/database/models"
	"userservice/internal/infrastructure/database/repositories"
	"userservice/internal/presentation/handlers"
	"userservice/internal/presentation/middleware"
	"userservice/internal/presentation/routes"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
	"github.com/joho/godotenv"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

func main() {
	// Load environment variables
	if err := godotenv.Load(); err != nil {
		log.Println("No .env file found, using environment variables")
	}

	// Setup logger
	logger := log.New(os.Stdout, "[USERSERVICE-GO] ", log.LstdFlags|log.Lshortfile)
	logger.Println("Starting SICORA UserService Go...")

	// Setup database
	dbConfig := database.NewConfig()
	db, err := database.NewConnection(dbConfig)
	if err != nil {
		logger.Fatalf("Failed to connect to database: %v", err)
	}
	defer db.Close()

	// Run migrations
	logger.Println("Running database migrations...")
	if err := db.Migrate(&models.UserModel{}); err != nil {
		logger.Fatalf("Failed to migrate database: %v", err)
	}
	logger.Println("Database migrations completed successfully")

	// Setup repository
	userRepo := repositories.NewPostgreSQLUserRepository(db.Connection)

	// Setup validator
	validate := validator.New()
	// Setup use cases
	createUserUseCase := usecases.NewCreateUserUseCase(userRepo, logger)
	getUserUseCase := usecases.NewGetUserUseCase(userRepo, logger)
	listUsersUseCase := usecases.NewListUsersUseCase(userRepo, logger)
	getProfileUseCase := usecases.NewGetProfileUseCase(userRepo, logger)
	updateProfileUseCase := usecases.NewUpdateProfileUseCase(userRepo, logger)
	authenticateUserUseCase := usecases.NewAuthenticateUserUseCase(userRepo, logger)
	refreshTokenUseCase := usecases.NewRefreshTokenUseCase(userRepo, logger)
	logoutUseCase := usecases.NewLogoutUseCase(userRepo, logger)
	forgotPasswordUseCase := usecases.NewForgotPasswordUseCase(userRepo, logger)
	resetPasswordUseCase := usecases.NewResetPasswordUseCase(userRepo, logger)
	forceChangePasswordUseCase := usecases.NewForceChangePasswordUseCase(userRepo, logger)

	// Admin use cases
	updateUserUseCase := usecases.NewUpdateUserUseCase(userRepo, logger)
	changePasswordUseCase := usecases.NewChangePasswordUseCase(userRepo, logger)
	deleteUserUseCase := usecases.NewDeleteUserUseCase(userRepo, logger)
	adminResetPasswordUseCase := usecases.NewAdminResetPasswordUseCase(userRepo, logger)
	// assignRoleUseCase := usecases.NewAssignRoleUseCase(userRepo, logger) // TODO: Implement when needed
	toggleUserStatusUseCase := usecases.NewToggleUserStatusUseCase(userRepo, logger)

	// Bulk use cases
	bulkUserUseCases := usecases.NewBulkUserUseCases(userRepo, validate)

	// Setup JWT service
	jwtSecret := os.Getenv("JWT_SECRET")
	if jwtSecret == "" {
		jwtSecret = "your-secret-key"
	}

	jwtService := auth.NewJWTService(jwtSecret, "sicora-userservice", 24*time.Hour)

	// Setup handlers
	userHandler := handlers.NewUserHandler(
		createUserUseCase,
		getUserUseCase,
		listUsersUseCase,
		getProfileUseCase,
		updateProfileUseCase,
		updateUserUseCase,
		deleteUserUseCase,
		authenticateUserUseCase,
		refreshTokenUseCase,
		logoutUseCase,
		forgotPasswordUseCase,
		resetPasswordUseCase,
		forceChangePasswordUseCase,
		changePasswordUseCase,
		adminResetPasswordUseCase,
		toggleUserStatusUseCase,
		bulkUserUseCases,
		validate,
		logger,
	)

	// Setup Gin router
	if os.Getenv("GIN_MODE") == "production" {
		gin.SetMode(gin.ReleaseMode)
	}

	router := gin.New()

	// Setup auth middleware configuration
	authConfig := &middleware.AuthConfig{
		JWTService: jwtService,
		SkipPaths: []string{
			"/health",
			"/docs",
			"/swagger",
			"/api/v1/auth",
			"/api/v1/users", // Only for POST (registration)
		},
		CacheTTL:        5 * time.Minute,
		EnableBlacklist: true,
	}

	// Setup rate limiter
	rateLimiter := middleware.NewRateLimiter(100, time.Minute)

	// Add global middleware
	router.Use(middleware.RequestIDMiddleware())
	router.Use(middleware.SecurityHeadersMiddleware())
	router.Use(middleware.LoggingMiddleware())
	router.Use(middleware.CORSMiddleware())
	router.Use(rateLimiter.RateLimitMiddleware()) // 100 requests per minute
	router.Use(middleware.CompressionMiddleware())
	router.Use(middleware.TimeoutMiddleware(30 * time.Second))
	router.Use(middleware.ErrorMiddleware(logger))
	router.Use(middleware.NotFoundMiddleware())

	// Setup routes with auth config
	routes.SetupUserRoutes(router, userHandler, authConfig)

	// Health check endpoint
	router.GET("/health", userHandler.HealthCheck)

	// Swagger documentation
	router.GET("/docs/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))
	router.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	// Server configuration
	port := os.Getenv("PORT")
	if port == "" {
		port = "8002" // Default port for Go UserService
	}

	server := &http.Server{
		Addr:    ":" + port,
		Handler: router,
	}

	// Start server in a goroutine
	go func() {
		logger.Printf("🚀 Server starting on port %s", port)
		logger.Printf("📊 Health check: http://localhost:%s/health", port)
		logger.Printf("📖 API endpoints: http://localhost:%s/api/v1/users", port)

		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.Fatalf("Failed to start server: %v", err)
		}
	}()

	// Wait for interrupt signal to gracefully shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	logger.Println("🛑 Shutting down server...")

	// Graceful shutdown with timeout
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		logger.Fatalf("Server forced to shutdown: %v", err)
	}

	logger.Println("✅ Server shutdown completed")
}
