package repositories

import (
	"context"
	"time"

	"softwarefactoryservice/internal/domain/entities"
)

// EvaluationRepository defines the interface for evaluation data operations
type EvaluationRepository interface {
	// Create creates a new evaluation
	Create(ctx context.Context, evaluation *entities.Evaluation) error
	
	// GetByID retrieves an evaluation by its ID
	GetByID(ctx context.Context, id string) (*entities.Evaluation, error)
	
	// GetByUserStoryID retrieves evaluations by user story ID
	GetByUserStoryID(ctx context.Context, userStoryID string) ([]*entities.Evaluation, error)
	
	// GetByEvaluatorID retrieves evaluations by evaluator ID
	GetByEvaluatorID(ctx context.Context, evaluatorID string) ([]*entities.Evaluation, error)
	
	// GetByStudentID retrieves evaluations by student ID
	GetByStudentID(ctx context.Context, studentID string) ([]*entities.Evaluation, error)
	
	// GetByProjectID retrieves evaluations by project ID
	GetByProjectID(ctx context.Context, projectID string) ([]*entities.Evaluation, error)
	
	// GetByType retrieves evaluations by type
	GetByType(ctx context.Context, evalType entities.EvaluationType) ([]*entities.Evaluation, error)
	
	// Update updates an existing evaluation
	Update(ctx context.Context, evaluation *entities.Evaluation) error
	
	// Delete soft deletes an evaluation
	Delete(ctx context.Context, id string) error
	
	// List retrieves evaluations with pagination and filters
	List(ctx context.Context, filters EvaluationFilters) ([]*entities.Evaluation, int64, error)
	
	// GetStudentProgress retrieves student progress in a project
	GetStudentProgress(ctx context.Context, studentID, projectID string) (*StudentProgress, error)
	
	// GetProjectStatistics retrieves evaluation statistics for a project
	GetProjectStatistics(ctx context.Context, projectID string) (*ProjectEvaluationStats, error)
	
	// GetAverageScoreByStudent retrieves average score for a student in a project
	GetAverageScoreByStudent(ctx context.Context, studentID, projectID string) (float64, error)
}

// EvaluationFilters defines filters for evaluation listing
type EvaluationFilters struct {
	UserStoryID  *string                    `json:"user_story_id,omitempty"`
	EvaluatorID  *string                    `json:"evaluator_id,omitempty"`
	StudentID    *string                    `json:"student_id,omitempty"`
	ProjectID    *string                    `json:"project_id,omitempty"`
	Type         *entities.EvaluationType   `json:"type,omitempty"`
	MinScore     *float64                   `json:"min_score,omitempty"`
	MaxScore     *float64                   `json:"max_score,omitempty"`
	StartDate    *time.Time                 `json:"start_date,omitempty"`
	EndDate      *time.Time                 `json:"end_date,omitempty"`
	Page         int                        `json:"page"`
	PageSize     int                        `json:"page_size"`
	SortBy       string                     `json:"sort_by"`
	SortOrder    string                     `json:"sort_order"`
}

// StudentProgress represents a student's progress in a project
type StudentProgress struct {
	StudentID            string    `json:"student_id"`
	ProjectID            string    `json:"project_id"`
	TotalEvaluations     int       `json:"total_evaluations"`
	CompletedStories     int       `json:"completed_stories"`
	AverageScore         float64   `json:"average_score"`
	TechnicalScore       float64   `json:"technical_score"`
	AcademicScore        float64   `json:"academic_score"`
	CollaborationScore   float64   `json:"collaboration_score"`
	LastEvaluationDate   time.Time `json:"last_evaluation_date"`
}

// ProjectEvaluationStats represents evaluation statistics for a project
type ProjectEvaluationStats struct {
	ProjectID              string  `json:"project_id"`
	TotalEvaluations       int     `json:"total_evaluations"`
	AverageScore           float64 `json:"average_score"`
	AverageTechnicalScore  float64 `json:"average_technical_score"`
	AverageAcademicScore   float64 `json:"average_academic_score"`
	AverageCollabScore     float64 `json:"average_collaboration_score"`
	StudentsEvaluated      int     `json:"students_evaluated"`
	CompletionRate         float64 `json:"completion_rate"`
}
