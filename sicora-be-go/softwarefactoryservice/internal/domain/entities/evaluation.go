package entities

import (
	"time"

	"github.com/google/uuid"
)

// EvaluationType representa el tipo de evaluación
type EvaluationType string

const (
	EvaluationSelf         EvaluationType = "self"
	EvaluationInstructor   EvaluationType = "instructor"
	EvaluationPeer         EvaluationType = "peer"
	EvaluationComprehensive EvaluationType = "comprehensive"
)

// Evaluation representa una evaluación continua de un aprendiz
type Evaluation struct {
	ID               uuid.UUID        `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	ApprenticeID     uuid.UUID        `json:"apprentice_id" gorm:"type:uuid;not null"`
	ProjectID        uuid.UUID        `json:"project_id" gorm:"type:uuid;not null"`
	SprintID         *uuid.UUID       `json:"sprint_id,omitempty" gorm:"type:uuid"`
	EvaluatorID      uuid.UUID        `json:"evaluator_id" gorm:"type:uuid;not null"`
	EvaluationType   EvaluationType   `json:"evaluation_type" gorm:"type:varchar(20)" validate:"required"`
	EvaluationDate   time.Time        `json:"evaluation_date" gorm:"not null"`
	TechnicalSkills  TechnicalSkills  `json:"technical_skills" gorm:"embedded;embeddedPrefix:tech_"`
	SoftSkills       SoftSkills       `json:"soft_skills" gorm:"embedded;embeddedPrefix:soft_"`
	LearningObjectivesMet []string    `json:"learning_objectives_met" gorm:"type:text[]"`
	AreasForImprovement   []string    `json:"areas_for_improvement" gorm:"type:text[]"`
	Recommendations       string      `json:"recommendations" gorm:"type:text"`
	OverallScore         float64      `json:"overall_score" gorm:"not null"`
	Notes                string       `json:"notes" gorm:"type:text"`
	CreatedAt            time.Time    `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt            time.Time    `json:"updated_at" gorm:"autoUpdateTime"`
	
	// Relationships
	Project              Project      `json:"project,omitempty" gorm:"foreignKey:ProjectID"`
	Sprint               *Sprint      `json:"sprint,omitempty" gorm:"foreignKey:SprintID"`
	ImprovementPlans     []ImprovementPlan `json:"improvement_plans,omitempty" gorm:"foreignKey:EvaluationID"`
}

// TechnicalSkills representa las habilidades técnicas evaluadas
type TechnicalSkills struct {
	CodingQuality      int `json:"coding_quality" gorm:"column:tech_coding_quality" validate:"min=1,max=5"`
	ProblemSolving     int `json:"problem_solving" gorm:"column:tech_problem_solving" validate:"min=1,max=5"`
	TechnologyAdoption int `json:"technology_adoption" gorm:"column:tech_technology_adoption" validate:"min=1,max=5"`
	TestingPractices   int `json:"testing_practices" gorm:"column:tech_testing_practices" validate:"min=1,max=5"`
}

// SoftSkills representa las habilidades blandas evaluadas
type SoftSkills struct {
	Communication int `json:"communication" gorm:"column:soft_communication" validate:"min=1,max=5"`
	Teamwork      int `json:"teamwork" gorm:"column:soft_teamwork" validate:"min=1,max=5"`
	Leadership    int `json:"leadership" gorm:"column:soft_leadership" validate:"min=1,max=5"`
	Adaptability  int `json:"adaptability" gorm:"column:soft_adaptability" validate:"min=1,max=5"`
}

// ImprovementPlan representa un plan de mejora personalizado
type ImprovementPlan struct {
	ID              uuid.UUID     `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	EvaluationID    uuid.UUID     `json:"evaluation_id" gorm:"type:uuid;not null"`
	CompetencyArea  string        `json:"competency_area" gorm:"not null;size:100"`
	CurrentLevel    int           `json:"current_level" gorm:"not null" validate:"min=1,max=5"`
	TargetLevel     int           `json:"target_level" gorm:"not null" validate:"min=1,max=5"`
	Activities      []Activity    `json:"activities" gorm:"serializer:json"`
	Resources       []Resource    `json:"resources" gorm:"serializer:json"`
	Timeline        Timeline      `json:"timeline" gorm:"embedded;embeddedPrefix:timeline_"`
	Status          PlanStatus    `json:"status" gorm:"type:varchar(20);default:'active'"`
	Progress        int           `json:"progress" gorm:"default:0" validate:"min=0,max=100"`
	CreatedAt       time.Time     `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt       time.Time     `json:"updated_at" gorm:"autoUpdateTime"`
	
	// Relationships
	Evaluation      Evaluation    `json:"evaluation,omitempty" gorm:"foreignKey:EvaluationID"`
	FollowUps       []FollowUp    `json:"follow_ups,omitempty" gorm:"foreignKey:ImprovementPlanID"`
}

