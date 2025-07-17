package routes

import (
	"log"

	"scheduleservice/internal/application/usecases"
	"scheduleservice/internal/presentation/handlers"
	"scheduleservice/internal/presentation/middleware"

	"github.com/gin-gonic/gin"
)

// SetupScheduleRoutes configura las rutas para horarios
func SetupScheduleRoutes(
	router *gin.Engine,
	createUseCase *usecases.CreateScheduleUseCase,
	getUseCase *usecases.GetScheduleUseCase,
	updateUseCase *usecases.UpdateScheduleUseCase,
	deleteUseCase *usecases.DeleteScheduleUseCase,
	listUseCase *usecases.ListSchedulesUseCase,
	bulkUseCases *usecases.BulkScheduleUseCases,
	authMiddleware *middleware.AuthMiddleware,
	logger *log.Logger,
) {
	// Crear handler
	scheduleHandler := handlers.NewScheduleHandler(
		createUseCase,
		getUseCase,
		updateUseCase,
		deleteUseCase,
		listUseCase,
		bulkUseCases,
		logger,
	)

	// Grupo de rutas API con autenticación
	api := router.Group("/api/v1")
	api.Use(authMiddleware.AuthenticateJWT())

	// Rutas de horarios
	schedules := api.Group("/schedules")
	{
		// CRUD básico
		schedules.POST("",
			authMiddleware.RequirePermission(middleware.PermScheduleCreate),
			scheduleHandler.CreateSchedule)

		schedules.GET("/:id",
			authMiddleware.RequirePermission(middleware.PermScheduleRead),
			scheduleHandler.GetSchedule)

		schedules.PUT("/:id",
			authMiddleware.RequirePermission(middleware.PermScheduleUpdate),
			scheduleHandler.UpdateSchedule)

		schedules.DELETE("/:id",
			authMiddleware.RequirePermission(middleware.PermScheduleDelete),
			scheduleHandler.DeleteSchedule)

		schedules.GET("",
			authMiddleware.RequirePermission(middleware.PermScheduleRead),
			scheduleHandler.ListSchedules)

		// Operaciones bulk
		schedules.POST("/bulk",
			authMiddleware.RequirePermission(middleware.PermScheduleBulkCreate),
			scheduleHandler.BulkCreateSchedules)

		schedules.POST("/upload-csv",
			authMiddleware.RequirePermission(middleware.PermScheduleBulkCreate),
			scheduleHandler.UploadSchedulesCSV)
	}
}

