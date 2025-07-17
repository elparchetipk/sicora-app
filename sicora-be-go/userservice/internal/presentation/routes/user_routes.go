package routes

import (
	"os"

	"userservice/internal/presentation/handlers"
	"userservice/internal/presentation/middleware"

	"github.com/gin-gonic/gin"
)

// SetupUserRoutes configures all user-related routes
func SetupUserRoutes(router *gin.Engine, userHandler *handlers.UserHandler, authConfig *middleware.AuthConfig) {
	// API v1 group
	v1 := router.Group("/api/v1")
	{
		// Auth routes (no authentication required)
		auth := v1.Group("/auth")
		{
			auth.POST("/login", userHandler.AuthenticateUser)
			auth.POST("/refresh", userHandler.RefreshToken)
			auth.POST("/logout", userHandler.Logout)
			auth.POST("/forgot-password", userHandler.ForgotPassword)
			auth.POST("/reset-password", userHandler.ResetPassword)
			auth.POST("/force-change-password", userHandler.ForceChangePassword)
			// TODO: Implement these endpoints
			// auth.POST("/register", userHandler.RegisterUser)
		}

		// User routes
		users := v1.Group("/users")
		{
			// Public user routes
			users.POST("", userHandler.CreateUser) // Registration

			// Protected user routes (require authentication)
			authorized := users.Group("")
			authorized.Use(middleware.AuthMiddlewareV2(authConfig))
			authorized.Use(middleware.RequireActiveUserMiddleware())
			authorized.Use(middleware.RequirePasswordChangeMiddleware())
			{
				authorized.GET("/:id", userHandler.GetUser)
				authorized.GET("", userHandler.ListUsers)
				authorized.PUT("/:id", userHandler.UpdateUser)
				authorized.DELETE("/:id", userHandler.DeleteUser)
				authorized.GET("/profile", userHandler.GetProfile)
				authorized.PUT("/profile", userHandler.UpdateProfile)
				authorized.PUT("/profile/change-password", userHandler.ChangePassword)
			}

			// Admin-only routes
			admin := users.Group("")
			admin.Use(middleware.AuthMiddlewareV2(authConfig))
			admin.Use(middleware.RequireActiveUserMiddleware())
			admin.Use(middleware.RequireRoleMiddleware("admin", "coordinador"))
			{
				// Bulk operations routes
				admin.POST("/bulk", userHandler.BulkCreateUsers)
				admin.PUT("/bulk", userHandler.BulkUpdateUsers)
				admin.DELETE("/bulk", userHandler.BulkDeleteUsers)
				admin.PATCH("/bulk/status", userHandler.BulkChangeStatus)

				// Individual admin operations
				admin.PATCH("/:id/status", userHandler.ToggleUserStatus)
				admin.POST("/:id/reset-password", userHandler.AdminResetPassword)
				// admin.PATCH("/:id/role", userHandler.AssignRole) // TODO: implement later
			}
		}
	}
}

// getJWTSecret retrieves JWT secret from environment
func getJWTSecret() string {
	secret := os.Getenv("JWT_SECRET")
	if secret == "" {
		return "your-secret-key" // Default for development
	}
	return secret
}
