package routes

import (
	"projectevalservice/internal/infrastructure/auth"
	"projectevalservice/internal/presentation/handlers"
	"projectevalservice/internal/presentation/middleware"

	"github.com/gin-gonic/gin"
)

func SetupRoutes(
	router *gin.Engine,
	projectHandler *handlers.ProjectHandler,
	submissionHandler *handlers.SubmissionHandler,
	evaluationHandler *handlers.EvaluationHandler,
	jwtService *auth.JWTService,
) {
	// Global middleware
	router.Use(middleware.CORS())

	// Health check
	router.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok", "service": "projectevalservice"})
	})

	// API v1 routes
	v1 := router.Group("/api/v1")
	v1.Use(middleware.JWTAuth(jwtService))

	// Project routes
	projects := v1.Group("/projects")
	{
		projects.POST("", middleware.RequireRole("instructor", "admin"), projectHandler.CreateProject)
		projects.GET("", projectHandler.GetProjects)
		projects.GET("/:id", projectHandler.GetProject)
		projects.PUT("/:id", middleware.RequireRole("instructor", "admin"), projectHandler.UpdateProject)
		projects.DELETE("/:id", middleware.RequireRole("instructor", "admin"), projectHandler.DeleteProject)
	}

	// Submission routes
	submissions := v1.Group("/submissions")
	{
		submissions.POST("", middleware.RequireRole("student", "admin"), submissionHandler.CreateSubmission)
		submissions.GET("", submissionHandler.GetSubmissions)
		submissions.GET("/:id", submissionHandler.GetSubmission)
		submissions.GET("/pending", middleware.RequireRole("instructor", "admin"), submissionHandler.GetPendingEvaluations)
	}

	// Evaluation routes
	evaluations := v1.Group("/evaluations")
	{
		evaluations.POST("", middleware.RequireRole("instructor", "admin"), evaluationHandler.CreateEvaluation)
		evaluations.GET("", evaluationHandler.GetEvaluations)
		evaluations.GET("/:id", evaluationHandler.GetEvaluation)
		evaluations.PATCH("/:id/complete", middleware.RequireRole("instructor", "admin"), evaluationHandler.CompleteEvaluation)
		evaluations.PATCH("/:id/publish", middleware.RequireRole("instructor", "admin"), evaluationHandler.PublishEvaluation)
	}
}
