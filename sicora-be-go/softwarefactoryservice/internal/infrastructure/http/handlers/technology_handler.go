package handlers

import (
	"net/http"
	"strconv"

	"softwarefactoryservice/internal/application/dtos"
	"softwarefactoryservice/internal/application/usecases"
	"softwarefactoryservice/internal/domain/entities"

	"github.com/gin-gonic/gin"
)

const (
	ErrInvalidTechnologyID = "Invalid technology ID"
	ErrInvalidCategory     = "Invalid category"
	ErrInvalidLevel        = "Invalid level"
)

// TechnologyHandler handles HTTP requests for technologies
type TechnologyHandler struct {
	technologyUseCases *usecases.TechnologyUseCases
}

// NewTechnologyHandler creates a new TechnologyHandler
func NewTechnologyHandler(technologyUseCases *usecases.TechnologyUseCases) *TechnologyHandler {
	return &TechnologyHandler{
		technologyUseCases: technologyUseCases,
	}
}

// CreateTechnology creates a new technology
// @Summary Create technology
// @Description Create a new technology entry
// @Tags technologies
// @Accept json
// @Produce json
// @Param technology body dtos.CreateTechnologyRequest true "Technology data"
// @Success 201 {object} dtos.TechnologyResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Failure 500 {object} map[string]interface{} "Internal server error"
// @Router /api/v1/technologies [post]
func (h *TechnologyHandler) CreateTechnology(c *gin.Context) {
	var req dtos.CreateTechnologyRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	technology, err := h.technologyUseCases.CreateTechnology(c.Request.Context(), &req)
	if err != nil {
		if validationErr, ok := err.(*entities.ValidationError); ok {
			c.JSON(http.StatusBadRequest, gin.H{"error": validationErr.Error(), "field": validationErr.Field})
			return
		}
		if conflictErr, ok := err.(*entities.ConflictError); ok {
			c.JSON(http.StatusConflict, gin.H{"error": conflictErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create technology"})
		return
	}

	c.JSON(http.StatusCreated, technology)
}

// GetTechnology retrieves a technology by ID
// @Summary Get technology
// @Description Get a technology by its ID
// @Tags technologies
// @Produce json
// @Param id path string true "Technology ID"
// @Success 200 {object} dtos.TechnologyResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Failure 404 {object} map[string]interface{} "Not found"
// @Router /api/v1/technologies/{id} [get]
func (h *TechnologyHandler) GetTechnology(c *gin.Context) {
	idStr := c.Param("id")
	if idStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidTechnologyID})
		return
	}

	technology, err := h.technologyUseCases.GetTechnology(c.Request.Context(), idStr)
	if err != nil {
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get technology"})
		return
	}

	c.JSON(http.StatusOK, technology)
}

// GetTechnologyByName retrieves a technology by name
// @Summary Get technology by name
// @Description Get a technology by its name
// @Tags technologies
// @Produce json
// @Param name path string true "Technology name"
// @Success 200 {object} dtos.TechnologyResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Failure 404 {object} map[string]interface{} "Not found"
// @Router /api/v1/technologies/name/{name} [get]
func (h *TechnologyHandler) GetTechnologyByName(c *gin.Context) {
	name := c.Param("name")
	if name == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Technology name is required"})
		return
	}

	technology, err := h.technologyUseCases.GetTechnologyByName(c.Request.Context(), name)
	if err != nil {
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get technology by name"})
		return
	}

	c.JSON(http.StatusOK, technology)
}

// ListTechnologies retrieves technologies with filters and pagination
// @Summary List technologies
// @Description Get technologies with optional filters and pagination
// @Tags technologies
// @Produce json
// @Param category query string false "Technology category" Enums(frontend, backend, database, devops, mobile, ai_ml, other)
// @Param level query string false "Technology level" Enums(beginner, intermediate, advanced, expert)
// @Param is_active query bool false "Is active"
// @Param search query string false "Search term (name or description)"
// @Param page query int false "Page number" default(1)
// @Param page_size query int false "Page size" default(10)
// @Success 200 {object} dtos.TechnologyListResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/technologies [get]
func (h *TechnologyHandler) ListTechnologies(c *gin.Context) {
	var filter dtos.TechnologyFilterRequest

	// Parse query parameters
	if category := c.Query("category"); category != "" {
		filter.Category = &category
	}
	if level := c.Query("level"); level != "" {
		filter.Level = &level
	}
	if search := c.Query("search"); search != "" {
		filter.Search = &search
	}
	if status := c.Query("status"); status != "" {
		filter.Status = &status
	}

	// Parse pagination
	filter.Page = 1
	if pageStr := c.Query("page"); pageStr != "" {
		if page, err := strconv.Atoi(pageStr); err == nil && page > 0 {
			filter.Page = page
		}
	}

	filter.PageSize = 10
	if pageSizeStr := c.Query("page_size"); pageSizeStr != "" {
		if pageSize, err := strconv.Atoi(pageSizeStr); err == nil && pageSize > 0 && pageSize <= 100 {
			filter.PageSize = pageSize
		}
	}

	technologies, err := h.technologyUseCases.ListTechnologies(c.Request.Context(), &filter)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get technologies"})
		return
	}

	c.JSON(http.StatusOK, technologies)
}

