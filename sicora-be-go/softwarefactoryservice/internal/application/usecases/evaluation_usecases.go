package usecases

import (
	"context"
	"fmt"
	"time"

	"softwarefactoryservice/internal/application/dtos"
	"softwarefactoryservice/internal/domain/entities"
	"softwarefactoryservice/internal/domain/repositories"
)

// EvaluationUseCases handles business logic for evaluations
type EvaluationUseCases struct {
	evaluationRepo repositories.EvaluationRepository
	projectRepo    repositories.ProjectRepository
	sprintRepo     repositories.SprintRepository
	userStoryRepo  repositories.UserStoryRepository
}

// NewEvaluationUseCases creates a new EvaluationUseCases instance
func NewEvaluationUseCases(
	evaluationRepo repositories.EvaluationRepository,
	projectRepo repositories.ProjectRepository,
	sprintRepo repositories.SprintRepository,
	userStoryRepo repositories.UserStoryRepository,
) *EvaluationUseCases {
	return &EvaluationUseCases{
		evaluationRepo: evaluationRepo,
		projectRepo:    projectRepo,
		sprintRepo:     sprintRepo,
		userStoryRepo:  userStoryRepo,
	}
}

// CreateEvaluation creates a new evaluation
func (e *EvaluationUseCases) CreateEvaluation(ctx context.Context, req *dtos.CreateEvaluationRequest) (*dtos.EvaluationResponse, error) {
	// Convert request to entity
	evaluation, err := req.ToEntity()
	if err != nil {
		return nil, fmt.Errorf("failed to convert request to entity: %w", err)
	}

	// Validate relationships
	if _, err := e.projectRepo.GetByID(ctx, req.ProjectID); err != nil {
		return nil, fmt.Errorf("project with ID %s not found: %w", req.ProjectID, err)
	}

	if req.SprintID != nil {
		if _, err := e.sprintRepo.GetByID(ctx, *req.SprintID); err != nil {
			return nil, fmt.Errorf("sprint with ID %s not found: %w", *req.SprintID, err)
		}
	}

	// Validate the evaluation
	if err := evaluation.Validate(); err != nil {
		return nil, err
	}

	// Create the evaluation
	if err := e.evaluationRepo.Create(ctx, evaluation); err != nil {
		return nil, err
	}

	// Convert to response
	response := &dtos.EvaluationResponse{}
	response.FromEntity(evaluation)
	return response, nil
}

// GetEvaluation retrieves an evaluation by ID
func (e *EvaluationUseCases) GetEvaluation(ctx context.Context, id string) (*dtos.EvaluationResponse, error) {
	evaluation, err := e.evaluationRepo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	response := &dtos.EvaluationResponse{}
	response.FromEntity(evaluation)
	return response, nil
}

// ListEvaluations retrieves evaluations with filtering and pagination
func (e *EvaluationUseCases) ListEvaluations(ctx context.Context, req *dtos.EvaluationFilterRequest) (*dtos.EvaluationListResponse, error) {
	filters := repositories.EvaluationFilters{
		UserStoryID: req.ApprenticeID,
		EvaluatorID: req.EvaluatorID,
		StudentID:   req.ApprenticeID,
		ProjectID:   req.ProjectID,
		Page:        req.Page,
		PageSize:    req.PageSize,
	}

	// Set defaults
	if filters.Page <= 0 {
		filters.Page = 1
	}
	if filters.PageSize <= 0 {
		filters.PageSize = 20
	}

	evaluations, total, err := e.evaluationRepo.List(ctx, filters)
	if err != nil {
		return nil, err
	}

	// Convert to slice of entities (dereferenced)
	var evaluationEntities []entities.Evaluation
	for _, eval := range evaluations {
		evaluationEntities = append(evaluationEntities, *eval)
	}

	response := &dtos.EvaluationListResponse{}
	response.FromEntityList(evaluationEntities, total, filters.Page, filters.PageSize)
	return response, nil
}

// UpdateEvaluation updates an existing evaluation
func (e *EvaluationUseCases) UpdateEvaluation(ctx context.Context, id string, req *dtos.UpdateEvaluationRequest) (*dtos.EvaluationResponse, error) {
	// Get existing evaluation
	evaluation, err := e.evaluationRepo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	// Apply updates
	if err := req.ApplyToEntity(evaluation); err != nil {
		return nil, err
	}

	evaluation.UpdatedAt = time.Now()

	// Validate the updated evaluation
	if err := evaluation.Validate(); err != nil {
		return nil, err
	}

	// Update in repository
	if err := e.evaluationRepo.Update(ctx, evaluation); err != nil {
		return nil, err
	}

	response := &dtos.EvaluationResponse{}
	response.FromEntity(evaluation)
	return response, nil
}

// DeleteEvaluation soft deletes an evaluation
func (e *EvaluationUseCases) DeleteEvaluation(ctx context.Context, id string) error {
	return e.evaluationRepo.Delete(ctx, id)
}

// GetStudentProgress retrieves student progress in a project
func (e *EvaluationUseCases) GetStudentProgress(ctx context.Context, studentID, projectID string) (*repositories.StudentProgress, error) {
	return e.evaluationRepo.GetStudentProgress(ctx, studentID, projectID)
}

// GetProjectEvaluationStats retrieves evaluation statistics for a project
func (e *EvaluationUseCases) GetProjectEvaluationStats(ctx context.Context, projectID string) (*repositories.ProjectEvaluationStats, error) {
	return e.evaluationRepo.GetProjectStatistics(ctx, projectID)
}

