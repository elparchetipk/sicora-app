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
	ErrInvalidUserStoryID = "Invalid user story ID"
	ErrInvalidProjectID   = "Invalid project ID"
	ErrInvalidSprintID    = "Invalid sprint ID"
)

// UserStoryHandler handles HTTP requests for user stories
type UserStoryHandler struct {
	userStoryUseCases *usecases.UserStoryUseCases
}

// NewUserStoryHandler creates a new UserStoryHandler
func NewUserStoryHandler(userStoryUseCases *usecases.UserStoryUseCases) *UserStoryHandler {
	return &UserStoryHandler{
		userStoryUseCases: userStoryUseCases,
	}
}

// CreateUserStory creates a new user story
// @Summary Create user story
// @Description Create a new user story in the software factory
// @Tags user-stories
// @Accept json
// @Produce json
// @Param user_story body dtos.CreateUserStoryRequest true "User story data"
// @Success 201 {object} dtos.UserStoryResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Failure 500 {object} map[string]interface{} "Internal server error"
// @Router /api/v1/user-stories [post]
func (h *UserStoryHandler) CreateUserStory(c *gin.Context) {
	var req dtos.CreateUserStoryRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	userStory, err := h.userStoryUseCases.CreateUserStory(c.Request.Context(), &req)
	if err != nil {
		if validationErr, ok := err.(*entities.ValidationError); ok {
			c.JSON(http.StatusBadRequest, gin.H{"error": validationErr.Error(), "field": validationErr.Field})
			return
		}
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create user story"})
		return
	}

	c.JSON(http.StatusCreated, userStory)
}

// GetUserStory retrieves a user story by ID
// @Summary Get user story
// @Description Get a user story by its ID
// @Tags user-stories
// @Produce json
// @Param id path string true "User story ID"
// @Success 200 {object} dtos.UserStoryResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Failure 404 {object} map[string]interface{} "Not found"
// @Router /api/v1/user-stories/{id} [get]
func (h *UserStoryHandler) GetUserStory(c *gin.Context) {
	idStr := c.Param("id")
	if idStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidUserStoryID})
		return
	}

	userStory, err := h.userStoryUseCases.GetUserStory(c.Request.Context(), idStr)
	if err != nil {
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get user story"})
		return
	}

	c.JSON(http.StatusOK, userStory)
}

// ListUserStories retrieves user stories with filters and pagination
// @Summary List user stories
// @Description Get user stories with optional filters and pagination
// @Tags user-stories
// @Produce json
// @Param project_id query string false "Project ID"
// @Param sprint_id query string false "Sprint ID"
// @Param assigned_to query string false "Assigned member ID"
// @Param status query string false "Story status" Enums(backlog, todo, in_progress, review, done)
// @Param type query string false "Story type" Enums(functional, academic, technical, bugfix)
// @Param priority query int false "Priority (1-5)"
// @Param min_story_points query int false "Minimum story points"
// @Param max_story_points query int false "Maximum story points"
// @Param tags query string false "Comma-separated tags"
// @Param has_dependencies query bool false "Has dependencies"
// @Param page query int false "Page number" default(1)
// @Param page_size query int false "Page size" default(10)
// @Success 200 {object} dtos.UserStoryListResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/user-stories [get]
func (h *UserStoryHandler) ListUserStories(c *gin.Context) {
	var filter dtos.UserStoryFilterRequest

	// Parse query parameters
	if projectID := c.Query("project_id"); projectID != "" {
		filter.ProjectID = &projectID
	}
	if sprintID := c.Query("sprint_id"); sprintID != "" {
		filter.SprintID = &sprintID
	}
	if assignedTo := c.Query("assigned_to"); assignedTo != "" {
		filter.AssignedTo = &assignedTo
	}
	if status := c.Query("status"); status != "" {
		filter.Status = &status
	}
	if storyType := c.Query("type"); storyType != "" {
		filter.Type = &storyType
	}
	if priorityStr := c.Query("priority"); priorityStr != "" {
		if priority, err := strconv.Atoi(priorityStr); err == nil {
			filter.Priority = &priority
		}
	}
	if minPointsStr := c.Query("min_story_points"); minPointsStr != "" {
		if minPoints, err := strconv.Atoi(minPointsStr); err == nil {
			filter.MinStoryPoints = &minPoints
		}
	}
	if maxPointsStr := c.Query("max_story_points"); maxPointsStr != "" {
		if maxPoints, err := strconv.Atoi(maxPointsStr); err == nil {
			filter.MaxStoryPoints = &maxPoints
		}
	}
	if tags := c.Query("tags"); tags != "" {
		filter.Tags = &tags
	}
	if hasDepsStr := c.Query("has_dependencies"); hasDepsStr != "" {
		if hasDeps, err := strconv.ParseBool(hasDepsStr); err == nil {
			filter.HasDependencies = &hasDeps
		}
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

	userStories, err := h.userStoryUseCases.ListUserStories(c.Request.Context(), &filter)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get user stories"})
		return
	}

	c.JSON(http.StatusOK, userStories)
}

