package repositories

import (
	"context"

	"projectevalservice/internal/domain/entities"

	"github.com/google/uuid"
)

type ProjectRepository interface {
	Create(ctx context.Context, project *entities.Project) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.Project, error)
	GetByInstructorID(ctx context.Context, instructorID uuid.UUID) ([]*entities.Project, error)
	GetAll(ctx context.Context) ([]*entities.Project, error)
	Update(ctx context.Context, project *entities.Project) error
	Delete(ctx context.Context, id uuid.UUID) error
	GetActiveProjects(ctx context.Context) ([]*entities.Project, error)
	GetProjectsByStatus(ctx context.Context, status entities.ProjectStatus) ([]*entities.Project, error)
}

type SubmissionRepository interface {
	Create(ctx context.Context, submission *entities.Submission) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.Submission, error)
	GetByProjectID(ctx context.Context, projectID uuid.UUID) ([]*entities.Submission, error)
	GetByStudentID(ctx context.Context, studentID uuid.UUID) ([]*entities.Submission, error)
	GetByProjectAndStudent(ctx context.Context, projectID, studentID uuid.UUID) (*entities.Submission, error)
	GetAll(ctx context.Context) ([]*entities.Submission, error)
	Update(ctx context.Context, submission *entities.Submission) error
	Delete(ctx context.Context, id uuid.UUID) error
	GetSubmissionsByStatus(ctx context.Context, status entities.SubmissionStatus) ([]*entities.Submission, error)
	GetPendingEvaluations(ctx context.Context) ([]*entities.Submission, error)
}

type EvaluationRepository interface {
	Create(ctx context.Context, evaluation *entities.Evaluation) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.Evaluation, error)
	GetBySubmissionID(ctx context.Context, submissionID uuid.UUID) ([]*entities.Evaluation, error)
	GetByEvaluatorID(ctx context.Context, evaluatorID uuid.UUID) ([]*entities.Evaluation, error)
	GetBySubmissionAndEvaluator(ctx context.Context, submissionID, evaluatorID uuid.UUID) (*entities.Evaluation, error)
	GetAll(ctx context.Context) ([]*entities.Evaluation, error)
	Update(ctx context.Context, evaluation *entities.Evaluation) error
	Delete(ctx context.Context, id uuid.UUID) error
	GetEvaluationsByStatus(ctx context.Context, status entities.EvaluationStatus) ([]*entities.Evaluation, error)
	GetCompletedEvaluations(ctx context.Context) ([]*entities.Evaluation, error)
}

type StakeholderRepository interface {
	Create(ctx context.Context, stakeholder *entities.Stakeholder) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.Stakeholder, error)
	GetByProjectID(ctx context.Context, projectID uuid.UUID) ([]*entities.Stakeholder, error)
	GetByUserID(ctx context.Context, userID uuid.UUID) ([]*entities.Stakeholder, error)
	GetByProjectAndUser(ctx context.Context, projectID, userID uuid.UUID) (*entities.Stakeholder, error)
	GetByRole(ctx context.Context, projectID uuid.UUID, role entities.StakeholderRole) ([]*entities.Stakeholder, error)
	Update(ctx context.Context, stakeholder *entities.Stakeholder) error
	Delete(ctx context.Context, id uuid.UUID) error
	List(ctx context.Context, filters map[string]interface{}) ([]*entities.Stakeholder, error)
}

type ProjectDocumentRepository interface {
	Create(ctx context.Context, document *entities.ProjectDocument) error
	GetByID(ctx context.Context, id uuid.UUID) (*entities.ProjectDocument, error)
	GetByProjectID(ctx context.Context, projectID uuid.UUID) ([]*entities.ProjectDocument, error)
	GetByUploadedBy(ctx context.Context, uploadedByID uuid.UUID) ([]*entities.ProjectDocument, error)
	GetByType(ctx context.Context, projectID uuid.UUID, docType entities.DocumentType) ([]*entities.ProjectDocument, error)
	GetByStatus(ctx context.Context, status entities.DocumentStatus) ([]*entities.ProjectDocument, error)
	Update(ctx context.Context, document *entities.ProjectDocument) error
	Delete(ctx context.Context, id uuid.UUID) error
	List(ctx context.Context, filters map[string]interface{}) ([]*entities.ProjectDocument, error)
	GetRequiredDocuments(ctx context.Context, projectID uuid.UUID) ([]*entities.ProjectDocument, error)
}