// GetStudentAverageScore retrieves average score for a student in a project
func (e *EvaluationUseCases) GetStudentAverageScore(ctx context.Context, studentID, projectID string) (float64, error) {
	return e.evaluationRepo.GetAverageScoreByStudent(ctx, studentID, projectID)
}

// GetEvaluationsByType retrieves evaluations by type
func (e *EvaluationUseCases) GetEvaluationsByType(ctx context.Context, evalType entities.EvaluationType) (*dtos.EvaluationListResponse, error) {
	evaluations, err := e.evaluationRepo.GetByType(ctx, evalType)
	if err != nil {
		return nil, err
	}

	// Convert to slice of entities (dereferenced)
	var evaluationEntities []entities.Evaluation
	for _, eval := range evaluations {
		evaluationEntities = append(evaluationEntities, *eval)
	}

	response := &dtos.EvaluationListResponse{}
	response.FromEntityList(evaluationEntities, int64(len(evaluationEntities)), 1, len(evaluationEntities))
	return response, nil
}

// GetEvaluationsByProject retrieves evaluations for a specific project
func (e *EvaluationUseCases) GetEvaluationsByProject(ctx context.Context, projectID string) (*dtos.EvaluationListResponse, error) {
	evaluations, err := e.evaluationRepo.GetByProjectID(ctx, projectID)
	if err != nil {
		return nil, err
	}

	// Convert to slice of entities (dereferenced)
	var evaluationEntities []entities.Evaluation
	for _, eval := range evaluations {
		evaluationEntities = append(evaluationEntities, *eval)
	}

	response := &dtos.EvaluationListResponse{}
	response.FromEntityList(evaluationEntities, int64(len(evaluationEntities)), 1, len(evaluationEntities))
	return response, nil
}

// GetEvaluationsByEvaluator retrieves evaluations by evaluator
func (e *EvaluationUseCases) GetEvaluationsByEvaluator(ctx context.Context, evaluatorID string) (*dtos.EvaluationListResponse, error) {
	evaluations, err := e.evaluationRepo.GetByEvaluatorID(ctx, evaluatorID)
	if err != nil {
		return nil, err
	}

	// Convert to slice of entities (dereferenced)
	var evaluationEntities []entities.Evaluation
	for _, eval := range evaluations {
		evaluationEntities = append(evaluationEntities, *eval)
	}

	response := &dtos.EvaluationListResponse{}
	response.FromEntityList(evaluationEntities, int64(len(evaluationEntities)), 1, len(evaluationEntities))
	return response, nil
}

// GetEvaluationsByStudent retrieves evaluations for a specific student
func (e *EvaluationUseCases) GetEvaluationsByStudent(ctx context.Context, studentID string) (*dtos.EvaluationListResponse, error) {
	evaluations, err := e.evaluationRepo.GetByStudentID(ctx, studentID)
	if err != nil {
		return nil, err
	}

	// Convert to slice of entities (dereferenced)
	var evaluationEntities []entities.Evaluation
	for _, eval := range evaluations {
		evaluationEntities = append(evaluationEntities, *eval)
	}

	response := &dtos.EvaluationListResponse{}
	response.FromEntityList(evaluationEntities, int64(len(evaluationEntities)), 1, len(evaluationEntities))
	return response, nil
}

// GetEvaluationStats retrieves evaluation statistics
func (e *EvaluationUseCases) GetEvaluationStats(ctx context.Context, filters repositories.EvaluationFilters) (*dtos.EvaluationStatsResponse, error) {
	evaluations, total, err := e.evaluationRepo.List(ctx, filters)
	if err != nil {
		return nil, err
	}

	if total == 0 {
		return &dtos.EvaluationStatsResponse{
			TotalEvaluations: 0,
		}, nil
	}

	stats := &dtos.EvaluationStatsResponse{
		TotalEvaluations:   total,
		EvaluationsByType:  make(map[string]int64),
		ScoreDistribution:  make(map[string]int64),
	}

	var totalOverallScore, totalTechnicalScore, totalSoftSkillsScore float64
	var needingImprovement int64

	for _, eval := range evaluations {
		// Count by type
		stats.EvaluationsByType[string(eval.EvaluationType)]++

		// Sum scores
		totalOverallScore += eval.OverallScore
		techAvg := eval.GetTechnicalAverage()
		softAvg := eval.GetSoftSkillsAverage()
		totalTechnicalScore += techAvg
		totalSoftSkillsScore += softAvg

		// Count needing improvement
		if eval.OverallScore < 3.0 {
			needingImprovement++
		}

		// Score distribution
		scoreRange := fmt.Sprintf("%.0f-%.0f", eval.OverallScore, eval.OverallScore+0.9)
		stats.ScoreDistribution[scoreRange]++
	}

	stats.AverageOverallScore = totalOverallScore / float64(total)
	stats.AverageTechnicalScore = totalTechnicalScore / float64(total)
	stats.AverageSoftSkillsScore = totalSoftSkillsScore / float64(total)
	stats.NeedingImprovement = needingImprovement
	
	if needingImprovement > 0 {
		stats.ImprovementRate = float64(needingImprovement) / float64(total) * 100
	}

	return stats, nil
}

// ValidateEvaluationScores validates that all scores are within valid ranges
func (e *EvaluationUseCases) ValidateEvaluationScores(technicalScore, softSkillsScore float64) error {
	if technicalScore < 1 || technicalScore > 5 {
		return fmt.Errorf("technical score must be between 1 and 5")
	}
	if softSkillsScore < 1 || softSkillsScore > 5 {
		return fmt.Errorf("soft skills score must be between 1 and 5")
	}
	return nil
}
