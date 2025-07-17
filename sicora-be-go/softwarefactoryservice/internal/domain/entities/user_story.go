package entities

import (
	"time"

	"github.com/google/uuid"
)

// StoryStatus representa el estado de una historia de usuario
type StoryStatus string

const (
	StoryStatusBacklog    StoryStatus = "backlog"
	StoryStatusTodo       StoryStatus = "todo"
	StoryStatusInProgress StoryStatus = "in_progress"
	StoryStatusReview     StoryStatus = "review"
	StoryStatusDone       StoryStatus = "done"
)

// StoryType representa el tipo de historia de usuario
type StoryType string

const (
	StoryTypeFunctional StoryType = "functional"
	StoryTypeAcademic   StoryType = "academic"
	StoryTypeTechnical  StoryType = "technical"
	StoryTypeBugfix     StoryType = "bugfix"
)

// UserStory representa una historia de usuario académica
type UserStory struct {
	ID                     uuid.UUID            `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	ProjectID              uuid.UUID            `json:"project_id" gorm:"type:uuid;not null"`
	SprintID               *uuid.UUID           `json:"sprint_id,omitempty" gorm:"type:uuid"`
	Title                  string               `json:"title" gorm:"not null;size:255" validate:"required,min=5,max=255"`
	Description            string               `json:"description" gorm:"type:text" validate:"required,min=10"`
	FunctionalObjective    string               `json:"functional_objective" gorm:"type:text" validate:"required"`
	AcademicObjective      string               `json:"academic_objective" gorm:"type:text" validate:"required"`
	AcceptanceCriteria     []AcceptanceCriterion `json:"acceptance_criteria" gorm:"serializer:json"`
	AcademicCriteria       []AcademicCriterion  `json:"academic_criteria" gorm:"serializer:json"`
	StoryPoints            int                  `json:"story_points" gorm:"not null" validate:"min=1,max=21"`
	Priority               int                  `json:"priority" gorm:"not null;default:3" validate:"min=1,max=5"`
	Type                   StoryType            `json:"type" gorm:"type:varchar(20);default:'functional'"`
	Status                 StoryStatus          `json:"status" gorm:"type:varchar(20);default:'backlog'"`
	AssignedTo             *uuid.UUID           `json:"assigned_to,omitempty" gorm:"type:uuid"`
	EstimatedHours         int                  `json:"estimated_hours" gorm:"default:0"`
	ActualHours            int                  `json:"actual_hours" gorm:"default:0"`
	LearningHours          int                  `json:"learning_hours" gorm:"default:0"` // Tiempo dedicado al aprendizaje
	Tags                   []string             `json:"tags" gorm:"type:text[]"`
	Dependencies           []uuid.UUID          `json:"dependencies" gorm:"type:uuid[]"`
	CreatedBy              uuid.UUID            `json:"created_by" gorm:"type:uuid;not null"`
	CreatedAt              time.Time            `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt              time.Time            `json:"updated_at" gorm:"autoUpdateTime"`
	CompletedAt            *time.Time           `json:"completed_at,omitempty"`
	
	// Relationships
	Project                Project              `json:"project,omitempty" gorm:"foreignKey:ProjectID"`
	Sprint                 *Sprint              `json:"sprint,omitempty" gorm:"foreignKey:SprintID"`
	Evidences              []Evidence           `json:"evidences,omitempty" gorm:"foreignKey:UserStoryID"`
	Comments               []StoryComment       `json:"comments,omitempty" gorm:"foreignKey:UserStoryID"`
}

// AcceptanceCriterion representa un criterio de aceptación técnico
type AcceptanceCriterion struct {
	ID          string `json:"id"`
	Description string `json:"description"`
	IsCompleted bool   `json:"is_completed"`
	TestCase    string `json:"test_case,omitempty"`
}

// AcademicCriterion representa un criterio de aceptación académico
type AcademicCriterion struct {
	ID               string   `json:"id"`
	Competency       string   `json:"competency"`       // Competencia SENA asociada
	Description      string   `json:"description"`
	EvidenceRequired []string `json:"evidence_required"` // Tipos de evidencia requerida
	IsCompleted      bool     `json:"is_completed"`
	RubricScale      int      `json:"rubric_scale"` // Escala de evaluación 1-5
}

