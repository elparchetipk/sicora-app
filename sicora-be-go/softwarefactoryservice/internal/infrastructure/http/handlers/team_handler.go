package handlers

import (
	"net/http"

	"softwarefactoryservice/internal/application/dtos"
	"softwarefactoryservice/internal/application/usecases"
	"softwarefactoryservice/internal/domain/repositories"

	"github.com/gin-gonic/gin"
)

// TeamHandler handles HTTP requests for teams
type TeamHandler struct {
	teamUseCases *usecases.TeamUseCases
}

// NewTeamHandler creates a new team handler
func NewTeamHandler(teamUseCases *usecases.TeamUseCases) *TeamHandler {
	return &TeamHandler{
		teamUseCases: teamUseCases,
	}
}

// CreateTeam handles team creation
// @Summary Create a new team
// @Description Creates a new development team for a project
// @Tags teams
// @Accept json
// @Produce json
// @Param team body dtos.CreateTeamRequest true "Team data"
// @Success 201 {object} dtos.TeamResponse
// @Failure 400 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /api/v1/teams [post]
func (h *TeamHandler) CreateTeam(c *gin.Context) {
	var req dtos.CreateTeamRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request body",
			Message: err.Error(),
		})
		return
	}

	team, err := h.teamUseCases.CreateTeam(c.Request.Context(), req)
	if err != nil {
		handleError(c, err)
		return
	}

	response := dtos.FromTeamEntity(team)
	c.JSON(http.StatusCreated, response)
}

// GetTeam handles team retrieval by ID
// @Summary Get a team by ID
// @Description Retrieves a team by its unique identifier
// @Tags teams
// @Produce json
// @Param id path string true "Team ID"
// @Success 200 {object} dtos.TeamResponse
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /api/v1/teams/{id} [get]
func (h *TeamHandler) GetTeam(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request",
			Message: "Team ID is required",
		})
		return
	}

	team, err := h.teamUseCases.GetTeam(c.Request.Context(), id)
	if err != nil {
		handleError(c, err)
		return
	}

	response := dtos.FromTeamEntity(team)
	c.JSON(http.StatusOK, response)
}

// UpdateTeam handles team updates
// @Summary Update a team
// @Description Updates an existing team
// @Tags teams
// @Accept json
// @Produce json
// @Param id path string true "Team ID"
// @Param team body dtos.UpdateTeamRequest true "Updated team data"
// @Success 200 {object} dtos.TeamResponse
// @Failure 400 {object} ErrorResponse
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /api/v1/teams/{id} [put]
func (h *TeamHandler) UpdateTeam(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request",
			Message: "Team ID is required",
		})
		return
	}

	var req dtos.UpdateTeamRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request body",
			Message: err.Error(),
		})
		return
	}

	team, err := h.teamUseCases.UpdateTeam(c.Request.Context(), id, req)
	if err != nil {
		handleError(c, err)
		return
	}

	response := dtos.FromTeamEntity(team)
	c.JSON(http.StatusOK, response)
}

// DeleteTeam handles team deletion
// @Summary Delete a team
// @Description Soft deletes a team
// @Tags teams
// @Produce json
// @Param id path string true "Team ID"
// @Success 204
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /api/v1/teams/{id} [delete]
func (h *TeamHandler) DeleteTeam(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request",
			Message: "Team ID is required",
		})
		return
	}

	err := h.teamUseCases.DeleteTeam(c.Request.Context(), id)
	if err != nil {
		handleError(c, err)
		return
	}

	c.Status(http.StatusNoContent)
}

// AddTeamMember handles adding a member to a team
// @Summary Add a member to a team
// @Description Adds a new member to an existing team
// @Tags teams
// @Accept json
// @Produce json
// @Param id path string true "Team ID"
// @Param member body dtos.AddTeamMemberRequest true "Member data"
// @Success 201
// @Failure 400 {object} ErrorResponse
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /api/v1/teams/{id}/members [post]
func (h *TeamHandler) AddTeamMember(c *gin.Context) {
	teamID := c.Param("id")
	if teamID == "" {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request",
			Message: "Team ID is required",
		})
		return
	}

	var req dtos.AddTeamMemberRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request body",
			Message: err.Error(),
		})
		return
	}

	err := h.teamUseCases.AddTeamMember(c.Request.Context(), teamID, req)
	if err != nil {
		handleError(c, err)
		return
	}

	c.Status(http.StatusCreated)
}

