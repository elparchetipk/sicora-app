package routes

import (
	"github.com/gin-gonic/gin"

	"mevalservice/internal/presentation/handlers"
	"mevalservice/internal/presentation/middleware"
)

// SetupRoutes configures all routes for the MEvalService
func SetupRoutes(
	r *gin.Engine,
	committeeHandler *handlers.CommitteeHandler,
	studentCaseHandler *handlers.StudentCaseHandler,
	improvementPlanHandler *handlers.ImprovementPlanHandler,
	sanctionHandler *handlers.SanctionHandler,
	appealHandler *handlers.AppealHandler,
	healthHandler *handlers.HealthHandler,
) {
	// Health check endpoint (no authentication required)
	r.GET("/health", healthHandler.Health)
	
	// API v1 routes
	v1 := r.Group("/api/v1")
	{
		// Apply middleware
		v1.Use(middleware.RequestLogger())
		v1.Use(middleware.CORS())
		
		// Committee routes
		committees := v1.Group("/committees")
		{
			committees.POST("", committeeHandler.CreateCommittee)
			committees.GET("", committeeHandler.GetAllCommittees)
			committees.GET("/:id", committeeHandler.GetCommitteeByID)
			committees.PUT("/:id", committeeHandler.UpdateCommittee)
			committees.DELETE("/:id", committeeHandler.DeleteCommittee)
			committees.GET("/by-center", committeeHandler.GetCommitteesByCenter)
			committees.GET("/by-type", committeeHandler.GetCommitteesByType)
		}

		// Student Cases routes
		studentCases := v1.Group("/student-cases")
		{
			studentCases.POST("", studentCaseHandler.CreateStudentCase)
			studentCases.GET("/:id", studentCaseHandler.GetStudentCaseByID)
			studentCases.PUT("/:id", studentCaseHandler.UpdateStudentCase)
			studentCases.GET("/by-student", studentCaseHandler.GetStudentCasesByStudentID)
			studentCases.GET("/pending", studentCaseHandler.GetPendingStudentCases)
			studentCases.GET("/overdue", studentCaseHandler.GetOverdueStudentCases)
		}

		// Improvement Plans routes
		improvementPlans := v1.Group("/improvement-plans")
		{
			improvementPlans.POST("", improvementPlanHandler.CreateImprovementPlan)
			improvementPlans.GET("/:id", improvementPlanHandler.GetImprovementPlanByID)
			improvementPlans.PUT("/:id", improvementPlanHandler.UpdateImprovementPlan)
			improvementPlans.GET("/student-case/:student_case_id", improvementPlanHandler.GetImprovementPlansByStudentCaseID)
			improvementPlans.PATCH("/:id/progress", improvementPlanHandler.UpdateProgress)
		}

		// Sanctions routes
		sanctions := v1.Group("/sanctions")
		{
			sanctions.POST("", sanctionHandler.CreateSanction)
			sanctions.GET("/:id", sanctionHandler.GetSanctionByID)
			sanctions.GET("/student/:student_id", sanctionHandler.GetSanctionsByStudentID)
			sanctions.PATCH("/:id/activate", sanctionHandler.ActivateSanction)
			sanctions.PATCH("/:id/complete", sanctionHandler.CompleteSanction)
		}

		// Appeals routes
		appeals := v1.Group("/appeals")
		{
			appeals.POST("", appealHandler.CreateAppeal)
			appeals.GET("/:id", appealHandler.GetAppealByID)
			appeals.GET("/student/:student_id", appealHandler.GetAppealsByStudentID)
			appeals.PATCH("/:id/process", appealHandler.ProcessAppeal)
		}
		// - Improvement Plans routes
		// - Sanctions routes  
		// - Appeals routes
		// - Committee Decisions routes
		// - Committee Members routes
	}
}