// GetTechnologiesByCategory retrieves technologies by category
// @Summary Get technologies by category
// @Description Get all technologies for a specific category
// @Tags technologies
// @Produce json
// @Param category path string true "Technology category" Enums(frontend, backend, database, devops, mobile, ai_ml, other)
// @Success 200 {object} dtos.TechnologyListResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/technologies/category/{category} [get]
func (h *TechnologyHandler) GetTechnologiesByCategory(c *gin.Context) {
	categoryStr := c.Param("category")
	if categoryStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidCategory})
		return
	}

	category := entities.TechnologyCategory(categoryStr)
	
	technologies, err := h.technologyUseCases.GetTechnologiesByCategory(c.Request.Context(), category)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get technologies by category"})
		return
	}

	c.JSON(http.StatusOK, technologies)
}

// GetTechnologiesByLevel retrieves technologies by level
// @Summary Get technologies by level
// @Description Get all technologies for a specific level
// @Tags technologies
// @Produce json
// @Param level path string true "Technology level" Enums(beginner, intermediate, advanced, expert)
// @Success 200 {object} dtos.TechnologyListResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/technologies/level/{level} [get]
func (h *TechnologyHandler) GetTechnologiesByLevel(c *gin.Context) {
	levelStr := c.Param("level")
	if levelStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidLevel})
		return
	}

	level := entities.TechnologyLevel(levelStr)
	
	technologies, err := h.technologyUseCases.GetTechnologiesByLevel(c.Request.Context(), level)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get technologies by level"})
		return
	}

	c.JSON(http.StatusOK, technologies)
}

// GetRecommendedTechnologies retrieves recommended technologies
// @Summary Get recommended technologies
// @Description Get recommended technologies based on category and level
// @Tags technologies
// @Produce json
// @Param category query string true "Technology category" Enums(frontend, backend, database, devops, mobile, ai_ml, other)
// @Param level query string true "Technology level" Enums(beginner, intermediate, advanced, expert)
// @Success 200 {object} dtos.TechnologyListResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/technologies/recommended [get]
func (h *TechnologyHandler) GetRecommendedTechnologies(c *gin.Context) {
	categoryStr := c.Query("category")
	if categoryStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Category parameter is required"})
		return
	}

	levelStr := c.Query("level")
	if levelStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Level parameter is required"})
		return
	}

	category := entities.TechnologyCategory(categoryStr)
	level := entities.TechnologyLevel(levelStr)
	
	technologies, err := h.technologyUseCases.GetRecommendedTechnologies(c.Request.Context(), category, level)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get recommended technologies"})
		return
	}

	c.JSON(http.StatusOK, technologies)
}

// UpdateTechnology updates an existing technology
// @Summary Update technology
// @Description Update an existing technology
// @Tags technologies
// @Accept json
// @Produce json
// @Param id path string true "Technology ID"
// @Param technology body dtos.UpdateTechnologyRequest true "Technology update data"
// @Success 200 {object} dtos.TechnologyResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Failure 404 {object} map[string]interface{} "Not found"
// @Router /api/v1/technologies/{id} [put]
func (h *TechnologyHandler) UpdateTechnology(c *gin.Context) {
	idStr := c.Param("id")
	if idStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidTechnologyID})
		return
	}

	var req dtos.UpdateTechnologyRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	technology, err := h.technologyUseCases.UpdateTechnology(c.Request.Context(), idStr, &req)
	if err != nil {
		if validationErr, ok := err.(*entities.ValidationError); ok {
			c.JSON(http.StatusBadRequest, gin.H{"error": validationErr.Error(), "field": validationErr.Field})
			return
		}
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update technology"})
		return
	}

	c.JSON(http.StatusOK, technology)
}

// DeleteTechnology deletes a technology
// @Summary Delete technology
// @Description Delete a technology by ID
// @Tags technologies
// @Param id path string true "Technology ID"
// @Success 204 "No content"
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Failure 404 {object} map[string]interface{} "Not found"
// @Router /api/v1/technologies/{id} [delete]
func (h *TechnologyHandler) DeleteTechnology(c *gin.Context) {
	idStr := c.Param("id")
	if idStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidTechnologyID})
		return
	}

	err := h.technologyUseCases.DeleteTechnology(c.Request.Context(), idStr)
	if err != nil {
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete technology"})
		return
	}

	c.Status(http.StatusNoContent)
}

