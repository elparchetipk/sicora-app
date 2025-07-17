package entities

import (
	"time"

	"github.com/google/uuid"
)

// SprintStatus representa el estado de un sprint académico
type SprintStatus string

const (
	SprintStatusPlanning  SprintStatus = "planning"
	SprintStatusActive    SprintStatus = "active"
	SprintStatusReview    SprintStatus = "review"
	SprintStatusCompleted SprintStatus = "completed"
)

// Sprint representa un sprint académico de 3 semanas
type Sprint struct {
	ID                   uuid.UUID       `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	ProjectID            uuid.UUID       `json:"project_id" gorm:"type:uuid;not null"`
	TeamID               uuid.UUID       `json:"team_id" gorm:"type:uuid;not null"`
	SprintNumber         int             `json:"sprint_number" gorm:"not null"`
	StartDate            time.Time       `json:"start_date" gorm:"not null"`
	EndDate              time.Time       `json:"end_date" gorm:"not null"`
	SprintGoal           string          `json:"sprint_goal" gorm:"type:text" validate:"required,min=10"`
	LearningObjectives   []string        `json:"learning_objectives" gorm:"type:text[]" validate:"required,min=1"`
	Status               SprintStatus    `json:"status" gorm:"type:varchar(20);default:'planning'"`
	VelocityPoints       int             `json:"velocity_points" gorm:"default:0"`
	StoriesCompleted     int             `json:"stories_completed" gorm:"default:0"`
	LearningEvaluation   LearningEvaluation `json:"learning_evaluation" gorm:"embedded;embeddedPrefix:learning_"`
	CreatedAt            time.Time       `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt            time.Time       `json:"updated_at" gorm:"autoUpdateTime"`
	
	// Relationships
	Project              Project         `json:"project,omitempty" gorm:"foreignKey:ProjectID"`
	Team                 Team            `json:"team,omitempty" gorm:"foreignKey:TeamID"`
	UserStories          []UserStory     `json:"user_stories,omitempty" gorm:"foreignKey:SprintID"`
	Ceremonies           []SprintCeremony `json:"ceremonies,omitempty" gorm:"foreignKey:SprintID"`
}

// LearningEvaluation representa la evaluación de aprendizaje del sprint
type LearningEvaluation struct {
	ObjectivesMet        []string    `json:"objectives_met" gorm:"column:learning_objectives_met;type:text[]"`
	CompetenciesDeveloped []string   `json:"competencies_developed" gorm:"column:learning_competencies_developed;type:text[]"`
	ChallengesFaced      []string    `json:"challenges_faced" gorm:"column:learning_challenges_faced;type:text[]"`
	LessonsLearned       []string    `json:"lessons_learned" gorm:"column:learning_lessons_learned;type:text[]"`
	OverallRating        int         `json:"overall_rating" gorm:"column:learning_overall_rating;default:0"` // 1-5
	InstructorFeedback   string      `json:"instructor_feedback" gorm:"column:learning_instructor_feedback;type:text"`
	EvaluatedAt          *time.Time  `json:"evaluated_at,omitempty" gorm:"column:learning_evaluated_at"`
}

// SprintCeremony representa una ceremonia de Scrum
type SprintCeremony struct {
	ID          uuid.UUID        `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	SprintID    uuid.UUID        `json:"sprint_id" gorm:"type:uuid;not null"`
	Type        CeremonyType     `json:"type" gorm:"type:varchar(30)" validate:"required"`
	ScheduledAt time.Time        `json:"scheduled_at" gorm:"not null"`
	Duration    int              `json:"duration" gorm:"not null"` // minutes
	Status      CeremonyStatus   `json:"status" gorm:"type:varchar(20);default:'scheduled'"`
	Facilitator uuid.UUID        `json:"facilitator" gorm:"type:uuid;not null"` // Instructor ID
	Notes       string           `json:"notes" gorm:"type:text"`
	Participants []uuid.UUID     `json:"participants" gorm:"type:uuid[]"`
	CreatedAt   time.Time        `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt   time.Time        `json:"updated_at" gorm:"autoUpdateTime"`
	
	// Relationships
	Sprint      Sprint           `json:"sprint,omitempty" gorm:"foreignKey:SprintID"`
}

// CeremonyType representa el tipo de ceremonia de Scrum
type CeremonyType string

const (
	CeremonyPlanning     CeremonyType = "planning"
	CeremonyDaily        CeremonyType = "daily"
	CeremonyReview       CeremonyType = "review"
	CeremonyRetrospective CeremonyType = "retrospective"
	CeremonyLearningReflection CeremonyType = "learning_reflection" // Ceremonia académica especial
)

// CeremonyStatus representa el estado de una ceremonia
type CeremonyStatus string

