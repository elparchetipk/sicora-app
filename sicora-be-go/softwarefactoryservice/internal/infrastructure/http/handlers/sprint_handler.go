package handlers

import (
	"net/http"
	"strconv"

	"softwarefactoryservice/internal/application/dtos"
	"softwarefactoryservice/internal/application/usecases"
	"softwarefactoryservice/internal/domain/entities"
	"softwarefactoryservice/internal/domain/repositories"

	"github.com/gin-gonic/gin"
)

// SprintHandler handles HTTP requests for sprints
type SprintHandler struct {
	sprintUseCases *usecases.SprintUseCases
}

// NewSprintHandler creates a new sprint handler
func NewSprintHandler(sprintUseCases *usecases.SprintUseCases) *SprintHandler {
	return &SprintHandler{
		sprintUseCases: sprintUseCases,
	}
}

// CreateSprint creates a new sprint
// @Summary Create a new sprint
// @Description Create a new sprint with learning objectives
// @Tags sprints
// @Accept json
// @Produce json
// @Param sprint body dtos.CreateSprintRequest true "Sprint data"
// @Success 201 {object} dtos.SprintResponse
// @Failure 400 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /sprints [post]
func (h *SprintHandler) CreateSprint(c *gin.Context) {
	var req dtos.CreateSprintRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	sprint, err := h.sprintUseCases.CreateSprint(c.Request.Context(), req)
	if err != nil {
		if _, ok := err.(*entities.ValidationError); ok {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		if _, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
			return
		}
		if _, ok := err.(*entities.BusinessRuleError); ok {
			c.JSON(http.StatusConflict, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
		return
	}

	response := dtos.ToSprintResponse(sprint)
	c.JSON(http.StatusCreated, response)
}

// GetSprint retrieves a sprint by ID
// @Summary Get sprint by ID
// @Description Get a specific sprint by its ID
// @Tags sprints
// @Produce json
// @Param id path string true "Sprint ID"
// @Success 200 {object} dtos.SprintResponse
// @Failure 404 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /sprints/{id} [get]
func (h *SprintHandler) GetSprint(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Sprint ID is required"})
		return
	}

	sprint, err := h.sprintUseCases.GetSprintByID(c.Request.Context(), id)
	if err != nil {
		if _, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
		return
	}

	response := dtos.ToSprintResponse(sprint)
	c.JSON(http.StatusOK, response)
}

// UpdateSprint updates an existing sprint
// @Summary Update sprint
// @Description Update an existing sprint
// @Tags sprints
// @Accept json
// @Produce json
// @Param id path string true "Sprint ID"
// @Param sprint body dtos.UpdateSprintRequest true "Sprint update data"
// @Success 200 {object} dtos.SprintResponse
// @Failure 400 {object} map[string]interface{}
// @Failure 404 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /sprints/{id} [put]
func (h *SprintHandler) UpdateSprint(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Sprint ID is required"})
		return
	}

	var req dtos.UpdateSprintRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	sprint, err := h.sprintUseCases.UpdateSprint(c.Request.Context(), id, req)
	if err != nil {
		if _, ok := err.(*entities.ValidationError); ok {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		if _, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
		return
	}

	response := dtos.ToSprintResponse(sprint)
	c.JSON(http.StatusOK, response)
}

// DeleteSprint deletes a sprint
// @Summary Delete sprint
// @Description Delete a sprint by ID
// @Tags sprints
// @Param id path string true "Sprint ID"
// @Success 204
// @Failure 404 {object} map[string]interface{}
// @Failure 409 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /sprints/{id} [delete]
func (h *SprintHandler) DeleteSprint(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Sprint ID is required"})
		return
	}

	err := h.sprintUseCases.DeleteSprint(c.Request.Context(), id)
	if err != nil {
		if _, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
			return
		}
		if _, ok := err.(*entities.BusinessRuleError); ok {
			c.JSON(http.StatusConflict, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
		return
	}

	c.Status(http.StatusNoContent)
}

// GetSprintsByProject retrieves sprints by project ID
// @Summary Get sprints by project
// @Description Get all sprints for a specific project
// @Tags sprints
// @Produce json
// @Param project_id path string true "Project ID"
// @Success 200 {array} dtos.SprintResponse
// @Failure 500 {object} map[string]interface{}
// @Router /projects/{project_id}/sprints [get]
func (h *SprintHandler) GetSprintsByProject(c *gin.Context) {
	projectID := c.Param("project_id")
	if projectID == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Project ID is required"})
		return
	}

	sprints, err := h.sprintUseCases.GetSprintsByProject(c.Request.Context(), projectID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
		return
	}

	responses := make([]dtos.SprintResponse, len(sprints))
	for i, sprint := range sprints {
		responses[i] = *dtos.ToSprintResponse(sprint)
	}

	c.JSON(http.StatusOK, responses)
}

