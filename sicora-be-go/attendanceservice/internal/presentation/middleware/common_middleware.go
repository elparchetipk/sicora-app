package middleware

import (
	"fmt"
	"time"

	"attendanceservice/configs"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

// CORSMiddleware configura CORS
func CORSMiddleware(config *configs.Config) gin.HandlerFunc {
	corsConfig := cors.Config{
		AllowOrigins:     config.CORS.AllowedOrigins,
		AllowMethods:     config.CORS.AllowedMethods,
		AllowHeaders:     config.CORS.AllowedHeaders,
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}

	return cors.New(corsConfig)
}

// RequestLoggingMiddleware middleware para logging de requests
func RequestLoggingMiddleware() gin.HandlerFunc {
	return gin.LoggerWithFormatter(func(param gin.LogFormatterParams) string {
		return fmt.Sprintf("%s - [%s] \"%s %s %s %d %s \"%s\" %s\"\n",
			param.ClientIP,
			param.TimeStamp.Format(time.RFC1123),
			param.Method,
			param.Path,
			param.Request.Proto,
			param.StatusCode,
			param.Latency,
			param.Request.UserAgent(),
			param.ErrorMessage,
		)
	})
}

// RecoveryMiddleware middleware para recovery de panics
func RecoveryMiddleware() gin.HandlerFunc {
	return gin.CustomRecovery(func(c *gin.Context, recovered interface{}) {
		if err, ok := recovered.(string); ok {
			c.JSON(500, gin.H{
				"error":   "Internal server error",
				"code":    "INTERNAL_ERROR",
				"message": "An unexpected error occurred",
				"details": err,
			})
		}
		c.AbortWithStatus(500)
	})
}

// ValidationErrorMiddleware middleware para manejo de errores de validación
func ValidationErrorMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Next()

		// Si hay errores de validación, formatearlos
		if len(c.Errors) > 0 {
			errorMsgs := make([]string, len(c.Errors))
			for i, e := range c.Errors {
				errorMsgs[i] = e.Error()
			}

			c.JSON(400, gin.H{
				"error":   "Validation failed",
				"code":    "VALIDATION_ERROR",
				"message": "Request validation failed",
				"details": errorMsgs,
			})
			c.Abort()
		}
	}
}