const (
	CeremonyScheduled  CeremonyStatus = "scheduled"
	CeremonyInProgress CeremonyStatus = "in_progress"
	CeremonyCompleted  CeremonyStatus = "completed"
	CeremonyCancelled  CeremonyStatus = "cancelled"
)

// TableName especifica el nombre de la tabla para GORM
func (Sprint) TableName() string {
	return "factory_sprints"
}

// TableName especifica el nombre de la tabla para GORM
func (SprintCeremony) TableName() string {
	return "factory_sprint_ceremonies"
}

// Validate valida las reglas de negocio del sprint
func (s *Sprint) Validate() error {
	// Sprint debe durar exactamente 3 semanas (21 días)
	duration := s.EndDate.Sub(s.StartDate)
	expectedDuration := 21 * 24 * time.Hour // 21 days
	
	if duration < expectedDuration-24*time.Hour || duration > expectedDuration+24*time.Hour {
		return &ValidationError{Field: "duration", Message: "sprint must be exactly 3 weeks (21 days)"}
	}
	
	if len(s.LearningObjectives) == 0 {
		return &ValidationError{Field: "learning_objectives", Message: "at least one learning objective must be specified"}
	}
	
	if s.SprintNumber < 1 {
		return &ValidationError{Field: "sprint_number", Message: "sprint number must be positive"}
	}
	
	return nil
}

// IsActive verifica si el sprint está activo
func (s *Sprint) IsActive() bool {
	return s.Status == SprintStatusActive
}

// CanStart verifica si el sprint puede iniciar
func (s *Sprint) CanStart() bool {
	return s.Status == SprintStatusPlanning && time.Now().After(s.StartDate.Add(-24*time.Hour))
}

// CanComplete verifica si el sprint puede completarse
func (s *Sprint) CanComplete() bool {
	return s.Status == SprintStatusReview && time.Now().After(s.EndDate)
}

// CalculateProgress calcula el progreso del sprint basado en historias completadas
func (s *Sprint) CalculateProgress() float64 {
	if len(s.UserStories) == 0 {
		return 0.0
	}
	
	completedStories := 0
	for _, story := range s.UserStories {
		if story.Status == StoryStatusDone {
			completedStories++
		}
	}
	
	return float64(completedStories) / float64(len(s.UserStories)) * 100
}

// GetVelocity calcula la velocidad del sprint (story points completados)
func (s *Sprint) GetVelocity() int {
	velocity := 0
	for _, story := range s.UserStories {
		if story.Status == StoryStatusDone {
			velocity += story.StoryPoints
		}
	}
	return velocity
}

// ScheduleStandardCeremonies crea las ceremonias estándar para el sprint
func (s *Sprint) ScheduleStandardCeremonies(facilitatorID uuid.UUID) []SprintCeremony {
	ceremonies := []SprintCeremony{
		{
			ID:          uuid.New(),
			SprintID:    s.ID,
			Type:        CeremonyPlanning,
			ScheduledAt: s.StartDate,
			Duration:    240, // 4 hours
			Facilitator: facilitatorID,
			Status:      CeremonyScheduled,
		},
		{
			ID:          uuid.New(),
			SprintID:    s.ID,
			Type:        CeremonyReview,
			ScheduledAt: s.EndDate.Add(-24 * time.Hour), // Day before end
			Duration:    120, // 2 hours
			Facilitator: facilitatorID,
			Status:      CeremonyScheduled,
		},
		{
			ID:          uuid.New(),
			SprintID:    s.ID,
			Type:        CeremonyRetrospective,
			ScheduledAt: s.EndDate.Add(-2 * time.Hour), // 2 hours after review
			Duration:    90, // 1.5 hours
			Facilitator: facilitatorID,
			Status:      CeremonyScheduled,
		},
		{
			ID:          uuid.New(),
			SprintID:    s.ID,
			Type:        CeremonyLearningReflection,
			ScheduledAt: s.EndDate.Add(-30 * time.Minute), // 30 min after retro
			Duration:    60, // 1 hour
			Facilitator: facilitatorID,
			Status:      CeremonyScheduled,
		},
	}
	
	return ceremonies
}

// Validate valida las reglas de negocio de la ceremonia
func (sc *SprintCeremony) Validate() error {
	if sc.Duration < 15 || sc.Duration > 480 { // 15 min to 8 hours
		return &ValidationError{Field: "duration", Message: "ceremony duration must be between 15 minutes and 8 hours"}
	}
	
	return nil
}

// IsCompleted verifica si la ceremonia está completada
func (sc *SprintCeremony) IsCompleted() bool {
	return sc.Status == CeremonyCompleted
}

// CanStart verifica si la ceremonia puede iniciar
func (sc *SprintCeremony) CanStart() bool {
	return sc.Status == CeremonyScheduled && time.Now().After(sc.ScheduledAt.Add(-15*time.Minute))
}
