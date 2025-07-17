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
	ErrInvalidEvaluationID = "Invalid evaluation ID"
	ErrInvalidStudentID    = "Invalid student ID"
	ErrInvalidEvaluatorID  = "Invalid evaluator ID"
)

// EvaluationHandler handles HTTP requests for evaluations
type EvaluationHandler struct {
	evaluationUseCases *usecases.EvaluationUseCases
}

// NewEvaluationHandler creates a new EvaluationHandler
func NewEvaluationHandler(evaluationUseCases *usecases.EvaluationUseCases) *EvaluationHandler {
	return &EvaluationHandler{
		evaluationUseCases: evaluationUseCases,
	}
}

// CreateEvaluation creates a new evaluation
// @Summary Create evaluation
// @Description Create a new evaluation for an apprentice
// @Tags evaluations
// @Accept json
// @Produce json
// @Param evaluation body dtos.CreateEvaluationRequest true "Evaluation data"
// @Success 201 {object} dtos.EvaluationResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Failure 500 {object} map[string]interface{} "Internal server error"
// @Router /api/v1/evaluations [post]
func (h *EvaluationHandler) CreateEvaluation(c *gin.Context) {
	var req dtos.CreateEvaluationRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	evaluation, err := h.evaluationUseCases.CreateEvaluation(c.Request.Context(), &req)
	if err != nil {
		if validationErr, ok := err.(*entities.ValidationError); ok {
			c.JSON(http.StatusBadRequest, gin.H{"error": validationErr.Error(), "field": validationErr.Field})
			return
		}
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create evaluation"})
		return
	}

	c.JSON(http.StatusCreated, evaluation)
}

// GetEvaluation retrieves an evaluation by ID
// @Summary Get evaluation
// @Description Get an evaluation by its ID
// @Tags evaluations
// @Produce json
// @Param id path string true "Evaluation ID"
// @Success 200 {object} dtos.EvaluationResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Failure 404 {object} map[string]interface{} "Not found"
// @Router /api/v1/evaluations/{id} [get]
func (h *EvaluationHandler) GetEvaluation(c *gin.Context) {
	idStr := c.Param("id")
	if idStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidEvaluationID})
		return
	}

	evaluation, err := h.evaluationUseCases.GetEvaluation(c.Request.Context(), idStr)
	if err != nil {
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get evaluation"})
		return
	}

	c.JSON(http.StatusOK, evaluation)
}

// ListEvaluations retrieves evaluations with filters and pagination
// @Summary List evaluations
// @Description Get evaluations with optional filters and pagination
// @Tags evaluations
// @Produce json
// @Param project_id query string false "Project ID"
// @Param sprint_id query string false "Sprint ID"
// @Param student_id query string false "Student ID"
// @Param evaluator_id query string false "Evaluator ID"
// @Param evaluation_type query string false "Evaluation type" Enums(initial, intermediate, final, peer, auto, academic)
// @Param min_technical_score query number false "Minimum technical score"
// @Param max_technical_score query number false "Maximum technical score"
// @Param min_soft_skills_score query number false "Minimum soft skills score"
// @Param max_soft_skills_score query number false "Maximum soft skills score"
// @Param min_overall_score query number false "Minimum overall score"
// @Param max_overall_score query number false "Maximum overall score"
// @Param page query int false "Page number" default(1)
// @Param page_size query int false "Page size" default(10)
// @Success 200 {object} dtos.EvaluationListResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/evaluations [get]
func (h *EvaluationHandler) ListEvaluations(c *gin.Context) {
	var filter dtos.EvaluationFilterRequest

	// Parse query parameters
	if projectID := c.Query("project_id"); projectID != "" {
		filter.ProjectID = &projectID
	}
	if sprintID := c.Query("sprint_id"); sprintID != "" {
		filter.SprintID = &sprintID
	}
	if apprenticeID := c.Query("apprentice_id"); apprenticeID != "" {
		filter.ApprenticeID = &apprenticeID
	}
	if evaluatorID := c.Query("evaluator_id"); evaluatorID != "" {
		filter.EvaluatorID = &evaluatorID
	}
	if evalType := c.Query("evaluation_type"); evalType != "" {
		filter.EvaluationType = &evalType
	}
	
	// Parse score ranges
	if minScoreStr := c.Query("min_score"); minScoreStr != "" {
		if minScore, err := strconv.ParseFloat(minScoreStr, 64); err == nil {
			filter.MinScore = &minScore
		}
	}
	if maxScoreStr := c.Query("max_score"); maxScoreStr != "" {
		if maxScore, err := strconv.ParseFloat(maxScoreStr, 64); err == nil {
			filter.MaxScore = &maxScore
		}
	}
	if needsImprovementStr := c.Query("needs_improvement"); needsImprovementStr != "" {
		if needsImprovement, err := strconv.ParseBool(needsImprovementStr); err == nil {
			filter.NeedsImprovement = &needsImprovement
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

	evaluations, err := h.evaluationUseCases.ListEvaluations(c.Request.Context(), &filter)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get evaluations"})
		return
	}

	c.JSON(http.StatusOK, evaluations)
}

// UpdateEvaluation updates an existing evaluation
// @Summary Update evaluation
// @Description Update an existing evaluation
// @Tags evaluations
// @Accept json
// @Produce json
// @Param id path string true "Evaluation ID"
// @Param evaluation body dtos.UpdateEvaluationRequest true "Evaluation update data"
// @Success 200 {object} dtos.EvaluationResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Failure 404 {object} map[string]interface{} "Not found"
// @Router /api/v1/evaluations/{id} [put]
func (h *EvaluationHandler) UpdateEvaluation(c *gin.Context) {
	idStr := c.Param("id")
	if idStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidEvaluationID})
		return
	}

	var req dtos.UpdateEvaluationRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	evaluation, err := h.evaluationUseCases.UpdateEvaluation(c.Request.Context(), idStr, &req)
	if err != nil {
		if validationErr, ok := err.(*entities.ValidationError); ok {
			c.JSON(http.StatusBadRequest, gin.H{"error": validationErr.Error(), "field": validationErr.Field})
			return
		}
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update evaluation"})
		return
	}

	c.JSON(http.StatusOK, evaluation)
}

