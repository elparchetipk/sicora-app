package middleware

import (
	"context"
	"fmt"
	"net/http"
	"strings"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
)

// RateLimiter estructura para rate limiting
type RateLimiter struct {
	requests map[string][]time.Time
	mutex    sync.RWMutex
	limit    int
	window   time.Duration
}

// NewRateLimiter crea un nuevo rate limiter
func NewRateLimiter(limit int, window time.Duration) *RateLimiter {
	return &RateLimiter{
		requests: make(map[string][]time.Time),
		limit:    limit,
		window:   window,
	}
}

// RateLimitMiddleware middleware para rate limiting
func (rl *RateLimiter) RateLimitMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		clientIP := c.ClientIP()

		rl.mutex.Lock()
		defer rl.mutex.Unlock()

		now := time.Now()

		// Limpiar requests antiguos
		if requests, exists := rl.requests[clientIP]; exists {
			var validRequests []time.Time
			cutoff := now.Add(-rl.window)

			for _, reqTime := range requests {
				if reqTime.After(cutoff) {
					validRequests = append(validRequests, reqTime)
				}
			}
			rl.requests[clientIP] = validRequests
		}

		// Verificar límite
		if len(rl.requests[clientIP]) >= rl.limit {
			c.JSON(http.StatusTooManyRequests, gin.H{
				"error":       "RATE_LIMIT_EXCEEDED",
				"message":     fmt.Sprintf("Rate limit exceeded. Maximum %d requests per %v", rl.limit, rl.window),
				"retry_after": rl.window.Seconds(),
			})
			c.Abort()
			return
		}

		// Agregar request actual
		rl.requests[clientIP] = append(rl.requests[clientIP], now)

		c.Next()
	}
}

// SecurityHeadersMiddleware agrega headers de seguridad
func SecurityHeadersMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Header("X-Content-Type-Options", "nosniff")
		c.Header("X-Frame-Options", "DENY")
		c.Header("X-XSS-Protection", "1; mode=block")
		c.Header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
		c.Header("Referrer-Policy", "strict-origin-when-cross-origin")
		c.Header("Content-Security-Policy", "default-src 'self'")
		c.Header("X-Permitted-Cross-Domain-Policies", "none")

		c.Next()
	}
}

// AdvancedRequestIDMiddleware agrega un ID único a cada request con más información
func AdvancedRequestIDMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		requestID := generateRequestID()
		c.Header("X-Request-ID", requestID)
		c.Set("request_id", requestID)
		c.Next()
	}
}

// AdvancedLoggingMiddleware logging mejorado con más información
func AdvancedLoggingMiddleware() gin.HandlerFunc {
	return gin.LoggerWithFormatter(func(param gin.LogFormatterParams) string {
		var statusColor, methodColor, resetColor string
		if param.IsOutputColor() {
			statusColor = param.StatusCodeColor()
			methodColor = param.MethodColor()
			resetColor = param.ResetColor()
		}

		userAgent := param.Request.UserAgent()
		if len(userAgent) > 50 {
			userAgent = userAgent[:50] + "..."
		}

		return fmt.Sprintf("[GIN] %v |%s %3d %s| %13v | %15s |%s %-7s %s %#v | %s | %s\n%s",
			param.TimeStamp.Format("2006/01/02 - 15:04:05"),
			statusColor, param.StatusCode, resetColor,
			param.Latency,
			param.ClientIP,
			methodColor, param.Method, resetColor,
			param.Path,
			userAgent,
			param.ErrorMessage,
			resetColor,
		)
	})
}

// ErrorHandlingMiddleware manejo centralizado de errores
func ErrorHandlingMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Next()

		// Procesar errores después de que se ejecuten los handlers
		if len(c.Errors) > 0 {
			err := c.Errors.Last()

			switch err.Type {
			case gin.ErrorTypeBind:
				c.JSON(http.StatusBadRequest, gin.H{
					"error":   "VALIDATION_ERROR",
					"message": "Invalid request format",
					"details": err.Error(),
				})
			case gin.ErrorTypePublic:
				c.JSON(http.StatusInternalServerError, gin.H{
					"error":   "INTERNAL_ERROR",
					"message": err.Error(),
				})
			default:
				c.JSON(http.StatusInternalServerError, gin.H{
					"error":   "UNKNOWN_ERROR",
					"message": "An unexpected error occurred",
				})
			}
		}
	}
}

// TimeoutMiddleware middleware para timeout de requests
func TimeoutMiddleware(timeout time.Duration) gin.HandlerFunc {
	return func(c *gin.Context) {
		// Crear un contexto con timeout
		ctx, cancel := context.WithTimeout(c.Request.Context(), timeout)
		defer cancel()

		// Reemplazar el contexto de la request
		c.Request = c.Request.WithContext(ctx)

		finished := make(chan struct{})
		go func() {
			c.Next()
			finished <- struct{}{}
		}()

		select {
		case <-finished:
			// Request completado normalmente
			return
		case <-ctx.Done():
			// Timeout alcanzado
			c.JSON(http.StatusRequestTimeout, gin.H{
				"error":   "REQUEST_TIMEOUT",
				"message": "Request timed out",
				"timeout": timeout.String(),
			})
			c.Abort()
		}
	}
}

// Helper functions

func generateRequestID() string {
	// Generar un ID único para el request
	// En producción, se podría usar una librería más robusta
	timestamp := time.Now().UnixNano()
	return fmt.Sprintf("req_%d", timestamp)
}

// CompressionMiddleware middleware para compresión de respuestas
func CompressionMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		// Verificar si el cliente acepta compresión
		acceptEncoding := c.GetHeader("Accept-Encoding")
		if strings.Contains(acceptEncoding, "gzip") {
			c.Header("Content-Encoding", "gzip")
		}
		c.Next()
	}
}

// HealthCheckSkipMiddleware omite middleware pesado para health checks
func HealthCheckSkipMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		if c.Request.URL.Path == "/health" || c.Request.URL.Path == "/readiness" {
			c.Next()
			return
		}
		c.Next()
	}
}
