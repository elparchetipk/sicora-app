package handlers

import (
	"net/http"

	"projectevalservice/internal/application/usecases"
	"projectevalservice/internal/domain/entities"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type SubmissionHandler struct {
	submissionUseCase *usecases.SubmissionUseCase
}

func NewSubmissionHandler(submissionUseCase *usecases.SubmissionUseCase) *SubmissionHandler {
	return &SubmissionHandler{
		submissionUseCase: submissionUseCase,
	}
}

type CreateSubmissionRequest struct {
	ProjectID              uuid.UUID `json:"project_id" binding:"required"`
	StudentID              uuid.UUID `json:"student_id" binding:"required"`
	RepositoryURL          string    `json:"repository_url" binding:"required,url"`
	DeploymentURL          string    `json:"deployment_url" binding:"omitempty,url"`
	Description            string    `json:"description"`
	TechnicalDocumentation string    `json:"technical_documentation"`
}

// @Summary Create a new submission
// @Description Submit a project for evaluation
// @Tags submissions
// @Accept json
// @Produce json
// @Param request body CreateSubmissionRequest true "Submission data"
// @Success 201 {object} entities.Submission
// @Failure 400 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Security BearerAuth
// @Router /submissions [post]
func (h *SubmissionHandler) CreateSubmission(c *gin.Context) {
	var req CreateSubmissionRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	submission := &entities.Submission{
		ProjectID:              req.ProjectID,
		StudentID:              req.StudentID,
		RepositoryURL:          req.RepositoryURL,
		DeploymentURL:          req.DeploymentURL,
		Description:            req.Description,
		TechnicalDocumentation: req.TechnicalDocumentation,
	}

	if err := h.submissionUseCase.CreateSubmission(c.Request.Context(), submission); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, submission)
}

// @Summary Get submission by ID
// @Description Get a specific submission by its ID
// @Tags submissions
// @Produce json
// @Param id path string true "Submission ID"
// @Success 200 {object} entities.Submission
// @Failure 400 {object} map[string]string
// @Failure 404 {object} map[string]string
// @Security BearerAuth
// @Router /submissions/{id} [get]
func (h *SubmissionHandler) GetSubmission(c *gin.Context) {
	idParam := c.Param("id")
	id, err := uuid.Parse(idParam)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid submission ID"})
		return
	}

	submission, err := h.submissionUseCase.GetSubmissionByID(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	if submission == nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Submission not found"})
		return
	}

	c.JSON(http.StatusOK, submission)
}

// @Summary Get submissions by project
// @Description Get all submissions for a specific project
// @Tags submissions
// @Produce json
// @Param project_id query string false "Filter by project ID"
// @Param student_id query string false "Filter by student ID"
// @Success 200 {array} entities.Submission
// @Failure 400 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Security BearerAuth
// @Router /submissions [get]
func (h *SubmissionHandler) GetSubmissions(c *gin.Context) {
	projectIDParam := c.Query("project_id")
	studentIDParam := c.Query("student_id")

	var submissions []*entities.Submission
	var err error

	if projectIDParam != "" {
		projectID, parseErr := uuid.Parse(projectIDParam)
		if parseErr != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid project ID"})
			return
		}
		submissions, err = h.submissionUseCase.GetSubmissionsByProject(c.Request.Context(), projectID)
	} else if studentIDParam != "" {
		studentID, parseErr := uuid.Parse(studentIDParam)
		if parseErr != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid student ID"})
			return
		}
		submissions, err = h.submissionUseCase.GetSubmissionsByStudent(c.Request.Context(), studentID)
	} else {
		c.JSON(http.StatusBadRequest, gin.H{"error": "project_id or student_id parameter required"})
		return
	}

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, submissions)
}

// @Summary Get pending evaluations
// @Description Get all submissions pending evaluation
// @Tags submissions
// @Produce json
// @Success 200 {array} entities.Submission
// @Failure 500 {object} map[string]string
// @Security BearerAuth
// @Router /submissions/pending [get]
func (h *SubmissionHandler) GetPendingEvaluations(c *gin.Context) {
	submissions, err := h.submissionUseCase.GetPendingEvaluations(c.Request.Context())
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, submissions)
}