// Activity representa una actividad del plan de mejora
type Activity struct {
	Name        string    `json:"name"`
	Description string    `json:"description"`
	Type        string    `json:"type"` // practice, study, mentoring, project
	Duration    int       `json:"duration"` // hours
	IsCompleted bool      `json:"is_completed"`
	DueDate     time.Time `json:"due_date"`
}

// Resource representa un recurso de aprendizaje
type Resource struct {
	Type        string `json:"type"` // article, video, course, book, documentation
	Title       string `json:"title"`
	URL         string `json:"url"`
	Description string `json:"description"`
	IsAccessed  bool   `json:"is_accessed"`
}

// Timeline representa el cronograma del plan de mejora
type Timeline struct {
	StartDate     time.Time  `json:"start_date" gorm:"column:timeline_start_date"`
	EndDate       time.Time  `json:"end_date" gorm:"column:timeline_end_date"`
	MilestoneDate *time.Time `json:"milestone_date,omitempty" gorm:"column:timeline_milestone_date"`
	ReviewDate    time.Time  `json:"review_date" gorm:"column:timeline_review_date"`
}

// PlanStatus representa el estado del plan de mejora
type PlanStatus string

const (
	PlanStatusActive    PlanStatus = "active"
	PlanStatusCompleted PlanStatus = "completed"
	PlanStatusPaused    PlanStatus = "paused"
	PlanStatusCancelled PlanStatus = "cancelled"
)

