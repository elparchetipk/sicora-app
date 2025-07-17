package handlers

import (
	"net/http"

	"projectevalservice/internal/application/usecases"
	"projectevalservice/internal/domain/entities"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type EvaluationHandler struct {
	evaluationUseCase *usecases.EvaluationUseCase
}

func NewEvaluationHandler(evaluationUseCase *usecases.EvaluationUseCase) *EvaluationHandler {
	return &EvaluationHandler{
		evaluationUseCase: evaluationUseCase,
	}
}

type CreateEvaluationRequest struct {
	SubmissionID          uuid.UUID `json:"submission_id" binding:"required"`
	EvaluatorID           uuid.UUID `json:"evaluator_id" binding:"required"`
	FunctionalityScore    float64   `json:"functionality_score" binding:"min=0,max=100"`
	CodeQualityScore      float64   `json:"code_quality_score" binding:"min=0,max=100"`
	ArchitectureScore     float64   `json:"architecture_score" binding:"min=0,max=100"`
	DocumentationScore    float64   `json:"documentation_score" binding:"min=0,max=100"`
	TestingScore          float64   `json:"testing_score" binding:"min=0,max=100"`
	DeploymentScore       float64   `json:"deployment_score" binding:"min=0,max=100"`
	SecurityScore         float64   `json:"security_score" binding:"min=0,max=100"`
	PerformanceScore      float64   `json:"performance_score" binding:"min=0,max=100"`
	GeneralComments       string    `json:"general_comments"`
	FunctionalityComments string    `json:"functionality_comments"`
	CodeQualityComments   string    `json:"code_quality_comments"`
	ArchitectureComments  string    `json:"architecture_comments"`
	DocumentationComments string    `json:"documentation_comments"`
	TestingComments       string    `json:"testing_comments"`
	DeploymentComments    string    `json:"deployment_comments"`
	SecurityComments      string    `json:"security_comments"`
	PerformanceComments   string    `json:"performance_comments"`
	Recommendations       string    `json:"recommendations"`
}

// @Summary Create a new evaluation
// @Description Create an evaluation for a submission
// @Tags evaluations
// @Accept json
// @Produce json
// @Param request body CreateEvaluationRequest true "Evaluation data"
// @Success 201 {object} entities.Evaluation
// @Failure 400 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Security BearerAuth
// @Router /evaluations [post]
func (h *EvaluationHandler) CreateEvaluation(c *gin.Context) {
	var req CreateEvaluationRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	evaluation := &entities.Evaluation{
		SubmissionID:          req.SubmissionID,
		EvaluatorID:           req.EvaluatorID,
		FunctionalityScore:    req.FunctionalityScore,
		CodeQualityScore:      req.CodeQualityScore,
		ArchitectureScore:     req.ArchitectureScore,
		DocumentationScore:    req.DocumentationScore,
		TestingScore:          req.TestingScore,
		DeploymentScore:       req.DeploymentScore,
		SecurityScore:         req.SecurityScore,
		PerformanceScore:      req.PerformanceScore,
		GeneralComments:       req.GeneralComments,
		FunctionalityComments: req.FunctionalityComments,
		CodeQualityComments:   req.CodeQualityComments,
		ArchitectureComments:  req.ArchitectureComments,
		DocumentationComments: req.DocumentationComments,
		TestingComments:       req.TestingComments,
		DeploymentComments:    req.DeploymentComments,
		SecurityComments:      req.SecurityComments,
		PerformanceComments:   req.PerformanceComments,
		Recommendations:       req.Recommendations,
	}

	if err := h.evaluationUseCase.CreateEvaluation(c.Request.Context(), evaluation); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, evaluation)
}

// @Summary Get evaluation by ID
// @Description Get a specific evaluation by its ID
// @Tags evaluations
// @Produce json
// @Param id path string true "Evaluation ID"
// @Success 200 {object} entities.Evaluation
// @Failure 400 {object} map[string]string
// @Failure 404 {object} map[string]string
// @Security BearerAuth
// @Router /evaluations/{id} [get]
func (h *EvaluationHandler) GetEvaluation(c *gin.Context) {
	idParam := c.Param("id")
	id, err := uuid.Parse(idParam)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid evaluation ID"})
		return
	}

	evaluation, err := h.evaluationUseCase.GetEvaluationByID(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	if evaluation == nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Evaluation not found"})
		return
	}

	c.JSON(http.StatusOK, evaluation)
}

// @Summary Get evaluations
// @Description Get evaluations filtered by submission or evaluator
// @Tags evaluations
// @Produce json
// @Param submission_id query string false "Filter by submission ID"
// @Param evaluator_id query string false "Filter by evaluator ID"
// @Success 200 {array} entities.Evaluation
// @Failure 400 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Security BearerAuth
// @Router /evaluations [get]
func (h *EvaluationHandler) GetEvaluations(c *gin.Context) {
	submissionIDParam := c.Query("submission_id")
	evaluatorIDParam := c.Query("evaluator_id")

	var evaluations []*entities.Evaluation
	var err error

	if submissionIDParam != "" {
		submissionID, parseErr := uuid.Parse(submissionIDParam)
		if parseErr != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid submission ID"})
			return
		}
		evaluations, err = h.evaluationUseCase.GetEvaluationsBySubmission(c.Request.Context(), submissionID)
	} else if evaluatorIDParam != "" {
		evaluatorID, parseErr := uuid.Parse(evaluatorIDParam)
		if parseErr != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid evaluator ID"})
			return
		}
		evaluations, err = h.evaluationUseCase.GetEvaluationsByEvaluator(c.Request.Context(), evaluatorID)
	} else {
		c.JSON(http.StatusBadRequest, gin.H{"error": "submission_id or evaluator_id parameter required"})
		return
	}

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, evaluations)
}

// @Summary Complete evaluation
// @Description Complete and calculate final scores for an evaluation
// @Tags evaluations
// @Param id path string true "Evaluation ID"
// @Success 200 {object} entities.Evaluation
// @Failure 400 {object} map[string]string
// @Failure 404 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Security BearerAuth
// @Router /evaluations/{id}/complete [patch]
func (h *EvaluationHandler) CompleteEvaluation(c *gin.Context) {
	idParam := c.Param("id")
	id, err := uuid.Parse(idParam)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid evaluation ID"})
		return
	}

	if err := h.evaluationUseCase.CompleteEvaluation(c.Request.Context(), id); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	evaluation, err := h.evaluationUseCase.GetEvaluationByID(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, evaluation)
}

// @Summary Publish evaluation
// @Description Publish a completed evaluation to make it visible to students
// @Tags evaluations
// @Param id path string true "Evaluation ID"
// @Success 200 {object} entities.Evaluation
// @Failure 400 {object} map[string]string
// @Failure 404 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Security BearerAuth
// @Router /evaluations/{id}/publish [patch]
func (h *EvaluationHandler) PublishEvaluation(c *gin.Context) {
	idParam := c.Param("id")
	id, err := uuid.Parse(idParam)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid evaluation ID"})
		return
	}

	if err := h.evaluationUseCase.PublishEvaluation(c.Request.Context(), id); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	evaluation, err := h.evaluationUseCase.GetEvaluationByID(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, evaluation)
}