// ActivateTechnology activates a technology
// @Summary Activate technology
// @Description Activate a technology by setting its status to active
// @Tags technologies
// @Param id path string true "Technology ID"
// @Success 200 {object} dtos.TechnologyResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Failure 404 {object} map[string]interface{} "Not found"
// @Router /api/v1/technologies/{id}/activate [post]
func (h *TechnologyHandler) ActivateTechnology(c *gin.Context) {
	idStr := c.Param("id")
	if idStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidTechnologyID})
		return
	}

	technology, err := h.technologyUseCases.ActivateTechnology(c.Request.Context(), idStr)
	if err != nil {
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to activate technology"})
		return
	}

	c.JSON(http.StatusOK, technology)
}

// DeactivateTechnology deactivates a technology
// @Summary Deactivate technology
// @Description Deactivate a technology by setting its status to inactive
// @Tags technologies
// @Param id path string true "Technology ID"
// @Success 200 {object} dtos.TechnologyResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Failure 404 {object} map[string]interface{} "Not found"
// @Router /api/v1/technologies/{id}/deactivate [post]
func (h *TechnologyHandler) DeactivateTechnology(c *gin.Context) {
	idStr := c.Param("id")
	if idStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidTechnologyID})
		return
	}

	technology, err := h.technologyUseCases.DeactivateTechnology(c.Request.Context(), idStr)
	if err != nil {
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to deactivate technology"})
		return
	}

	c.JSON(http.StatusOK, technology)
}

// GetProjectTechnologies retrieves technologies for a project
// @Summary Get project technologies
// @Description Get all technologies associated with a project
// @Tags technologies
// @Produce json
// @Param project_id path string true "Project ID"
// @Success 200 {object} dtos.TechnologyListResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/projects/{project_id}/technologies [get]
func (h *TechnologyHandler) GetProjectTechnologies(c *gin.Context) {
	projectIDStr := c.Param("project_id")
	if projectIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidProjectID})
		return
	}

	technologies, err := h.technologyUseCases.GetProjectTechnologies(c.Request.Context(), projectIDStr)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get project technologies"})
		return
	}

	c.JSON(http.StatusOK, technologies)
}

// AddProjectTechnology adds a technology to a project
// @Summary Add technology to project
// @Description Associate a technology with a project
// @Tags technologies
// @Param project_id path string true "Project ID"
// @Param technology_id path string true "Technology ID"
// @Success 200 {object} map[string]interface{} "Success message"
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/projects/{project_id}/technologies/{technology_id} [post]
func (h *TechnologyHandler) AddProjectTechnology(c *gin.Context) {
	projectIDStr := c.Param("project_id")
	if projectIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidProjectID})
		return
	}

	technologyIDStr := c.Param("technology_id")
	if technologyIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidTechnologyID})
		return
	}

	err := h.technologyUseCases.AddProjectTechnology(c.Request.Context(), projectIDStr, technologyIDStr)
	if err != nil {
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to add technology to project"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Technology added to project successfully"})
}

// RemoveProjectTechnology removes a technology from a project
// @Summary Remove technology from project
// @Description Remove a technology association from a project
// @Tags technologies
// @Param project_id path string true "Project ID"
// @Param technology_id path string true "Technology ID"
// @Success 200 {object} map[string]interface{} "Success message"
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/projects/{project_id}/technologies/{technology_id} [delete]
func (h *TechnologyHandler) RemoveProjectTechnology(c *gin.Context) {
	projectIDStr := c.Param("project_id")
	if projectIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidProjectID})
		return
	}

	technologyIDStr := c.Param("technology_id")
	if technologyIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidTechnologyID})
		return
	}

	err := h.technologyUseCases.RemoveProjectTechnology(c.Request.Context(), projectIDStr, technologyIDStr)
	if err != nil {
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to remove technology from project"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Technology removed from project successfully"})
}

// GetTechnologyStats retrieves technology statistics
// @Summary Get technology statistics
// @Description Get overall technology usage statistics
// @Tags technologies
// @Produce json
// @Success 200 {object} dtos.TechnologyStatsResponse
// @Router /api/v1/technologies/stats [get]
func (h *TechnologyHandler) GetTechnologyStats(c *gin.Context) {
	stats, err := h.technologyUseCases.GetTechnologyStats(c.Request.Context())
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get technology statistics"})
		return
	}

	c.JSON(http.StatusOK, stats)
}