// StartSprint starts a sprint
// @Summary Start sprint
// @Description Start a sprint (change status to active)
// @Tags sprints
// @Param id path string true "Sprint ID"
// @Success 200 {object} dtos.SprintResponse
// @Failure 404 {object} map[string]interface{}
// @Failure 409 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /sprints/{id}/start [post]
func (h *SprintHandler) StartSprint(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Sprint ID is required"})
		return
	}

	sprint, err := h.sprintUseCases.StartSprint(c.Request.Context(), id)
	if err != nil {
		if _, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
			return
		}
		if _, ok := err.(*entities.BusinessRuleError); ok {
			c.JSON(http.StatusConflict, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
		return
	}

	response := dtos.ToSprintResponse(sprint)
	c.JSON(http.StatusOK, response)
}

// CompleteSprint completes a sprint
// @Summary Complete sprint
// @Description Complete a sprint (change status to completed)
// @Tags sprints
// @Param id path string true "Sprint ID"
// @Success 200 {object} dtos.SprintResponse
// @Failure 404 {object} map[string]interface{}
// @Failure 409 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /sprints/{id}/complete [post]
func (h *SprintHandler) CompleteSprint(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Sprint ID is required"})
		return
	}

	sprint, err := h.sprintUseCases.CompleteSprint(c.Request.Context(), id)
	if err != nil {
		if _, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
			return
		}
		if _, ok := err.(*entities.BusinessRuleError); ok {
			c.JSON(http.StatusConflict, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
		return
	}

	response := dtos.ToSprintResponse(sprint)
	c.JSON(http.StatusOK, response)
}

// GetSprintStatistics retrieves sprint statistics
// @Summary Get sprint statistics
// @Description Get detailed statistics for a sprint
// @Tags sprints
// @Produce json
// @Param id path string true "Sprint ID"
// @Success 200 {object} dtos.SprintStatisticsDTO
// @Failure 404 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /sprints/{id}/statistics [get]
func (h *SprintHandler) GetSprintStatistics(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Sprint ID is required"})
		return
	}

	stats, err := h.sprintUseCases.GetSprintStatistics(c.Request.Context(), id)
	if err != nil {
		if _, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
		return
	}

	c.JSON(http.StatusOK, stats)
}

// ListSprints retrieves sprints with pagination
// @Summary List sprints
// @Description Get a paginated list of sprints
// @Tags sprints
// @Produce json
// @Param page query int false "Page number" default(1)
// @Param page_size query int false "Page size" default(10)
// @Param project_id query string false "Filter by project ID"
// @Param status query string false "Filter by status"
// @Success 200 {object} dtos.SprintListResponse
// @Failure 400 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /sprints [get]
func (h *SprintHandler) ListSprints(c *gin.Context) {
	// Parse query parameters
	page := 1
	if pageStr := c.Query("page"); pageStr != "" {
		if p, err := strconv.Atoi(pageStr); err == nil && p > 0 {
			page = p
		}
	}

	pageSize := 10
	if pageSizeStr := c.Query("page_size"); pageSizeStr != "" {
		if ps, err := strconv.Atoi(pageSizeStr); err == nil && ps > 0 && ps <= 100 {
			pageSize = ps
		}
	}

	// Build filters
	filters := repositories.SprintFilters{
		Page:     page,
		PageSize: pageSize,
	}

	if projectID := c.Query("project_id"); projectID != "" {
		filters.ProjectID = &projectID
	}

	if statusStr := c.Query("status"); statusStr != "" {
		status := entities.SprintStatus(statusStr)
		filters.Status = &status
	}

	// Get sprints with filters - for now get all sprints from a project
	// In a full implementation, you'd add a ListSprints method to the use cases
	var sprints []*entities.Sprint
	var err error
	
	if projectID := filters.ProjectID; projectID != nil {
		sprints, err = h.sprintUseCases.GetSprintsByProject(c.Request.Context(), *projectID)
	} else {
		// For now, return empty list if no project filter
		sprints = []*entities.Sprint{}
	}
	
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
		return
	}

	// Simple pagination
	total := int64(len(sprints))
	start := (page - 1) * pageSize
	end := start + pageSize
	
	if start > len(sprints) {
		sprints = []*entities.Sprint{}
	} else if end > len(sprints) {
		sprints = sprints[start:]
	} else {
		sprints = sprints[start:end]
	}

	response := dtos.ToSprintListResponse(sprints, total, page, pageSize)
	c.JSON(http.StatusOK, response)
}

// GetSprintBacklog retrieves the sprint backlog (user stories)
// @Summary Get sprint backlog
// @Description Get all user stories in a sprint backlog
// @Tags sprints
// @Produce json
// @Param id path string true "Sprint ID"
// @Success 200 {object} map[string]interface{}
// @Failure 404 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /sprints/{id}/backlog [get]
func (h *SprintHandler) GetSprintBacklog(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Sprint ID is required"})
		return
	}

	// Get sprint
	sprint, err := h.sprintUseCases.GetSprintByID(c.Request.Context(), id)
	if err != nil {
		if _, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
		return
	}

	// For now, return a simple response. In a full implementation,
	// you would need a UserStoryUseCases to get the user stories
	response := gin.H{
		"sprint": dtos.ToSprintResponse(sprint),
		"user_stories": []interface{}{}, // Empty for now
		"total_points": 0,
	}

	c.JSON(http.StatusOK, response)
}
