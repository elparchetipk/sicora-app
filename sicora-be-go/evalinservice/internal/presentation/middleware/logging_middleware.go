package middleware

import (
	"bytes"
	"io"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

// LoggingMiddleware proporciona logging estructurado para las requests HTTP
type LoggingMiddleware struct {
	logger *logrus.Logger
}

// responseWriter envuelve el ResponseWriter para capturar el body de la respuesta
type responseWriter struct {
	gin.ResponseWriter
	body *bytes.Buffer
}

// Write captura el contenido de la respuesta
func (w responseWriter) Write(b []byte) (int, error) {
	w.body.Write(b)
	return w.ResponseWriter.Write(b)
}

// NewLoggingMiddleware crea un nuevo middleware de logging
func NewLoggingMiddleware(logger *logrus.Logger) *LoggingMiddleware {
	return &LoggingMiddleware{
		logger: logger,
	}
}

// Logger middleware que registra todas las requests HTTP
func (m *LoggingMiddleware) Logger() gin.HandlerFunc {
	return func(c *gin.Context) {
		startTime := time.Now()

		// Crear un nuevo responseWriter para capturar la respuesta
		bodyBuffer := &bytes.Buffer{}
		writer := &responseWriter{
			ResponseWriter: c.Writer,
			body:           bodyBuffer,
		}
		c.Writer = writer

		// Capturar el body de la request si es necesario
		var requestBody []byte
		if c.Request.Body != nil {
			requestBody, _ = io.ReadAll(c.Request.Body)
			c.Request.Body = io.NopCloser(bytes.NewBuffer(requestBody))
		}

		// Procesar la request
		c.Next()

		// Calcular el tiempo de respuesta
		latency := time.Since(startTime)

		// Obtener información del usuario si está disponible
		userID, _ := c.Get("user_id")
		userRole, _ := c.Get("user_role")

		// Determinar el nivel de log basado en el status code
		logLevel := m.getLogLevel(c.Writer.Status())

		// Crear el log entry
		logEntry := m.logger.WithFields(logrus.Fields{
			"method":        c.Request.Method,
			"path":          c.Request.URL.Path,
			"query":         c.Request.URL.RawQuery,
			"status_code":   c.Writer.Status(),
			"latency":       latency,
			"client_ip":     c.ClientIP(),
			"user_agent":    c.Request.UserAgent(),
			"referer":       c.Request.Referer(),
			"request_id":    c.GetHeader("X-Request-ID"),
			"content_type":  c.Request.Header.Get("Content-Type"),
			"response_size": bodyBuffer.Len(),
		})

		// Agregar información del usuario si está disponible
		if userID != nil {
			logEntry = logEntry.WithField("user_id", userID)
		}
		if userRole != nil {
			logEntry = logEntry.WithField("user_role", userRole)
		}

		// Agregar body de la request para métodos que lo requieren (solo para debug)
		if len(requestBody) > 0 && m.shouldLogRequestBody(c.Request.Method) {
			logEntry = logEntry.WithField("request_body", string(requestBody))
		}

		// Agregar errores si existen
		if len(c.Errors) > 0 {
			logEntry = logEntry.WithField("errors", c.Errors)
		}

		// Registrar según el nivel apropiado
		switch logLevel {
		case logrus.ErrorLevel:
			logEntry.Error("HTTP Request")
		case logrus.WarnLevel:
			logEntry.Warn("HTTP Request")
		case logrus.InfoLevel:
			logEntry.Info("HTTP Request")
		default:
			logEntry.Debug("HTTP Request")
		}
	}
}

// getLogLevel determina el nivel de log basado en el status code
func (m *LoggingMiddleware) getLogLevel(statusCode int) logrus.Level {
	switch {
	case statusCode >= 500:
		return logrus.ErrorLevel
	case statusCode >= 400:
		return logrus.WarnLevel
	case statusCode >= 300:
		return logrus.InfoLevel
	default:
		return logrus.InfoLevel
	}
}

// shouldLogRequestBody determina si se debe registrar el body de la request
func (m *LoggingMiddleware) shouldLogRequestBody(method string) bool {
	return method == "POST" || method == "PUT" || method == "PATCH"
}

// RequestID middleware que agrega un ID único a cada request
func RequestID() gin.HandlerFunc {
	return func(c *gin.Context) {
		requestID := c.GetHeader("X-Request-ID")
		if requestID == "" {
			requestID = generateRequestID()
		}

		c.Header("X-Request-ID", requestID)
		c.Set("request_id", requestID)
		c.Next()
	}
}

// generateRequestID genera un ID único para la request
func generateRequestID() string {
	// Implementación simple usando timestamp + random
	return time.Now().Format("20060102150405") + "-" + "random"
}

// Recovery middleware personalizado que registra panics
func Recovery(logger *logrus.Logger) gin.HandlerFunc {
	return gin.CustomRecovery(func(c *gin.Context, recovered interface{}) {
		logger.WithFields(logrus.Fields{
			"panic":      recovered,
			"method":     c.Request.Method,
			"path":       c.Request.URL.Path,
			"client_ip":  c.ClientIP(),
			"user_agent": c.Request.UserAgent(),
			"request_id": c.GetHeader("X-Request-ID"),
		}).Error("Panic recovered")

		c.JSON(500, gin.H{
			"error":   "Internal server error",
			"message": "An unexpected error occurred",
		})
	})
}
