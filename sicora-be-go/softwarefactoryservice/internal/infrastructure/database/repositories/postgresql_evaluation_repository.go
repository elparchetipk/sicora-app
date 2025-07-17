package repositories

import (
	"context"
	"fmt"
	"time"

	"gorm.io/gorm"

	"softwarefactoryservice/internal/domain/entities"
	"softwarefactoryservice/internal/domain/repositories"
)

const (
	avgScoreQuery = "AVG(overall_score) as avg_score, COUNT(*) as count"
)

type PostgreSQLEvaluationRepository struct {
	db *gorm.DB
}

func NewPostgreSQLEvaluationRepository(db *gorm.DB) repositories.EvaluationRepository {
	return &PostgreSQLEvaluationRepository{db: db}
}

// Create creates a new evaluation in the database
func (r *PostgreSQLEvaluationRepository) Create(ctx context.Context, evaluation *entities.Evaluation) error {
	if err := r.db.WithContext(ctx).Create(evaluation).Error; err != nil {
		return fmt.Errorf("failed to create evaluation: %w", err)
	}
	return nil
}

// GetByID retrieves an evaluation by ID
func (r *PostgreSQLEvaluationRepository) GetByID(ctx context.Context, id string) (*entities.Evaluation, error) {
	var evaluation entities.Evaluation
	if err := r.db.WithContext(ctx).First(&evaluation, "id = ?", id).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, entities.NewNotFoundError("evaluation", id)
		}
		return nil, fmt.Errorf("failed to get evaluation: %w", err)
	}
	return &evaluation, nil
}

// GetByUserStoryID retrieves all evaluations for a specific user story
func (r *PostgreSQLEvaluationRepository) GetByUserStoryID(ctx context.Context, userStoryID string) ([]*entities.Evaluation, error) {
	var evaluations []*entities.Evaluation
	if err := r.db.WithContext(ctx).Where("user_story_id = ?", userStoryID).Find(&evaluations).Error; err != nil {
		return nil, fmt.Errorf("failed to get evaluations by user story ID: %w", err)
	}
	return evaluations, nil
}

// GetByProjectID retrieves all evaluations for a specific project
func (r *PostgreSQLEvaluationRepository) GetByProjectID(ctx context.Context, projectID string) ([]*entities.Evaluation, error) {
	var evaluations []*entities.Evaluation
	if err := r.db.WithContext(ctx).Where("project_id = ?", projectID).Find(&evaluations).Error; err != nil {
		return nil, fmt.Errorf("failed to get evaluations by project ID: %w", err)
	}
	return evaluations, nil
}

// GetByStudentID retrieves all evaluations for a specific student
func (r *PostgreSQLEvaluationRepository) GetByStudentID(ctx context.Context, studentID string) ([]*entities.Evaluation, error) {
	var evaluations []*entities.Evaluation
	if err := r.db.WithContext(ctx).Where("apprentice_id = ?", studentID).Find(&evaluations).Error; err != nil {
		return nil, fmt.Errorf("failed to get evaluations by student ID: %w", err)
	}
	return evaluations, nil
}

// GetByEvaluatorID retrieves all evaluations made by a specific evaluator
func (r *PostgreSQLEvaluationRepository) GetByEvaluatorID(ctx context.Context, evaluatorID string) ([]*entities.Evaluation, error) {
	var evaluations []*entities.Evaluation
	if err := r.db.WithContext(ctx).Where("evaluator_id = ?", evaluatorID).Find(&evaluations).Error; err != nil {
		return nil, fmt.Errorf("failed to get evaluations by evaluator ID: %w", err)
	}
	return evaluations, nil
}

// GetByType retrieves all evaluations of a specific type
func (r *PostgreSQLEvaluationRepository) GetByType(ctx context.Context, evaluationType entities.EvaluationType) ([]*entities.Evaluation, error) {
	var evaluations []*entities.Evaluation
	if err := r.db.WithContext(ctx).Where("evaluation_type = ?", evaluationType).Find(&evaluations).Error; err != nil {
		return nil, fmt.Errorf("failed to get evaluations by type: %w", err)
	}
	return evaluations, nil
}

// Update updates an existing evaluation
func (r *PostgreSQLEvaluationRepository) Update(ctx context.Context, evaluation *entities.Evaluation) error {
	if err := r.db.WithContext(ctx).Save(evaluation).Error; err != nil {
		return fmt.Errorf("failed to update evaluation: %w", err)
	}
	return nil
}

// Delete deletes an evaluation by ID
func (r *PostgreSQLEvaluationRepository) Delete(ctx context.Context, id string) error {
	result := r.db.WithContext(ctx).Delete(&entities.Evaluation{}, "id = ?", id)
	if result.Error != nil {
		return fmt.Errorf("failed to delete evaluation: %w", result.Error)
	}
	if result.RowsAffected == 0 {
		return entities.NewNotFoundError("evaluation", id)
	}
	return nil
}

