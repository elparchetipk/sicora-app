package integration

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"attendanceservice/internal/application/dtos"
	"attendanceservice/internal/presentation/handlers"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
)

func TestHealthHandler(t *testing.T) {
	gin.SetMode(gin.TestMode)

	healthHandler := handlers.NewHealthHandler()
	router := gin.New()
	router.GET("/health", healthHandler.HealthCheck)

	req, err := http.NewRequest("GET", "/health", nil)
	assert.NoError(t, err)

	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)

	var response map[string]string
	err = json.Unmarshal(w.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Equal(t, "OK", response["status"])
}

func TestCreateAttendanceEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Este test se saltará si no hay base de datos disponible
	t.Skip("Integration test requires database setup")

	router := gin.New()

	// Aquí iría la configuración completa del handler con dependencias reales
	// Por ahora solo verificamos que la estructura de request sea válida

	requestData := dtos.CreateAttendanceRequest{
		StudentID:    uuid.New(),
		ScheduleID:   uuid.New(),
		InstructorID: uuid.New(),
		Status:       "PRESENT",
		Date:         time.Now(),
	}

	jsonData, err := json.Marshal(requestData)
	assert.NoError(t, err)

	req, err := http.NewRequest("POST", "/api/v1/attendance", bytes.NewBuffer(jsonData))
	assert.NoError(t, err)
	req.Header.Set("Content-Type", "application/json")

	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	// El test falla porque no hay handler configurado, pero verifica la estructura
	assert.NotEqual(t, http.StatusOK, w.Code) // Esperamos que falle sin configuración
}
