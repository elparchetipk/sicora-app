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

// ProjectHandler handles HTTP requests for projects
type ProjectHandler struct {
	projectUseCases *usecases.ProjectUseCases
}

// NewProjectHandler creates a new project handler
func NewProjectHandler(projectUseCases *usecases.ProjectUseCases) *ProjectHandler {
	return &ProjectHandler{
		projectUseCases: projectUseCases,
	}
}

// CreateProject handles project creation
// @Summary Create a new project
// @Description Creates a new software factory project
// @Tags projects
// @Accept json
// @Produce json
// @Param project body dtos.CreateProjectRequest true "Project data"
// @Success 201 {object} dtos.ProjectResponse
// @Failure 400 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /api/v1/projects [post]
func (h *ProjectHandler) CreateProject(c *gin.Context) {
	var req dtos.CreateProjectRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request body",
			Message: err.Error(),
		})
		return
	}

	project, err := h.projectUseCases.CreateProject(c.Request.Context(), req)
	if err != nil {
		handleError(c, err)
		return
	}

	response := dtos.FromProjectEntity(project)
	c.JSON(http.StatusCreated, response)
}

// GetProject handles project retrieval by ID
// @Summary Get a project by ID
// @Description Retrieves a project by its unique identifier
// @Tags projects
// @Produce json
// @Param id path string true "Project ID"
// @Success 200 {object} dtos.ProjectResponse
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /api/v1/projects/{id} [get]
func (h *ProjectHandler) GetProject(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request",
			Message: "Project ID is required",
		})
		return
	}

	project, err := h.projectUseCases.GetProject(c.Request.Context(), id)
	if err != nil {
		handleError(c, err)
		return
	}

	response := dtos.FromProjectEntity(project)
	c.JSON(http.StatusOK, response)
}

// UpdateProject handles project updates
// @Summary Update a project
// @Description Updates an existing project
// @Tags projects
// @Accept json
// @Produce json
// @Param id path string true "Project ID"
// @Param project body dtos.UpdateProjectRequest true "Updated project data"
// @Success 200 {object} dtos.ProjectResponse
// @Failure 400 {object} ErrorResponse
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /api/v1/projects/{id} [put]
func (h *ProjectHandler) UpdateProject(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request",
			Message: "Project ID is required",
		})
		return
	}

	var req dtos.UpdateProjectRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request body",
			Message: err.Error(),
		})
		return
	}

	project, err := h.projectUseCases.UpdateProject(c.Request.Context(), id, req)
	if err != nil {
		handleError(c, err)
		return
	}

	response := dtos.FromProjectEntity(project)
	c.JSON(http.StatusOK, response)
}

// DeleteProject handles project deletion
// @Summary Delete a project
// @Description Soft deletes a project
// @Tags projects
// @Produce json
// @Param id path string true "Project ID"
// @Success 204
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /api/v1/projects/{id} [delete]
func (h *ProjectHandler) DeleteProject(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request",
			Message: "Project ID is required",
		})
		return
	}

	err := h.projectUseCases.DeleteProject(c.Request.Context(), id)
	if err != nil {
		handleError(c, err)
		return
	}

	c.Status(http.StatusNoContent)
}

// ListProjects handles project listing with filters
// @Summary List projects
// @Description Retrieves a paginated list of projects with optional filters
// @Tags projects
// @Produce json
// @Param instructor_id query string false "Filter by instructor ID"
// @Param course_id query string false "Filter by course ID"
// @Param status query string false "Filter by status"
// @Param technology query string false "Filter by technology"
// @Param search query string false "Search in name and description"
// @Param page query int false "Page number" default(1)
// @Param page_size query int false "Page size" default(20)
// @Param sort_by query string false "Sort field" default("created_at")
// @Param sort_order query string false "Sort order (asc/desc)" default("desc")
// @Success 200 {object} dtos.ProjectListResponse
// @Failure 400 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /api/v1/projects [get]
func (h *ProjectHandler) ListProjects(c *gin.Context) {
	// Parse query parameters
	filters := repositories.ProjectFilters{
		Page:      getIntParam(c, "page", 1),
		PageSize:  getIntParam(c, "page_size", 20),
		SortBy:    c.DefaultQuery("sort_by", "created_at"),
		SortOrder: c.DefaultQuery("sort_order", "desc"),
	}

	// Parse optional filters
	if instructorID := c.Query("instructor_id"); instructorID != "" {
		filters.InstructorID = &instructorID
	}
	if courseID := c.Query("course_id"); courseID != "" {
		filters.CourseID = &courseID
	}
	if statusStr := c.Query("status"); statusStr != "" {
		// Note: You might want to validate the status value here
		status := entities.ProjectStatus(statusStr)
		filters.Status = &status
	}
	if technology := c.Query("technology"); technology != "" {
		filters.Technology = &technology
	}
	if search := c.Query("search"); search != "" {
		filters.Search = &search
	}

	projects, totalCount, err := h.projectUseCases.ListProjects(c.Request.Context(), filters)
	if err != nil {
		handleError(c, err)
		return
	}

	// Convert to response format
	projectResponses := make([]dtos.ProjectResponse, len(projects))
	for i, project := range projects {
		projectResponses[i] = dtos.FromProjectEntity(project)
	}

	totalPages := int((totalCount + int64(filters.PageSize) - 1) / int64(filters.PageSize))

	response := dtos.ProjectListResponse{
		Projects:   projectResponses,
		TotalCount: totalCount,
		Page:       filters.Page,
		PageSize:   filters.PageSize,
		TotalPages: totalPages,
	}

	c.JSON(http.StatusOK, response)
}

// GetProjectStats handles project statistics retrieval
// @Summary Get project statistics
// @Description Retrieves statistics for a project
// @Tags projects
// @Produce json
// @Param id path string true "Project ID"
// @Success 200 {object} dtos.ProjectStats
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /api/v1/projects/{id}/stats [get]
func (h *ProjectHandler) GetProjectStats(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request",
			Message: "Project ID is required",
		})
		return
	}

	stats, err := h.projectUseCases.GetProjectStats(c.Request.Context(), id)
	if err != nil {
		handleError(c, err)
		return
	}

	c.JSON(http.StatusOK, stats)
}

// ErrorResponse represents an error response
type ErrorResponse struct {
	Error   string `json:"error"`
	Message string `json:"message"`
}

// getIntParam extracts an integer parameter from query with default value
func getIntParam(c *gin.Context, param string, defaultValue int) int {
	if valueStr := c.Query(param); valueStr != "" {
		if value, err := strconv.Atoi(valueStr); err == nil {
			return value
		}
	}
	return defaultValue
}

// handleError handles different types of errors and returns appropriate HTTP responses
func handleError(c *gin.Context, err error) {
	// Here you would implement error type checking and return appropriate status codes
	// For now, we'll use a simple implementation
	c.JSON(http.StatusInternalServerError, ErrorResponse{
		Error:   "Internal server error",
		Message: err.Error(),
	})
}