// DeleteEvaluation deletes an evaluation
// @Summary Delete evaluation
// @Description Delete an evaluation by ID
// @Tags evaluations
// @Param id path string true "Evaluation ID"
// @Success 204 "No content"
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Failure 404 {object} map[string]interface{} "Not found"
// @Router /api/v1/evaluations/{id} [delete]
func (h *EvaluationHandler) DeleteEvaluation(c *gin.Context) {
	idStr := c.Param("id")
	if idStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidEvaluationID})
		return
	}

	err := h.evaluationUseCases.DeleteEvaluation(c.Request.Context(), idStr)
	if err != nil {
		if notFoundErr, ok := err.(*entities.NotFoundError); ok {
			c.JSON(http.StatusNotFound, gin.H{"error": notFoundErr.Error()})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete evaluation"})
		return
	}

	c.Status(http.StatusNoContent)
}

// GetEvaluationsByProject retrieves evaluations for a specific project
// @Summary Get evaluations by project
// @Description Get all evaluations for a specific project
// @Tags evaluations
// @Produce json
// @Param project_id path string true "Project ID"
// @Success 200 {object} dtos.EvaluationListResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/projects/{project_id}/evaluations [get]
func (h *EvaluationHandler) GetEvaluationsByProject(c *gin.Context) {
	projectIDStr := c.Param("project_id")
	if projectIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidProjectID})
		return
	}

	evaluations, err := h.evaluationUseCases.GetEvaluationsByProject(c.Request.Context(), projectIDStr)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get evaluations by project"})
		return
	}

	c.JSON(http.StatusOK, evaluations)
}

// GetEvaluationsByStudent retrieves evaluations for a specific student
// @Summary Get evaluations by student
// @Description Get all evaluations for a specific student
// @Tags evaluations
// @Produce json
// @Param student_id path string true "Student ID"
// @Success 200 {object} dtos.EvaluationListResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/students/{student_id}/evaluations [get]
func (h *EvaluationHandler) GetEvaluationsByStudent(c *gin.Context) {
	studentIDStr := c.Param("student_id")
	if studentIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidStudentID})
		return
	}

	evaluations, err := h.evaluationUseCases.GetEvaluationsByStudent(c.Request.Context(), studentIDStr)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get evaluations by student"})
		return
	}

	c.JSON(http.StatusOK, evaluations)
}

// GetEvaluationsByEvaluator retrieves evaluations for a specific evaluator
// @Summary Get evaluations by evaluator
// @Description Get all evaluations for a specific evaluator
// @Tags evaluations
// @Produce json
// @Param evaluator_id path string true "Evaluator ID"
// @Success 200 {object} dtos.EvaluationListResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/evaluators/{evaluator_id}/evaluations [get]
func (h *EvaluationHandler) GetEvaluationsByEvaluator(c *gin.Context) {
	evaluatorIDStr := c.Param("evaluator_id")
	if evaluatorIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidEvaluatorID})
		return
	}

	evaluations, err := h.evaluationUseCases.GetEvaluationsByEvaluator(c.Request.Context(), evaluatorIDStr)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get evaluations by evaluator"})
		return
	}

	c.JSON(http.StatusOK, evaluations)
}

// GetEvaluationsByType retrieves evaluations of a specific type
// @Summary Get evaluations by type
// @Description Get all evaluations of a specific type
// @Tags evaluations
// @Produce json
// @Param evaluation_type path string true "Evaluation type" Enums(initial, intermediate, final, peer, auto, academic)
// @Success 200 {object} dtos.EvaluationListResponse
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/evaluations/type/{evaluation_type} [get]
func (h *EvaluationHandler) GetEvaluationsByType(c *gin.Context) {
	evalTypeStr := c.Param("evaluation_type")
	if evalTypeStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Evaluation type is required"})
		return
	}

	evalType := entities.EvaluationType(evalTypeStr)
	
	evaluations, err := h.evaluationUseCases.GetEvaluationsByType(c.Request.Context(), evalType)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get evaluations by type"})
		return
	}

	c.JSON(http.StatusOK, evaluations)
}

// GetStudentAverageScore retrieves the average score for a student in a project
// @Summary Get student average score
// @Description Get the average score for a student in a specific project
// @Tags evaluations
// @Produce json
// @Param student_id path string true "Student ID"
// @Param project_id path string true "Project ID"
// @Success 200 {object} map[string]interface{} "Average score"
// @Failure 400 {object} map[string]interface{} "Bad request"
// @Router /api/v1/students/{student_id}/projects/{project_id}/average-score [get]
func (h *EvaluationHandler) GetStudentAverageScore(c *gin.Context) {
	studentIDStr := c.Param("student_id")
	if studentIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidStudentID})
		return
	}

	projectIDStr := c.Param("project_id")
	if projectIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": ErrInvalidProjectID})
		return
	}

	avgScore, err := h.evaluationUseCases.GetStudentAverageScore(c.Request.Context(), studentIDStr, projectIDStr)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get student average score"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"student_id":     studentIDStr,
		"project_id":     projectIDStr,
		"average_score":  avgScore,
	})
}