// Evidence representa evidencia de aprendizaje para una historia
type Evidence struct {
	ID          uuid.UUID    `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	UserStoryID uuid.UUID    `json:"user_story_id" gorm:"type:uuid;not null"`
	Type        EvidenceType `json:"type" gorm:"type:varchar(30)" validate:"required"`
	Title       string       `json:"title" gorm:"not null;size:255"`
	Description string       `json:"description" gorm:"type:text"`
	URL         string       `json:"url" gorm:"size:512"`  // URL del archivo o repositorio
	FilePath    string       `json:"file_path" gorm:"size:512"` // Ruta del archivo
	SubmittedBy uuid.UUID    `json:"submitted_by" gorm:"type:uuid;not null"`
	SubmittedAt time.Time    `json:"submitted_at" gorm:"autoCreateTime"`
	ReviewedBy  *uuid.UUID   `json:"reviewed_by,omitempty" gorm:"type:uuid"`
	ReviewedAt  *time.Time   `json:"reviewed_at,omitempty"`
	IsApproved  bool         `json:"is_approved" gorm:"default:false"`
	Feedback    string       `json:"feedback" gorm:"type:text"`
	
	// Relationships
	UserStory   UserStory    `json:"user_story,omitempty" gorm:"foreignKey:UserStoryID"`
}

// EvidenceType representa el tipo de evidencia
type EvidenceType string

const (
	EvidenceCode        EvidenceType = "code"
	EvidenceDemo        EvidenceType = "demo"
	EvidenceDocument    EvidenceType = "document"
	EvidenceScreenshot  EvidenceType = "screenshot"
	EvidenceVideo       EvidenceType = "video"
	EvidencePresentation EvidenceType = "presentation"
	EvidenceTest        EvidenceType = "test"
)

// StoryComment representa un comentario en una historia de usuario
type StoryComment struct {
	ID          uuid.UUID     `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	UserStoryID uuid.UUID     `json:"user_story_id" gorm:"type:uuid;not null"`
	AuthorID    uuid.UUID     `json:"author_id" gorm:"type:uuid;not null"`
	Content     string        `json:"content" gorm:"type:text" validate:"required,min=1"`
	Type        CommentType   `json:"type" gorm:"type:varchar(20);default:'general'"`
	CreatedAt   time.Time     `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt   time.Time     `json:"updated_at" gorm:"autoUpdateTime"`
	
	// Relationships
	UserStory   UserStory     `json:"user_story,omitempty" gorm:"foreignKey:UserStoryID"`
}

// CommentType representa el tipo de comentario
type CommentType string

const (
	CommentGeneral     CommentType = "general"
	CommentFeedback    CommentType = "feedback"
	CommentQuestion    CommentType = "question"
	CommentBlocking    CommentType = "blocking"
	CommentReview      CommentType = "review"
)

// TableName especifica el nombre de la tabla para GORM
func (UserStory) TableName() string {
	return "factory_user_stories"
}

// TableName especifica el nombre de la tabla para GORM
func (Evidence) TableName() string {
	return "factory_evidences"
}

// TableName especifica el nombre de la tabla para GORM
func (StoryComment) TableName() string {
	return "factory_story_comments"
}

// Validate valida las reglas de negocio de la historia de usuario
func (us *UserStory) Validate() error {
	if us.StoryPoints < 1 || us.StoryPoints > 21 {
		return &ValidationError{Field: "story_points", Message: "story points must be between 1 and 21"}
	}
	
	if us.Priority < 1 || us.Priority > 5 {
		return &ValidationError{Field: "priority", Message: "priority must be between 1 and 5"}
	}
	
	if len(us.AcceptanceCriteria) == 0 {
		return &ValidationError{Field: "acceptance_criteria", Message: "at least one acceptance criterion must be specified"}
	}
	
	if len(us.AcademicCriteria) == 0 {
		return &ValidationError{Field: "academic_criteria", Message: "at least one academic criterion must be specified"}
	}
	
	return nil
}

// CanTransitionTo verifica si la historia puede cambiar al estado especificado
func (us *UserStory) CanTransitionTo(newStatus StoryStatus) bool {
	transitions := map[StoryStatus][]StoryStatus{
		StoryStatusBacklog:    {StoryStatusTodo},
		StoryStatusTodo:       {StoryStatusInProgress, StoryStatusBacklog},
		StoryStatusInProgress: {StoryStatusReview, StoryStatusTodo},
		StoryStatusReview:     {StoryStatusDone, StoryStatusInProgress},
		StoryStatusDone:       {StoryStatusReview}, // Can reopen if needed
	}
	
	allowedTransitions, exists := transitions[us.Status]
	if !exists {
		return false
	}
	
	for _, allowed := range allowedTransitions {
		if allowed == newStatus {
			return true
		}
	}
	
	return false
}

// IsCompleted verifica si la historia está completada
func (us *UserStory) IsCompleted() bool {
	return us.Status == StoryStatusDone
}

// GetProgress calcula el progreso de la historia basado en criterios completados
func (us *UserStory) GetProgress() float64 {
	totalCriteria := len(us.AcceptanceCriteria) + len(us.AcademicCriteria)
	if totalCriteria == 0 {
		return 0.0
	}
	
	completedCriteria := 0
	for _, criterion := range us.AcceptanceCriteria {
		if criterion.IsCompleted {
			completedCriteria++
		}
	}
	
	for _, criterion := range us.AcademicCriteria {
		if criterion.IsCompleted {
			completedCriteria++
		}
	}
	
	return float64(completedCriteria) / float64(totalCriteria) * 100
}

// HasDependencies verifica si la historia tiene dependencias
func (us *UserStory) HasDependencies() bool {
	return len(us.Dependencies) > 0
}

// GetTotalHours retorna las horas totales (estimadas + aprendizaje)
func (us *UserStory) GetTotalHours() int {
	return us.EstimatedHours + us.LearningHours
}

// MarkCompleted marca la historia como completada
func (us *UserStory) MarkCompleted() {
	us.Status = StoryStatusDone
	now := time.Now()
	us.CompletedAt = &now
}

// Validate valida las reglas de negocio de la evidencia
func (e *Evidence) Validate() error {
	if e.URL == "" && e.FilePath == "" {
		return &ValidationError{Field: "url_or_file_path", Message: "either URL or file path must be provided"}
	}
	
	return nil
}

// IsApprovalPending verifica si la evidencia está pendiente de aprobación
func (e *Evidence) IsApprovalPending() bool {
	return !e.IsApproved && e.ReviewedBy == nil
}

// Approve aprueba la evidencia
func (e *Evidence) Approve(reviewerID uuid.UUID, feedback string) {
	e.IsApproved = true
	e.ReviewedBy = &reviewerID
	now := time.Now()
	e.ReviewedAt = &now
	e.Feedback = feedback
}

// Reject rechaza la evidencia
func (e *Evidence) Reject(reviewerID uuid.UUID, feedback string) {
	e.IsApproved = false
	e.ReviewedBy = &reviewerID
	now := time.Now()
	e.ReviewedAt = &now
	e.Feedback = feedback
}
