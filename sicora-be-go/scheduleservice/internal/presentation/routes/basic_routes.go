package routes

import (
	"net/http"
	"time"

	"scheduleservice/configs"
	"scheduleservice/internal/presentation/handlers"

	"github.com/gin-gonic/gin"
)

// SetupBasicRoutes configura rutas básicas con handlers temporales
func SetupBasicRoutes(config *configs.Config) *gin.Engine {
	router := gin.New()

	// Middleware
	router.Use(gin.Logger())
	router.Use(gin.Recovery())

	// Health check endpoint
	router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":    "ok",
			"service":   "scheduleservice",
			"timestamp": time.Now(),
		})
	})

	// Handlers básicos temporales
	scheduleHandler := handlers.NewBasicScheduleHandler()
	masterDataHandler := handlers.NewBasicMasterDataHandler()

	// API routes
	api := router.Group("/api/v1")
	{
		// Schedule routes
		schedules := api.Group("/schedules")
		{
			schedules.POST("", scheduleHandler.CreateSchedule)
			schedules.GET("/:id", scheduleHandler.GetSchedule)
			schedules.GET("", scheduleHandler.ListSchedules)
			schedules.PUT("/:id", scheduleHandler.UpdateSchedule)
			schedules.DELETE("/:id", scheduleHandler.DeleteSchedule)
		}

		// Master data routes
		masterData := api.Group("/master-data")
		{
			// Academic Programs
			masterData.POST("/academic-programs", masterDataHandler.CreateAcademicProgram)
			masterData.GET("/academic-programs", masterDataHandler.ListAcademicPrograms)

			// Academic Groups
			masterData.POST("/academic-groups", masterDataHandler.CreateAcademicGroup)
			masterData.GET("/academic-groups", masterDataHandler.ListAcademicGroups)

			// Venues
			masterData.POST("/venues", masterDataHandler.CreateVenue)
			masterData.GET("/venues", masterDataHandler.ListVenues)

			// Campuses
			masterData.POST("/campuses", masterDataHandler.CreateCampus)
			masterData.GET("/campuses", masterDataHandler.ListCampuses)
		}
	}

	return router
}