// SetupMasterDataRoutes configura las rutas para entidades maestras
func SetupMasterDataRoutes(
	router *gin.Engine,
	// Academic Program use cases
	createProgramUseCase *usecases.CreateAcademicProgramUseCase,
	getProgramUseCase *usecases.GetAcademicProgramUseCase,
	updateProgramUseCase *usecases.UpdateAcademicProgramUseCase,
	deleteProgramUseCase *usecases.DeleteAcademicProgramUseCase,
	listProgramsUseCase *usecases.ListAcademicProgramsUseCase,

	// Academic Group use cases
	createGroupUseCase *usecases.CreateAcademicGroupUseCase,
	getGroupUseCase *usecases.GetAcademicGroupUseCase,
	updateGroupUseCase *usecases.UpdateAcademicGroupUseCase,
	deleteGroupUseCase *usecases.DeleteAcademicGroupUseCase,
	listGroupsUseCase *usecases.ListAcademicGroupsUseCase,

	// Venue use cases
	createVenueUseCase *usecases.CreateVenueUseCase,
	getVenueUseCase *usecases.GetVenueUseCase,
	updateVenueUseCase *usecases.UpdateVenueUseCase,
	deleteVenueUseCase *usecases.DeleteVenueUseCase,
	listVenuesUseCase *usecases.ListVenuesUseCase,

	// Campus use cases
	createCampusUseCase *usecases.CreateCampusUseCase,
	getCampusUseCase *usecases.GetCampusUseCase,
	updateCampusUseCase *usecases.UpdateCampusUseCase,
	deleteCampusUseCase *usecases.DeleteCampusUseCase,
	listCampusesUseCase *usecases.ListCampusesUseCase,

	authMiddleware *middleware.AuthMiddleware,
	logger *log.Logger,
) {
	// Crear handlers para entidades maestras
	masterDataHandler := handlers.NewMasterDataHandler(
		// Program handlers
		createProgramUseCase, getProgramUseCase, updateProgramUseCase,
		deleteProgramUseCase, listProgramsUseCase,
		// Group handlers
		createGroupUseCase, getGroupUseCase, updateGroupUseCase,
		deleteGroupUseCase, listGroupsUseCase,
		// Venue handlers
		createVenueUseCase, getVenueUseCase, updateVenueUseCase,
		deleteVenueUseCase, listVenuesUseCase,
		// Campus handlers
		createCampusUseCase, getCampusUseCase, updateCampusUseCase,
		deleteCampusUseCase, listCampusesUseCase,
		logger,
	)

	// Grupo de rutas API con autenticación
	api := router.Group("/api/v1")
	api.Use(authMiddleware.AuthenticateJWT())

	// Rutas para programas académicos
	programs := api.Group("/academic-programs")
	programs.Use(authMiddleware.RequirePermission(middleware.PermMasterDataRead))
	{
		programs.GET("", masterDataHandler.ListAcademicPrograms)
		programs.GET("/:id", masterDataHandler.GetAcademicProgram)

		// Solo administradores pueden modificar
		programs.POST("",
			authMiddleware.RequirePermission(middleware.PermMasterDataCreate),
			masterDataHandler.CreateAcademicProgram)
		programs.PUT("/:id",
			authMiddleware.RequirePermission(middleware.PermMasterDataUpdate),
			masterDataHandler.UpdateAcademicProgram)
		programs.DELETE("/:id",
			authMiddleware.RequirePermission(middleware.PermMasterDataDelete),
			masterDataHandler.DeleteAcademicProgram)
	}

	// Rutas para grupos académicos
	groups := api.Group("/academic-groups")
	groups.Use(authMiddleware.RequirePermission(middleware.PermMasterDataRead))
	{
		groups.GET("", masterDataHandler.ListAcademicGroups)
		groups.GET("/:id", masterDataHandler.GetAcademicGroup)

		groups.POST("",
			authMiddleware.RequirePermission(middleware.PermMasterDataCreate),
			masterDataHandler.CreateAcademicGroup)
		groups.PUT("/:id",
			authMiddleware.RequirePermission(middleware.PermMasterDataUpdate),
			masterDataHandler.UpdateAcademicGroup)
		groups.DELETE("/:id",
			authMiddleware.RequirePermission(middleware.PermMasterDataDelete),
			masterDataHandler.DeleteAcademicGroup)
	}

	// Rutas para ambientes
	venues := api.Group("/venues")
	venues.Use(authMiddleware.RequirePermission(middleware.PermMasterDataRead))
	{
		venues.GET("", masterDataHandler.ListVenues)
		venues.GET("/:id", masterDataHandler.GetVenue)

		venues.POST("",
			authMiddleware.RequirePermission(middleware.PermMasterDataCreate),
			masterDataHandler.CreateVenue)
		venues.PUT("/:id",
			authMiddleware.RequirePermission(middleware.PermMasterDataUpdate),
			masterDataHandler.UpdateVenue)
		venues.DELETE("/:id",
			authMiddleware.RequirePermission(middleware.PermMasterDataDelete),
			masterDataHandler.DeleteVenue)
	}

	// Rutas para sedes
	campuses := api.Group("/campuses")
	campuses.Use(authMiddleware.RequirePermission(middleware.PermMasterDataRead))
	{
		campuses.GET("", masterDataHandler.ListCampuses)
		campuses.GET("/:id", masterDataHandler.GetCampus)

		campuses.POST("",
			authMiddleware.RequirePermission(middleware.PermMasterDataCreate),
			masterDataHandler.CreateCampus)
		campuses.PUT("/:id",
			authMiddleware.RequirePermission(middleware.PermMasterDataUpdate),
			masterDataHandler.UpdateCampus)
		campuses.DELETE("/:id",
			authMiddleware.RequirePermission(middleware.PermMasterDataDelete),
			masterDataHandler.DeleteCampus)
	}
}

// SetupHealthRoutes configura rutas de salud del servicio
func SetupHealthRoutes(router *gin.Engine) {
	health := router.Group("/health")
	{
		health.GET("/", func(c *gin.Context) {
			c.JSON(200, gin.H{
				"status":  "OK",
				"service": "scheduleservice",
				"version": "1.0.0",
			})
		})

		health.GET("/ready", func(c *gin.Context) {
			// TODO: Add database connectivity check
			c.JSON(200, gin.H{
				"status": "ready",
			})
		})

		health.GET("/live", func(c *gin.Context) {
			c.JSON(200, gin.H{
				"status": "alive",
			})
		})
	}
}