// List retrieves evaluations with pagination and filters
func (r *PostgreSQLEvaluationRepository) List(ctx context.Context, filters repositories.EvaluationFilters) ([]*entities.Evaluation, int64, error) {
	var evaluations []*entities.Evaluation
	var total int64

	query := r.db.WithContext(ctx).Model(&entities.Evaluation{})

	// Apply filters
	if filters.UserStoryID != nil {
		query = query.Where("user_story_id = ?", *filters.UserStoryID)
	}
	if filters.EvaluatorID != nil {
		query = query.Where("evaluator_id = ?", *filters.EvaluatorID)
	}
	if filters.StudentID != nil {
		query = query.Where("apprentice_id = ?", *filters.StudentID)
	}
	if filters.ProjectID != nil {
		query = query.Where("project_id = ?", *filters.ProjectID)
	}
	if filters.Type != nil {
		query = query.Where("evaluation_type = ?", *filters.Type)
	}
	if filters.MinScore != nil {
		query = query.Where("overall_score >= ?", *filters.MinScore)
	}
	if filters.MaxScore != nil {
		query = query.Where("overall_score <= ?", *filters.MaxScore)
	}
	if filters.StartDate != nil {
		query = query.Where("evaluation_date >= ?", *filters.StartDate)
	}
	if filters.EndDate != nil {
		query = query.Where("evaluation_date <= ?", *filters.EndDate)
	}

	// Count total
	if err := query.Count(&total).Error; err != nil {
		return nil, 0, fmt.Errorf("failed to count evaluations: %w", err)
	}

	// Apply pagination
	offset := (filters.Page - 1) * filters.PageSize
	query = query.Offset(offset).Limit(filters.PageSize)

	// Apply sorting
	if filters.SortBy != "" {
		order := filters.SortBy
		if filters.SortOrder == "desc" {
			order += " desc"
		}
		query = query.Order(order)
	} else {
		query = query.Order("evaluation_date desc")
	}

	if err := query.Find(&evaluations).Error; err != nil {
		return nil, 0, fmt.Errorf("failed to list evaluations: %w", err)
	}

	return evaluations, total, nil
}

// GetStudentProgress retrieves student progress in a project
func (r *PostgreSQLEvaluationRepository) GetStudentProgress(ctx context.Context, studentID, projectID string) (*repositories.StudentProgress, error) {
	var result struct {
		TotalEvaluations   int64     `json:"total_evaluations"`
		AverageScore       float64   `json:"average_score"`
		TechnicalScore     float64   `json:"technical_score"`
		LastEvaluationDate time.Time `json:"last_evaluation_date"`
	}

	query := r.db.WithContext(ctx).Model(&entities.Evaluation{}).
		Select(`
			COUNT(*) as total_evaluations,
			AVG(overall_score) as average_score,
			AVG((tech_coding_quality + tech_problem_solving + tech_technology_adoption + tech_testing_practices) / 4.0) as technical_score,
			MAX(evaluation_date) as last_evaluation_date
		`).
		Where("apprentice_id = ? AND project_id = ?", studentID, projectID)

	if err := query.Scan(&result).Error; err != nil {
		return nil, fmt.Errorf("failed to get student progress: %w", err)
	}

	return &repositories.StudentProgress{
		StudentID:          studentID,
		ProjectID:          projectID,
		TotalEvaluations:   int(result.TotalEvaluations),
		AverageScore:       result.AverageScore,
		TechnicalScore:     result.TechnicalScore,
		LastEvaluationDate: result.LastEvaluationDate,
	}, nil
}

// GetProjectStatistics retrieves evaluation statistics for a project
func (r *PostgreSQLEvaluationRepository) GetProjectStatistics(ctx context.Context, projectID string) (*repositories.ProjectEvaluationStats, error) {
	var result struct {
		TotalEvaluations      int64   `json:"total_evaluations"`
		AverageScore          float64 `json:"average_score"`
		AverageTechnicalScore float64 `json:"average_technical_score"`
		StudentsEvaluated     int64   `json:"students_evaluated"`
	}

	query := r.db.WithContext(ctx).Model(&entities.Evaluation{}).
		Select(`
			COUNT(*) as total_evaluations,
			AVG(overall_score) as average_score,
			AVG((tech_coding_quality + tech_problem_solving + tech_technology_adoption + tech_testing_practices) / 4.0) as average_technical_score,
			COUNT(DISTINCT apprentice_id) as students_evaluated
		`).
		Where("project_id = ?", projectID)

	if err := query.Scan(&result).Error; err != nil {
		return nil, fmt.Errorf("failed to get project statistics: %w", err)
	}

	return &repositories.ProjectEvaluationStats{
		ProjectID:             projectID,
		TotalEvaluations:      int(result.TotalEvaluations),
		AverageScore:          result.AverageScore,
		AverageTechnicalScore: result.AverageTechnicalScore,
		StudentsEvaluated:     int(result.StudentsEvaluated),
	}, nil
}

// GetAverageScoreByStudent retrieves average score for a student in a project
func (r *PostgreSQLEvaluationRepository) GetAverageScoreByStudent(ctx context.Context, studentID, projectID string) (float64, error) {
	var avgScore float64

	if err := r.db.WithContext(ctx).Model(&entities.Evaluation{}).
		Select("AVG(overall_score)").
		Where("apprentice_id = ? AND project_id = ?", studentID, projectID).
		Scan(&avgScore).Error; err != nil {
		return 0, fmt.Errorf("failed to get average score: %w", err)
	}

	return avgScore, nil
}
