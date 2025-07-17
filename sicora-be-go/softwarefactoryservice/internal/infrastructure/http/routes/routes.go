package routes

import (
	"net/http"

	"softwarefactoryservice/internal/infrastructure/http/handlers"

	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

// Router holds all the route handlers
type Router struct {
	projectHandler    *handlers.ProjectHandler
	teamHandler       *handlers.TeamHandler
	sprintHandler     *handlers.SprintHandler
	userStoryHandler  *handlers.UserStoryHandler
	evaluationHandler *handlers.EvaluationHandler
	technologyHandler *handlers.TechnologyHandler
}

// NewRouter creates a new router instance
func NewRouter(
	projectHandler *handlers.ProjectHandler,
	teamHandler *handlers.TeamHandler,
	sprintHandler *handlers.SprintHandler,
	userStoryHandler *handlers.UserStoryHandler,
	evaluationHandler *handlers.EvaluationHandler,
	technologyHandler *handlers.TechnologyHandler,
) *Router {
	return &Router{
		projectHandler:    projectHandler,
		teamHandler:       teamHandler,
		sprintHandler:     sprintHandler,
		userStoryHandler:  userStoryHandler,
		evaluationHandler: evaluationHandler,
		technologyHandler: technologyHandler,
	}
}

// SetupRoutes configures all the routes
func (r *Router) SetupRoutes() *gin.Engine {
	// Create Gin router
	router := gin.New()

	// Add middleware
	router.Use(gin.Logger())
	router.Use(gin.Recovery())
	router.Use(CORSMiddleware())

	// Health check
	router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":  "healthy",
			"service": "softwarefactoryservice",
			"version": "1.0.0",
		})
	})

	// API documentation
	router.GET("/docs/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	// API v1 routes
	v1 := router.Group("/api/v1")
	{
		// Project routes
		projects := v1.Group("/projects")
		{
			projects.POST("", r.projectHandler.CreateProject)
			projects.GET("", r.projectHandler.ListProjects)
			projects.GET("/:id", r.projectHandler.GetProject)
			projects.PUT("/:id", r.projectHandler.UpdateProject)
			projects.DELETE("/:id", r.projectHandler.DeleteProject)
			projects.GET("/:id/stats", r.projectHandler.GetProjectStats)
		}

		// Team routes
		teams := v1.Group("/teams")
		{
			teams.POST("", r.teamHandler.CreateTeam)
			teams.GET("", r.teamHandler.ListTeams)
			teams.GET("/:id", r.teamHandler.GetTeam)
			teams.PUT("/:id", r.teamHandler.UpdateTeam)
			teams.DELETE("/:id", r.teamHandler.DeleteTeam)
			teams.POST("/:id/members", r.teamHandler.AddTeamMember)
			teams.DELETE("/:id/members/:userId", r.teamHandler.RemoveTeamMember)
			teams.GET("/:id/members", r.teamHandler.GetTeamMembers)
			teams.GET("/:id/stats", r.teamHandler.GetTeamStats)
		}

		// Sprint routes
		sprints := v1.Group("/sprints")
		{
			sprints.POST("", r.sprintHandler.CreateSprint)
			sprints.GET("", r.sprintHandler.ListSprints)
			sprints.GET("/:id", r.sprintHandler.GetSprint)
			sprints.PUT("/:id", r.sprintHandler.UpdateSprint)
			sprints.DELETE("/:id", r.sprintHandler.DeleteSprint)
			sprints.POST("/:id/start", r.sprintHandler.StartSprint)
			sprints.POST("/:id/complete", r.sprintHandler.CompleteSprint)
			sprints.GET("/:id/backlog", r.sprintHandler.GetSprintBacklog)
			// User stories in sprint
			sprints.GET("/:sprint_id/user-stories", r.userStoryHandler.GetUserStoriesBySprint)
		}

		// User Story routes
		userStories := v1.Group("/user-stories")
		{
			userStories.POST("", r.userStoryHandler.CreateUserStory)
			userStories.GET("", r.userStoryHandler.ListUserStories)
			userStories.GET("/:id", r.userStoryHandler.GetUserStory)
			userStories.PUT("/:id", r.userStoryHandler.UpdateUserStory)
			userStories.DELETE("/:id", r.userStoryHandler.DeleteUserStory)
			userStories.POST("/:user_story_id/assign-sprint/:sprint_id", r.userStoryHandler.AssignToSprint)
			userStories.POST("/:user_story_id/unassign-sprint", r.userStoryHandler.UnassignFromSprint)
			userStories.PUT("/:user_story_id/status", r.userStoryHandler.UpdateStatus)
		}

		// Project-specific user story routes
		projects.GET("/:project_id/user-stories", r.userStoryHandler.GetUserStoriesByProject)
		projects.GET("/:project_id/backlog", r.userStoryHandler.GetBacklog)
		
		// Evaluation routes
		evaluations := v1.Group("/evaluations")
		{
			evaluations.POST("", r.evaluationHandler.CreateEvaluation)
			evaluations.GET("", r.evaluationHandler.ListEvaluations)
			evaluations.GET("/:id", r.evaluationHandler.GetEvaluation)
			evaluations.PUT("/:id", r.evaluationHandler.UpdateEvaluation)
			evaluations.DELETE("/:id", r.evaluationHandler.DeleteEvaluation)
			evaluations.GET("/type/:evaluation_type", r.evaluationHandler.GetEvaluationsByType)
		}

		// Project-specific evaluation routes
		projects.GET("/:project_id/evaluations", r.evaluationHandler.GetEvaluationsByProject)
		
		// Student-specific evaluation routes
		students := v1.Group("/students")
		{
			students.GET("/:student_id/evaluations", r.evaluationHandler.GetEvaluationsByStudent)
			students.GET("/:student_id/projects/:project_id/average-score", r.evaluationHandler.GetStudentAverageScore)
		}

		// Evaluator-specific evaluation routes
		evaluators := v1.Group("/evaluators")
		{
			evaluators.GET("/:evaluator_id/evaluations", r.evaluationHandler.GetEvaluationsByEvaluator)
		}

		// Technology routes
		technologies := v1.Group("/technologies")
		{
			technologies.POST("", r.technologyHandler.CreateTechnology)
			technologies.GET("", r.technologyHandler.ListTechnologies)
			technologies.GET("/:id", r.technologyHandler.GetTechnology)
			technologies.PUT("/:id", r.technologyHandler.UpdateTechnology)
			technologies.DELETE("/:id", r.technologyHandler.DeleteTechnology)
			technologies.GET("/name/:name", r.technologyHandler.GetTechnologyByName)
			technologies.GET("/category/:category", r.technologyHandler.GetTechnologiesByCategory)
			technologies.GET("/level/:level", r.technologyHandler.GetTechnologiesByLevel)
			technologies.GET("/recommended", r.technologyHandler.GetRecommendedTechnologies)
			technologies.GET("/stats", r.technologyHandler.GetTechnologyStats)
			technologies.POST("/:id/activate", r.technologyHandler.ActivateTechnology)
			technologies.POST("/:id/deactivate", r.technologyHandler.DeactivateTechnology)
		}

		// Project-specific technology routes
		projects.GET("/:project_id/technologies", r.technologyHandler.GetProjectTechnologies)
		projects.POST("/:project_id/technologies/:technology_id", r.technologyHandler.AddProjectTechnology)
		projects.DELETE("/:project_id/technologies/:technology_id", r.technologyHandler.RemoveProjectTechnology)
	}

	return router
}

// CORSMiddleware handles CORS headers
func CORSMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, DELETE")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	}
}