// UpdateUserStory updates an existing user story
// @Summary Update user story
// @Description Update an existing user story
// @Tags user-stories
// @Accept json
// @Produce json
// @Param id path string true "User story ID"
// @Param user_story body dtos.UpdateUserStoryRequest true "User story update data"
// @Success 200 {object} dtos.UserStoryResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Failure 404 {object} map[string]interface{} "Not found"
// @Router /api/v1/user-stories/{id} [put]
func (h *UserStoryHandler) UpdateUserStory(c *gin.Context) {
	idStr := c.Param("id")
	if idStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidUserStoryID})
		return
	}

	var req dtos.UpdateUserStoryRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	userStory, err := h.userStoryUseCases.UpdateUserStory(c.Request.Context(), idStr, &req)
	if err != nil {
		if validationErr, ok := err.(*entities.ValidationError); ok {
			c.JSON(http.StatusBadRequest, gin.H{"error": validationErr.Error(), "field": validationErr.Field})
			return
		}
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update user story"})
		return
	}

	c.JSON(http.StatusOK, userStory)
}

// DeleteUserStory deletes a user story
// @Summary Delete user story
// @Description Delete a user story by ID
// @Tags user-stories
// @Param id path string true "User story ID"
// @Success 204 "No content"
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Failure 404 {object} map[string]interface{} "Not found"
// @Router /api/v1/user-stories/{id} [delete]
func (h *UserStoryHandler) DeleteUserStory(c *gin.Context) {
	idStr := c.Param("id")
	if idStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidUserStoryID})
		return
	}

	err := h.userStoryUseCases.DeleteUserStory(c.Request.Context(), idStr)
	if err != nil {
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete user story"})
		return
	}

	c.Status(http.StatusNoContent)
}

// GetUserStoriesByProject retrieves user stories for a specific project
// @Summary Get user stories by project
// @Description Get all user stories for a specific project
// @Tags user-stories
// @Produce json
// @Param project_id path string true "Project ID"
// @Success 200 {object} dtos.UserStoryListResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/projects/{project_id}/user-stories [get]
func (h *UserStoryHandler) GetUserStoriesByProject(c *gin.Context) {
	projectIDStr := c.Param("project_id")
	if projectIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidProjectID})
		return
	}

	userStories, err := h.userStoryUseCases.GetUserStoriesByProject(c.Request.Context(), projectIDStr)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get user stories by project"})
		return
	}

	c.JSON(http.StatusOK, userStories)
}

// GetUserStoriesBySprint retrieves user stories for a specific sprint
// @Summary Get user stories by sprint
// @Description Get all user stories for a specific sprint
// @Tags user-stories
// @Produce json
// @Param sprint_id path string true "Sprint ID"
// @Success 200 {object} dtos.UserStoryListResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/sprints/{sprint_id}/user-stories [get]
func (h *UserStoryHandler) GetUserStoriesBySprint(c *gin.Context) {
	sprintIDStr := c.Param("sprint_id")
	if sprintIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidSprintID})
		return
	}

	userStories, err := h.userStoryUseCases.GetUserStoriesBySprint(c.Request.Context(), sprintIDStr)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get user stories by sprint"})
		return
	}

	c.JSON(http.StatusOK, userStories)
}