// FollowUp representa un seguimiento del plan de mejora
type FollowUp struct {
	ID                 uuid.UUID    `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	ImprovementPlanID  uuid.UUID    `json:"improvement_plan_id" gorm:"type:uuid;not null"`
	ReviewerID         uuid.UUID    `json:"reviewer_id" gorm:"type:uuid;not null"`
	ReviewDate         time.Time    `json:"review_date" gorm:"not null"`
	ProgressAssessment int          `json:"progress_assessment" validate:"min=0,max=100"`
	Observations       string       `json:"observations" gorm:"type:text"`
	Adjustments        []string     `json:"adjustments" gorm:"type:text[]"`
	NextSteps          []string     `json:"next_steps" gorm:"type:text[]"`
	CreatedAt          time.Time    `json:"created_at" gorm:"autoCreateTime"`
	
	// Relationships
	ImprovementPlan    ImprovementPlan `json:"improvement_plan,omitempty" gorm:"foreignKey:ImprovementPlanID"`
}

// TableName especifica el nombre de la tabla para GORM
func (Evaluation) TableName() string {
	return "factory_evaluations"
}

// TableName especifica el nombre de la tabla para GORM
func (ImprovementPlan) TableName() string {
	return "factory_improvement_plans"
}

// TableName especifica el nombre de la tabla para GORM
func (FollowUp) TableName() string {
	return "factory_follow_ups"
}

// Validate valida las reglas de negocio de la evaluación
func (e *Evaluation) Validate() error {
	if e.OverallScore < 1.0 || e.OverallScore > 5.0 {
		return &ValidationError{Field: "overall_score", Message: "overall score must be between 1.0 and 5.0"}
	}
	
	// Validar que todas las habilidades técnicas estén en rango 1-5
	if e.TechnicalSkills.CodingQuality < 1 || e.TechnicalSkills.CodingQuality > 5 {
		return &ValidationError{Field: "technical_skills.coding_quality", Message: "score must be between 1 and 5"}
	}
	
	if e.TechnicalSkills.ProblemSolving < 1 || e.TechnicalSkills.ProblemSolving > 5 {
		return &ValidationError{Field: "technical_skills.problem_solving", Message: "score must be between 1 and 5"}
	}
	
	if e.TechnicalSkills.TechnologyAdoption < 1 || e.TechnicalSkills.TechnologyAdoption > 5 {
		return &ValidationError{Field: "technical_skills.technology_adoption", Message: "score must be between 1 and 5"}
	}
	
	if e.TechnicalSkills.TestingPractices < 1 || e.TechnicalSkills.TestingPractices > 5 {
		return &ValidationError{Field: "technical_skills.testing_practices", Message: "score must be between 1 and 5"}
	}
	
	// Validar que todas las habilidades blandas estén en rango 1-5
	if e.SoftSkills.Communication < 1 || e.SoftSkills.Communication > 5 {
		return &ValidationError{Field: "soft_skills.communication", Message: "score must be between 1 and 5"}
	}
	
	if e.SoftSkills.Teamwork < 1 || e.SoftSkills.Teamwork > 5 {
		return &ValidationError{Field: "soft_skills.teamwork", Message: "score must be between 1 and 5"}
	}
	
	if e.SoftSkills.Leadership < 1 || e.SoftSkills.Leadership > 5 {
		return &ValidationError{Field: "soft_skills.leadership", Message: "score must be between 1 and 5"}
	}
	
	if e.SoftSkills.Adaptability < 1 || e.SoftSkills.Adaptability > 5 {
		return &ValidationError{Field: "soft_skills.adaptability", Message: "score must be between 1 and 5"}
	}
	
	return nil
}

// CalculateOverallScore calcula el puntaje general basado en habilidades técnicas y blandas
func (e *Evaluation) CalculateOverallScore() float64 {
	techAvg := float64(e.TechnicalSkills.CodingQuality+e.TechnicalSkills.ProblemSolving+
		e.TechnicalSkills.TechnologyAdoption+e.TechnicalSkills.TestingPractices) / 4.0
	
	softAvg := float64(e.SoftSkills.Communication+e.SoftSkills.Teamwork+
		e.SoftSkills.Leadership+e.SoftSkills.Adaptability) / 4.0
	
	// Peso: 60% técnicas, 40% blandas
	return (techAvg*0.6 + softAvg*0.4)
}

// GetTechnicalAverage calcula el promedio de habilidades técnicas
func (e *Evaluation) GetTechnicalAverage() float64 {
	return float64(e.TechnicalSkills.CodingQuality+e.TechnicalSkills.ProblemSolving+
		e.TechnicalSkills.TechnologyAdoption+e.TechnicalSkills.TestingPractices) / 4.0
}

// GetSoftSkillsAverage calcula el promedio de habilidades blandas
func (e *Evaluation) GetSoftSkillsAverage() float64 {
	return float64(e.SoftSkills.Communication+e.SoftSkills.Teamwork+
		e.SoftSkills.Leadership+e.SoftSkills.Adaptability) / 4.0
}

// NeedsImprovement verifica si la evaluación indica necesidad de mejora
func (e *Evaluation) NeedsImprovement() bool {
	return e.OverallScore < 3.0
}

// GetWeakAreas identifica las áreas más débiles para crear planes de mejora
func (e *Evaluation) GetWeakAreas() []string {
	var weakAreas []string
	
	if e.TechnicalSkills.CodingQuality <= 2 {
		weakAreas = append(weakAreas, "coding_quality")
	}
	if e.TechnicalSkills.ProblemSolving <= 2 {
		weakAreas = append(weakAreas, "problem_solving")
	}
	if e.TechnicalSkills.TechnologyAdoption <= 2 {
		weakAreas = append(weakAreas, "technology_adoption")
	}
	if e.TechnicalSkills.TestingPractices <= 2 {
		weakAreas = append(weakAreas, "testing_practices")
	}
	if e.SoftSkills.Communication <= 2 {
		weakAreas = append(weakAreas, "communication")
	}
	if e.SoftSkills.Teamwork <= 2 {
		weakAreas = append(weakAreas, "teamwork")
	}
	if e.SoftSkills.Leadership <= 2 {
		weakAreas = append(weakAreas, "leadership")
	}
	if e.SoftSkills.Adaptability <= 2 {
		weakAreas = append(weakAreas, "adaptability")
	}
	
	return weakAreas
}

// Validate valida las reglas de negocio del plan de mejora
func (ip *ImprovementPlan) Validate() error {
	if ip.CurrentLevel < 1 || ip.CurrentLevel > 5 {
		return &ValidationError{Field: "current_level", Message: "current level must be between 1 and 5"}
	}
	
	if ip.TargetLevel < 1 || ip.TargetLevel > 5 {
		return &ValidationError{Field: "target_level", Message: "target level must be between 1 and 5"}
	}
	
	if ip.TargetLevel <= ip.CurrentLevel {
		return &ValidationError{Field: "target_level", Message: "target level must be higher than current level"}
	}
	
	if ip.Timeline.EndDate.Before(ip.Timeline.StartDate) {
		return &ValidationError{Field: "timeline", Message: "end date must be after start date"}
	}
	
	return nil
}

// IsActive verifica si el plan de mejora está activo
func (ip *ImprovementPlan) IsActive() bool {
	return ip.Status == PlanStatusActive
}

// IsOverdue verifica si el plan está atrasado
func (ip *ImprovementPlan) IsOverdue() bool {
	return time.Now().After(ip.Timeline.EndDate) && ip.Status == PlanStatusActive
}

// UpdateProgress actualiza el progreso del plan
func (ip *ImprovementPlan) UpdateProgress() {
	if len(ip.Activities) == 0 {
		ip.Progress = 0
		return
	}
	
	completedActivities := 0
	for _, activity := range ip.Activities {
		if activity.IsCompleted {
			completedActivities++
		}
	}
	
	ip.Progress = (completedActivities * 100) / len(ip.Activities)
	
	if ip.Progress >= 100 {
		ip.Status = PlanStatusCompleted
	}
}

// CanComplete verifica si el plan puede completarse
func (ip *ImprovementPlan) CanComplete() bool {
	return ip.Progress >= 80 && ip.Status == PlanStatusActive
}
