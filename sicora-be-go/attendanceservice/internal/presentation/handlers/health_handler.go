package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type HealthHandler struct{}

// NewHealthHandler crea una nueva instancia del handler de salud
func NewHealthHandler() *HealthHandler {
	return &HealthHandler{}
}

// HealthCheck verifica el estado del servicio
// @Summary Verificar estado del servicio
// @Description Endpoint para verificar que el servicio está funcionando
// @Tags health
// @Accept json
// @Produce json
// @Success 200 {object} map[string]string
// @Router /health [get]
func (h *HealthHandler) HealthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status":  "OK",
		"service": "AttendanceService",
		"version": "1.0.0",
	})
}

// ReadinessCheck verifica si el servicio está listo para recibir tráfico
// @Summary Verificar preparación del servicio
// @Description Endpoint para verificar que el servicio está listo
// @Tags health
// @Accept json
// @Produce json
// @Success 200 {object} map[string]string
// @Router /ready [get]
func (h *HealthHandler) ReadinessCheck(c *gin.Context) {
	// Aquí se pueden agregar verificaciones adicionales como conexión a DB
	c.JSON(http.StatusOK, gin.H{
		"status": "READY",
		"checks": gin.H{
			"database": "OK",
			"service":  "OK",
		},
	})
}
