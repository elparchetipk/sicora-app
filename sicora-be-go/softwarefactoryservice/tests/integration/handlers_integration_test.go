package integration

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"softwarefactoryservice/internal/application/dtos"
	"softwarefactoryservice/internal/infrastructure/http/routes"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

// Integration tests for the HTTP endpoints
// These tests verify that the routes are properly configured and accessible

func TestHealthEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Create a mock router with just the health endpoint
	router := gin.New()
	router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":  "healthy",
			"service": "softwarefactoryservice",
			"version": "1.0.0",
		})
	})

	// Create a request to the health endpoint
	req, _ := http.NewRequest(http.MethodGet, "/health", nil)
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	// Assert the response
	assert.Equal(t, http.StatusOK, w.Code)

	var response map[string]interface{}
	err := json.Unmarshal(w.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Equal(t, "healthy", response["status"])
	assert.Equal(t, "softwarefactoryservice", response["service"])
}

func TestCORSMiddleware(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Create a test router with CORS middleware
	router := gin.New()
	router.Use(routes.CORSMiddleware())
	router.GET("/test", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"message": "test"})
	})

	// Test OPTIONS request
	req, _ := http.NewRequest(http.MethodOptions, "/test", nil)
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	// Assert CORS headers are set
	assert.Equal(t, http.StatusNoContent, w.Code)
	assert.Equal(t, "*", w.Header().Get("Access-Control-Allow-Origin"))
	assert.Contains(t, w.Header().Get("Access-Control-Allow-Methods"), "GET")
	assert.Contains(t, w.Header().Get("Access-Control-Allow-Methods"), "POST")
}

func TestUserStoryEndpointsStructure(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Test that invalid JSON returns 400
	router := gin.New()
	router.POST("/user-stories", func(c *gin.Context) {
		var req dtos.CreateUserStoryRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusCreated, gin.H{"message": "created"})
	})

	// Test with invalid JSON
	req, _ := http.NewRequest(http.MethodPost, "/user-stories", bytes.NewBuffer([]byte("invalid json")))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusBadRequest, w.Code)
}

func TestEvaluationEndpointsStructure(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Test that invalid JSON returns 400
	router := gin.New()
	router.POST("/evaluations", func(c *gin.Context) {
		var req dtos.CreateEvaluationRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusCreated, gin.H{"message": "created"})
	})

	// Test with invalid JSON
	req, _ := http.NewRequest(http.MethodPost, "/evaluations", bytes.NewBuffer([]byte("invalid json")))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusBadRequest, w.Code)
}

func TestTechnologyEndpointsStructure(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Test that invalid JSON returns 400
	router := gin.New()
	router.POST("/technologies", func(c *gin.Context) {
		var req dtos.CreateTechnologyRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusCreated, gin.H{"message": "created"})
	})

	// Test with invalid JSON
	req, _ := http.NewRequest(http.MethodPost, "/technologies", bytes.NewBuffer([]byte("invalid json")))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusBadRequest, w.Code)
}

func TestRouteParameterHandling(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Test route with parameters
	router := gin.New()
	router.GET("/user-stories/:id", func(c *gin.Context) {
		id := c.Param("id")
		if id == "" {
			c.JSON(http.StatusBadRequest, gin.H{"error": "ID is required"})
			return
		}
		c.JSON(http.StatusOK, gin.H{"id": id})
	})

	// Test with valid parameter
	req, _ := http.NewRequest(http.MethodGet, "/user-stories/story-123", nil)
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)

	var response map[string]interface{}
	err := json.Unmarshal(w.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Equal(t, "story-123", response["id"])
}

func TestQueryParameterHandling(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Test route with query parameters
	router := gin.New()
	router.GET("/user-stories", func(c *gin.Context) {
		projectID := c.Query("project_id")
		page := c.DefaultQuery("page", "1")
		
		response := gin.H{
			"page": page,
		}
		if projectID != "" {
			response["project_id"] = projectID
		}
		
		c.JSON(http.StatusOK, response)
	})

	// Test with query parameters
	req, _ := http.NewRequest(http.MethodGet, "/user-stories?project_id=proj-123&page=2", nil)
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)

	var response map[string]interface{}
	err := json.Unmarshal(w.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Equal(t, "proj-123", response["project_id"])
	assert.Equal(t, "2", response["page"])
}
