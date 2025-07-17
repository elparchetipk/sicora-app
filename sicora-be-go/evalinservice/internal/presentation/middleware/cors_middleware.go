package middleware

import (
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

// CORSConfig configuración para CORS
type CORSConfig struct {
	AllowOrigins     []string
	AllowMethods     []string
	AllowHeaders     []string
	ExposeHeaders    []string
	AllowCredentials bool
	MaxAge           int
}

// DefaultCORSConfig configuración por defecto para CORS
func DefaultCORSConfig() *CORSConfig {
	return &CORSConfig{
		AllowOrigins: []string{"*"},
		AllowMethods: []string{
			http.MethodGet,
			http.MethodPost,
			http.MethodPut,
			http.MethodPatch,
			http.MethodDelete,
			http.MethodOptions,
		},
		AllowHeaders: []string{
			"Origin",
			"Content-Type",
			"Accept",
			"Authorization",
			"X-Requested-With",
			"X-Request-ID",
		},
		ExposeHeaders: []string{
			"X-Request-ID",
			"X-Total-Count",
		},
		AllowCredentials: true,
		MaxAge:           86400, // 24 horas
	}
}

// CORS middleware que maneja las políticas de CORS
func CORS(config *CORSConfig) gin.HandlerFunc {
	if config == nil {
		config = DefaultCORSConfig()
	}

	return func(c *gin.Context) {
		origin := c.Request.Header.Get("Origin")

		// Verificar si el origen está permitido
		if len(config.AllowOrigins) > 0 {
			allowed := false
			for _, allowedOrigin := range config.AllowOrigins {
				if allowedOrigin == "*" || allowedOrigin == origin {
					allowed = true
					break
				}
			}

			if allowed {
				if origin != "" {
					c.Header("Access-Control-Allow-Origin", origin)
				} else if len(config.AllowOrigins) == 1 && config.AllowOrigins[0] != "*" {
					c.Header("Access-Control-Allow-Origin", config.AllowOrigins[0])
				} else {
					c.Header("Access-Control-Allow-Origin", "*")
				}
			}
		}

		// Configurar métodos permitidos
		if len(config.AllowMethods) > 0 {
			c.Header("Access-Control-Allow-Methods", strings.Join(config.AllowMethods, ", "))
		}

		// Configurar headers permitidos
		if len(config.AllowHeaders) > 0 {
			c.Header("Access-Control-Allow-Headers", strings.Join(config.AllowHeaders, ", "))
		}

		// Configurar headers expuestos
		if len(config.ExposeHeaders) > 0 {
			c.Header("Access-Control-Expose-Headers", strings.Join(config.ExposeHeaders, ", "))
		}

		// Configurar credenciales
		if config.AllowCredentials {
			c.Header("Access-Control-Allow-Credentials", "true")
		}

		// Configurar Max-Age
		if config.MaxAge > 0 {
			c.Header("Access-Control-Max-Age", string(rune(config.MaxAge)))
		}

		// Manejar preflight requests
		if c.Request.Method == http.MethodOptions {
			c.AbortWithStatus(http.StatusNoContent)
			return
		}

		c.Next()
	}
}

// SecurityHeaders middleware que agrega headers de seguridad
func SecurityHeaders() gin.HandlerFunc {
	return func(c *gin.Context) {
		// Prevenir ataques XSS
		c.Header("X-Content-Type-Options", "nosniff")
		c.Header("X-Frame-Options", "DENY")
		c.Header("X-XSS-Protection", "1; mode=block")

		// Configurar Content Security Policy
		c.Header("Content-Security-Policy", "default-src 'self'")

		// Prevenir información sobre el servidor
		c.Header("Server", "EvalinService")

		// Configurar referrer policy
		c.Header("Referrer-Policy", "strict-origin-when-cross-origin")

		c.Next()
	}
}

// RateLimiting middleware básico de rate limiting
func RateLimiting() gin.HandlerFunc {
	// TODO: Implementar rate limiting real con Redis o memoria
	return func(c *gin.Context) {
		// Por ahora, solo pasa la request
		c.Next()
	}
}

// Compression middleware que habilita compresión gzip
func Compression() gin.HandlerFunc {
	// TODO: Implementar compresión gzip
	return func(c *gin.Context) {
		c.Next()
	}
}