// AssignToSprint assigns a user story to a sprint
// @Summary Assign user story to sprint
// @Description Assign a user story to a specific sprint
// @Tags user-stories
// @Param user_story_id path string true "User story ID"
// @Param sprint_id path string true "Sprint ID"
// @Success 200 {object} dtos.UserStoryResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/user-stories/{user_story_id}/assign-sprint/{sprint_id} [post]
func (h *UserStoryHandler) AssignToSprint(c *gin.Context) {
	userStoryIDStr := c.Param("user_story_id")
	if userStoryIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidUserStoryID})
		return
	}

	sprintIDStr := c.Param("sprint_id")
	if sprintIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidSprintID})
		return
	}

	userStory, err := h.userStoryUseCases.AssignToSprint(c.Request.Context(), userStoryIDStr, sprintIDStr)
	if err != nil {
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to assign user story to sprint"})
		return
	}

	c.JSON(http.StatusOK, userStory)
}

// UnassignFromSprint removes a user story from a sprint
// @Summary Remove user story from sprint
// @Description Remove a user story from its current sprint (moves to backlog)
// @Tags user-stories
// @Param user_story_id path string true "User story ID"
// @Success 200 {object} dtos.UserStoryResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/user-stories/{user_story_id}/unassign-sprint [post]
func (h *UserStoryHandler) UnassignFromSprint(c *gin.Context) {
	userStoryIDStr := c.Param("user_story_id")
	if userStoryIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidUserStoryID})
		return
	}

	userStory, err := h.userStoryUseCases.UnassignFromSprint(c.Request.Context(), userStoryIDStr)
	if err != nil {
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to remove user story from sprint"})
		return
	}

	c.JSON(http.StatusOK, userStory)
}

// UpdateStatus updates the status of a user story
// @Summary Update user story status
// @Description Update the status of a user story
// @Tags user-stories
// @Param user_story_id path string true "User story ID"
// @Param status query string true "New status" Enums(backlog, todo, in_progress, review, done)
// @Success 200 {object} dtos.UserStoryResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/user-stories/{user_story_id}/status [put]
func (h *UserStoryHandler) UpdateStatus(c *gin.Context) {
	userStoryIDStr := c.Param("user_story_id")
	if userStoryIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidUserStoryID})
		return
	}

	statusStr := c.Query("status")
	if statusStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Status parameter is required"})
		return
	}

	status := entities.StoryStatus(statusStr)
	
	userStory, err := h.userStoryUseCases.UpdateStatus(c.Request.Context(), userStoryIDStr, status)
	if err != nil {
		if validationErr, ok := err.(*entities.ValidationError); ok {
			c.JSON(http.StatusBadRequest, gin.H{"error": validationErr.Error(), "field": validationErr.Field})
			return
		}
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update user story status"})
		return
	}

	c.JSON(http.StatusOK, userStory)
}

// GetBacklog retrieves the product backlog for a project
// @Summary Get product backlog
// @Description Get the prioritized product backlog for a project
// @Tags user-stories
// @Produce json
// @Param project_id path string true "Project ID"
// @Success 200 {object} dtos.UserStoryListResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/projects/{project_id}/backlog [get]
func (h *UserStoryHandler) GetBacklog(c *gin.Context) {
	projectIDStr := c.Param("project_id")
	if projectIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidProjectID})
		return
	}

	backlog, err := h.userStoryUseCases.GetBacklog(c.Request.Context(), projectIDStr)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get backlog"})
		return
	}

	c.JSON(http.StatusOK, backlog)
}

// GetSprintBacklog retrieves the sprint backlog
// @Summary Get sprint backlog
// @Description Get the sprint backlog for a specific sprint
// @Tags user-stories
// @Produce json
// @Param sprint_id path string true "Sprint ID"
// @Success 200 {object} dtos.UserStoryListResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/sprints/{sprint_id}/backlog [get]
func (h *UserStoryHandler) GetSprintBacklog(c *gin.Context) {
	sprintIDStr := c.Param("sprint_id")
	if sprintIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidSprintID})
		return
	}

	backlog, err := h.userStoryUseCases.GetSprintBacklog(c.Request.Context(), sprintIDStr)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get sprint backlog"})
		return
	}

	c.JSON(http.StatusOK, backlog)
}
