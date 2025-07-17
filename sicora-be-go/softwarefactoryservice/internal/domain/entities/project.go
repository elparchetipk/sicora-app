package entities

import (
	"time"

	"github.com/google/uuid"
)

// ProjectStatus representa los estados de un proyecto en la fábrica
type ProjectStatus string

const (
	ProjectStatusPlanning   ProjectStatus = "planning"
	ProjectStatusActive     ProjectStatus = "active"
	ProjectStatusOnHold     ProjectStatus = "on_hold"
	ProjectStatusCompleted  ProjectStatus = "completed"
	ProjectStatusCancelled  ProjectStatus = "cancelled"
)

// ComplexityLevel representa el nivel de complejidad de un proyecto
type ComplexityLevel string

const (
	ComplexityBeginner     ComplexityLevel = "beginner"
	ComplexityIntermediate ComplexityLevel = "intermediate"
	ComplexityAdvanced     ComplexityLevel = "advanced"
)

// Project representa un proyecto de la fábrica de software académica
type Project struct {
	ID                    uuid.UUID       `json:"id" gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
	Name                  string          `json:"name" gorm:"not null;size:255" validate:"required,min=3,max=100"`
	Description           string          `json:"description" gorm:"type:text" validate:"required,min=10"`
	ClientInfo            ClientInfo      `json:"client_info" gorm:"embedded;embeddedPrefix:client_"`
	TechStack             []string        `json:"tech_stack" gorm:"type:text[]" validate:"required,min=1"`
	LearningObjectives    []string        `json:"learning_objectives" gorm:"type:text[]" validate:"required,min=1"`
	ComplexityLevel       ComplexityLevel `json:"complexity_level" gorm:"type:varchar(20)" validate:"required"`
	EstimatedDurationWeeks int            `json:"estimated_duration_weeks" gorm:"not null" validate:"required,min=4,max=26"`
	Status                ProjectStatus   `json:"status" gorm:"type:varchar(20);default:'planning'" validate:"required"`
	EvaluationCriteria    []EvaluationCriterion `json:"evaluation_criteria" gorm:"serializer:json"`
	Deliverables          []Deliverable   `json:"deliverables" gorm:"serializer:json"`
	Milestones           []Milestone     `json:"milestones" gorm:"serializer:json"`
	CreatedBy            uuid.UUID       `json:"created_by" gorm:"type:uuid;not null"`
	CreatedAt            time.Time       `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt            time.Time       `json:"updated_at" gorm:"autoUpdateTime"`
	StartDate            *time.Time      `json:"start_date,omitempty"`
	EndDate              *time.Time      `json:"end_date,omitempty"`
	
	// Relationships
	Teams                []Team          `json:"teams,omitempty" gorm:"foreignKey:ProjectID"`
	Sprints              []Sprint        `json:"sprints,omitempty" gorm:"foreignKey:ProjectID"`
}

// ClientInfo representa la información del cliente/stakeholder
type ClientInfo struct {
	Name        string `json:"name" gorm:"column:client_name"`
	Contact     string `json:"contact" gorm:"column:client_contact"`
	Department  string `json:"department" gorm:"column:client_department"`
	IsInternal  bool   `json:"is_internal" gorm:"column:client_is_internal;default:true"`
}

// EvaluationCriterion representa un criterio de evaluación del proyecto
type EvaluationCriterion struct {
	Name        string `json:"name"`
	Description string `json:"description"`
	Weight      int    `json:"weight"` // Peso en porcentaje
	Type        string `json:"type"`   // technical, academic, quality
}

// Deliverable representa un entregable del proyecto
type Deliverable struct {
	Name        string     `json:"name"`
	Description string     `json:"description"`
	DueDate     time.Time  `json:"due_date"`
	Status      string     `json:"status"` // pending, in_progress, completed
	Criteria    []string   `json:"criteria"`
}

// Milestone representa un hito del proyecto
type Milestone struct {
	Name        string    `json:"name"`
	Description string    `json:"description"`
	TargetDate  time.Time `json:"target_date"`
	Status      string    `json:"status"` // pending, achieved, delayed
	Progress    int       `json:"progress"` // Porcentaje 0-100
}

// TableName especifica el nombre de la tabla para GORM
func (Project) TableName() string {
	return "factory_projects"
}

// Validate valida las reglas de negocio del proyecto
func (p *Project) Validate() error {
	if len(p.TechStack) == 0 {
		return &ValidationError{Field: "tech_stack", Message: "at least one technology must be specified"}
	}
	
	if len(p.LearningObjectives) == 0 {
		return &ValidationError{Field: "learning_objectives", Message: "at least one learning objective must be specified"}
	}
	
	if p.EstimatedDurationWeeks < 4 || p.EstimatedDurationWeeks > 26 {
		return &ValidationError{Field: "estimated_duration_weeks", Message: "duration must be between 4 and 26 weeks"}
	}
	
	return nil
}

// CanTransitionTo verifica si el proyecto puede cambiar al estado especificado
func (p *Project) CanTransitionTo(newStatus ProjectStatus) bool {
	transitions := map[ProjectStatus][]ProjectStatus{
		ProjectStatusPlanning:  {ProjectStatusActive, ProjectStatusCancelled},
		ProjectStatusActive:    {ProjectStatusOnHold, ProjectStatusCompleted, ProjectStatusCancelled},
		ProjectStatusOnHold:    {ProjectStatusActive, ProjectStatusCancelled},
		ProjectStatusCompleted: {}, // Estado final
		ProjectStatusCancelled: {}, // Estado final
	}
	
	allowedTransitions, exists := transitions[p.Status]
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

// IsActive verifica si el proyecto está en estado activo
func (p *Project) IsActive() bool {
	return p.Status == ProjectStatusActive
}

// CalculateProgress calcula el progreso general del proyecto basado en milestones
func (p *Project) CalculateProgress() int {
	if len(p.Milestones) == 0 {
		return 0
	}
	
	totalProgress := 0
	for _, milestone := range p.Milestones {
		totalProgress += milestone.Progress
	}
	
	return totalProgress / len(p.Milestones)
}