// RemoveTeamMember handles removing a member from a team
// @Summary Remove a member from a team
// @Description Removes a member from an existing team
// @Tags teams
// @Produce json
// @Param id path string true "Team ID"
// @Param userId path string true "User ID"
// @Success 204
// @Failure 400 {object} ErrorResponse
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /api/v1/teams/{id}/members/{userId} [delete]
func (h *TeamHandler) RemoveTeamMember(c *gin.Context) {
	teamID := c.Param("id")
	userID := c.Param("userId")
	
	if teamID == "" || userID == "" {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request",
			Message: "Team ID and User ID are required",
		})
		return
	}

	err := h.teamUseCases.RemoveTeamMember(c.Request.Context(), teamID, userID)
	if err != nil {
		handleError(c, err)
		return
	}

	c.Status(http.StatusNoContent)
}

// GetTeamMembers handles retrieving team members
// @Summary Get team members
// @Description Retrieves all members of a team
// @Tags teams
// @Produce json
// @Param id path string true "Team ID"
// @Success 200 {array} string
// @Failure 400 {object} ErrorResponse
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /api/v1/teams/{id}/members [get]
func (h *TeamHandler) GetTeamMembers(c *gin.Context) {
	teamID := c.Param("id")
	if teamID == "" {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request",
			Message: "Team ID is required",
		})
		return
	}

	members, err := h.teamUseCases.GetTeamMembers(c.Request.Context(), teamID)
	if err != nil {
		handleError(c, err)
		return
	}

	c.JSON(http.StatusOK, gin.H{"members": members})
}

// ListTeams handles team listing with filters
// @Summary List teams
// @Description Retrieves a paginated list of teams with optional filters
// @Tags teams
// @Produce json
// @Param project_id query string false "Filter by project ID"
// @Param leader_id query string false "Filter by leader ID"
// @Param min_size query int false "Filter by minimum team size"
// @Param max_size query int false "Filter by maximum team size"
// @Param search query string false "Search in team name"
// @Param page query int false "Page number" default(1)
// @Param page_size query int false "Page size" default(20)
// @Param sort_by query string false "Sort field" default("created_at")
// @Param sort_order query string false "Sort order (asc/desc)" default("desc")
// @Success 200 {object} dtos.TeamListResponse
// @Failure 400 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /api/v1/teams [get]
func (h *TeamHandler) ListTeams(c *gin.Context) {
	// Parse query parameters
	filters := repositories.TeamFilters{
		Page:      getIntParam(c, "page", 1),
		PageSize:  getIntParam(c, "page_size", 20),
		SortBy:    c.DefaultQuery("sort_by", "created_at"),
		SortOrder: c.DefaultQuery("sort_order", "desc"),
	}

	// Parse optional filters
	if projectID := c.Query("project_id"); projectID != "" {
		filters.ProjectID = &projectID
	}
	if leaderID := c.Query("leader_id"); leaderID != "" {
		filters.LeaderID = &leaderID
	}
	if minSize := getIntParam(c, "min_size", 0); minSize > 0 {
		filters.MinSize = &minSize
	}
	if maxSize := getIntParam(c, "max_size", 0); maxSize > 0 {
		filters.MaxSize = &maxSize
	}
	if search := c.Query("search"); search != "" {
		filters.Search = &search
	}

	teams, totalCount, err := h.teamUseCases.ListTeams(c.Request.Context(), filters)
	if err != nil {
		handleError(c, err)
		return
	}

	// Convert to response format
	teamResponses := make([]dtos.TeamResponse, len(teams))
	for i, team := range teams {
		teamResponses[i] = dtos.FromTeamEntity(team)
	}

	totalPages := int((totalCount + int64(filters.PageSize) - 1) / int64(filters.PageSize))

	response := dtos.TeamListResponse{
		Teams:      teamResponses,
		TotalCount: totalCount,
		Page:       filters.Page,
		PageSize:   filters.PageSize,
		TotalPages: totalPages,
	}

	c.JSON(http.StatusOK, response)
}

// GetTeamStats handles team statistics retrieval
// @Summary Get team statistics
// @Description Retrieves statistics for a team
// @Tags teams
// @Produce json
// @Param id path string true "Team ID"
// @Success 200 {object} dtos.TeamStats
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /api/v1/teams/{id}/stats [get]
func (h *TeamHandler) GetTeamStats(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Error:   "Invalid request",
			Message: "Team ID is required",
		})
		return
	}

	stats, err := h.teamUseCases.GetTeamStats(c.Request.Context(), id)
	if err != nil {
		handleError(c, err)
		return
	}

	c.JSON(http.StatusOK, stats)
}
